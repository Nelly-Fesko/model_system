import heapq
import numpy as np

lambda1, lambda2 = 2.0, 0.5
p = 0.7
buffer_capacity = 3
T_p = 0.136
simulation_time = 10

event_queue = []  

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
for arrival_time in arrival_times:
    heapq.heappush(event_queue, (arrival_time, "arrival", None))

buffer = []  
processors = [0, 0]  
current_time = 0 
rejects = 0 
processed = 0  


while event_queue:
    current_time, event_type, event_data = heapq.heappop(event_queue)

    if event_type == "arrival":

        if len(buffer) < buffer_capacity:
            buffer.append(T_p)
            for i in range(len(processors)):
                if processors[i] == 0:
                    processors[i] = buffer.pop(0)
                    heapq.heappush(event_queue, (current_time + T_p, "processing_end", i))
                    break
        else:
            rejects += 1

    elif event_type == "processing_end":
        processor_id = event_data
        processors[processor_id] = 0
        processed += 1
        if buffer:
            processors[processor_id] = buffer.pop(0)
            heapq.heappush(event_queue, (current_time + T_p, "processing_end", processor_id))

print(f"Обработано пакетов: {processed}")
print(f"Отказы: {rejects}")
