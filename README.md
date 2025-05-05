# AI_Task_Manager
AI based Task Manager Agent that uses OpenAI's GPT to extract and organize tasks from natural language input and uses sql database for storage and retrieval.

# Features and Extraction
#Natural language task input
#Automatic extraction of task details:
 #Task description
 Priority (urgent, high, medium, low)
 Status (defaults to "Not Started")
 Deadline dates
 
# Storage and retrieval
Local SQLite database storage
View all saved tasks

# Requirements
Python
OpenAI API Key
 Create a .env.txt file in the project directory with your OpenAI API key

# Commands
Enter tasks in natural language: "I need to finish the report by next Friday"
Type show to display all saved tasks
Type exit to quit the application


