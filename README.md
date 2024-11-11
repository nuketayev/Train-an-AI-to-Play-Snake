
# 🐍 Snake Game AI 🎮

A fun twist on the classic Snake Game! Play it yourself or watch an AI agent learn and play autonomously using **Deep Q-Learning**. Built with **Python** and **Pygame** for the game, and **PyTorch** for the neural network and training.

---

## ✨ Features

- **👾 Human Mode**: Play the classic Snake Game with keyboard controls.
- **🤖 AI Mode**: Watch the AI learn and play autonomously with Deep Q-Learning.
- **📊 Training Visualization**: Real-time plot of training stats like scores and mean scores.
- **⏩ Adjustable Game Speed**: Speed up or slow down the game during AI training.
- **➡️ Directional Arrow for Food:**: In human control mode, an arrow appears at the top of the screen, pointing toward the food using basic trigonometric calculations.
Implementing a guide arrow like this in a game turned out to be surprisingly straightforward!
Here’s a quick overview of the approach used in the game: All that's needed are the (x, y) coordinates of the player’s current position (in this case, the snake's head) and the coordinates of the target object (the food).
![alt text](https://github.com/nuketayev/Train-an-AI-to-Play-Snake/16.png "map")

---

## 🗂️ Project Structure

- **`agent.py`**: Handles AI interactions and neural network training.
- **`AI_snake_game.py`**: Snake game logic for AI mode.
- **`helper.py`**: Utility for plotting training statistics.
- **`human_snake_game.py`**: Snake game logic for human mode.
- **`model.py`**: Defines the neural network architecture.
- **`start_game.py`**: Entry point to select and start game modes.

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nuketayev/Train-an-AI-to-Play-Snake.git
   cd Train-an-AI-to-Play-Snake
   ```
2. **Install dependencies:**
   ```bash
   pip install -r "requirements"
   ```

---

## 🎮 Usage

### **Human Mode**
- Run the game and select **"Play Game"** in the main menu.
- **Controls**: Arrow keys or WASD to move, `R` to restart, `ESC` to pause, `SPACE` for no-wall mode.

### **AI Mode**
- Run the game and select **"Train AI"** in the main menu.
- **Controls**: `W`/UP to increase speed, `S`/DOWN to decrease speed, `R` to reset speed, `Q` to quit.

---

## 🧠 Neural Network

A simple feedforward network with one hidden layer of 256 units, optimized with Deep Q-Learning:
1. **Experience Collection**: Collects state-action-reward experiences.
2. **Replay Memory**: Stores experiences for efficient training.
3. **Training Loop**: Samples mini-batches from memory to train the model.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements or bug fixes.

---

## 🙏 Acknowledgements

Built with **Pygame** and **PyTorch**. Enjoy the game, and happy coding! 🐍💻🎉
