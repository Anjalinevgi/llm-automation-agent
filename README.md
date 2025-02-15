LLM-Based Automation Agent 🚀
This project is an AI-powered automation agent that parses task descriptions and executes various operational and business-related tasks, including file processing, web scraping, SQL queries, API interactions, and more.

📌 Features
Task Execution via LLM: Interprets tasks and performs relevant operations.
Operational Tasks:
Count occurrences of weekdays in log files
Extract emails and card numbers from text/images
Convert Markdown to HTML
Filter and return JSON from CSV
Business Tasks:
Fetch data from an API
Clone a GitHub repository and commit changes
Run SQL queries on SQLite/DuckDB
Scrape website data
Transcribe audio from an MP3 file
Security Compliance:
❌ No file deletions
❌ No access beyond /data directory
⚙️ Installation & Setup
1️⃣ Clone the Repository

Copy
Edit
git clone https://github.com/your-username/your-repo.git
cd your-repo
2️⃣ Install Dependencies
Ensure you have Python 3.8+ installed, then run:

Copy
Edit
pip install -r requirements.txt
3️⃣ Run the Application

Copy
Edit
python app.py
4️⃣ Use the API
Run a Task

Copy
Edit
curl -X POST "http://localhost:8000/run?task=fetch+data+from+an+API"
Read a File

Copy
Edit
curl -X GET "http://localhost:8000/read?path=/data/api_data.json"
🐳 Run with Docker
1️⃣ Build the Docker Image

Copy
Edit
docker build -t your-username/llm-agent .
2️⃣ Run the Container

Copy
Edit
docker run -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 your-username/llm-agent
3️⃣ Access the API

Copy
Edit
curl -X POST "http://localhost:8000/run?task=convert+Markdown+to+HTML"
📜 Security & Compliance
🔒 Files outside /data/ are never accessed or modified.
🔒 No file deletions are allowed.
🔒 Uses AIPROXY_TOKEN securely via environment variables.
🏆 Evaluation Criteria
✅ GitHub repository with MIT License
✅ Functional API handling all defined tasks
✅ Docker container deploys API correctly
✅ Passing POST /run?task=... and GET /read?path=... tests

📌 License
This project is licensed under the MIT License. See the LICENSE file for details.

🤝 Contributing
Want to improve this project? Feel free to fork, create a PR, or open an issue! 🚀
