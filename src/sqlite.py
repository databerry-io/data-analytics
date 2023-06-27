
def log_prompt(conn, cursor, prompt, answer, code_executed, code_generated, error):
    # Insert a new prompt-answer pair into the database
    cursor.execute('''INSERT INTO prompt_log (prompt, answer, code_executed, code_generated, error)
                      VALUES (?, ?, ?, ?, ?)''', (prompt, answer, code_executed, code_generated, error))
    conn.commit()

def retrieve_prompt_log(cursor):
    # Retrieve all prompt-answer pairs from the database
    cursor.execute('''SELECT * FROM prompt_log''')
    log_data = cursor.fetchall()
    return log_data