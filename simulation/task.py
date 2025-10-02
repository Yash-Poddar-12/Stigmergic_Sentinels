# simulation/task.py
import itertools
import numpy as np
from config import TASK_CPU_BURST_RANGE, TASK_PRIORITY_RANGE

class Task:
    id_iter = itertools.count()

    def __init__(self, arrival_time, threat_probability):
        self.id = next(self.id_iter)
        self.arrival_time = arrival_time
        self.cpu_burst = np.random.randint(*TASK_CPU_BURST_RANGE)
        self.remaining_burst = self.cpu_burst
        self.priority = np.random.randint(*TASK_PRIORITY_RANGE)
        self.is_malicious = np.random.rand() < threat_probability
        self.vruntime = 0
        self.detected_malicious = False
        self.detection_time = -1
        self.completion_time = -1

    def __repr__(self):
        return f"Task(id={self.id}, burst={self.remaining_burst}/{self.cpu_burst}, malicious={self.is_malicious})"