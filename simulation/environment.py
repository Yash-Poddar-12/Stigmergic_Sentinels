# simulation/environment.py
import numpy as np
from tqdm import tqdm

from .task import Task
from .core import Core
from .thermal_model import ThermalModel
from .security_monitor import SecurityMonitor
from utils.metrics import Metrics
from config import SIMULATION_DURATION, TASK_ARRIVAL_RATE, NUM_CORES

class Environment:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.cores = [Core(i) for i in range(NUM_CORES)]
        self.task_queue = []
        self.thermal_model = ThermalModel(NUM_CORES)
        self.security_monitor = SecurityMonitor()
        self.metrics = Metrics(NUM_CORES, SIMULATION_DURATION)
        self.current_time = 0

    def run(self):
        print(f"--- Running simulation for: {self.scheduler} ---")
        for t in tqdm(range(SIMULATION_DURATION)):
            self.current_time = t
            
            # 1. Task Generation
            if np.random.poisson(TASK_ARRIVAL_RATE / 1000.0):
                self.task_queue.append(Task(self.current_time))

            # 2. Scheduling
            self.scheduler.schedule(self.task_queue, self.cores, self.current_time)

            # 3. Core Processing & State Updates
            for core in self.cores:
                if not core.is_idle():
                    task = core.current_task
                    
                    if hasattr(task, 'vruntime'):
                        task.vruntime += 1
                        
                    task.remaining_burst -= 1
                    core.busy_time += 1
                    
                    if not task.detected_malicious:
                        detected, is_correct = self.security_monitor.check_task(task)
                        if detected:
                            task.detected_malicious = True
                            task.detection_time = self.current_time
                            if hasattr(self.scheduler, 'update'):
                                self.scheduler.update(self.cores, self.current_time)
                    
                    if task.remaining_burst <= 0:
                        task.completion_time = self.current_time
                        if task.detected_malicious:
                            self.metrics.record_isolation(task, self.current_time)
                        core.current_task = None

            # 4. Update Models
            self.thermal_model.update(self.cores)
            if hasattr(self.scheduler, 'update'):
                self.scheduler.update(self.cores, self.current_time)
            
            # 5. Collect Metrics
            self.metrics.update(self.cores, self.task_queue, self.current_time)
            
        return self.metrics # Return the entire metrics object