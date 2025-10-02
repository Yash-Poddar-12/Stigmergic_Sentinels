# schedulers/base_scheduler.py
from abc import ABC, abstractmethod

class BaseScheduler(ABC):
    def __init__(self, num_cores):
        self.num_cores = num_cores

    @abstractmethod
    def schedule(self, tasks, cores, current_time):
        pass

    def update(self, cores, current_time):
        pass
        
    def __str__(self):
        # A simple way to get a clean name for the progress bar
        return self.__class__.__name__.replace("Scheduler", "")