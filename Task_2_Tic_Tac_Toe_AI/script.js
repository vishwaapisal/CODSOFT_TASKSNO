const state = {
  board: Array(9).fill(""),
  human: "X",
  ai: "O",
  current: "X",
  gameOver: false,
  scores: { X: 0, O: 0, draw: 0 }
};

const winningLines = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

const cells = [...document.querySelectorAll(".cell")];
const playerScore = document.getElementById("playerScore");
const aiScore = document.getElementById("aiScore");
const drawScore = document.getElementById("drawScore");
const roundTitle = document.getElementById("roundTitle");
const turnText = document.getElementById("turnText");
const turnSymbol = document.querySelector(".turn-symbol");
const messageText = document.getElementById("messageText");
const statusText = document.getElementById("statusText");
const statusPill = document.getElementById("statusPill");
const resultModal = document.getElementById("resultModal");
const resultTitle = document.getElementById("resultTitle");
const resultSubtitle = document.getElementById("resultSubtitle");
const resultIcon = document.getElementById("resultIcon");

cells.forEach(cell => cell.addEventListener("click", () => humanMove(Number(cell.dataset.index))));
document.getElementById("newGameBtn").addEventListener("click", newRound);
document.getElementById("modalNewGame").addEventListener("click", () => { closeModal(); newRound(); });
document.getElementById("modalClose").addEventListener("click", closeModal);
resultModal.addEventListener("click", e => { if (e.target === resultModal) closeModal(); });

document.querySelectorAll(".mark-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    if (state.board.some(Boolean)) {
      newRound(btn.dataset.mark);
    } else {
      setMark(btn.dataset.mark);
      newRound();
    }
  });
});

document.getElementById("resetScoreBtn").addEventListener("click", () => {
  state.scores = { X: 0, O: 0, draw: 0 };
  updateScores();
  setMessage("Score reset. Start a fresh round.");
});

function setMark(mark) {
  state.human = mark;
  state.ai = mark === "X" ? "O" : "X";
  document.querySelectorAll(".mark-btn").forEach(btn => btn.classList.toggle("active", btn.dataset.mark === mark));
}

function newRound(mark = state.human) {
  setMark(mark);
  state.board = Array(9).fill("");
  state.current = "X";
  state.gameOver = false;
  closeModal();
  render();
  if (state.ai === "X") {
    state.current = "X";
    setMessage("AI is making the first move…");
    updateTurn();
    setTimeout(aiMove, 350);
  } else {
    setMessage("Make your first move.");
  }
}

function humanMove(index) {
  if (state.gameOver || state.current !== state.human || state.board[index]) return;

  placeMove(index, state.human);
  const result = evaluate(state.board);
  if (finishIfNeeded(result)) return;

  state.current = state.ai;
  setMessage("AI is thinking…");
  updateTurn();
  setTimeout(aiMove, 300);
}

function aiMove() {
  if (state.gameOver || state.current !== state.ai) return;

  const move = getBestMove(state.board, state.ai, state.human);
  if (move !== -1) placeMove(move, state.ai);

  const result = evaluate(state.board);
  if (finishIfNeeded(result)) return;

  state.current = state.human;
  setMessage("Your move. Find the best line.");
  updateTurn();
}

function placeMove(index, mark) {
  state.board[index] = mark;
  render();
  const cell = cells[index];
  cell.classList.add("pop");
  setTimeout(() => cell.classList.remove("pop"), 260);
}

function render() {
  cells.forEach((cell, i) => {
    const mark = state.board[i];
    cell.textContent = mark;
    cell.classList.toggle("filled", Boolean(mark));
    cell.classList.toggle("x", mark === "X");
    cell.classList.toggle("o", mark === "O");
    cell.setAttribute("aria-label", mark ? `Cell ${i + 1}: ${mark}` : `Cell ${i + 1}: Empty`);
    cell.classList.remove("win");
  });
  updateScores();
  updateTurn();
}

function updateScores() {
  playerScore.textContent = state.scores[state.human];
  aiScore.textContent = state.scores[state.ai];
  drawScore.textContent = state.scores.draw;
}

