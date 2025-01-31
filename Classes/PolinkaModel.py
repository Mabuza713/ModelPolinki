from math import exp, factorial, floor, ceil
import configparser
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from collections import deque


from Passanger import Passanger
from Gondola import Gondola
from utils import Utils


config = configparser.ConfigParser()
config.read("Config/config.ini")

symulation_step = int(config.get("ModelParameters", "symulation_step"))
symulation_time = int(config.get("ModelParameters", "symulation_time"))

max_people_in_que = int(config.get("ModelParameters", "max_people_in_que"))
max_time_to_wait_mean = int(config.get("PassangerParameters", "max_time_to_wait_mean"))
max_time_to_wait_std = int(config.get("PassangerParameters", "max_time_to_wait_std"))

n_samples = 1000




class Symulacja:
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


    def __init__(self,cabins_amount):
        # two fifo queues in which we will append/pop elements (object of class human? <- class needs to be created)
        self.first_line = []
        self.second_line = []

        # variables will be filled in function
        self.first_line_histogrammed = None
        self.second_line_histogrammed = None

        # initial symulation status is waiting
        self.current_status = self.status("waiting")

        self.cabins_amount = cabins_amount

        # variables to then calculate statistics
        self.already_transported_passangers = []
        self.passangers_that_left_que = []

        self.temp_first_que = deque()     # <- temp ques that will help us track who is waiting to get into the gondola
        self.temp_second_que = deque()


    def PassengerSimulation(self):
        # The day has come, we are modeling Gaussian mixture model
        # list containting tuples in where numbers mean:
        # (mean, standard deviation, weight)
        hourly_parameters = [
            (7.20 * 3600, 0.2 * 3600, 0.05),
            (9 * 3600, 0.4 * 3600, 0.1),
            (11.50 * 3600, 0.4 * 3600, 0.1),
            (13 * 3600, 0.3 * 3600, 0.2),
            (14.50 * 3600, 0.2 * 3600, 0.1),
            (16 * 3600, 0.2 * 3600, 0.15),
            (17.50 * 3600, 0.4 * 3600, 0.1),
            (19 * 3600, 0.4 * 3600, 0.1),
            (20.50 * 3600, 0.4 * 3600, 0.1),
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

        self.VisualizeQueue(np.array(passangers_vis))
        return passengers


    def VisualizeQueue(self, array):
        array = array.reshape(-1, 1)

        plt.hist(array, bins=100, alpha=0.5, color='lightblue', label='Passenger Distribution')
        plt.xlim(left=7 * 3600)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of Passengers')
        plt.legend()
        plt.title('Passenger Arrival Distribution')
        plt.show()


    def InitializeQueues(self):
        # Creating two queues and creating hisogram with amount of bin equal to amount
        # of seconds in working model devided by simulation step
        self.first_line = self.PassengerSimulation()
        self.second_line = self.PassengerSimulation()
        self.first_line_histogrammed = np.histogram([x.arrival_time for x in self.first_line], bins = int(symulation_time))
        self.second_line_histogrammed = np.histogram([x.arrival_time for x in self.second_line], bins = int(symulation_time))

        # Good to control + might use it in visualisation


    def CheckWhoLeavesQueue(self, queue, queue_name, time):
        for index, passanger in enumerate(queue):
            if passanger.arrival_time + passanger.max_time_to_wait <= time:
                self.passangers_that_left_que.append(passanger)
                print(f"Passanger left {queue_name} the queue arrival time: {Utils.seconds_to_hms(passanger.arrival_time)} and waited for {passanger.max_time_to_wait}")
                passanger.left_queue = True
                queue[index] = None


    def CleanQueue(self, queue):
        """
        Args:
            queue: A deque object to be cleaned of None values.
        """
        return deque([x for x in queue if x is not None])


    def ProcessQueue(self, queue, queue_name, time):
        """
        Args:
            queue: A deque object representing the queue to process.
            queue_name: A string indicating the name of the queue (e.g., "first" or "second").
            time: The current simulation time.
        """
        # Check and log passengers who leave the queue
        self.CheckWhoLeavesQueue(queue, queue_name, time)
        # Remove None values from the queue
        return self.CleanQueue(queue)


    def SimulateStep(self, time):
        """
        Args:
            time: Aktualny czas symulacji.
        """
        self.temp_first_que = self.ProcessQueue(self.temp_first_que, "first", time)
        self.temp_second_que = self.ProcessQueue(self.temp_second_que, "second", time)


    def SimulationProcess(self):
        self.InitializeQueues()

        gondola_que = deque()

        for i in range(0, self.cabins_amount):
             gondola_que.append(Gondola(15, 180, 30, 10, "gondola_" + str(i)))


        for time in range(7 * 60 * 60 - 100, 21 * 60 * 60):
            self.SimulateStep(time)

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
            if (self.current_status == self.status("waiting")):
                first_gondola = gondola_que[0]; second_gondola = gondola_que[len(gondola_que) - 1]
                while (len(first_gondola.people_in_cabin) < first_gondola.cabins_capacity and len(self.temp_first_que) > 0):
                    if (first_gondola.count_time == None):
                        first_gondola.count_time = time
                    first_gondola.people_in_cabin.append(self.temp_first_que.popleft())

                while (len(second_gondola.people_in_cabin) < second_gondola.cabins_capacity and len(self.temp_second_que) > 0):
                    if (second_gondola.count_time == None):
                        second_gondola.count_time = time
                    second_gondola.people_in_cabin.append(self.temp_second_que.popleft())

                if (first_gondola.count_time != None or len(first_gondola.people_in_cabin) == first_gondola.cabins_capacity):
                    if (first_gondola.count_time + first_gondola.max_stay_time <= time or len(first_gondola.people_in_cabin) == first_gondola.cabins_capacity):
                        first_gondola.departure_time = time
                        print(f"""First gondola departure time: {Utils.seconds_to_hms(first_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        self.current_status = self.status("moving")

                if (second_gondola.count_time != None or len(second_gondola.people_in_cabin) == second_gondola.cabins_capacity):
                    if (second_gondola.count_time + second_gondola.max_stay_time <= time or len(second_gondola.people_in_cabin) == second_gondola.cabins_capacity):
                        second_gondola.departure_time = time
                        print(f"""Second gondola departure time: {Utils.seconds_to_hms(second_gondola.departure_time)}\nwith {len(first_gondola.people_in_cabin)} in first gondola\nand  {len(second_gondola.people_in_cabin)} in second gondola\n""")
                        self.current_status = self.status("moving")


            if (self.current_status == self.status("moving")):
                if (first_gondola.departure_time != None):
                    if (first_gondola.departure_time + second_gondola.travel_time <= time):
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

            self.SimulateStep(time)
temp = Symulacja(2)
temp.SimulationProcess()

print(len(temp.passangers_that_left_que))
print(len(temp.already_transported_passangers))