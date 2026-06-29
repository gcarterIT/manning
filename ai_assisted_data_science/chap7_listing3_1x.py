import argparse
import openai
import sqlite3
import time

def get_structure(data_path):
    with sqlite3.connect(data_path) as connection:
        cursor = connection.cursor()
        cursor.execute("select sql from sqlite_master where type = 'table';")
        table_rows = cursor.fetchall()
        table_ddls = [r[0] for r in table_rows]
        return '\n'.join(table_ddls)

def create_prompt(description, question):
    parts = []
    parts += ['Database:']
    parts += [description]
    parts += ['Translate this question into SQL query:']
    parts += [question]
    parts += ['SQL Query:']
    return '\n'.join(parts)

def call_llm(prompt):
    for nr_retries in range(1, 4):
        #response = openai.ChatCompletion.create(
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role':'user', 'content':prompt}
                ]
            )
        # return response['choices'][0]['message']['content']
        return response.choices[0].message.content


def process_query(data_path, query):
    with sqlite3.connect(data_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        table_rows = cursor.fetchall()
        table_strings = [str(r) for r in table_rows]
        return '\n'.join(table_strings)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('dbpath', type=str, help='Path to SQLite data')
    parser.add_argument('openaikey', type=str, help='OpenAI access key')
    args = parser.parse_args()

    openai.api_key = args.openaikey
    data_structure = get_structure(args.dbpath)
    
     # new
    from openai import OpenAI
    client = OpenAI(api_key=args.openaikey,)  # this is also the default, it can be omitted

    while True:
        
        user_input = input('Enter question:')
        if user_input == 'quit':
            break
        
        prompt = create_prompt(data_structure, user_input)
        query = call_llm(prompt)
        print(f'SQL: {query}')

        try:    
            answer = process_query(args.dbpath, query)
            print(f'Answer: {answer}')
        except:
            print('Error processing query! Try to reformulate.')