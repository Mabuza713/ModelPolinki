from math import exp, factorial
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
n_samples = 10000


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
        self.first_line = Queue(maxsize = max_people_in_que)
        self.second_line = Queue(maxsize = max_people_in_que)
        
    def PassengerSimulation(self):
        # The day has come, we are modeling Gaussian mixture model
        # list containting tuples in where numbers mean:
        # (mean, standard deviation, weight)
        hourly_parameters = [
            (7.50, 0.5, 1),
            (9, 0.4, 1),
            (11.50, 0.4, 1),
            (13, 0.4, 1),
            (14.50, 0.4, 1),
            (16, 0.4, 1),
            (17.50, 0.4, 1),
            (19, 0.4, 1),
            (20.50, 0.4, 1),
        ]
        
        passengers = []
        for mean, std, weight in hourly_parameters:
            n = int(n_samples * weight)
            passengers.append(np.random.normal(mean, std, n))
        
        return np.concatenate(passengers)
    
    # vvvv check if good
    def ProofOfConcept(self):
        self.first_line = self.PassengerSimulation()
        self.first_line = self.first_line.reshape(-1,1)
        gmm = GaussianMixture(n_components=3, random_state=3)
        gmm.fit(self.first_line)

        plt.hist(self.first_line, bins=int(symulation_time/symulation_step), alpha=0.5, color='gray', label='concept')
        plt.show()
        
temp = polinkaModel(0,0,0,0,0)
temp.ProofOfConcept()