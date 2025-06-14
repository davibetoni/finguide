# 💰 Finance Manager

Um aplicativo de gerenciamento financeiro pessoal desenvolvido com **Streamlit**, que permite:

- Importar faturas dos cartões **Inter** e **Nubank** em PDF
- Categorização automática dos gastos com auxílio de **IA**
- Adição de despesas fixas mensais
- Gráficos de análise por **categoria** e **comparativo entre meses**
- Definição e acompanhamento de **metas de gastos**
- Interface **segura com autenticação por senha**
- Armazenamento protegido em **arquivo Excel criptografado**

---

## 🚀 Funcionalidades

- 📂 **Importação de Faturas**: Leia faturas do Inter e Nubank em PDF e extraia transações automaticamente.
- 🤖 **Classificação Automática**: Utiliza um classificador treinado com IA para prever a categoria de cada gasto.
- ➕ **Gastos Fixos**: Adicione manualmente despesas recorrentes como aluguel, contas etc.
- 📈 **Análise Gráfica**: Visualize seus gastos por categoria e por mês com gráficos interativos (Plotly).
- 🎯 **Metas de Categoria**: Defina metas mensais por categoria e receba alertas se forem ultrapassadas.
- 🔒 **Segurança**: O sistema é protegido por senha e os dados são criptografados em arquivo `.xlsx`.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [pandas](https://pandas.pydata.org/)
- [scikit-learn](https://scikit-learn.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) (para criptografia de Excel)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🔐 Segurança

- Ao iniciar o sistema, é gerado um arquivo Excel protegido com uma **senha aleatória**.
- A senha é exibida no terminal no primeiro uso e salva **de forma segura no `.env`** como hash.
- A aplicação exige essa senha para abrir o app no navegador.
- O arquivo Excel **só pode ser aberto com a senha correta**, mesmo fora do app.

---

## 📁 Estrutura de Arquivos

```bash
read-invoice/
├── app.py                 # Interface principal do Streamlit
├── parser.py              # Lógica para importar faturas
├── inter_parser.py        # Parser de faturas do Inter
├── nubank_parser.py       # Parser de faturas do Nubank
├── classifier.py          # IA para categorizar automaticamente
├── goals.py               # Módulo de metas por categoria
├── guard.py               # Segurança e criptografia
├── utils.py               # Funções auxiliares
├── files/                 # Planilhas .xlsx salvas com os dados
├── .env                   # Senha hash salva aqui (não commitado)
└── requirements.txt       # Dependências do projeto
```
