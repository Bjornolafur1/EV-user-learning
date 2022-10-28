from datetime import datetime, timedelta
from lib2to3.pgen2 import driver
from driver import *
import gym
import numpy as np
import random




class Environment:
    def __init__(self, interval, date_time, n_cars):
        self.interval = interval    #Initialize an interval of minutes
        self.date_time =  datetime.strptime(date_time, "%Y-%m-%d-%H:%M")   #Starting date of simulations
        self.n_cars = n_cars    #Number of cars in circulation
        self.get_drivers()  #Initialize drivers in simulation
        self.update_state()    #Get initial state
        self.decay = 0.015 #Decay factor for the reward function
        
    def get_drivers(self):    #Fill the driver list with instances of the driver class
        self.driver_lis = []
        shift_arr = np.array([0 if i <= 0.6 else 1 if 0.6 < i <= 0.825 else 2 for i in np.random.rand(self.n_cars)])   #Initialize the shifts of the users, 0 for day shift, 1 for evening shifts, 2 for night shifts
        capacity_arr = np.array([0.15 if i <= 0.4 else 0.2 if 0.4 < i <= 0.7 else 0.3 for i in np.random.rand(self.n_cars)]) #Initialize the battery capacities of the EV's, the capacity will dictate the charge consumption
        dock_lis = [1 if random.uniform(0, 1) > 0.5 else 0 for i in range(self.n_cars)]

        for i in range(self.n_cars):
            if shift_arr[i] == 0:
                driver = DriverDay(i, capacity_arr[i], dock_lis[i], np.random.uniform(0.2, 0.7, 1)[0], self.interval)    #Initialize an instance of the day driver class
            elif shift_arr[i] == 1:
                driver = DriverEvening(i, capacity_arr[i], dock_lis[i], np.random.uniform(0.2, 0.7, 1)[0], self.interval)    #Initialize an instance of the evening driver class
            else:
                driver = DriverNight(i, capacity_arr[i], dock_lis[i], np.random.uniform(0.2, 0.7, 1)[0], self.interval)    #Initialize an instance of the night driver class
            self.driver_lis.append(driver)   #Append the driver to the driver list
    
    def update_state(self):
        day = self.date_time.weekday()   #Get the weekday, Monday is 0 and Sunday is 6
        hour = self.date_time.hour   #Get the current hour
        #Generate the available charge according to the time of day
        if 0 <= hour < 6 or 21 < hour:
            available_charge = random.uniform((0.015/(60/self.interval)), (0.0175/(60/self.interval)))*self.n_cars
        elif 17 <= hour <= 21:
            available_charge = random.uniform((0.0075/(60/self.interval)), (0.01/(60/self.interval)))*self.n_cars
        else:
            available_charge = random.uniform((0.02/(60/self.interval)), (0.025/(60/self.interval)))*self.n_cars
        
        dock_lis = []
        charge_lis = []
        for driver in self.driver_lis:
            if driver.location == 1:
                dock_lis.append(1)
                charge_lis.append(driver.soc)
            else:
                dock_lis.append(0)
                charge_lis.append(0)        
        self.state =  np.array(dock_lis + charge_lis + [available_charge] + [day] + [hour], dtype=np.float32)
    
    def get_reward(self):
        #Here we get the rewards for the state transition
        reward = 0
        for i in range(len(self.driver_lis)):
            if self.driver_lis[i].left == 1.:
                if self.driver_lis[i].soc < 0.8:
                    reward += -(np.power(self.decay, self.driver_lis[i].soc)*1)
                else:
                    reward += -((0.7*self.driver_lis[i].soc)-0.5)
        return reward
    
    def step(self, action):
        #Here all the model agents act
        self.out_of_battery = 0
        charge = self.state[2*self.n_cars]
        for a in range(len(action)):
            if action[a] == 1:
                self.driver_lis[a].soc = charge  #Each action updates the state of charge for some EV


        self.reward = 0
        
        for driver in self.driver_lis:   #Loop over every EV user
                driver.behavior(self.date_time.weekday(), self.date_time.hour)    #Let each EV user make a decision on their location
                if driver.location == 0:
                    out_of_battery, out_of_battery_penalty = driver.consume_charge()  #Those EV users that are not home will use charge
                    self.reward += out_of_battery_penalty    #Add reward for cars running out of battery
                    self.out_of_battery += out_of_battery
        self.reward += self.get_reward() #Add reward for the cars leaving home
    
        self.date_time += timedelta(minutes = self.interval)     #Increment date time with interval

        self.update_state()

        return self.state, self.reward

        
class BasicWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.env = env
        
    def step(self, action):
        next_state, reward = self.env.step(action)
        # modify ...
        return next_state, reward


