# schedulers/single_aco_scheduler.py
import numpy as np
from .base_scheduler import BaseScheduler
from config import RHO_SINGLE_ACO, ALPHA_SINGLE_ACO, BETA_SINGLE_ACO

class SingleACOScheduler(BaseScheduler):
    def __init__(self, num_cores):
        super().__init__(num_cores)
        self.performance_pheromone = np.ones(num_cores)

    def schedule(self, tasks, cores, current_time):
        idle_cores = [core for core in cores if core.is_idle()]
        if not tasks or not idle_cores:
            return

        for task in tasks[:]:
            if not idle_cores:
                break

            idle_core_ids = [c.id for c in idle_cores]
            pheromones = self.performance_pheromone[idle_core_ids]
            heuristics = np.array([1.0 / (c.temperature + 1e-5) for c in idle_cores])
            
            probabilities = (pheromones ** ALPHA_SINGLE_ACO) * (heuristics ** BETA_SINGLE_ACO)
            if np.sum(probabilities) == 0:
                probabilities = np.ones_like(probabilities)
            
            probabilities /= np.sum(probabilities)

            chosen_core_idx = np.random.choice(len(idle_cores), p=probabilities)
            chosen_core = idle_cores.pop(chosen_core_idx)
            
            chosen_core.current_task = task
            tasks.remove(task)
            
    def update(self, cores, current_time):
        self.performance_pheromone *= (1 - RHO_SINGLE_ACO)
        for core in cores:
            if not core.is_idle():
                reward = 1.0 / (core.current_task.remaining_burst + 1)
                self.performance_pheromone[core.id] += reward