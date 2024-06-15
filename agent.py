import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque, namedtuple

torch.manual_seed(0)
np.random.seed(1)

Transition = namedtuple('Transition',
                        ('state', 'action', 'reward', 'next_state', 'done'))

class Agent:
    def __init__(self,
                env, discount_factor = 0.95,
                epsilon=1, epsilon_min=0.01, epsilon_decay=0.995,
                learning_rate = 0.01, max_memory_size=2000) -> None:
        self.env = env
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.memory = deque(maxlen=max_memory_size)
        # size of the Tetris state, arbitrary number for now (from env)
        self.state_size = 5
        # number of actions available, arbitrary for now as well (from env)
        self.action_size = 5
        self.build_NN()
    
    def build_NN(self):
        self.model = nn.Sequential(
            # input layer goes to hidden layer with 16 neurons
            nn.Linear(self.state_size, 32),
            # Will use the ReLU activation function for transition to next layer:
            # z^(L) = w^(L) * a^(L-1) + b(L)
            # a^(L) = ReLU(z^(L))
            nn.ReLU(), 
            # hidden layer 1 goes to hidden layer 2 (arbitrarily chose two hidden layers each with size 32)
            nn.Linear(32, 32),
            # also uses ReLU activation function
            nn.ReLU(),
            # hidden layer 2 goes to output layer
            nn.Linear(32, self.action_size)
        )
        # Will use Mean Squared Error Loss function
        self.loss_fn = nn.MSELoss()
        # Will use stochastic gradient descent algorithm
        self.optimizer = torch.optim.SGD(self.model.parameters(), self.learning_rate)
        
    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        
        # don't want calculate gradients b/c we're not backpropagating at this step, 
        # just finding out which action to take given the current nn
        with torch.no_grad():
            # makes a forward pass through model with the given state
            # [0] is to keep the return value a 1d tensor 
            q_vals = self.model(torch.tensor(state))[0]
        
        # returns highest rewarded action as a regular python number, not a tensor
        return torch.argmax(q_vals).item()
    
    def store_in_memory(self, transition):
        self.memory.append(transition)

    def lower_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay if self.epsilon > self.epsilon_min else self.epsilon

    def optimize_model(self):
        pass