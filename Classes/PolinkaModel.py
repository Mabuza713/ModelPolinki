from math import exp, factorial, floor, ceil
import configparser
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from collections import deque


from Passanger import Passanger
from Gondola import Gondola


config = configparser.ConfigParser()
config.read("Config/config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))

n_samples = 1000




class Symulacja:
    """
    Model parameters:
    symulation_step - Amount of min/sec we will move with each iteration
    max_people_in_que - Maximum amount of peaople in queue after witch people will just say its 
                        not worth to wait, pass 0 for infinity queue capacity
    cabins_amount - How many gondolas will be simulated in our model

    temp_first_que and temp_second_que are both lists to which we will append and pop passangers
    
    Probabilistic parameters:
    to model such destribution function containing our initial conditions, we will need to 
    
    """
    
    # while testing using seed
    np.random.seed(10)
    
    # Possible symulation states
    class status(Enum):
        waiting = "waiting"
        moving = "moving"
        counting_time = "counting_time"
        
        
    def __init__(self,cabins_amount):
        # two fifo queues in which we will append/pop elements (object of class human? <- class needs to be created)
        self.first_line = []
        self.second_line = []
        
        # variables will be filled in function
        self.first_line_histogrammed = None
        self.second_line_histogrammed = None
        
        # initial symulation status is waiting
        self.current_status = self.status("waiting")
        
        self.cabins_amount = cabins_amount
        
        # variables to then calculate statistics
        self.already_transported_passangers = []
        self.passangers_that_left_que = []
    
        self.temp_first_que = deque()     # <- temp ques that will help us track who is waiting to get into the gondola
        self.temp_second_que = deque()
        
    def PassengerSimulation(self):
        # The day has come, we are modeling Gaussian mixture model
        # list containting tuples in where numbers mean:
        # (mean, standard deviation, weight)
        hourly_parameters = [
            (7.20 * 3600, 0.2 * 3600, 0.05),
            (9 * 3600, 0.4* 3600, 0.1),
            (11.50 * 3600, 0.4* 3600, 0.1),
            (13* 3600, 0.3* 3600, 0.2),
            (14.50* 3600, 0.2* 3600, 0.1),
            (16* 3600, 0.2* 3600, 0.15),
            (17.50* 3600, 0.4* 3600, 0.1),
            (19* 3600, 0.4* 3600, 0.1),
            (20.50* 3600, 0.4* 3600, 0.1),
        ]
        
        passengers = []
        passangers_vis = []
        for mean, std, weight in hourly_parameters:
            n = int(n_samples * weight)
            temp_time_list = []
            for _ in range(n):
                temp = np.random.normal(mean, std)
                temp_time_list.append(temp)
            
            temp_time_list.sort()
            for time in temp_time_list:
                if (time >= 25100):
                    passangers_vis.append(int(time))
                    passengers.append(Passanger(int(time)))
                    
        #self.VisualizeQueue(np.array(passangers_vis))
        return passengers
    
    def VisualizeQueue(self, array):
        array = array.reshape(-1,1)
        
        plt.hist(array, bins=100, alpha=0.5, color='gray', label='concept')
        plt.xlim(left = 7 * 3600)
        plt.show()
    
    
    def InitializeQueues(self):
        # Creating two queues and creating hisogram with amount of bin equal to amount 
        # of seconds in working model devided by simulation step
        self.first_line = self.PassengerSimulation()
        self.second_line = self.PassengerSimulation()
        self.first_line_histogrammed = np.histogram([x.arrival_time for x in self.first_line], bins = int(symulation_time))
        self.second_line_histogrammed = np.histogram([x.arrival_time for x in self.second_line], bins = int(symulation_time))

        # Good to control + might use it in visualisation
        
    def TimeToNormal(self, liczba):
        godzina = liczba // 3600
        minuta = (liczba - godzina * 3600) // 60
        sekunda = liczba - (godzina * 3600) - (minuta * 60)
        return {"godzina":godzina, "minuta":minuta, "sekunda":sekunda}





    def CheckWhoLeavesQueues(self, time): # <- this function takes temp queues
        for index, passanger in enumerate(self.first_line):
            if passanger.arrival_time + passanger.max_time_to_wait < time:
                self.passangers_that_left_que.append(passanger)
                passanger.left_queue = True
                self.first_line[index] = None
        
        for index, passanger in enumerate(self.second_line):
            if passanger.arrival_time + passanger.max_time_to_wait < time:
                self.passangers_that_left_que.append(passanger)
                passanger.left_queue = True
                self.second_line[index] = None

    def DeleteNoneValuesFromQueues(self):
        self.first_line = [x for x in self.first_line if x is not None]
        self.second_line = [x for x in self.second_line if x is not None]

    def SimulationProcess(self):
        self.InitializeQueues()

        gondola_que = deque()
        
        for i in range(0, self.cabins_amount):
             gondola_que.append(Gondola(15, 180, 30, 15, "gondola_" + str(i)))
            
        
        for time in range(7 * 60 * 60 - 100, 21 * 60 * 60):
            self.DeleteNoneValuesFromQueues()
            self.CheckWhoLeavesQueues(time)
            self.DeleteNoneValuesFromQueues()
            
            for index, passanger in enumerate(self.first_line):
                if passanger.arrival_time <= time:
                    passanger.wait_time = time - passanger.arrival_time
                    self.temp_first_que.append(passanger)
                    self.first_line[index] = None
                else:
                    break
            for index, passanger in enumerate(self.second_line):
                if passanger.arrival_time <= time:
                    passanger.wait_time = time - passanger.arrival_time
                    self.temp_second_que.append(passanger)
                    self.second_line[index] = None
                else:
                    break
            if (self.current_status == self.status("waiting")):
                first_gondola = gondola_que[0]; second_gondola = gondola_que[len(gondola_que) - 1]

                while (len(first_gondola.people_in_cabin) <= first_gondola.cabins_capacity and len(self.temp_first_que) > 0):
                    if (first_gondola.count_time != None):
                        first_gondola.count_time = time
                    first_gondola.people_in_cabin.append(self.temp_first_que.popleft())
                    
                while (len(second_gondola.people_in_cabin) <= second_gondola.cabins_capacity and len(self.temp_second_que) > 0):
                    if (second_gondola.count_time != None):
                        second_gondola.count_time = time
                    second_gondola.people_in_cabin.append(self.temp_second_que.popleft())
                    
                if (first_gondola.count_time != None):
                    if (first_gondola.count_time + first_gondola.max_stay_time > time):
                        self.current_status = self.status("moving")
                
                if (second_gondola.count_time != None):
                    if (second_gondola.count_time + second_gondola.max_stay_time > time):
                        self.current_status = self.status("moving")
                

            if (self.current_status == self.status("moving")):
                if (second_gondola.count_time != None):
                    if (second_gondola.count_time + second_gondola.max_stay_time + second_gondola.travel_time < time):
                        second_gondola.count_time = None
                        first_gondola.count_time = None
                        second_gondola.arrival_time = time
                        first_gondola.arrival_time = time
                        
                        
                    


temp = Symulacja(2)
temp.SimulationProcess()