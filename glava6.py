import simpy
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

def packet_arrival(env, buffer, processors, event_queue):
    while True:
        arrival_time = event_queue.pop(0) if len(event_queue) > 0 else 10
        yield env.timeout(arrival_time)

        if len(buffer) < buffer_capacity:
            buffer.append(T_p)
            print(f"Пакет поступил в буфер в {env.now:.2f} секунд")

            for i in range(len(processors)):
                if processors[i] == 0:  
                    processors[i] = buffer.pop(0)
                    print(f"Процессор {i+1} начинает обработку пакета в {env.now:.2f} секунд")
                    env.process(processing_end(env, processors, i))
                    break
        else:
            print(f"Отказ: буфер переполнен в {env.now:.2f} секунд")

def processing_end(env, processors, processor_id):
    yield env.timeout(T_p)
    processors[processor_id] = 0 
    print(f"Процессор {processor_id + 1} завершил обработку пакета в {env.now:.2f} секунд")


def run_simulation():
    env = simpy.Environment() 

    buffer = [] 
    processors = [0, 0]  
    event_queue = generate_arrival_times(simulation_time, lambda1, lambda2, p)  

    env.process(packet_arrival(env, buffer, processors, event_queue))

    env.run(until=simulation_time)

run_simulation()
