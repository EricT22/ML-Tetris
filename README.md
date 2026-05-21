# Machine Learning in Tetris — Deep-Q Learning Agent

A reinforcement learning agent that teaches itself to play Tetris from scratch using a Deep-Q Network (DQN), ultimately achieving scores exceeding **5 billion points**. Built with PyTorch and a custom Tetris environment in Python/Pygame.

Published at the **2024 Southern California Conference for Undergraduate Research (SCCUR)**.

---

## Demo

![Agent gameplay demo](demo/demo.gif)

> Score: 211,826,590 | Level: 627 | Lines: 6,262 — a snapshot mid-run. Peak performance exceeds 5B points.

---

## What is a DQN?

A **Deep-Q Network** is a neural network that learns to make decisions by estimating how "good" any given situation is — what Reinforcement Learning calls a **Q-value** (quality value).

The core idea: instead of being told what to do, the agent tries actions, observes the outcomes, and gradually learns which situations lead to high scores. Over hundreds of games, it gets better at predicting which board states are worth pursuing.

This agent takes a slightly different approach than a standard DQN. Rather than asking *"given the current board, how good is each action?"*, it asks *"given all the board states I could reach, which one looks best?"* The network evaluates each reachable next state and the agent picks the highest-valued one.

---

## How the Agent Works

### State Representation

Before placing each piece, the agent simulates every possible placement (all rotations × all columns × hold option) and evaluates each resulting board using **5 hand-crafted features**:

| Feature | Description |
|---|---|
| **Holes** | Empty cells with a filled cell above them — the agent learns to minimize these |
| **Bumpiness** | Sum of height differences between adjacent columns |
| **Max height** | Height of the tallest column |
| **Min height** | Height of the shortest column |
| **Lines cleared** | How many lines the placement would immediately clear |

These 5 numbers fully describe the board state the agent learns from.

### Neural Network Architecture

```
Input (5 features)
    → Linear(5 → 42) + ReLU
    → Linear(42 → 42) + ReLU
    → Linear(42 → 1)   ← predicted Q-value for this board state
```

A compact 3-layer network with He initialization, MSE loss, and Adam optimizer (lr = 0.001). Each forward pass takes a candidate board state and returns a single score estimating its long-term value.

### Reward Function

The reward for each piece placement is the **score gained from that move**:

- **Line clears**: 100 × level (1 line), 300 × level (2 lines), 500 × level (3 lines), 800 × level (4 lines / Tetris)
- **Hard drop bonus**: 2 points per row dropped
- **No line cleared**: effectively 0 reward, pushing the agent toward productive placements

As the agent levels up, line clears become more valuable — so clearing lines efficiently is always incentivized.

### Training Strategy

The agent uses standard DQN techniques to learn stably:

- **Epsilon-greedy exploration**: Starts fully random (ε = 1.0) and decays to 0 over ~500 games, shifting from exploration to exploitation
- **Experience replay**: Stores up to 4,500 transitions in a replay buffer; samples random mini-batches of 512 to break correlation between consecutive experiences
- **Bellman target**: `Q(s) = r + γ · max Q(s')` with γ = 0.995, weighting future rewards heavily
- **Batch learning**: The network only updates after the replay buffer is full, preventing early overfitting to sparse data

---

## Performance

| Metric | Value |
|---|---|
| Peak score | **5,000,000,000+** |
| Recorded run | 211,826,590 (level 627, 6,262 lines) |
| Games to convergence | ~500 |
| Training hardware | MacBook (CPU only) |
| Approx. training time | ~10–15 hours |

The agent learns to keep the board flat, prioritize line clears, and use the hold piece strategically — behaviors that emerge entirely from the reward signal.

---

## Project Structure

```
├── main.py          # Training loop — runs the agent and updates the network
├── test_nn.py       # Inference mode — watch the trained agent play (no learning)
├── agent.py         # DQN agent: network architecture, epsilon-greedy, replay
├── tetris_game.py   # Tetris environment: state, actions, rewards, game logic
├── board.py         # Board rendering (Pygame)
├── pieces.py        # Tetromino definitions and movement
├── bag.py           # 7-bag random piece generator
├── cfg.py           # All hyperparameters and constants
└── model/
    └── checkpoint.tar   # Trained model weights
```

---

## Running the Project

**Requirements**: Python 3.10+, PyTorch, Pygame, Matplotlib, NumPy

```bash
pip install torch pygame matplotlib numpy
```

**Watch the trained agent play** (recommended starting point):
```bash
python test_nn.py
```

**Train from scratch** (resumes from checkpoint if one exists):
```bash
python main.py
```

Close the Pygame window to stop training — the model saves automatically on exit. A score/loss plot appears when training ends.

---

## Key Challenges

- **State design**: The 5-feature hand-crafted state is compact enough to train quickly but expressive enough for the agent to learn strong play. Getting the right features (especially holes and bumpiness) was critical.
- **Reward sparsity**: Early in training, the agent rarely clears lines, so rewards are sparse. The replay buffer fill requirement delays learning until enough diverse experience is collected.
- **Speed vs. quality**: The game runs in real-time during training, so the agent must make decisions fast enough to keep up with the tick rate — particularly at high levels where pieces fall at ~60fps.

---

## Extending the Project

- **Deeper network**: Add more hidden layers or increase neuron count for potentially stronger play
- **CNN on raw board**: Replace hand-crafted features with a convolutional network reading the full 20×10 grid
- **Lookahead**: Incorporate the next piece into the state (currently only current + hold are considered)
- **Hyperparameter tuning**: Adjust `GAMMA`, `BATCH_SIZE`, or `EPSILON_DECAY` in `cfg.py` — small changes can meaningfully affect convergence speed
