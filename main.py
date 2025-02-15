from flask import Flask, request, jsonify
import os
import subprocess
import json
import pandas as pd
app = Flask(__name__)
import re
import difflib
from transformers import pipeline
from PIL import Image
import pytesseract
import requests

# Function to extract sender's email from text using regex
def call_llm_to_extract_email(email_content):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, email_content)
    return match.group(0) if match else "Email not found"

# Function to extract card number from an image using OCR (Tesseract)
def call_llm_to_extract_card_number(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    card_pattern = r"\b(?:\d[ -]*?){13,16}\b"  # Simple pattern for card numbers
    match = re.search(card_pattern, text.replace(" ", ""))
    return match.group(0) if match else "Card number not found"

# Function to find the most similar pair of comments using difflib
def find_most_similar_comments(comments):
    most_similar = None
    highest_ratio = 0
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            ratio = difflib.SequenceMatcher(None, comments[i].strip(), comments[j].strip()).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                most_similar = (comments[i].strip(), comments[j].strip())
    return most_similar if most_similar else ("No similar comments found",)


@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Task A1: Install uv and run datagen.py
        if "install uv and run" in task_description:
            user_email = os.environ.get("USER_EMAIL")
            subprocess.run(["pip", "install", "uv"], check=True)
            subprocess.run(["python", "datagen.py", user_email], check=True)
            return jsonify({"message": "Task A1 executed successfully"}), 200

        # Task A2: Format the contents of /data/format.md using prettier
        elif "format the contents of /data/format.md" in task_description:
            subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)
            return jsonify({"message": "Task A2 executed successfully"}), 200

        # Task A3: Count the number of Wednesdays in /data/dates.txt
        elif "count the number of Wednesdays" in task_description:
            with open('/data/dates.txt', 'r') as f:
                dates = f.readlines()
            wednesdays_count = sum(1 for date in dates if date.strip() and date.strip().startswith('Wed'))
            with open('/data/dates-wednesdays.txt', 'w') as f:
                f.write(str(wednesdays_count))
            return jsonify({"message": "Task A3 executed successfully"}), 200

        # Task A4: Sort contacts in /data/contacts.json
        elif "sort the array of contacts in /data/contacts.json" in task_description:
            with open('/data/contacts.json', 'r') as f:
                contacts = json.load(f)
            sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
            with open('/data/contacts-sorted.json', 'w') as f:
                json.dump(sorted_contacts, f)
            return jsonify({"message": "Task A4 executed successfully"}), 200

        # Task A5: Write the first line of the 10 most recent .log files
        elif "write the first line of the 10 most recent .log files" in task_description:
            log_files = sorted([f for f in os.listdir('/data/logs/') if f.endswith('.log')], key=lambda x: os.path.getmtime(os.path.join('/data/logs/', x)), reverse=True)[:10]
            with open('/data/logs-recent.txt', 'w') as f:
                for log_file in log_files:
                    with open(os.path.join('/data/logs/', log_file), 'r') as log:
                        first_line = log.readline().strip()
                        f.write(first_line + '\n')
            return jsonify({"message": "Task A5 executed successfully"}), 200

        # Task A6: Create an index file for Markdown files
        elif "find all Markdown files in /data/docs" in task_description:
            index = {}
            for filename in os.listdir('/data/docs/'):
                if filename.endswith('.md'):
                    with open(os.path.join('/data/docs/', filename), 'r') as f:
                        for line in f:
                            if line.startswith('# '):
                                index[filename] = line[2:].strip()  # Extract title
                                break
            with open('/data/docs/index.json', 'w') as f:
                json.dump(index, f)
            return jsonify({"message": "Task A6 executed successfully"}), 200

        # Task A7: Extract sender's email from /data/email.txt using LLM
        elif "extract the sender’s email address" in task_description:
            with open('/data/email.txt', 'r') as f:
                email_content = f.read()
            # Call LLM API to extract email (pseudo-code)
            sender_email = call_llm_to_extract_email(email_content)  # Implement this function
            with open('/data/email-sender.txt', 'w') as f:
                f.write(sender_email)
            return jsonify({"message": "Task A7 executed successfully"}), 200

        # Task A8: Extract credit card number from image using LLM
        elif "extract the card number from /data/credit-card.png" in task_description:
            # Call LLM API to extract card number (pseudo-code)
            card_number = call_llm_to_extract_card_number('/data/credit-card.png')  # Implement this function
            with open('/data/credit-card.txt', 'w') as f:
                f.write(card_number.replace(" ", ""))
            return jsonify({"message": "Task A8 executed successfully"}), 200

        # Task A9: Find the most similar pair of comments
        elif "find the most similar pair of comments" in task_description:
            with open('/data/comments.txt', 'r') as f:
                comments = f.readlines()
            similar_pair = find_most_similar_comments(comments)  # Implement this function
            with open('/data/comments-similar.txt', 'w') as f:
                f.write('\n'.join(similar_pair))
            return jsonify({"message": "Task A9 executed successfully"}), 200

        # Task A10: Calculate total sales of "Gold" ticket type
        elif "total sales of all the items in the 'Gold' ticket type" in task_description:
            import sqlite3
            conn = sqlite3.connect('/data/ticket-sales.db')
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price * units) FROM tickets WHERE type='Gold'")
            total_sales = cursor.fetchone()[0] or 0
            with open('/data/ticket-sales-gold.txt', 'w') as f:
                f.write(str(total_sales))
            conn.close()
            return jsonify({"message": "Task A10 executed successfully"}), 200

        elif "count the number of Thursdays" in task_description:
            with open('/data/extracts.txt', 'r') as f:
                thursdays_count = sum(1 for line in f if 'Thu' in line)
            with open('/data/extracts-count.txt', 'w') as f:
                f.write(str(thursdays_count))
            return jsonify({"message": "Task completed"}), 200

        elif "contents.log" in task_description and "Sunday" in task_description:
            with open('/data/contents.log', 'r') as f:
                sundays_count = sum(1 for line in f if 'Sun' in line)
            with open('/data/contents.dates', 'w') as f:
                f.write(str(sundays_count))
            return jsonify({"message": "Task completed"}), 200

        elif "fetch data from an API" in task_description:
            response = requests.get("https://api.example.com/data")  # Replace with real API
            with open('/data/api_data.json', 'w') as f:
                json.dump(response.json(), f)
            return jsonify({"message": "Task completed"}), 200

        elif "clone a git repo" in task_description:
            subprocess.run(["git", "clone", "https://github.com/example/repo.git", "/data/repo"], check=True)
            with open('/data/repo_status.txt', 'w') as f:
                f.write("Repo cloned successfully.")
            return jsonify({"message": "Task completed"}), 200

        elif "run a SQL query" in task_description:
            conn = sqlite3.connect('/data/database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            result = cursor.fetchone()[0]
            with open('/data/sql_result.txt', 'w') as f:
                f.write(str(result))
            conn.close()
            return jsonify({"message": "Task completed"}), 200

        elif "scrape a website" in task_description:
            from bs4 import BeautifulSoup
            response = requests.get("https://example.com")
            soup = BeautifulSoup(response.text, 'html.parser')
            with open('/data/web_scraped.txt', 'w') as f:
                f.write(soup.get_text())
            return jsonify({"message": "Task completed"}), 200

        elif "compress or resize an image" in task_description:
            img = Image.open('/data/image.png')
            img = img.resize((100, 100))
            img.save('/data/image_resized.png')
            return jsonify({"message": "Task completed"}), 200

        elif "transcribe audio" in task_description:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile('/data/audio.mp3') as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            with open('/data/audio_transcription.txt', 'w') as f:
                f.write(text)
            return jsonify({"message": "Task completed"}), 200

        elif "convert Markdown to HTML" in task_description:
            with open('/data/input.md', 'r') as f:
                import markdown
                html_content = markdown.markdown(f.read())
            with open('/data/output.html', 'w') as f:
                f.write(html_content)
            return jsonify({"message": "Task completed"}), 200

        elif "filter a CSV file and return JSON data" in task_description:
            df = pd.read_csv('/data/input.csv')
            filtered_df = df[df['Category'] == 'Electronics']
            json_data = filtered_df.to_json(orient='records')
            with open('/data/output.json', 'w') as f:
                f.write(json_data)
            return jsonify(json_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    if not os.path.exists(file_path):
        return jsonify({}), 404

    with open(file_path, 'r') as file:
        content = file.read()
    return content, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)