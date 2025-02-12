from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    # Logic to parse and execute the task
    return {"message": "Task executed successfully"}

@app.get("/read")
async def read_file(path: str):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return {"content": file.read()}
    else:
        raise HTTPException(status_code=404, detail="File not found")

import os
import subprocess
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException

app = FastAPI()

# A1: Install uv and run datagen.py
def a1_run_datagen(user_email):
    try:
        subprocess.run(["pip", "install", "uv"], check=True)
        subprocess.run(["python3", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", user_email], check=True)
        return {"message": "Data generation completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A2: Format the contents of /data/format.md using prettier
def a2_format_markdown():
    try:
        subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)
        return {"message": "File formatted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A3: Count the number of Wednesdays in /data/dates.txt
def a3_count_wednesdays():
    try:
        with open('/data/dates.txt', 'r') as file:
            dates = file.readlines()
        wednesday_count = sum(1 for date in dates if datetime.strptime(date.strip(), '%Y-%m-%d').weekday() == 2)
        with open('/data/dates-wednesdays.txt', 'w') as file:
            file.write(str(wednesday_count))
        return {"message": "Count of Wednesdays written to /data/dates-wednesdays.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A4: Sort contacts in /data/contacts.json
def a4_sort_contacts():
    try:
        with open('/data/contacts.json', 'r') as file:
            contacts = json.load(file)
        sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
        with open('/data/contacts-sorted.json', 'w') as file:
            json.dump(sorted_contacts, file)
        return {"message": "Contacts sorted and written to /data/contacts-sorted.json."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A5: Write the first line of the 10 most recent .log files
def a5_recent_log_lines():
    try:
        log_files = sorted([f for f in os.listdir('/data/logs/') if f.endswith('.log')], key=lambda x: os.path.getmtime(os.path.join('/data/logs/', x)), reverse=True)[:10]
        recent_lines = []
        for log_file in log_files:
            with open(os.path.join('/data/logs/', log_file), 'r') as file:
                recent_lines.append(file.readline().strip())
        with open('/data/logs-recent.txt', 'w') as file:
            file.write('\n'.join(recent_lines))
        return {"message": "Recent log lines written to /data/logs-recent.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A6: Create an index of H1 titles from Markdown files
def a6_create_index():
    try:
        index = {}
        for filename in os.listdir('/data/docs/'):
            if filename.endswith('.md'):
                with open(os.path.join('/data/docs/', filename), 'r') as file:
                    for line in file:
                        if line.startswith('# '):
                            index[filename] = line[2:].strip()  # Extract title
                            break
        with open('/data/docs/index.json', 'w') as file:
            json.dump(index, file)
        return {"message": "Index created and written to /data/docs/index.json."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A7: Extract sender's email from /data/email.txt using LLM
def a7_extract_sender_email():
    try:
        with open('/data/email.txt', 'r') as file:
            email_content = file.read()
        # Call LLM here to extract sender's email
        # Assuming you have a function `call_llm` that takes the content and returns the email
        sender_email = call_llm(email_content)  # Implement this function
        with open('/data/email-sender.txt', 'w') as file:
            file.write(sender_email)
        return {"message": "Sender's email extracted and written to /data/email-sender.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A8: Extract credit card number from image using LLM
def a8_extract_credit_card():
    try:
        # Call LLM here to extract credit card number from the image
        # Assuming you have a function `extract_credit_card_from_image` that takes the image path and returns the number
        card_number = extract_credit_card_from_image('/data/credit-card.png')  # Implement this function
        with open('/data/credit-card.txt', 'w') as file:
            file.write(card_number.replace(" ", ""))  # Remove spaces
        return {"message": "Credit card number extracted and written to /data/credit-card.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A9: Find the most similar pair of comments
def a9_find_similar_comments():
    try:
        with open('/data/comments.txt', 'r') as file:
            comments = file.readlines()
        # Call LLM or use embeddings to find the most similar comments
        similar_comments = find_most_similar_comments(comments)  # Implement this function
        with open('/data/comments-similar.txt', 'w') as file:
            file.write('\n'.join(similar_comments))
        return {"message": "Most similar comments written to /data/comments-similar.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A10: Calculate total sales of "Gold" ticket type
def a10_total_gold_sales():
    try:
        import sqlite3
        conn = sqlite3.connect('/data/ticket-sales.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
        total_sales = cursor.fetchone()[0] or 0
        with open('/data/ticket-sales-gold.txt', 'w') as file:
            file.write(str(total_sales))
        conn.close()
        return {"message": "Total sales of Gold tickets written to /data/ticket-sales-gold.txt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example of how to call these functions in your /run endpoint
@app.post("/run")
async def run_task(task: str):
    # Parse the task description and call the appropriate function
    if "datagen" in task:
        return a1_run_datagen("user@example.com")  # Replace with actual user email
    elif "format" in task:
        return a2_format_markdown()
    elif "Wednesdays" in task:
        return a3_count_wednesdays()
    elif "sort contacts" in task:
        return a4_sort_contacts()
    elif "recent log" in task:
        return a5_recent_log_lines()
    elif "index" in task:
        return a6_create_index()
    elif "extract sender's email" in task:
        return a7_extract_sender_email()
    elif "extract credit card" in task:
        return a8_extract_credit_card()
    elif "similar comments" in task:
        return a9_find_similar_comments()
    elif "total sales of Gold" in task:
        return a10_total_gold_sales()
    else:
        raise HTTPException(status_code=400, detail="Task not recognized.")
    
import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Function to call the LLM API
def call_llm(task_description):
    url = "https://api.aiproxy.com/v1/llm"  # Replace with the actual LLM API endpoint
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",  # Specify the model
        "prompt": task_description,
        "max_tokens": 150,  # Adjust based on your needs
        "temperature": 0.5,  # Adjust for creativity
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get("output")  # Adjust based on the actual response structure
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example of how to use the LLM in a task
@app.post("/run")
async def run_task(task: str):
    # Parse the task description and call the appropriate function
    if "extract sender's email" in task:
        email_content = "..."  # Get the email content from the file or input
        sender_email = call_llm(f"Extract the sender's email from the following content: {email_content}")
        with open('/data/email-sender.txt', 'w') as file:
            file.write(sender_email)
        return {"message": "Sender's email extracted and written to /data/email-sender.txt."}
    elif "extract credit card" in task:
        # Similar logic for extracting credit card number
        pass
    # Add other tasks as needed
    else:
        raise HTTPException(status_code=400, detail="Task not recognized.")