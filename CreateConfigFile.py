# This file contains method used to change model parameters

import configparser

def CreateConfig():
    config = configparser.ConfigParser()
    config["ModelParameters"] = {"symulation_step": 1, 
                                 "max_people_in_que": 2}
    
    with (open("config.ini", "w")) as configFile:
        config.write(configFile)
  
  
        
CreateConfig()