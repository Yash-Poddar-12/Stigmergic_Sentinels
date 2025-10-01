# simulation/task.py
import itertools
import numpy as np
from config import TASK_CPU_BURST_RANGE, TASK_PRIORITY_RANGE, THREAT_PROBABILITY

class Task:
    id_iter = itertools.count()

    def __init__(self, arrival_time):
        self.id = next(self.id_iter)
        self.arrival_time = arrival_time
        self.cpu_burst = np.random.randint(*TASK_CPU_BURST_RANGE)
        self.remaining_burst = self.cpu_burst
        self.priority = np.random.randint(*TASK_PRIORITY_RANGE)
        self.is_malicious = np.random.rand() < THREAT_PROBABILITY
        self.vruntime = 0 # For CFS scheduler
        self.detected_malicious = False
        self.detection_time = -1
        self.completion_time = -1

    def __repr__(self):
        return f"Task(id={self.id}, burst={self.remaining_burst}/{self.cpu_burst}, malicious={self.is_malicious})"