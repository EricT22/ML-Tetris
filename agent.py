import cfg
import os
import torch
import torch.nn as nn
import numpy as np
from collections import deque
from random import sample

torch.manual_seed(0)
np.random.seed(1)


class Agent:
    def __init__(self, env) -> None:
        self.env = env
        self.gamma = cfg.GAMMA
        self.epsilon = cfg.EPSILON
        self.epsilon_min = cfg.EPSILON_MIN
        self.epsilon_decay = cfg.EPSILON_DECAY
        self.learning_rate = cfg.SGD_LEARNING_RATE
        self.memory = deque(maxlen=cfg.MAX_MEMORY_SIZE)

        # size of the Tetris state
        self.state_size = env.state_size
        
        # each state gets one overall rating
        self.size_of_state_rating = 1

        self.build_NN()
        self.load()
    
    def build_NN(self):
        self.model = nn.Sequential(
            # input layer goes to hidden layer with 16 neurons
            nn.Linear(self.state_size, 16),
            # Will use the ReLU activation function for transition to next layer:
            # z^(L) = w^(L) * a^(L-1) + b(L)
            # a^(L) = ReLU(z^(L))
            nn.ReLU(), 
            # hidden layer 1 goes to hidden layer 2 (arbitrarily chose two hidden layers each with size 16)
            nn.Linear(16, 16),
            # also uses ReLU activation function
            nn.ReLU(),
            # hidden layer 2 goes to output layer
            nn.Linear(16, self.size_of_state_rating)
        )

        # Will use Mean Squared Error Loss function
        self.loss_fn = nn.MSELoss()
        
        # Will use stochastic gradient descent algorithm
        self.optimizer = torch.optim.SGD(self.model.parameters(), self.learning_rate)
        



    # returns a list of length 2 as: 
    # [actions to be taken, resulting state]
    def choose_action(self, next_states: dict) -> list:
        
        # unpacks dictionary into keys and values
        next_actions, corresponding_states = zip(*next_states.items())


        if np.random.rand() <= self.epsilon:
            ind = np.random.choice(len(next_states))

            return [next_actions[ind], corresponding_states[ind]]
        


        # don't want calculate gradients b/c we're not backpropagating at this step, 
        # just finding out which action to take given the current nn and all possible next states
        self.model.eval()
        with torch.no_grad():
            # makes a forward pass through model with the given states 
            q_vals = self.model(torch.tensor(corresponding_states, dtype=torch.float32))
            
            # flattens output into 1d tensor
            q_vals = torch.flatten(q_vals)
        
        ind = torch.argmax(q_vals).item()

        # setting back to training mode
        self.model.train()

        return [next_actions[ind], corresponding_states[ind]]




    def store_in_memory(self, transition):
        self.memory.append(transition)




    def lower_greedy_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay if self.epsilon > self.epsilon_min else self.epsilon




    def learn(self, batch):
        batch_states = []
        batch_targets = []

        for transition in batch:
            s, a, r, ns, done = transition

            self.model.eval()
            with torch.no_grad():
                if done:
                    target = r
                else:
                    pred = torch.flatten(self.model(torch.tensor(ns, dtype=torch.float32)))
                    target = r + self.gamma * pred.item()
            self.model.train()

            batch_states.append(s)
            batch_targets.append(target)


        self.lower_greedy_epsilon()

        self.optimizer.zero_grad()
        output = self.model(torch.tensor(batch_states, dtype=torch.float32))
        loss = self.loss_fn(output, torch.tensor(batch_targets, dtype=torch.float32).unsqueeze(1))
        loss.backward()
        self.optimizer.step()

        # if I want to graph the loss later
        return loss.item()



    def replay(self):
        batch = sample(self.memory, cfg.BATCH_SIZE)
        self.learn(batch)


    def save(self):
        torch.save({"model_state_dict" : self.model.state_dict(),
                    "optim_state_dict" : self.optimizer.state_dict(),
                    "current_epsilon" : self.epsilon
                    }, cfg.CHECKPOINT_FILE_PATH)
        


    def load(self):
        if os.path.isfile(cfg.CHECKPOINT_FILE_PATH):
            checkpoint = torch.load(cfg.CHECKPOINT_FILE_PATH)
            
            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.optimizer.load_state_dict(checkpoint["optim_state_dict"])
            self.epsilon = checkpoint["current_epsilon"]