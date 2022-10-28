import random

#First class is the day shift drivers

class DriverDay:
    def __init__(self, id, capacity, location, soc, interval) -> None:
        self.id = id    #The driver id
        self.capacity = capacity    #The battery capacity of this EV
        self.location = location  #The location of the driver, whether he is home, 1, or driving, 0
        self.soc = soc  #The state of charge, soc, for the driver, each EV will have 300km range on full battery
        self.interval = interval  #The interval of the simulation
        self.left = 0 #Indication whether the agent left home at time step, 1 if yes 0 if no
    
    def behavior(self, day, hour):
        leave = random.uniform(0,1)
        returns = random.uniform(0,1)
        if day < 8:
                if 6 <= hour < 9:
                    if self.location == 1:
                        prob_leaving = 0.975/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.01/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 9 <= hour < 16:
                    if self.location == 1:
                        prob_leaving = 0.35/(360/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.025/(360/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else: 
                            self.left = 0
                elif 16 <= hour < 19:
                    if self.location == 1:
                        prob_leaving = 0.075/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.85/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 19 <= hour:
                    if self.location == 1:
                        prob_leaving = 0.25/(300/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.8/(300/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                else:
                    if self.location == 1:
                        prob_leaving = 0.025/(360/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.875/(360/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
    
    def consume_charge(self):
        out_of_battery = 0
        reward = 0
        if self.location == 0:
            consumption = random.uniform(self.capacity, self.capacity+0.3)/((24*60)/(self.interval))  #Charge consumed on timestep
            if self.soc - consumption <= 0:
                self.soc = 0
                out_of_battery = 1
                self.soc = 0.1   
                reward = -2  
            else:
                self.soc -= consumption
        return out_of_battery, reward

#Next class is the evening shift drivers

class DriverEvening:
    def __init__(self, id, capacity, location, soc, interval) -> None:
        self.id = id    #The driver id
        self.capacity = capacity    #The battery capacity of this EV
        self.location = location  #The location of the driver, whether he is home, 1, or driving, 0
        self.soc = soc  #The state of charge, soc, for the driver, each EV will have 300km range on full battery
        self.interval = interval  #The interval of the simulation
        self.left = 0 #Indication whether the agent left home at time step, 1 if yes 0 if no
    
    def behavior(self, day, hour):
        leave = random.uniform(0,1)
        returns = random.uniform(0,1)
        if day < 8:
                if 7 <= hour < 12:
                    if self.location == 1:
                        prob_leaving = 0.4/(300/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.5/(300/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 12 <= hour < 15:
                    if self.location == 1:
                        prob_leaving = 0.6/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.3/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else: 
                            self.left = 0
                elif 15 <= hour < 18:
                    if self.location == 1:
                        prob_leaving = 0.9/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.025/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 18 <= hour < 22:
                    if self.location == 1:
                        prob_leaving = 0.4/(240/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.5/(240/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 22 <= hour:
                    if self.location == 1:
                        prob_leaving = 0.025/(420/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.95/(420/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                else:
                    if self.location == 1:
                        prob_leaving = 0.05/(420/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.9/(420/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
    
    def consume_charge(self):
        out_of_battery = 0
        reward = 0
        if self.location == 0:
            consumption = random.uniform(self.capacity, self.capacity+0.3)/((24*60)/(self.interval))  #Charge consumed on timestep
            if self.soc - consumption <= 0:
                self.soc = 0
                out_of_battery = 1
                self.soc = 0.1   
                reward = -2  
            else:
                self.soc -= consumption
        return out_of_battery, reward

#Last class is night shift driver

class DriverNight:
    def __init__(self, id, capacity, location, soc, interval) -> None:
        self.id = id    #The driver id
        self.capacity = capacity    #The battery capacity of this EV
        self.location = location  #The location of the driver, whether he is home, 1, or driving, 0
        self.soc = soc  #The state of charge, soc, for the driver, each EV will have 300km range on full battery
        self.interval = interval  #The interval of the simulation
        self.left = 0 #Indication whether the agent left home at time step, 1 if yes 0 if no
    
    def behavior(self, day, hour):
        leave = random.uniform(0,1)
        returns = random.uniform(0,1)
        if day < 8:
                if 6 <= hour < 9:
                    if self.location == 1:
                        prob_leaving = 0.05/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.85/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                elif 9 <= hour < 15:
                    if self.location == 1:
                        prob_leaving = 0.075/(360/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.8/(360/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else: 
                            self.left = 0
                elif 15 <= hour < 19:
                    if self.location == 1:
                        prob_leaving = 0.7/(240/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.3/(240/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else: 
                            self.left = 0
                elif 19 <= hour < 22:
                    if self.location == 1:
                        prob_leaving = 0.975/(180/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return = 0.01/(180/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
                else:
                    if self.location == 1:
                        prob_leaving = 0.25/(420/self.interval)
                        if prob_leaving >= leave:
                            self.location = 0
                            self.left = 1
                    else:
                        prob_return =  0.05/(420/self.interval)
                        if prob_return >= returns:
                            self.location = 1
                            self.left = 0
                        else:
                            self.left = 0
    
    def consume_charge(self):
        out_of_battery = 0
        reward = 0
        if self.location == 0:
            consumption = random.uniform(self.capacity, self.capacity+0.3)/((24*60)/(self.interval))  #Charge consumed on timestep
            if self.soc - consumption <= 0:
                self.soc = 0
                out_of_battery = 1
                self.soc = 0.1   
                reward = -2  
            else:
                self.soc -= consumption
        return out_of_battery, reward
