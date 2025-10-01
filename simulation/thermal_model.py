# simulation/thermal_model.py
import numpy as np
from config import (THERMAL_AMBIENT, THERMAL_ACTIVE_INCREASE,
                    THERMAL_IDLE_DECREASE, THERMAL_NEIGHBOR_INFLUENCE)

class ThermalModel:
    def __init__(self, num_cores):
        self.num_cores = num_cores

    def update(self, cores):
        current_temps = np.array([core.temperature for core in cores])
        next_temps = np.copy(current_temps)

        for core in cores:
            # Self-heating/cooling
            if not core.is_idle():
                next_temps[core.id] += THERMAL_ACTIVE_INCREASE
            else:
                decrease = (core.temperature - THERMAL_AMBIENT) * THERMAL_IDLE_DECREASE
                next_temps[core.id] -= max(0, decrease) # Don't go below ambient

            # Neighbor influence (simple model: average of immediate neighbors)
            left_neighbor_temp = current_temps[core.id - 1] if core.id > 0 else current_temps[core.id]
            right_neighbor_temp = current_temps[core.id + 1] if core.id < self.num_cores - 1 else current_temps[core.id]
            avg_neighbor_temp = (left_neighbor_temp + right_neighbor_temp) / 2
            
            influence = (avg_neighbor_temp - current_temps[core.id]) * THERMAL_NEIGHBOR_INFLUENCE
            next_temps[core.id] += influence

        for i, core in enumerate(cores):
            core.temperature = next_temps[i]