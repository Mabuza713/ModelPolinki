from math import exp, factorial, floor, ceil
import configparser
import numpy as np

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