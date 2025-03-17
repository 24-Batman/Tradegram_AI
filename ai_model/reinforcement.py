import logging
import numpy as np
from typing import Dict, Any, List, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

logger = logging.getLogger(__name__)

class DQNNetwork(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ReinforcementLearner:
    def __init__(self):
        """Initialize the reinforcement learning model"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state_size = 10  # Number of state features
        self.action_size = 3  # Buy, Sell, Hold
        
        # DQN hyperparameters
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 32
        
        # Initialize networks
        self.policy_net = DQNNetwork(self.state_size, self.action_size).to(self.device)
        self.target_net = DQNNetwork(self.state_size, self.action_size).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.learning_rate)
        self.memory = deque(maxlen=10000)
        
        logger.info("Reinforcement learning model initialized")

    async def train(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray):
        """Train the model with new experience"""
        try:
            # Store experience in memory
            self.memory.append((state, action, reward, next_state))
            
            # Start training only if we have enough samples
            if len(self.memory) < self.batch_size:
                return
            
            # Sample random batch from memory
            batch = random.sample(self.memory, self.batch_size)
            states, actions, rewards, next_states = zip(*batch)
            
            # Convert to tensors
            states = torch.FloatTensor(states).to(self.device)
            actions = torch.LongTensor(actions).to(self.device)
            rewards = torch.FloatTensor(rewards).to(self.device)
            next_states = torch.FloatTensor(next_states).to(self.device)
            
            # Get current Q values
            current_q = self.policy_net(states).gather(1, actions.unsqueeze(1))
            
            # Get next Q values
            with torch.no_grad():
                next_q = self.target_net(next_states).max(1)[0]
            
            # Calculate target Q values
            target_q = rewards + self.gamma * next_q
            
            # Calculate loss and update policy network
            loss = nn.MSELoss()(current_q.squeeze(), target_q)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Update target network periodically
            self._update_target_network()
            
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
        except Exception as e:
            logger.error(f"Error in training: {str(e)}")

    async def predict_action(self, state: np.ndarray) -> int:
        """Predict the next action based on current state"""
        try:
            if random.random() < self.epsilon:
                return random.randrange(self.action_size)
            
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state_tensor)
                return q_values.argmax().item()
                
        except Exception as e:
            logger.error(f"Error in action prediction: {str(e)}")
            return 2  # Default to HOLD action

    def _update_target_network(self):
        """Update target network weights"""
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save_model(self, path: str):
        """Save model weights"""
        try:
            torch.save({
                'policy_net_state_dict': self.policy_net.state_dict(),
                'target_net_state_dict': self.target_net.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'epsilon': self.epsilon
            }, path)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")

    def load_model(self, path: str):
        """Load model weights"""
        try:
            checkpoint = torch.load(path)
            self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
            self.target_net.load_state_dict(checkpoint['target_net_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.epsilon = checkpoint['epsilon']
            logger.info(f"Model loaded from {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}") 