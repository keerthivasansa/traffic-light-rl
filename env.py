# State -> (current_light)
# vehicle_speed, vehicle_count, vehicle_size

# Action -> (time: 1 to 100)
import enum

from vehicle import Vehicle, VehicleState
import numpy as np
import sys
 
sys.setrecursionlimit(10**4)

class TrafficSignal(enum.Enum):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'

class Environment:
    def __init__(self):
        self.times = []
        self.time = 0
        self.current = TrafficSignal.RED
        self.road_length = 50
        self.total_time = 0

        self.next_signal = {
            TrafficSignal.GREEN: TrafficSignal.YELLOW,
            TrafficSignal.YELLOW: TrafficSignal.RED,
            TrafficSignal.RED: TrafficSignal.GREEN,
        }

        self.preserved_state = []

    def get_states(self):
        return [TrafficSignal.RED, TrafficSignal.YELLOW, TrafficSignal.GREEN]

    def get_actions(self, state):
        if state == TrafficSignal.YELLOW:
            return range(10, 45, 5)
        else:            
            return range(10, 180, 3)

    def perform_action(self, state, time, preserved_index = -1):
        total_time = time
        vehicles = []

        if preserved_index != -1:
            time_used, old_vehicles = self.preserved_state[preserved_index]
            total_time += time_used
            vehicles.extend(old_vehicles)

        if total_time >= 1500: # stop iterations
            return None, 0, -1

        for _ in range(time // 40):
            rand_halt = np.random.randint(15, 25)
            vehicles.append(Vehicle(rand_halt, self.road_length))
        else:
            rand_halt = np.random.randint(15, 25)
            vehicles.append(Vehicle(rand_halt, self.road_length))

        passed = 0
        next_state = self.next_signal[state]
        curr_time = time

        while vehicles and curr_time > 0:
            v : Vehicle = vehicles[0]
            if state == TrafficSignal.RED:
                v_state = v.brake(curr_time)
                if v_state == VehicleState.CRASH:
                    vehicles.pop(0)
                    passed = -8
                break
            elif state == TrafficSignal.YELLOW:
                v_state = v.slow(curr_time)
                break
            else:
                v_state, time_taken = v.accelerate(curr_time)
                if v_state == VehicleState.PASSED:
                    passed += 1
                    vehicles.pop(0)
                curr_time -= time_taken

        if preserved_index == -1:
            preserved_index = len(self.preserved_state)
            self.preserved_state.append((total_time, vehicles))
        else:
            self.preserved_state[preserved_index] = (total_time, vehicles)
        
        return next_state, passed * 20, preserved_index
