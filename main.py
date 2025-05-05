import os
from dotenv import load_dotenv
from openai import OpenAI
import sqlite3
import json

load_dotenv(dotenv_path="D:\\one_data_assessment\\ai_task_manager\\.env.txt")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

conn= sqlite3.connect("tasks.db")
cursor= conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, priority TEXT, status TEXT, deadline DATE)")
conn.commit()

system_message = """ You are a smart task manager assistant. The user will give you one or more tasks in natural language. For each task, extract the following:
- task: A short summary of the task
- priority: Choose from [urgent, high, medium, low]
- status: Default to 'Not Started' unless the user says otherwise
- deadline: Extract any mentioned due date (in 'YYYY-MM-DD' format). If not mentioned, return null.
Return the result strictly as a JSON array. Do not include any explanation or additional text.
Example:
Input: "I need to finalize the Walmart dataset analysis by May 5. Also, I want to learn agentic AI before May 8."
Output:
[  {"task": "Finalize the Walmart dataset analysis",
    "priority": "high",
    "status": "Not Started", 
    "deadline": "2025-05-05"}, 
    
    {"task": "Learn agentic AI",
    "priority": "medium",
    "status": "Not Started",
    "deadline": "2025-05-08"}]"""

messages=[{"role":"system", "content":system_message}]
task_list=[]

print("Hello! I'm your Task Manager Assistant – input a task, or type 'show' to see all tasks, or 'exit' to quit: ")

while True:
    user_input= input("you: ")
     
    if user_input.lower()=="exit":
        break

    if user_input.lower()=="show":
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

        for row in rows:
          print(row)
        break

         

    messages.append({"role":"user", "content":user_input})

    response=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0
    )

    assistant_reply=response.choices[0].message.content
    print("Task Manager:",assistant_reply)

    task_list.append(assistant_reply)

    try:
        tasks= json.loads(assistant_reply)
        for task in tasks:
            cursor.execute("Insert into tasks(task,priority,status,deadline) values(?, ?, ?, ? )",
                           (task["task"], task["priority"], task["status"], task["deadline"]))
            conn.commit()
            print("Tasks saved to the database")
    except Exception as e:
            print("Failed to save tasks to the database",e)


    messages.append({"role":"assistant", "content":assistant_reply})





