from environment import Environment, BasicWrapper
from baseline_agent import Baseline_agent
from Q_learning_agent import QAgent
import numpy as np
from tqdm import tqdm
import time
import seaborn as sns
import matplotlib.pyplot as plt

#Framework function for the simulation

def simulate(n_cars, interval, weeks):
    e = Environment(interval, '2019-11-24-07:30', n_cars)   #The simulation environment
    agent = QAgent(0.025, 0.5, 0.5, ((2*n_cars)+3), 72, n_cars)   #The charge station agent
    wrapper = BasicWrapper(e)   #Wrapper for the environment
    state = e.state #Initial state of the environment
    
    start_time = time.time()
    episode_reward = np.zeros(weeks)

    for m in tqdm(range(weeks)):   #Each episode is a month
        out_of_battery_count = 0
        total_reward = 0

        for n in tqdm(range(int(7 * 24 * (60 / interval)))):   #Set the number of observations
            action = agent.choose_action(state) #Choose an action for the state
            state_old = state   #Old state for state transition
            state, reward = wrapper.step(action)    #New state and reward for the action taken
            agent.store_transition(state_old, action, reward, state)
            agent.learn()

            out_of_battery_count += e.out_of_battery
            total_reward += reward
            
        episode_reward[m] = total_reward
        print("\nAn EV went out of battery {} times for this episode and the total reward was {:.3f}\n".format(out_of_battery_count, total_reward))
    
    sns.lineplot(episode_reward)
    plt.show()
    end_time = time.time()
    duration = end_time-start_time
    print("\nSimulation took {:.2f} minutes to complete".format(duration/60))


if __name__ == "__main__":
    simulate(5, 10, 26)
