# schedulers/stigmergic_sentinel.py
import numpy as np
from .base_scheduler import BaseScheduler
from config import (RHO_T, RHO_E, RHO_C, ALPHA, BETA, GAMMA, DELTA, EPSILON)

class StigmergicSentinelsScheduler(BaseScheduler):
    def __init__(self, num_cores):
        super().__init__(num_cores)
        self.attractive_pheromone = np.ones(num_cores)
        self.threat_pheromone = np.zeros(num_cores)
        self.env_pheromone = np.ones(num_cores)
        self.contention_pheromone = np.ones(num_cores)

    def schedule(self, tasks, cores, current_time):
        idle_cores = [core for core in cores if core.is_idle()]
        schedulable_tasks = [t for t in tasks if not t.detected_malicious]

        if not schedulable_tasks or not idle_cores:
            return

        for task in schedulable_tasks[:]:
            if not idle_cores:
                break
            
            idle_core_ids = [c.id for c in idle_cores]
            attr_ph = self.attractive_pheromone[idle_core_ids]
            heuristic = 1.0 / (task.remaining_burst + 1e-5)
            threat_ph = self.threat_pheromone[idle_core_ids]
            env_ph = self.env_pheromone[idle_core_ids]
            cont_ph = self.contention_pheromone[idle_core_ids]
            
            numerator = (attr_ph ** ALPHA) * (heuristic ** BETA)
            denominator = ((threat_ph + 1e-5) ** GAMMA) * \
                          ((env_ph + 1e-5) ** DELTA) * \
                          ((cont_ph + 1e-5) ** EPSILON)
            
            probabilities = numerator / denominator
            
            if np.sum(probabilities) <= 0:
                probabilities = np.ones_like(probabilities)
            
            probabilities /= np.sum(probabilities)

            chosen_core_idx = np.random.choice(len(idle_cores), p=probabilities)
            chosen_core = idle_cores.pop(chosen_core_idx)
            
            chosen_core.current_task = task
            tasks.remove(task)

    def update(self, cores, current_time):
        self.attractive_pheromone *= (1 - RHO_C)
        self.threat_pheromone *= (1 - RHO_T)
        self.env_pheromone *= (1 - RHO_E)
        self.contention_pheromone *= (1 - RHO_C)

        for core in cores:
            self.env_pheromone[core.id] += RHO_E * core.temperature
            if not core.is_idle():
                task = core.current_task
                if task.detected_malicious:
                    self.threat_pheromone[core.id] += RHO_T * 100
                self.contention_pheromone[core.id] += RHO_C
                self.attractive_pheromone[core.id] += RHO_C / (task.remaining_burst + 1)