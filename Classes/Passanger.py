from math import exp, factorial, floor, ceil
import configparser
import numpy as np

config = configparser.ConfigParser()
config.read("Config/config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))


class Passanger:
    """
    Passanger parameters:
    max_time_to_wait_mean - Mean time after which passanger will just leave in our model we will try to minimalize amount of people that will just leave
    max_time_to_wait_std - Standard deviation of that
    
    """
    # np.random.seed(10)
    def __init__(self, arrival_numeric):
        self.max_time_to_wait = int(np.random.normal(max_time_to_wait_mean, max_time_to_wait_std))
        if self.max_time_to_wait < 0:
            self.max_time_to_wait = 0
            
        self.arrival_time = arrival_numeric
        self.wait_time = 0
        self.finish_time = 0
        self.left_queue = False
        
    # Method that will check if Passanger gets angry and just leaves
    # True - he leaves
    # False - he is keep waiting
    def CheckIfWaitTimeExceed(self, current_time):
        return True if abs(self.arrival_time - current_time) > self.max_time_to_wait else False
