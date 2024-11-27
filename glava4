import numpy as np

lambda1, lambda2 = 2.0, 0.5  
p = 0.7  
buffer_capacity = 3  
T_p = 0.136 
simulation_time = 10  

def generate_arrival_times(simulation_time, lambda1, lambda2, p):
    times = []
    current_time = 0
    while current_time < simulation_time:
        phase = np.random.choice([1, 2], p=[p, 1 - p])
        rate = lambda1 if phase == 1 else lambda2
        interval = np.random.exponential(1 / rate)
        current_time += interval
        if current_time < simulation_time:
            times.append(current_time)
    return times

arrival_times = generate_arrival_times(simulation_time, lambda1, lambda2, p)
buffer = []
processors = [0, 0]  
rejects = 0
processed = 0

for t in np.linspace(0, simulation_time, 1000):
    if len(arrival_times) > 0 and t >= arrival_times[0]:
        arrival_times.pop(0)
        if len(buffer) < buffer_capacity:
            buffer.append(T_p)
        else:
            rejects += 1  

    for i in range(2):
        if processors[i] == 0 and len(buffer) > 0:
            processors[i] = buffer.pop(0)
        if processors[i] > 0:
            processors[i] -= simulation_time / 1000
            if processors[i] <= 0:
                processed += 1
                processors[i] = 0

print(f"Обработано пакетов: {processed}")
print(f"Отказы: {rejects}")
