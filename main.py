from flask import Flask, request, render_template
import vertexai
from vertexai.preview import agents
import uuid

app = Flask(__name__)

# Vertex AI configuration
PROJECT_ID = "hacker2025-team-112-dev"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = "projects/hacker2025-team-112-dev/locations/us-central1/agents/5e6e3b1f-3f8e-4f3e-9e3e-2f3e3e3e3e3e"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create Agent instance
agent = agents.Agent.from_agent_resource_name(AGENT_RESOURCE_NAME)

# In-memory chat history
chat_history = []

@app.route('/')
def home():
    return render_template("index.html", chat_history=chat_history)

@app.route('/my_coach', methods=['GET'])
def my_coach():
    return render_template('my_coach.html', chat_history=chat_history)

@app.route('/ask_coach', methods=['POST'])
def ask_coach():
    user_query = request.form.get("coach_input", "")
    chat_history.append({"user": user_query})
    session_id = str(uuid.uuid4())

    try:
        response = agent.chat(
            user_message=user_query,
            session_id=session_id,
        )
        agent_reply = response.text
    except Exception as e:
        agent_reply = f"Error: {str(e)}"

    chat_history[-1]["agent"] = agent_reply
    return render_template("my_coach.html", chat_history=chat_history)

@app.route('/clear_chat', methods=['POST'])
@app.route('/new_chat', methods=['POST'])
def clear_chat():
    chat_history.clear()
    return render_template("my_coach.html", chat_history=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
