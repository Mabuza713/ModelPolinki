from math import exp, factorial, floor, ceil
import configparser
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from collections import deque

import csv


from Passanger import Passanger
from Gondola import Gondola


config = configparser.ConfigParser()
config.read("Config/config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))

n_samples = 1000




class Symulacja():
    """
    Model parameters:
    symulation_step - Amount of min/sec we will move with each iteration
    max_people_in_que - Maximum amount of peaople in queue after witch people will just say its
                        not worth to wait, pass 0 for infinity queue capacity
    cabins_amount - How many gondolas will be simulated in our model

    temp_first_que and temp_second_que are both lists to which we will append and pop passangers

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


    def __init__(self,cabins_capacity, travel_time, max_stay_time):
        # two fifo queues in which we will append/pop elements (object of class human? <- class needs to be created)
        self.first_line = []
        self.second_line = []

        # variables will be filled in function
        self.first_line_histogrammed = None
        self.second_line_histogrammed = None

        # Gondola parameters
        self.cabins_capacity = cabins_capacity
        self.travel_time = travel_time
        self.max_stay_time = max_stay_time


        # initial symulation status is waiting
        self.current_status = self.status("waiting")

        # variables to then calculate statistics
        self.already_transported_passangers = []
        self.passangers_that_left_que = []

        self.temp_first_que = deque()     # <- temp ques that will help us track who is waiting to get into the gondola
        self.temp_second_que = deque()

        # Lists for data. Each value refer to current time. Idk whether make sense

        self.simulation_time_data = []
        self.amount_people_who_come = []
        self.people_in_queue_data = []
        self.people_who_left_data = []
        self.people_transported_data = []

        self.temp_variable = 0



    def PassengerSimulation(self):
        # The day has come, we are modeling Gaussian mixture model
        # list containting tuples in where numbers mean:
        # (mean, standard deviation, weight)
        hourly_parameters = [
            (7.20 * 3600, 0.2* 3600, 0.05),
            (9 * 3600   , 0.4* 3600, 0.15),
            (11.50 *3600, 0.4* 3600, 0.1),
            (13* 3600   , 0.3* 3600, 0.2),
            (14.50* 3600, 0.2* 3600, 0.1),
            (16* 3600   , 0.2* 3600, 0.2),
            (17.50* 3600, 0.4* 3600, 0.1),
            (19* 3600   , 0.4* 3600, 0.05),
            (20.50* 3600, 0.4* 3600, 0.05),
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
                if (time >= 25100):
                    passangers_vis.append(int(time))
                    passengers.append(Passanger(int(time)))

        self.amount_people_who_come += passangers_vis
        # self.VisualizeQueue(np.array(passangers_vis))
        return passengers




    def VisualizeQueue(self, array):
        array = array.reshape(-1,1)/3600

        plt.hist(array, bins=100, alpha=1, color='gray', label='concept')
        plt.xlim(7, 22)
        plt.xticks(ticks=np.arange(7, 22, 1), labels=(np.arange(7, 22, 1)))
        array = array.reshape(-1,1)/3600

        plt.hist(array, bins=100, alpha=1, color='gray', label='concept')
        plt.xlim(7, 22)
        plt.xticks(ticks=np.arange(7, 22, 1), labels=(np.arange(7, 22, 1)))
        plt.show()


    # Creating data file for simulation
    def DataToFile(self,scenario):
        names = ["Symulation time","Real time","People who come","People in queue(first/second)","People who left","Transported People"]

        datas = [
            self.simulation_time_data,
            [self.TimeToNormal(time) for time in self.simulation_time_data],
            [self.amount_people_who_come.count(value) for value in self.simulation_time_data],
            self.people_in_queue_data,
            self.people_who_left_data,
            self.people_transported_data,
        ]

        with open(f'data{scenario}.csv', 'w') as file:
            writer = csv.writer(file, delimiter="|")
            writer.writerow(names)

            for i in range(len(self.simulation_time_data)):
                row = [(data[i] if i < len(data) else "") for data in datas]
                writer.writerow(row)

    def InitializeQueues(self):
        # Creating two queues and creating histogram with amount of bin equal to amount
        # Creating two queues and creating histogram with amount of bin equal to amount
        # of seconds in working model devided by simulation step
        self.first_line = self.PassengerSimulation()
        self.second_line = self.PassengerSimulation()
        self.first_line_histogrammed = np.histogram([x.arrival_time for x in self.first_line], bins = int(symulation_time))
        self.second_line_histogrammed = np.histogram([x.arrival_time for x in self.second_line], bins = int(symulation_time))

        # Good to control + might use it in visualisation

    # Converting time in seconds to normal time
    def TimeToNormal(self, number):
        hours = number // 3600
        minutes  = (number - hours * 3600) // 60
        seconds = number - (hours * 3600) - (minutes * 60)
        return hours,minutes,seconds

    def CheckWhoLeavesQueues(self, time): # <- this function takes temp queues
        for index, passanger in enumerate(self.temp_first_que):
            if passanger.arrival_time + passanger.max_time_to_wait <= time:
                self.passangers_that_left_que.append(passanger)
                # print(f"Passanger left first the queue arrival time: {self.TimeToNormal(passanger.arrival_time)} and waited for: {self.TimeToNormal(passanger.max_time_to_wait)}")
                passanger.left_queue = True
                self.temp_first_que[index] = None


        for index, passanger in enumerate(self.temp_second_que):
            if passanger.arrival_time + passanger.max_time_to_wait <= time:
                self.passangers_that_left_que.append(passanger)
                # print(f"Passanger left second the queue arrival time: {self.TimeToNormal(passanger.arrival_time)} and waited for: {self.TimeToNormal(passanger.max_time_to_wait)}")
                passanger.left_queue = True
                self.temp_second_que[index] = None


    def DeleteNoneValuesFromQueues(self):
        temp_temp_first_que = [x for x in self.temp_first_que if x is not None]
        self.temp_first_que = deque()
        for passanger in temp_temp_first_que:
            self.temp_first_que.append(passanger)


        temp_temp_second_que = [x for x in self.temp_second_que if x is not None]
        self.temp_second_que = deque()
        for passanger in temp_temp_second_que:
            self.temp_second_que.append(passanger)

    # Counts the total number of people in both queues at the current simulation time.
    def CountPeopleInQueues(self):
        count_first_queue = len(self.temp_first_que)
        count_second_queue = len(self.temp_second_que)
        return  count_first_queue,count_second_queue

    def SimulationProcess(self):

        self.InitializeQueues()

        gondola_que = deque()

        for i in range(0, 2):
             gondola_que.append(Gondola(self.cabins_capacity, self.travel_time, self.max_stay_time))


        for time in range(7 * 60 * 60 - 100, 21 * 60 * 60):


            self.DeleteNoneValuesFromQueues()
            self.CheckWhoLeavesQueues(time)
            self.DeleteNoneValuesFromQueues()

            for index, passanger in enumerate(self.first_line):
                if self.first_line[index] != None:
                    if passanger.arrival_time <= time :
                        passanger.wait_time = time - passanger.arrival_time
                        self.temp_first_que.append(passanger)
                        self.first_line[index] = None
                    else:
                        break
            for index, passanger in enumerate(self.second_line):
                if (self.second_line[index] != None):
                    if passanger.arrival_time <= time:
                        passanger.wait_time = time - passanger.arrival_time
                        self.temp_second_que.append(passanger)
                        self.second_line[index] = None
                    else:
                        break

            # Counting people in queue
            first_line, second_line = self.CountPeopleInQueues()
            self.people_in_queue_data.append([first_line,second_line])


            if (self.current_status == self.status("waiting") and time >= 7*3600):


                first_gondola = gondola_que[0]
                second_gondola = gondola_que[len(gondola_que)-1]


                while (len(first_gondola.people_in_cabin) < first_gondola.cabins_capacity and len(self.temp_first_que) > 0 ):
                    if (first_gondola.count_time == None):
                        first_gondola.count_time = time
                    first_gondola.people_in_cabin.append(self.temp_first_que.popleft())



                while (len(second_gondola.people_in_cabin) < second_gondola.cabins_capacity and len(self.temp_second_que) > 0 ):
                    if (second_gondola.count_time == None):
                        second_gondola.count_time = time
                    second_gondola.people_in_cabin.append(self.temp_second_que.popleft())


                if (first_gondola.count_time != None or len(first_gondola.people_in_cabin) == first_gondola.cabins_capacity):
                    if (first_gondola.count_time + first_gondola.max_stay_time <= time or len(first_gondola.people_in_cabin) == first_gondola.cabins_capacity):
                        first_gondola.departure_time = time
                        # print(f"""First gondola departure time: {self.TimeToNormal(first_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        # print(f"""First gondola departure time: {self.TimeToNormal(first_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        self.current_status = self.status("moving")

                if (second_gondola.count_time != None or len(second_gondola.people_in_cabin) == second_gondola.cabins_capacity):
                    if (second_gondola.count_time + second_gondola.max_stay_time <= time or len(second_gondola.people_in_cabin) == second_gondola.cabins_capacity):
                        second_gondola.departure_time = time
                        # print(f"""Second gondola departure time: {self.TimeToNormal(second_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        # print(f"""Second gondola departure time: {self.TimeToNormal(second_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        self.current_status = self.status("moving")



            if (self.current_status == self.status("moving")):
                if (first_gondola.departure_time != None):
                    if (first_gondola.departure_time + first_gondola.travel_time <= time):
                        second_gondola.arrival_time = time
                        first_gondola.arrival_time = time
                        second_gondola.count_time = None
                        first_gondola.count_time = None

                        for passanger in first_gondola.people_in_cabin:
                            passanger.finish_time = time
                            self.already_transported_passangers.append(passanger)

                        first_gondola.people_in_cabin = []

                        for passanger in second_gondola.people_in_cabin:
                            passanger.finish_time = time
                            self.already_transported_passangers.append(passanger)

                        second_gondola.people_in_cabin = []

                        self.current_status = self.status("waiting")

                elif (second_gondola.departure_time != None):
                    if (second_gondola.departure_time + second_gondola.travel_time < time):
                        second_gondola.count_time = None
                        first_gondola.count_time = None
                        second_gondola.arrival_time = time
                        first_gondola.arrival_time = time

                        for passanger in first_gondola.people_in_cabin:
                            passanger.finish_time = time
                            self.already_transported_passangers.append(passanger)

                        first_gondola.people_in_cabin = []

                        for passanger in second_gondola.people_in_cabin:
                            passanger.finish_time = time
                            self.already_transported_passangers.append(passanger)

                        second_gondola.people_in_cabin = []

                        self.current_status = self.status("waiting")

            self.DeleteNoneValuesFromQueues()
            self.simulation_time_data.append(time)
            self.people_who_left_data.append(len(self.passangers_that_left_que))
            # self.people_who_left_data.append(len(self.passangers_that_left_que)-sum(self.people_who_left_data))
            self.people_transported_data.append(len(self.already_transported_passangers))
            self.CheckWhoLeavesQueues(time)
            self.DeleteNoneValuesFromQueues()

# In first scenario we have gondolas who have 10 cabacity, 180s travel time and 30s wait time
first_scenario = Symulacja(10,180,30)

# In first scenario we have gondolas who have 2 cabacity, 45s travel time and 10s wait time
second_scenario = Symulacja(2,45,10)

first_scenario.SimulationProcess()
second_scenario.SimulationProcess()
first_scenario.DataToFile(1)
second_scenario.DataToFile(2)

# Scenarios have different queues. Must be changed
print("Output for 1st scenario")
print(f"People who came: {len(first_scenario.amount_people_who_come)}")
print(f"People who left: {len(first_scenario.passangers_that_left_que)}")
print(f"Transported people: {len(first_scenario.already_transported_passangers)}")

print("\nOutput for 2nd scenario")
print(f"People who came: {len(second_scenario.amount_people_who_come)}")
print(f"People who left: {len(second_scenario.passangers_that_left_que)}")
print(f"Transported people: {len(second_scenario.already_transported_passangers)}")

print()
print(first_scenario.temp_variable)