function updateTurn() {
  if (state.gameOver) return;
  const mine = state.current === state.human;
  roundTitle.textContent = mine ? "Your turn" : "AI turn";
  turnText.textContent = mine ? "YOUR MOVE" : "AI THINKING";
  turnSymbol.textContent = state.current;
  turnSymbol.style.color = state.current === "X" ? "#59b8ff" : "#a695ff";
  statusText.textContent = mine ? "Your turn" : "AI is thinking";
  statusPill.querySelector(".status-dot").style.background = mine ? "#56e39f" : "#59b8ff";
}

function setMessage(text) {
  messageText.textContent = text;
}

function evaluate(board) {
  for (const [a,b,c] of winningLines) {
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return { winner: board[a], line: [a,b,c] };
    }
  }
  if (board.every(Boolean)) return { winner: "draw", line: [] };
  return null;
}

function finishIfNeeded(result) {
  if (!result) return false;
  state.gameOver = true;

  if (result.winner === "draw") {
    state.scores.draw++;
    setMessage("A perfect defense from both sides — draw.");
    showResult("Draw", "Neither side could find a winning path.", "=", false);
  } else {
    state.scores[result.winner]++;
    result.line.forEach(i => cells[i].classList.add("win"));
    const humanWon = result.winner === state.human;
    setMessage(humanWon ? "You found the winning line!" : "The AI found the winning line.");
    showResult(
      humanWon ? "You win!" : "AI wins",
      humanWon ? "Outstanding. You beat the optimal search." : "Minimax found the best available path.",
      humanWon ? "✓" : "⌬",
      humanWon
    );
  }
  render();
  statusText.textContent = "Round complete";
  statusPill.querySelector(".status-dot").style.background = "#56e39f";
  return true;
}

function showResult(title, subtitle, icon, playerWin) {
  resultTitle.textContent = title;
  resultSubtitle.textContent = subtitle;
  resultIcon.textContent = icon;
  resultIcon.style.color = playerWin ? "#56e39f" : "#59b8ff";
  resultIcon.style.background = playerWin ? "rgba(86,227,159,.1)" : "rgba(66,165,255,.1)";
  setTimeout(() => resultModal.classList.add("show"), 380);
}

function closeModal() {
  resultModal.classList.remove("show");
}

function getBestMove(board, ai, human) {
  const empty = board.map((v,i) => v ? -1 : i).filter(i => i !== -1);
  if (!empty.length) return -1;

  // Fast opening preference makes the AI feel natural while staying optimal.
  if (empty.length === 9) return 4;
  if (empty.length === 8 && board[4] === human) {
    const corners = [0,2,6,8].filter(i => !board[i]);
    if (corners.length) return corners[Math.floor(Math.random() * corners.length)];
  }

  let bestScore = -Infinity;
  let bestMoves = [];

  for (const i of empty) {
    board[i] = ai;
    const score = minimax(board, 0, false, ai, human);
    board[i] = "";
    if (score > bestScore) {
      bestScore = score;
      bestMoves = [i];
    } else if (score === bestScore) {
      bestMoves.push(i);
    }
  }
  return bestMoves[Math.floor(Math.random() * bestMoves.length)];
}

function minimax(board, depth, maximizing, ai, human) {
  const result = evaluate(board);
  if (result) {
    if (result.winner === ai) return 10 - depth;
    if (result.winner === human) return depth - 10;
    return 0;
  }

  const empty = board.map((v,i) => v ? -1 : i).filter(i => i !== -1);

  if (maximizing) {
    let best = -Infinity;
    for (const i of empty) {
      board[i] = ai;
      best = Math.max(best, minimax(board, depth + 1, false, ai, human));
      board[i] = "";
    }
    return best;
  } else {
    let best = Infinity;
    for (const i of empty) {
      board[i] = human;
      best = Math.min(best, minimax(board, depth + 1, true, ai, human));
      board[i] = "";
    }
    return best;
  }
}

// Start the first round.
newRound("X");
