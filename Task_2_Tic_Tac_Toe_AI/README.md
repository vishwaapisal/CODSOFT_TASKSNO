# CODSOFT Task 2 — Tic-Tac-Toe AI

A polished, responsive Tic-Tac-Toe web application where a human plays against an **unbeatable AI** powered by the **Minimax algorithm**.

## Features

- Human vs AI gameplay
- Unbeatable Minimax decision-making
- X / O selection
- Scoreboard for player, AI, and draws
- New Game and Reset Score controls
- Winning-cell animation
- AI thinking state
- Responsive modern UI/UX
- No backend or installation required
- Works directly in a browser

## How to run

1. Extract the ZIP.
2. Open `index.html` in Chrome, Edge, Firefox, or another modern browser.
3. Choose X or O and start playing.

## AI approach

The AI evaluates possible future game states using Minimax:

- AI win → positive score
- Human win → negative score
- Draw → zero
- Earlier wins are preferred and earlier losses are avoided.

Because Tic-Tac-Toe has a small finite search space, the complete game tree can be searched without needing a machine-learning model.

## Project structure

```text
CODSOFT_TASK2_TicTacToe_AI/
├── index.html
├── style.css
├── script.js
└── README.md
```

## CODSOFT requirement

The supplied internship brief describes Task 2 as implementing an AI agent that plays Tic-Tac-Toe against a human and suggests Minimax with or without Alpha-Beta pruning to make the AI unbeatable.
