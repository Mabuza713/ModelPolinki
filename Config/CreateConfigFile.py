# This file contains method used to change model parameters


# Symualtion time in secounds
import configparser

def CreateConfig():
    config = configparser.ConfigParser()
    config["ModelParameters"] = {"symulation_step": 1, # <-- in secounds 
                                 "max_people_in_que": 2,
                                 "symulation_time": (21 - 7) * 60 * 60} 
    
    config["PassangerParameters"] = {"max_time_to_wait_std": 60,
                                     "max_time_to_wait_mean": 360}
    with (open("Config/config.ini", "w")) as configFile:
        config.write(configFile)
  
  
        
CreateConfig()