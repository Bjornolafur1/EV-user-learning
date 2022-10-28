from random import randint
import numpy as np
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class DeepQNetwork(nn.Module):
    def __init__(self, alpha, input_dims, fc1_dims, fc2_dims, n_actions):
        super(DeepQNetwork, self).__init__()
        self.alpha = alpha  #The learning rate of the agent
        self.input_dims = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
        self.optimizer = optim.Adam(self.parameters(), lr= alpha)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)
    
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        actions = T.sigmoid(x)
        return actions

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.argmax(self.q[state])
        else: #choose a random action
            pass

class QAgent():
    def __init__(self, alpha, epsilon, gamma, input_dims, batch_size, n_actions, max_mem_size = 252, eps_end = 0.01, eps_dec = 5e-4):
        self.alpha = alpha  #The learning rate of the agent
        self.epsilon = epsilon  #The percentage of best action, else random action
        self.gamma = gamma  #Discount factor of future rewards
        self.input_dims = input_dims
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.batch_size = batch_size
        # self.action_space = [i for i in range(n_actions)]
        self.n_actions = n_actions
        self.mem_size = max_mem_size
        self.mem_cntr = 0
        self.Q_eval = DeepQNetwork(self.alpha, input_dims = input_dims, fc1_dims= 26, fc2_dims= 26, n_actions = n_actions)

        self.state_memory = np.zeros((self.mem_size, input_dims), dtype= np.float32)
        self.new_state_memory = np.zeros((self.mem_size, input_dims), dtype= np.float32)

        self.action_memory = np.zeros((self.mem_size, self.n_actions), dtype= np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype= np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype= np.bool)

    def store_transition(self, state, action, reward, state_, done = False):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_cntr += 1
    
    def random_action(self, observation):
        n_cars = np.count_nonzero(observation[:self.n_actions])
        if n_cars == 0:
            return np.zeros(self.n_actions)
        n_cars_to_charge = np.random.randint(0, n_cars)
        car_index_list = np.array([i for i in range(len(observation[:self.n_actions])) if observation[i] == 1.])
        cars_picked = np.random.choice(car_index_list, n_cars_to_charge)
        action = np.zeros(self.n_actions)
        for id in cars_picked:
            action[id] = 1
        return action

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.Q_eval.device)
            actions = self.Q_eval.forward(state)
            action = actions[0].cpu().detach().numpy()
            action = np.where(action >= 0.5, 1, action)
            action = np.where(action < 0.5, 0, action)
        else:
            action = self.random_action(observation)
        return action

    def learn(self):
        if self.mem_cntr < self.batch_size:
            return
        
        self.Q_eval.optimizer.zero_grad()

        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace= False)

        batch_lis = []
        index_lis = []
        for i in range(self.n_actions):
            index_lis.append(i)
        for i in range(self.batch_size):
            batch_lis.append(index_lis)
        batch_index = np.array(batch_lis, dtype= np.int32)

        # batch_index = np.arange(self.batch_size, dtype= np.int32)

        state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
        new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
        # terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)

        action_batch = self.action_memory[batch]
        # print(self.Q_eval)
        q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q_eval.forward(new_state_batch)
        # q_next[terminal_batch] = 0.0

        q_target = np.zeros((self.batch_size, self.n_actions), dtype= np.float32)

        for i in range(self.batch_size-1):
            for j in range(self.n_actions-1):
                q_target[i][j] = reward_batch[i] + self.gamma * q_next[i][j]
        
        q_target = T.from_numpy(q_target)

        loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
        loss.backward()
        self.Q_eval.optimizer.step()

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min \
            else self.eps_min