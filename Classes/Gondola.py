from math import exp, factorial, floor, ceil
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
    name - Variable that will help debug our system
    
    arrival time - Time in which gondola arrived to location
    count time - Time of first passanger going on board
    """
    
    # while testing using seed
    np.random.seed(10)
    
    
    def __init__(self,cabins_capacity, travel_time, max_stay_time, people_to_departure, name):
        self.name = name
        self.cabins_capacity = cabins_capacity
        self.travel_time = travel_time
        self.max_stay_time = max_stay_time
        self.people_to_departure = people_to_departure
        self.people_in_cabin = []
        self.arrival_time = 7 * 60 * 50
        self.count_time = None