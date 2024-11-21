from math import exp, factorial
from queue import Queue
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))

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
    
    
    """
    def __init__(self, cabins_amount, cabins_capacity, cabins_speed, max_stay_time, people_to_departure):
        self.cabins_amount = cabins_amount
        self.cabins_capacity = cabins_capacity
        self.cabins_speed = cabins_speed
        self.max_stay_time = max_stay_time
        self.people_to_departure = people_to_departure
        
        # two fifo queues that will 
        self.first_line = Queue(maxsize = max_people_in_que)
        self.second_line = []
        
    def PassengerSimulation(self):
        # we will model it using poisson oneday
        
        pass        

temp = polinkaModel(0,0,0,0,0).PassengerSimulation()