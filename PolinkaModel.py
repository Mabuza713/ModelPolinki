from math import exp, factorial, floor, ceil
from queue import Queue
import configparser
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.mixture import GaussianMixture


config = configparser.ConfigParser()
config.read("config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))

n_samples = 500



class Passanger:
    """
    Passanger parameters:
    max_time_to_wait_mean - Mean time after which passanger will just leave in our model we will try to minimalize amount of people that will just leave
    max_time_to_wait_std - Standard deviation of that
    
    """
    
    def __init__(self, arrival_numeric):
        self.max_time_to_wait = np.random.normal(max_time_to_wait_mean, max_time_to_wait_std)
        self.arrival_numeric = arrival_numeric
        self.arrival_hour = int(arrival_numeric) + 0.01 *floor((arrival_numeric - int(arrival_numeric)) * 60)
        
    # Method that will check if Passanger gets angry and just leaves
    # True - he leaves
    # False - he is keep waiting
    def CheckIfWaitTimeExceed(self, current_time):
        return True if abs(self.arrival_numeric - current_time) > self.max_time_to_wait else False
            
    # Functions that will allow us to change between numberic and time notation
    def ChangeMinutesIntoFloat(self, hour):
        return round(60 * (hour - int(hour)), 2)
        
    def ChangeFloatIntoMinutes(self, hour):
        return round((hour- int(hour)) / 60, 2) 
class polinkaModel:
    """
    Model parameters:
    symulation_step - Amount of min/sec we will move with each iteration
    max_people_in_que - Maximum amount of peaople in queue after witch people will just say its 
                        not worth to wait, pass 0 for infinity queue capacity
    
    Deterministic parameters:
    
    cabins_amount - How many gondolas will be simulated in our model
    cabing_capacity - How many people can fit into one gondola
    cabins_speed - Mean speed of a cabin
    max_stay_time - Timer after witch cabin will departure even with one person on board
    people_to_departure - Amount of peaople needed for cabin to departure instanlt
    
    
    Probabilistic parameters:
    to model such destribution function containing our initial conditions, we will need to 
    
    """
    
    # while testing using seed
    np.random.seed(10)
    
    
    def __init__(self, cabins_amount, cabins_capacity, cabins_speed, max_stay_time, people_to_departure):
        self.cabins_amount = cabins_amount
        self.cabins_capacity = cabins_capacity
        self.cabins_speed = cabins_speed
        self.max_stay_time = max_stay_time
        self.people_to_departure = people_to_departure
        
        # two fifo queues in which we will append/pop elements (object of class human? <- class needs to be created)
        self.first_line = []
        self.second_line = []
        
        # variables will be filled in function
        self.first_line_histogrammed = None
        self.second_line_histogrammed = None
        
        
    def PassengerSimulation(self):
        # The day has come, we are modeling Gaussian mixture model
        # list containting tuples in where numbers mean:
        # (mean, standard deviation, weight)
        hourly_parameters = [
            (7.20, 0.2, 0.05),
            (9, 0.4, 0.1),
            (11.50, 0.4, 0.1),
            (13, 0.3, 0.2),
            (14.50, 0.2, 0.1),
            (16, 0.2, 0.15),
            (17.50, 0.4, 0.1),
            (19, 0.4, 0.1),
            (20.50, 0.4, 0.1),
        ]
        
        passengers = []
        for mean, std, weight in hourly_parameters:
            n = int(n_samples * weight)
            for _ in range(n):
                passengers.append(Passanger(np.random.normal(mean, std)))
        
        return passengers
    
    def VisualizeQueue(self, array):
        array = array.reshape(-1,1)
        
        plt.hist(array, bins=int(symulation_time/symulation_step), alpha=0.5, color='gray', label='concept')
        plt.show()
    
    
    def InitializeQueues(self):
        # Creating two queues and creating hisogram with amount of bin equal to amount 
        # of seconds in working model devided by simulation step
        self.first_line = self.PassengerSimulation()
        self.second_line = self.PassengerSimulation()
        self.first_line_histogrammed = np.histogram([x.arrival_numeric for x in self.first_line], bins = int(symulation_time/symulation_step))
        self.second_line_histogrammed = np.histogram([x.arrival_numeric for x in self.second_line], bins = int(symulation_time/symulation_step))


        # Good to control + might use it in visualisation
        with open("record.txt", "w") as record:
            record.write("'amount_of_ppl'; 'time_of_day'; 'second_of_day'\n")
            for i in range(len(self.second_line_histogrammed[0])):
                record.write(f"{self.second_line_histogrammed[0][i]}; {self.ChangeFloatIntoMinutes(self.second_line_histogrammed[1][i])}; {self.second_line_histogrammed[1][i]* 60 * 60}\n")

        
        
    def ChangeMinutesIntoFloat(self, hour):
        return int(hour) + round(0.01 * 60 / (hour - int(hour)) , 3)- 0.01 # <--- might be wrong will see
        
    def ChangeFloatIntoMinutes(self, hour):
        return int(hour) + 0.01 *floor((hour - int(hour)) * 60)


    def SimulationProcess(self):
        self.InitializeQueues()
        
        



temp = polinkaModel(0,0,0,0,0)
temp.SimulationProcess()