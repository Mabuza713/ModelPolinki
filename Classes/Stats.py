import numpy as np
import matplotlib.pyplot as plt
from PolinkaModel import Symulacja  # Upewnij się, że ścieżka importu jest prawidłowa

# Parametry stałe dla symulacji
fixed_travel_time = 180    # czas przejazdu (s)
fixed_max_stay_time = 30   # maksymalny czas oczekiwania (s)

# Lista wartości, dla których zmieniamy pojemność gondoli
capacities = [2, 4, 6, 8, 10]

# Listy do przechowywania wyników
total_passengers_list = []
transported_list = []
left_queue_list = []
avg_wait_time_list = []
avg_occupancy_list = []
avg_queue_length_list = []

# Uruchamiamy symulację dla kolejnych wartości pojemności
for cap in capacities:
    sim = Symulacja(cap, fixed_travel_time, fixed_max_stay_time)
    sim.SimulationProcess()

    # Zbieramy statystyki
    total_passengers = len(sim.amount_people_who_come)
    transported = len(sim.already_transported_passangers)
    left_queue = len(sim.passangers_that_left_que)

    # Obliczamy średni czas oczekiwania (dla pasażerów, którzy zostali obsłużeni)
    if transported > 0:
        avg_wait_time = np.mean([p.wait_time for p in sim.already_transported_passangers])
    else:
        avg_wait_time = 0

    # Średni stopień zapełnienia gondoli (na podstawie zarejestrowanych wartości)
    if len(sim.gondola_occupancies) > 0:
        avg_occupancy = np.mean(sim.gondola_occupancies)
    else:
        avg_occupancy = 0

    # Średnia liczba osób oczekujących w kolejce (suma z obu kolejek w każdej iteracji)
    avg_queue = np.mean([sum(q) for q in sim.people_in_queue_data])

    # Zapisujemy wyniki
    total_passengers_list.append(total_passengers)
    transported_list.append(transported)
    left_queue_list.append(left_queue)
    avg_wait_time_list.append(avg_wait_time)
    avg_occupancy_list.append(avg_occupancy)
    avg_queue_length_list.append(avg_queue)

    print(f"Symulacja dla pojemności gondoli = {cap}:")
    print(f"  Liczba pasażerów w systemie: {total_passengers}")
    print(f"  Pasażerów obsłużonych: {transported}")
    print(f"  Pasażerów, którzy opuścili kolejkę: {left_queue}")
    print(f"  Średni czas oczekiwania: {avg_wait_time:.2f} s")
    print(f"  Średni stopień zapełnienia gondoli: {avg_occupancy:.2f}")
    print(f"  Średnia liczba pasażerów w kolejce: {avg_queue:.2f}")
    print("------------------------------------------------------")

plt.figure(figsize=(12, 10))

plt.subplot(321)
plt.plot(capacities, total_passengers_list, marker='o', linestyle='-')
plt.title("Liczba pasażerów w systemie")
plt.xlabel("Pojemność gondoli")
plt.ylabel("Liczba pasażerów")

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
plt.show()
