import mysql.connector
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'plurall_ph'
}

task_context_data = {
    'name': 'objective_home_activities_task',
    'code': 'objective_home_activities_task',
    'test_type': 'Atividades para casa objetivas',
    'group': 'ph',
    'group_name': 'ph',
    'group_field': 'group_field',
    'should_display_official_answer': 1,
    'suggested_filter': None,
    'source_filters': 'discipline',
    'max_answers_on_multiple_choice': 1,
    'max_answers_on_open_response': 1,
    'allow_change_answer_until_due_date': 0,
    'display_answer_feedback': 1,
    'hide_help_options': 1,
    'quick_answer_enabled': 1,
    'show_task_instructions': 0,
    'require_manual_finish': 0,
    'accessible_only_by_context': 0,
    'node_type': 'test',
    'menu_title': 'Atividades para casa objetivas',
    'allow_video': 0,
    'allow_reopen_task': 0,
    'allow_notify': 0,
    'allow_read_task': 0,
    'created_at': datetime.now(),
    'updated_at': datetime.now()
}

sku_values = [
    'SKU_851335', 'SKU_852717',
    'SKU_851337', 'SKU_852719',
    'SKU_851339', 'SKU_852721',
    'SKU_851347', 'SKU_852749',
    'SKU_851349', 'SKU_852751',
    'SKU_851351', 'SKU_852777',
    'SKU_851369', 'SKU_852813',
    'SKU_851371', 'SKU_852815',
    'SKU_851373', 'SKU_852817',
    'SKU_851394', 'SKU_852846',
    'SKU_851396', 'SKU_852850',
    'SKU_851398', 'SKU_852854',
]

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    task_context_query = """
    INSERT INTO task_contexts (
        name, code, test_type, `group`, group_name, group_field,
        should_display_official_answer, suggested_filter, source_filters,
        max_answers_on_multiple_choice, max_answers_on_open_response,
        allow_change_answer_until_due_date, display_answer_feedback,
        hide_help_options, quick_answer_enabled, show_task_instructions,
        require_manual_finish, accessible_only_by_context,
        created_at, updated_at, node_type, menu_title,
        allow_video, allow_reopen_task, allow_notify, allow_read_task
    ) VALUES (
        %(name)s, %(code)s, %(test_type)s, %(group)s, %(group_name)s, %(group_field)s,
        %(should_display_official_answer)s, %(suggested_filter)s, %(source_filters)s,
        %(max_answers_on_multiple_choice)s, %(max_answers_on_open_response)s,
        %(allow_change_answer_until_due_date)s, %(display_answer_feedback)s,
        %(hide_help_options)s, %(quick_answer_enabled)s, %(show_task_instructions)s,
        %(require_manual_finish)s, %(accessible_only_by_context)s,
        %(created_at)s, %(updated_at)s, %(node_type)s, %(menu_title)s,
        %(allow_video)s, %(allow_reopen_task)s, %(allow_notify)s, %(allow_read_task)s
    )
    """
    cursor.execute(task_context_query, task_context_data)
    task_context_id = cursor.lastrowid

    task_context_years_query = """
    INSERT INTO task_context_years (years_with_access, created_at, updated_at, task_context_id)
    VALUES (%s, %s, %s, %s)
    """

    now = datetime.now()
    years_data = [(sku, now, now, task_context_id) for sku in sku_values]
    cursor.executemany(task_context_years_query, years_data)

    conn.commit()
    print(f"task_context inserido com id = {task_context_id}")
    print(f"{len(sku_values)} SKUs inseridos com sucesso em task_context_years.")

except mysql.connector.Error as err:
    print(f"Erro ao executar: {err}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
