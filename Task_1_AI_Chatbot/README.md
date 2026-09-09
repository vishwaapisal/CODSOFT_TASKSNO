# CodBot AI Chatbot

A simple rule-based chatbot web app built with Python and Flask. It runs in the browser and responds to common greetings and questions using pattern-based logic.

## Project Overview

This project is a lightweight chatbot interface inspired by a terminal/command-line look. The app uses:

- Python for the backend logic
- Flask for routing and API handling
- HTML for the chatbot layout
- CSS for the terminal-style design
- JavaScript for sending messages and displaying responses

The main purpose of the app is to demonstrate a basic AI chatbot workflow and how a frontend can connect with a backend API.

## Features

- Friendly text-based chatbot interface
- Rule-based response matching using regular expressions
- Handles greetings, help messages, AI/Python questions, date/time queries, and general fallback responses
- JSON API endpoint for chatbot responses
- Responsive terminal-style UI

## Rule Type Used

This chatbot uses a rule-based approach, not a machine learning model.

The logic is implemented in [app.py](app.py) using regular expressions (regex) and a dictionary of patterns. For example:

- Greeting patterns such as `hi`, `hello`, and `hey`
- Question patterns such as `what is your name`, `who are you`, and `what can you do`
- Topic rules for `ai`, `python`, `programming`, `time`, and `date`
- Fallback responses when the input does not match any known rule

The workflow is:

1. Convert the user message to lowercase.
2. Search the message against each regex rule.
3. If a rule matches, return one random response from that category.
4. If no rule matches, return a fallback response.

This is a classic pattern-matching chatbot design used for simple conversational systems.

## Project Structure

- app.py — Flask application and chatbot logic
- templates/index.html — main chatbot page
- static/style.css — terminal-inspired styling
- static/script.js — frontend message sending logic
- requirements.txt — Python dependencies

## How It Works

1. The browser loads the HTML page from the Flask server.
2. The user types a message in the chat box.
3. JavaScript sends the message to the /chat endpoint as JSON.
4. Flask receives the request and calls the chatbot response logic.
5. A matching response is generated and sent back to the frontend.
6. The frontend displays the bot reply in the chat window.

## Tech Stack

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Flask server:

```bash
python app.py
```

Then open the browser and visit:

```text
http://127.0.0.1:5000
```

## Example Questions

- Hello
- Who are you?
- What can you do?
- What is AI?
- What is Python?
- What is the time?
- What is the date?
- Thank you
- Goodbye

## Notes

This is a rule-based chatbot rather than a machine learning model. It works by matching user input against predefined patterns and returning appropriate responses. It is ideal for learning how chatbot logic and web app integration work together.
