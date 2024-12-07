from math import exp, factorial, floor, ceil
import configparser
import numpy as np
import matplotlib.pyplot as plt
from Passanger import Passanger


class Gondola:
    """
    Deterministic parameters:
    cabins_capacity - How many people can fit into one gondola
    cabins_speed - Time needed for cabin to reach second station
    max_stay_time - Timer after witch cabin will departure even with one person on board
    people_to_departure - Amount of peaople needed for cabin to departure instanlt
    
    """
    
    # while testing using seed
    np.random.seed(10)
    
    
    def __init__(self,cabins_capacity, cabins_speed, max_stay_time, people_to_departure):
        self.cabins_capacity = cabins_capacity
        self.cabins_speed = cabins_speed
        self.max_stay_time = max_stay_time
        self.people_to_departure = people_to_departure
        
        self.peaople_in_cabin = []
    
        
