import streamlit as st
import pandas as pd
import plotly.express as px
from utils import parse_amount, list_categories, list_months, get_month_number_by_name, months
from utils import get_data_file, get_month_name_by_number, remove_sheet_if_exists
from guard import initialize_system, check_password, logout_system
from goals import load_goals, save_goal
from parser import parse_invoice
import os

def load_data_for_month(month):  
    path = get_data_file()
    if os.path.exists(path) and month:
        try:
            return pd.read_excel(path, sheet_name=month)
        except:
            return pd.DataFrame(columns=["date", "description", "amount", "category", "source"])
    return pd.DataFrame(columns=["date", "description", "amount", "category", "source"])

def load_data_all_months():
    path = get_data_file()
    if not os.path.exists(path):
        return pd.DataFrame(columns=["date", "description", "amount", "category", "source", "month"])

    all_data = []
    excel = pd.ExcelFile(path)
    for sheet in excel.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)
        df["month"] = sheet
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

def save_month_data(df, month):
    path = get_data_file()
    with pd.ExcelWriter(path, engine="openpyxl", mode="a" if os.path.exists(path) else "w", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=month, index=False)
    remove_sheet_if_exists(get_data_file(), sheet_name="template")

initialize_system()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.set_page_config(page_title="Login", layout="centered")
    st.title("🔐 Acesso")
    user_input = st.text_input("Digite sua senha:", type="password")
    if st.button("Entrar"):
        if check_password(user_input):
            st.success("Acesso autorizado.")
            st.session_state["authenticated"] = True
            st.session_state["password"] = user_input
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

st.set_page_config(page_title="FinGuide", layout="wide")

# Columns for title and logout button
col1, col2 = st.columns([6, 1])
with col1:
    st.title("💰 Gerenciador de Despesas")
with col2:
    if st.button("🔒 Sair do sistema"):
        logout_system(st.session_state["password"])
        st.session_state["authenticated"] = False
        st.session_state.pop("password", None)
        st.rerun()

path = get_data_file()
months_available = []
if os.path.exists(path):
    sheet_names = pd.ExcelFile(path).sheet_names
    sheet_months = [x for x in sheet_names if x != "template"]
    months_available = sorted(sheet_months, key=lambda x: get_month_number_by_name(x))
    
st.sidebar.header("🔎 Filtro")
selected_month = st.sidebar.selectbox("📅 Selecione o mês", options=months_available)
selected_month_view = "Selecione um mês" if not selected_month else selected_month

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Gastos por Categoria", "📈 Comparativo entre Meses", "🎯 Metas"])

# ================================
# 📊 TAB 1 - Gastos por Categoria
# ================================
with tab1:
    df = load_data_for_month(selected_month)

    st.header(f"📊 Gastos por Categoria - {selected_month_view}")
    if not df.empty:
        summary = df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(summary, names="category", values="amount", title="Distribuição por Categoria", hole=0.4)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum gasto registrado para este mês.")

    # Adicionar despesa fixa
    st.subheader("➕ Adicionar Despesa Fixa")
    with st.form("fixed_expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            description = st.text_input("Descrição")
            amount = st.text_input("Valor (R$)")
            date = st.date_input("Data")
        with col2:
            category = st.selectbox("Categoria", options=list_categories())
        submitted = st.form_submit_button("Salvar")
        if submitted:
            try:
                amount = parse_amount(amount)
                month_name = get_month_name_by_number(date.month)
                new_row = pd.DataFrame([{
                    "date": date.strftime("%d/%m/%Y"),
                    "description": description,
                    "amount": amount,
                    "category": category,
                    "source": "Fixed Expenses"
                }])
                existing_df = load_data_for_month(month_name)
                
                if existing_df.empty:
                    existing_df = pd.DataFrame(columns=["date", "description", "amount", "category", "source"])
                
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                save_month_data(updated_df, month_name)
                st.success("Despesa fixa adicionada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar: {e}")

    # Importar fatura
    st.subheader("📂 Importar Fatura do Cartão")
    with st.form("invoice_import_form"):
        col1, col2 = st.columns(2)
        with col1:
            invoice_type = st.selectbox("Tipo de fatura", ["Inter", "Nubank"])
            month = st.selectbox("Mês de referência", list_months())
        with col2:
            pdf_file = st.file_uploader("Upload do PDF da fatura", type="pdf")
            password = st.text_input("Senha do PDF (se houver)", type="password")
        imported = st.form_submit_button("Importar Fatura")

        if imported and pdf_file and month:
            try:
                temp_path = "temp_invoice.pdf"
                with open(temp_path, "wb") as f:
                    f.write(pdf_file.read())

                new_df = parse_invoice(temp_path, invoice_type, password)
                existing_df = load_data_for_month(month)
                full_df = pd.concat([existing_df, new_df], ignore_index=True)
                save_month_data(full_df, month)
                os.remove(temp_path)
                st.success("Fatura importada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao importar fatura: {e}")

# =================================
# 📈 TAB 2 - Comparativo Mensal
# =================================
with tab2:
    st.header("📆 Evolução de Gastos Mensais")
    df_all = load_data_all_months()
    if df_all.empty:
        st.warning("Nenhum dado disponível para comparar.")
    else:
        monthly_total = df_all.groupby("month")["amount"].sum().reset_index()
        monthly_total["month_num"] = monthly_total["month"].map(months())
        monthly_total = monthly_total.sort_values("month_num")
        fig = px.bar(monthly_total, x="month", y="amount", title="Gastos Totais por Mês")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📂 Comparativo por Categoria")
        by_cat = df_all.groupby(["month", "category"])["amount"].sum().reset_index()
        by_cat["month_num"] = by_cat["month"].map(months())
        by_cat = by_cat.sort_values("month_num")
        fig2 = px.bar(by_cat, x="month", y="amount", color="category", barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

# =================================
# 📈 TAB 2 - Metas
# =================================
with tab3:
    st.header(f"🎯 Planejamento de Gastos por Categoria - {selected_month_view}")

    with st.form("set_goal_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            goal_category = st.selectbox("Categoria", options=list_categories(), key="goal_category")
        with col2:
            goal_amount = st.text_input("Meta de Gasto (R$)", key="goal_amount")
        with col3:
            set_goal = st.form_submit_button("Salvar Meta")

        if set_goal:
            try:
                goal_value = parse_amount(goal_amount)
                save_goal(selected_month, goal_category, goal_value)
                st.success("Meta salva com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar meta: {e}")

    goals = load_goals()
    if selected_month in goals:
        meta_data = []
        for cat, meta in goals[selected_month].items():
            gasto = summary.loc[summary["category"] == cat, "amount"].sum()
            meta_data.append({"Categoria": cat, "Meta": meta, "Gasto": gasto})
        df_meta = pd.DataFrame(meta_data)

        fig_goal = px.bar(df_meta, x="Categoria", y=["Meta", "Gasto"], barmode="group",
                          title="📊 Comparativo Meta x Gasto")
        fig_goal.update_layout(yaxis_title="Valor (R$)")
        st.plotly_chart(fig_goal, use_container_width=True)