from datetime import datetime, timedelta
import numpy as np
import random
from collections import deque



class Simulation:
    def __init__(self, interval, date_time, duration, episodes, n_cars, n_docks):
        self.interval = interval    #Initialize an interval of minutes
        self.date_time = date_time  #Starting date of simulations
        self.duration = duration  #Duration of the simulation in years
        self.episodes = episodes  #Number of episodes
        self.n_cars = n_cars    #Number of cars in circulation
        self.n_docks = n_docks  #Number of charging docks

        
        
    def run(self):  #Run the simulation
        n_observations = int(self.duration * 365 * 24 * (60 / self.interval))   #Set the number of observations
        total_drivers = 0
        total_docked = 0
        total_queued = 0

        for episode in range(self.episodes): 

            date_time = datetime.strptime(self.date_time, "%Y-%m-%d-%H:%M")    #Starting date time for each episode
            charge_arr = np.random.uniform(0.2, 0.8, self.n_cars)   #Initial charge of the vehicles in circulation
            dock_arr = self.initial_dock_state()
            driving_arr = [i if i not in dock_arr else 0 for i in range(1, 1 + self.n_cars)]  #Cars driving initially
            driving_arr = np.array(driving_arr, dtype=int)
            print('Initial dock is {}'.format(dock_arr))
            print('Initial driving is {}'.format(driving_arr))
            input('')
            dock_queue = deque([])  #Queue for cars if all docks are in use

            for n in range(n_observations):



                state = []  #Initialize a state for current interval

                day = date_time.weekday()   #Get the weekday, Monday is 0 and Sunday is 6
                hour = date_time.hour   #Get the current hour
                
                arrive, depart = self.get_arrival_departure(dock_arr, driving_arr, dock_queue, day, hour) #Get the id's of the cars coming and leaving

                dock_arr, dock_queue = self.change_home_state(dock_arr, dock_queue, arrive, depart) #Change the state of the dock and queue
                
                driving_arr = self.change_driving_state(driving_arr, depart, arrive)    #Change the state of drivers

                # if n > 25000:
                #     print('Departures are {}'.format(depart))
                #     print('Arrivals are {}'.format(arrive))
                #     print('Drivers are {}'.format(driving_arr))
                #     print('Cars docked are {}'.format(dock_arr))
                #     print('Cars queued are {}'.format(dock_queue))
                #     input('')

                date_time += timedelta(minutes = self.interval)     #Increment date time with interval 
                
                


    def initial_dock_state(self):   #Initialize cars in dock and their id's
        dock_arr = np.zeros(self.n_docks, dtype=int)  #Initialize the dock array
        n_cars_in_dock = np.random.randint(0, self.n_docks)    #Number of cars in docks at start
        car_ids = random.sample(range(1, self.n_cars), n_cars_in_dock)  #The id's of the cars placed in docks at start
        for i in range(len(car_ids)):
            dock_arr[i] = car_ids[i]    #Fill the car id into the dock array
        return dock_arr

    def get_arrival_departure(self, dock_arr, driving_arr, dock_queue, day, hour):

        depart = []
        arrive = []

        home_arr = list(dock_arr) + list(dock_queue)   #Id's of cars not driving
        home_arr = np.array(home_arr, dtype=int)

        if np.count_nonzero(driving_arr) == 0:     #Check if anyone is driving
            pass
        else:
            if 7 < hour < 9:
                l_lower = ((0.1*1.25*self.n_cars)/2)/(60/self.interval)
                l_upper = ((0.1*1.5*self.n_cars)/2)/(60/self.interval)
                l_arrival = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_arrive = np.random.poisson(lam=l_arrival)     #Number of cars coming in
            elif 9 < hour < 15:
                l_lower = ((0.05*1.25*self.n_cars)/6)/(60/self.interval)
                l_upper = ((0.05*1.5*self.n_cars)/6)/(60/self.interval)
                l_arrival = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_arrive = np.random.poisson(lam=l_arrival)     #Number of cars coming in
            elif 15 < hour < 18:
                l_lower = ((0.5*1.25*self.n_cars)/3)/(60/self.interval)
                l_upper = ((0.5*1.5*self.n_cars)/3)/(60/self.interval)
                l_arrival = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_arrive = np.random.poisson(lam=l_arrival)     #Number of cars coming in
            elif 18 < hour < 22:
                l_lower = ((0.3*1.25*self.n_cars)/4)/(60/self.interval)
                l_upper = ((0.3*1.5*self.n_cars)/4)/(60/self.interval)
                l_arrival = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_arrive = np.random.poisson(lam=l_arrival)     #Number of cars coming in
            else:
                l_lower = ((0.05*1.25*self.n_cars)/9)/(60/self.interval)
                l_upper = ((0.05*1.5*self.n_cars)/9)/(60/self.interval)
                l_arrival = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_arrive = np.random.poisson(lam=l_arrival)     #Number of cars coming in

            driving_clone = [i for i in driving_arr if i != 0]   #Clone driving arr without zeros
            if n_arrive <= len(driving_clone):  #Check if there are enough drivers to arrive
                for i in range(n_arrive):
                    index = np.random.choice(driving_clone)
                    arrive.append(int(index)   )  #Add arrival id to arrival array
                    driving_clone = np.delete(driving_clone, np.where(driving_clone == index))
            else:
                n_arrive = len(driving_clone)   #Set arrival number to number of drivers if number of drivers is smaller
                for i in range(n_arrive):
                    index = np.random.choice(driving_clone)
                    arrive.append(int(index))
                    driving_clone = np.delete(driving_clone, np.where(driving_clone == index))

        
        if np.count_nonzero(home_arr) == 0:    #Check if anyone is home
            pass
        else:
            if 7 < hour < 9:
                l_lower = ((0.7*1.25*self.n_cars)/2)/(60/self.interval)
                l_upper = ((0.7*1.5*self.n_cars)/2)/(60/self.interval)
                l_depart = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_depart = np.random.poisson(lam=l_depart)     #Number of cars coming in
            elif 9 < hour < 15:
                l_lower = ((0.05*1.25*self.n_cars)/6)/(60/self.interval)
                l_upper = ((0.05*1.5*self.n_cars)/6)/(60/self.interval)
                l_depart = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_depart = np.random.poisson(lam=l_depart)     #Number of cars coming in
            elif 15 < hour < 18:
                l_lower = ((0.1*1.25*self.n_cars)/3)/(60/self.interval)
                l_upper = ((0.1*1.5*self.n_cars)/3)/(60/self.interval)
                l_depart = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_depart = np.random.poisson(lam=l_depart)     #Number of cars coming in
            elif 18 < hour < 22:
                l_lower = ((0.1*1.25*self.n_cars)/4)/(60/self.interval)
                l_upper = ((0.1*1.5*self.n_cars)/4)/(60/self.interval)
                l_depart = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_depart = np.random.poisson(lam=l_depart)     #Number of cars coming in
            else:
                l_lower = ((0.05*1.25*self.n_cars)/9)/(60/self.interval)
                l_upper = ((0.05*1.5*self.n_cars)/9)/(60/self.interval)
                l_depart = np.random.uniform(l_lower, l_upper)   #Arrival rate, to be modeled to change depending on time of day and week
                n_depart = np.random.poisson(lam=l_depart)     #Number of cars coming in

            home_clone = [i for i in home_arr if i != 0]
            if n_depart <= len(home_clone):
                for i in range(n_depart):
                    index = np.random.choice(home_clone)
                    depart.append(int(index))
                    home_clone = np.delete(home_clone, np.where(home_clone == index))
            else:
                n_depart = len(home_clone)
                for i in range(n_depart):
                    index = np.random.choice(home_clone)
                    depart.append(int(index))
                    home_clone = np.delete(home_clone, np.where(home_clone == index))

        if len(arrive) == 0:
            arrive = None

        if len(depart) == 0:
            depart = None

        return arrive, depart

    def change_home_state(self, dock_arr, dock_queue, arrive, depart):

        if depart != None:  #Check for departures
            for i in depart:
                try:
                    dock_queue.remove(i)    #Check if departing id is in queue and remove it
                except ValueError:
                    pass
                for j in range(len(dock_arr)):
                    if dock_arr[j] == i:    #Check if departing id is in dock
                        dock_arr[j] = 0    #Remove id


        for i in range(len(dock_arr)):
            if dock_arr[i] == 0: #Check for free spots in dock
                try:
                    dock_arr[i] = dock_queue.pop()  #The queue has priority over arrivals
                except IndexError:
                    pass

        if arrive != None:
            for i in range(len(dock_arr)):
                if dock_arr[i] != 0:
                    continue
                else:
                    index = np.random.choice(arrive)
                    dock_arr[i] = index
                    arrive = np.delete(arrive, np.where(arrive == index))
                    if len(arrive) == 0:
                        break

            if len(arrive) > 0:
                for i in arrive:
                    dock_queue.appendleft(i)

        return dock_arr, dock_queue

    def change_driving_state(self, driving_arr, depart, arrive):
        
        if depart != None:
            for i in depart:
                # print('I is {} and driving_arr[i-1] is {}'.format(i, driving_arr[i-1]))
                driving_arr[i-1] = i

        if arrive != None:
            for i in arrive:
                # print('I is {} and driving_arr[i-1] is {}'.format(i, driving_arr[i-1]))
                driving_arr[i-1] = 0

        return driving_arr


    def __str__(self):
        return '{}'.format(self.dock_arr)

