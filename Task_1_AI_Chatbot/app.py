from flask import Flask, render_template, request, jsonify
import random
import re
from datetime import datetime

app = Flask(__name__)


def get_bot_response(message):
    message = message.lower().strip()

    rules = {
        r"\b(hi|hello|hey|hii)\b": [
            "Hello! 👋 I'm CodBot, your AI assistant. How can I help you today?",
            "Hey there! 😊 Nice to meet you. What can I help you with?",
            "Hi! 👋 I'm here and ready to chat with you."
        ],

        r"\bhow are you\b": [
            "I'm doing great! 🤖 Thanks for asking. How are you doing?",
            "I'm functioning perfectly! ⚡ Ready to help you."
        ],

        r"\bwhat is your name\b|\bwho are you\b": [
            "I'm CodBot 🤖, a rule-based AI chatbot created for the CodSoft Artificial Intelligence Internship."
        ],

        r"\bhelp\b|\bwhat can you do\b": [
            "I can have simple conversations with you! Try asking me about my name, the time, today's date, programming, AI, or just say hello. 😊"
        ],

        r"\b(ai|artificial intelligence)\b": [
            "Artificial Intelligence, or AI, is a branch of computer science focused on creating systems that can perform tasks normally requiring human intelligence. 🤖"
        ],

        r"\bpython\b": [
            "Python is a popular programming language known for its simple syntax. It is widely used in AI, machine learning, web development, and data science. 🐍"
        ],

        r"\bprogramming\b|\bcoding\b": [
            "Programming is the process of writing instructions that tell a computer what to do. Python is a great language to start with! 💻"
        ],

        r"\btime\b": [
            f"The current server time is {datetime.now().strftime('%I:%M %p')} ⏰"
        ],

        r"\bdate\b|\btoday\b": [
            f"Today's date is {datetime.now().strftime('%d %B %Y')} 📅"
        ],

        r"\bthank you\b|\bthanks\b": [
            "You're most welcome! 😊",
            "Happy to help! 🚀",
            "Anytime! Let me know if you need anything else. 🤖"
        ],

        r"\bbye\b|\bgoodbye\b|\bsee you\b": [
            "Goodbye! 👋 Have a wonderful day!",
            "See you later! 😊 Keep learning and keep building! 🚀"
        ]
    }

    for pattern, responses in rules.items():
        if re.search(pattern, message):
            return random.choice(responses)

    fallback_responses = [
        "Hmm, I don't understand that yet. Try asking me something about AI, Python, programming, time, or date. 🤔",
        "That's interesting! I'm still a rule-based chatbot, so I may not understand every question. 😊",
        "Sorry, I don't have a predefined response for that yet. Try another question! 🤖"
    ]

    return random.choice(fallback_responses)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"response": "Please type a message first! 😊"})

    response = get_bot_response(user_message)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)