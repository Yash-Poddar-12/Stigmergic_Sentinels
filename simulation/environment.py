# simulation/environment.py
import numpy as np
from tqdm import tqdm

from .task import Task
from .core import Core
from .thermal_model import ThermalModel
from .security_monitor import SecurityMonitor
from utils.metrics import Metrics
from config import METRICS_LOG_INTERVAL

class Environment:
    def __init__(self, scheduler, config):
        self.scheduler = scheduler
        self.config = config
        self.num_cores = self.config['NUM_CORES']
        
        self.cores = [Core(i) for i in range(self.num_cores)]
        self.task_queue = []
        self.thermal_model = ThermalModel(self.num_cores)
        self.security_monitor = SecurityMonitor()
        self.metrics = Metrics(self.num_cores, self.config['SIMULATION_DURATION'])
        self.current_time = 0

    def run(self):
        pbar_desc = f"Scheduler: {str(self.scheduler):<27}"
        with tqdm(total=self.config['SIMULATION_DURATION'], desc=pbar_desc, leave=False, ncols=100) as pbar:
            for t in range(self.config['SIMULATION_DURATION']):
                self.current_time = t
                
                if np.random.poisson(self.config['TASK_ARRIVAL_RATE'] / 1000.0):
                    new_task = Task(self.current_time, self.config['THREAT_PROBABILITY'])
                    self.task_queue.append(new_task)

                self.scheduler.schedule(self.task_queue, self.cores, self.current_time)

                for core in self.cores:
                    if not core.is_idle():
                        task = core.current_task
                        
                        if hasattr(task, 'vruntime'): task.vruntime += 1
                        task.remaining_burst -= 1
                        core.busy_time += 1
                        
                        if not task.detected_malicious:
                            detected, _ = self.security_monitor.check_task(task)
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

                self.thermal_model.update(self.cores)
                if hasattr(self.scheduler, 'update'):
                    self.scheduler.update(self.cores, self.current_time)
                
                if t % METRICS_LOG_INTERVAL == 0:
                    self.metrics.update(self.cores, self.task_queue, self.current_time)
                pbar.update(1)
            
        return self.metrics