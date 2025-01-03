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
![alt text](https://github.com/nuketayev/Train-an-AI-to-Play-Snake/blob/main/16.png "map")

The arrow is an image, and by default, it points to the right. By calculating the angle, we simply rotate the image so it points directly at the food.

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

## 🚀 Launching the Game

To start the game, run the `start_game.py` script. This will open a menu where you can select between Human Mode and AI Mode.

```bash
python start_game.py
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

## 🧠 How the AI Learns

### Simple Explanation

Imagine you are teaching a pet to play a game. At first, th epet doesn't know what to do, so it tries different things. When it does something good, like finding food, you give it a treat. When it does something bad, like bumping into a wall, you say "no" and it loses points. Over time, the pet learns what actions lead to treats and what actions lead to "no".

In this game, the AI is like the pet. It tries different, random at the beginning, moves to find food and avoid walls. When it finds food, it gets points. When it hits a wall, it loses points. The AI remembers what moves were good and what moves were bad, and it gets better at the game over time.

### Detailed Explanation

The AI in this game uses a technique called **Deep Q-Learning**. Here's how it works:

1. **Experience Collection**: The AI collects experiences as it plays the game. Each experience is a tuple of (state, action, reward, next_state, done). The state is the current situation in the game, the action is the move the AI made, the reward is the points it got, the next_state is the situation after the move, and done is whether the game is over.

   ```python
   def remember(self, state, action, reward, next_state, done):
       self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
   ```

2. **Replay Memory**: The AI stores these experiences in a replay memory. This allows it to remember past experiences and learn from them.

   ```python
   self.memory = deque(maxlen=MAX_MEMORY) # if max is reached -> popleft()
   ```

3. **Training Loop**: The AI trains its neural network using mini-batches of experiences from the replay memory. This helps it learn which actions are good and which are bad.

   ```python
   def train_long_memory(self):
       if len(self.memory) > BATCH_SIZE:
           mini_sample = random.sample(self.memory, BATCH_SIZE)
       else:
           mini_sample = self.memory

       states, actions, rewards, next_states, dones = zip(*mini_sample)
       self.trainer.train_step(states, actions, rewards, next_states, dones)
   ```

4. **Neural Network**: The AI uses a neural network to predict the best move to make in a given state. The network is trained to minimize the difference between its predictions and the actual rewards.

   ```python
   class Linear_QNet(nn.Module):
       def __init__(self, input_size, hidden_size, output_size):
           super().__init__()
           self.linear1 = nn.Linear(input_size, hidden_size)
           self.linear2 = nn.Linear(hidden_size, output_size)

       def forward(self, x):
           x = F.relu(self.linear1(x))
           x = self.linear2(x)
           return x
   ```

5. **Exploration vs. Exploitation**: The AI balances between exploring new moves and exploiting known good moves. At the beginning, it explores more (random moves) to learn about the game. As it gets better, it exploits its knowledge to score higher.

   ```python
   def get_action(self, state):
       self.epsilon = 80 - self.n_games
       final_move = [0,0,0]
       if random.randint(0, 200) < self.epsilon:
           move = random.randint(0, 2)
           final_move[move] = 1
       else:
           state0 = torch.tensor(state, dtype=torch.float)
           prediction = self.model(state0)
           move = torch.argmax(prediction).item()
           final_move[move] = 1

       return final_move
   ```

By following these steps, the AI learns to play the Snake Game better and better over time.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements or bug fixes.

---

## 🙏 Acknowledgements

Built with **Pygame** and **PyTorch**. Enjoy the game, and happy coding! 🐍💻🎉
