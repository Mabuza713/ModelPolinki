import numpy as np
import matplotlib.pyplot as plt
from PolinkaModel import Symulacja  # Upewnij się, że ścieżka importu jest prawidłowa

# Parametry stałe dla symulacji
fixed_capacity = 10          # Pojemność gondoli
fixed_travel_time = 100      # Czas przejazdu (s)

# Lista wartości maksymalnego czasu oczekiwania do przetestowania
stay_times = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60]

n_trials = 3  # Liczba prób

for trial in range(1, n_trials + 1):
    # Inicjalizacja list wyników dla danej próby
    total_passengers_list_st = []
    transported_list_st = []
    left_queue_list_st = []
    avg_wait_time_list_st = []
    avg_occupancy_list_st = []
    avg_queue_length_list_st = []

    print(f"\n--- Trial {trial} (Stay Time Experiment) ---")
    for st in stay_times:
        sim = Symulacja(fixed_capacity, fixed_travel_time, st)
        sim.SimulationProcess()

        total_passengers = len(sim.amount_people_who_come)
        transported = len(sim.already_transported_passangers)
        left_queue = len(sim.passangers_that_left_que)

        if transported > 0:
            avg_wait_time = np.mean([p.wait_time for p in sim.already_transported_passangers])
        else:
            avg_wait_time = 0

        if len(sim.gondola_occupancies) > 0:
            avg_occupancy = np.mean(sim.gondola_occupancies)
        else:
            avg_occupancy = 0

        avg_queue = np.mean([sum(q) for q in sim.people_in_queue_data])

        total_passengers_list_st.append(total_passengers)
        transported_list_st.append(transported)
        left_queue_list_st.append(left_queue)
        avg_wait_time_list_st.append(avg_wait_time)
        avg_occupancy_list_st.append(avg_occupancy)
        avg_queue_length_list_st.append(avg_queue)

        print(f"Max stay time = {st} s:")
        print(f"  Total passengers: {total_passengers}")
        print(f"  Transported: {transported}")
        print(f"  Left queue: {left_queue}")
        print(f"  Avg wait time: {avg_wait_time:.2f} s")
        print(f"  Avg occupancy: {avg_occupancy:.2f}")
        print(f"  Avg queue length: {avg_queue:.2f}")
        print("------")

    # Rysowanie wykresów dla danej próby
    plt.figure(figsize=(12, 10))

    plt.subplot(321)
    plt.plot(stay_times, total_passengers_list_st, marker='o', linestyle='-')
    plt.title("Liczba pasażerów w systemie")
    plt.xlabel("Maksymalny czas oczekiwania (s)")
    plt.ylabel("Liczba pasażerów")
    plt.ylim(0, max(total_passengers_list_st) * 1.1)

    plt.subplot(322)
    plt.plot(stay_times, transported_list_st, marker='o', label='Obsłużonych')
    plt.plot(stay_times, left_queue_list_st, marker='o', label='Opuściło kolejkę')
    plt.title("Obsłużeni vs Opuścili kolejkę")
    plt.xlabel("Maksymalny czas oczekiwania (s)")
    plt.ylabel("Liczba pasażerów")
    plt.legend()

    plt.subplot(323)
    plt.plot(stay_times, avg_wait_time_list_st, marker='o', linestyle='-')
    plt.title("Średni czas oczekiwania")
    plt.xlabel("Maksymalny czas oczekiwania (s)")
    plt.ylabel("Czas oczekiwania (s)")

    plt.subplot(324)
    plt.plot(stay_times, avg_occupancy_list_st, marker='o', linestyle='-')
    plt.title("Średni stopień zapełnienia gondoli")
    plt.xlabel("Maksymalny czas oczekiwania (s)")
    plt.ylabel("Liczba pasażerów")

    plt.subplot(325)
    plt.plot(stay_times, avg_queue_length_list_st, marker='o', linestyle='-')
    plt.title("Średnia liczba pasażerów w kolejce")
    plt.xlabel("Maksymalny czas oczekiwania (s)")
    plt.ylabel("Liczba pasażerów")

    plt.tight_layout()
    filename = f"simulation_results_staytime_trial_{trial}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Wykres zapisany jako {filename}\n")
