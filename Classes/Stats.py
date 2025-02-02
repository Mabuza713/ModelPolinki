import numpy as np
import matplotlib.pyplot as plt
from PolinkaModel import Symulacja  # Upewnij się, że importujesz poprawną ścieżkę

# Parametry stałe dla symulacji
fixed_travel_time = 120    # czas przejazdu (s)
fixed_max_stay_time = 30   # maksymalny czas oczekiwania (s)

# Lista wartości pojemności gondoli do testowania
capacities = [2, 4, 6, 8, 10, 12, 15, 18, 20, 25, 30]

n_trials = 3  # liczba prób dla danego zestawu parametrów

for trial in range(1, n_trials + 1):
    # Inicjujemy listy, w których będziemy zbierać statystyki
    total_passengers_list = []
    transported_list = []
    left_queue_list = []
    avg_wait_time_list = []
    avg_occupancy_list = []
    avg_queue_length_list = []

    print(f"\n--- Trial {trial} ---")
    for cap in capacities:
        # Dla danej pojemności tworzymy instancję symulacji
        sim = Symulacja(cap, fixed_travel_time, fixed_max_stay_time)
        sim.SimulationProcess()

        # Zbieramy statystyki
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

        # Zapisujemy wyniki dla danego cap
        total_passengers_list.append(total_passengers)
        transported_list.append(transported)
        left_queue_list.append(left_queue)
        avg_wait_time_list.append(avg_wait_time)
        avg_occupancy_list.append(avg_occupancy)
        avg_queue_length_list.append(avg_queue)

        # Wypisujemy wyniki dla danego wariantu
        print(f"Capacity = {cap}:")
        print(f"  Total passengers: {total_passengers}")
        print(f"  Transported: {transported}")
        print(f"  Left queue: {left_queue}")
        print(f"  Avg wait time: {avg_wait_time:.2f} s")
        print(f"  Avg occupancy: {avg_occupancy:.2f}")
        print(f"  Avg queue length: {avg_queue:.2f}")
        print("------")

    # Rysujemy wykresy dla danego triala
    plt.figure(figsize=(12, 10))

    plt.subplot(321)
    plt.plot(capacities, total_passengers_list, marker='o', linestyle='-')
    plt.title("Liczba pasażerów w systemie")
    plt.xlabel("Pojemność gondoli")
    plt.ylabel("Liczba pasażerów")
    plt.ylim(0, max(total_passengers_list) * 1.1)

    plt.subplot(322)
    plt.plot(capacities, transported_list, marker='o', label='Obsłużonych')
    plt.plot(capacities, left_queue_list, marker='o', label='Opuściło kolejkę')
    plt.title("Obsłużeni vs Opuścili kolejkę")
    plt.xlabel("Pojemność gondoli")
    plt.ylabel("Liczba pasażerów")
    plt.legend()

    plt.subplot(323)
    plt.plot(capacities, avg_wait_time_list, marker='o', linestyle='-')
    plt.title("Średni czas oczekiwania")
    plt.xlabel("Pojemność gondoli")
    plt.ylabel("Czas (s)")

    plt.subplot(324)
    plt.plot(capacities, avg_occupancy_list, marker='o', linestyle='-')
    plt.title("Średni stopień zapełnienia gondoli")
    plt.xlabel("Pojemność gondoli")
    plt.ylabel("Liczba pasażerów")

    plt.subplot(325)
    plt.plot(capacities, avg_queue_length_list, marker='o', linestyle='-')
    plt.title("Średnia liczba pasażerów w kolejce")
    plt.xlabel("Pojemność gondoli")
    plt.ylabel("Liczba pasażerów")

    plt.tight_layout()
    # Zapisujemy wykres do pliku, a następnie zamykamy go
    filename = f"simulation_results_trial_{trial}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Wykres zapisany jako {filename}\n")
