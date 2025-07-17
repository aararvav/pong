# 🏓 Pong!!!

A classic Pong game made with Python and Pygame!  
Supports both **Single-player (with AI)** and **2-player** modes:
- Score tracking
- Mode selector screen
- AI difficulty levels (Easy, Medium, Hard)
- Gradually increasing ball speed per difficulty
- Sound effects (bounce, score)
- Paddle boundary control
- Win screen

---

## 📷 Preview

![Pong Screenshot](screenshot.png)

---

## 🚀 Features

- 🎮 Single-player with AI (Easy / Medium / Hard)
- 🎮 2-player controls (W/S and UP/DOWN)
- 🧠 Mode selector screen (choose between single or multiplayer)
- 🔊 Sound effects on bounce and score
- 📈 Gradually increasing ball speed (based on difficulty)
- 🧱 Paddle boundaries (no flying off-screen)
- 🏆 Win message when a player reaches 6 points
- ⏳ Smooth gameplay with `delta_time` for frame consistency

---

## 🛠️ How to Run

1. Install [Python](https://www.python.org/downloads/)
2. Install `pygame` using pip:

```bash
pip install pygame
```

3. Place your sound files in the same folder:
   - `bounce.wav` → for ball bounces
   - `score.wav` → for goals

4. Run the game:

```bash
python pong.py
```

---

## 🎮 Controls

| Player | Move Up | Move Down |
|--------|---------|-----------|
| P1     | `W`     | `S`       |
| P2     | `↑`     | `↓`       |

- Press `Space` to start
- Use `↑` / `↓` keys to navigate menus
- Press `Enter` to confirm selection

---

## 🧠 Planned Features

- [ ] Restart after win
- [ ] Pause / Resume functionality
- [ ] Power-ups / Extra challenges

---

## 🧪 Made With

- Python 🐍
- Pygame 🎮

---

## 🙌 Credits

Made with ❤️ by [aararvav](https://github.com/aararvav)
