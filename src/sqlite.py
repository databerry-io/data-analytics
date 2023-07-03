
"""
This module contains functions for logging prompt-answer pairs in a SQLite database
"""

def log_prompt(conn, cursor, prompt, full_prompt, answer, code_executed, code_generated, error):
    """
    Log a prompt-answer pair in the database
    """

    # Insert a new prompt-answer pair into the database
    cursor.execute('''INSERT INTO prompt_log (prompt, full_prompt, answer, code_executed, code_generated, error)
                      VALUES (?, ?, ?, ?, ?, ?)''', (prompt, full_prompt, answer, code_executed, code_generated, error))
    conn.commit()

# def retrieve_prompt_log(cursor):
#     """
#     Retrieve all prompt-answer pairs from the database
#     """
#     cursor.execute('''SELECT * FROM prompt_log''')
#     log_data = cursor.fetchall()
#     log_data = log_data[::-1]
#     return log_data

def retrieve_prompt_log(cursor):
    """
    Retrieve all prompt-answer pairs from the database, starting with the latest entry
    """
    cursor.execute('''SELECT * FROM prompt_log ORDER BY id DESC''')
    for row in cursor.fetchall():
        yield row