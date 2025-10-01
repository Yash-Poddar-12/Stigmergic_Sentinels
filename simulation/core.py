# simulation/core.py
from config import THERMAL_AMBIENT

class Core:
    def __init__(self, id):
        self.id = id
        self.current_task = None
        self.temperature = THERMAL_AMBIENT
        self.busy_time = 0

    def is_idle(self):
        return self.current_task is None

    def __repr__(self):
        task_id = self.current_task.id if self.current_task else "None"
        return f"Core(id={self.id}, task={task_id}, temp={self.temperature:.2f})"