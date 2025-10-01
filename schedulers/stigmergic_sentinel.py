# schedulers/stigmergic_sentinel.py
import numpy as np
from .base_scheduler import BaseScheduler
from config import (RHO_T, RHO_E, RHO_C, ALPHA, BETA, GAMMA, DELTA, EPSILON)

class StigmergicSentinelsScheduler(BaseScheduler):
    def __init__(self, num_cores):
        super().__init__(num_cores)
        # Initialize pheromone trails
        self.attractive_pheromone = np.ones(num_cores) # Base performance pheromone
        self.threat_pheromone = np.zeros(num_cores)     # Repulsive
        self.env_pheromone = np.ones(num_cores)      # Lower is hotter/worse
        self.contention_pheromone = np.ones(num_cores) # Higher is more contended/worse

    def schedule(self, tasks, cores, current_time):
        idle_cores = [core for core in cores if core.is_idle()]
        
        # Filter out tasks that have been identified as malicious
        schedulable_tasks = [t for t in tasks if not t.detected_malicious]

        if not schedulable_tasks or not idle_cores:
            return

        for task in schedulable_tasks[:]:
            if not idle_cores:
                break
            
            idle_core_ids = [c.id for c in idle_cores]
            
            # --- Implementing Equation (4) ---
            # τ_attractive
            attr_ph = self.attractive_pheromone[idle_core_ids]
            # η_ij (heuristic: shorter job is better)
            heuristic = 1.0 / (task.remaining_burst + 1e-5)
            # τ_threat (repulsive)
            threat_ph = self.threat_pheromone[idle_core_ids]
            # τ_env
            env_ph = self.env_pheromone[idle_core_ids]
            # τ_cont
            cont_ph = self.contention_pheromone[idle_core_ids]
            
            # Combine signals
            numerator = (attr_ph ** ALPHA) * (heuristic ** BETA)
            denominator = (threat_ph + 1e-5) ** GAMMA * \
                          (env_ph ** DELTA) * \
                          (cont_ph ** EPSILON)
            
            probabilities = numerator / denominator
            
            if np.sum(probabilities) <= 0:
                probabilities = np.ones_like(probabilities) # Fallback
            
            probabilities /= np.sum(probabilities)

            # Roulette wheel selection
            chosen_core_idx = np.random.choice(len(idle_cores), p=probabilities)
            chosen_core = idle_cores.pop(chosen_core_idx)
            
            chosen_core.current_task = task
            tasks.remove(task)

    def update(self, cores, current_time):
        # --- Pheromone Evaporation ---
        self.attractive_pheromone *= (1 - RHO_C) # Using contention rate
        self.threat_pheromone *= (1 - RHO_T)
        self.env_pheromone *= (1 - RHO_E)
        self.contention_pheromone *= (1 - RHO_C)

        # --- Pheromone Deposition ---
        for core in cores:
            # --- Environmental Pheromone Update (Equation 3 analog) ---
            # Higher temperature leads to higher pheromone value (worse)
            self.env_pheromone[core.id] += RHO_E * core.temperature
            
            if not core.is_idle():
                task = core.current_task
                
                # --- Threat Pheromone Update (Equation 2 analog) ---
                if task.detected_malicious:
                    self.threat_pheromone[core.id] += RHO_T * 100 # Strong repulsive signal
                
                # --- Contention Pheromone Update ---
                # A busy core signals contention
                self.contention_pheromone[core.id] += RHO_C
                
                # --- Attractive Pheromone Update ---
                # Reward for progress
                self.attractive_pheromone[core.id] += RHO_C / (task.remaining_burst + 1)