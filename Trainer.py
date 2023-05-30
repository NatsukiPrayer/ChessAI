import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # state = torch.tensor(state, dtype=torch.float)
        # next_state = torch.tensor(next_state, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        reward = torch.unsqueeze(reward, 0)
        done = (done,)
        # (n, x)

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = action * reward

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
