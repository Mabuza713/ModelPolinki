from math import exp, factorial, floor, ceil
import configparser
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


from Passanger import Passanger
from Gondola import Gondola


config = configparser.ConfigParser()
config.read("config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))

n_samples = 500




class Symulacja:
    """
    Model parameters:
    symulation_step - Amount of min/sec we will move with each iteration
    max_people_in_que - Maximum amount of peaople in queue after witch people will just say its 
                        not worth to wait, pass 0 for infinity queue capacity
    cabins_amount - How many gondolas will be simulated in our model

    
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
                if (time >= 7):
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
        self.first_line_histogrammed = np.histogram([x.arrival_numeric for x in self.first_line], bins = int(symulation_time))
        self.second_line_histogrammed = np.histogram([x.arrival_numeric for x in self.second_line], bins = int(symulation_time))

        # Good to control + might use it in visualisation
        with open("record.txt", "w") as record:
            record.write("'amount_of_ppl'; 'time_of_day'; 'second_of_day'\n")
            for i in range(len(self.second_line_histogrammed[0])):
                record.write(f"{self.second_line_histogrammed[0][i]}; {self.second_line_histogrammed[1][i]* 60 * 60 - 7 * 60 * 60}\n")

    def SimulationProcess(self):
        self.InitializeQueues()
        first_que = self.first_line
        second_que = self.second_line
        
        def TimeToNormal(liczba):
            godzina = liczba // 3600
            minuta = (liczba - godzina * 3600) // 60
            sekunda = liczba - (godzina * 3600) - (minuta * 60)
            print(f"godzina: {godzina} --- minuta: {minuta} ---- sekunda: {sekunda}")
        
        
        
        for time in range(7 * 60 * 60, 21 * 60 * 60, symulation_step):
            
        


        
        



temp = Symulacja(2)
temp.SimulationProcess()