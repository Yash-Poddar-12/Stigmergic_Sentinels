# schedulers/base_scheduler.py
from abc import ABC, abstractmethod

class BaseScheduler(ABC):
    def __init__(self, num_cores):
        self.num_cores = num_cores

    @abstractmethod
    def schedule(self, tasks, cores, current_time):
        """Assigns tasks to idle cores."""
        pass

    def update(self, cores, current_time):
        """Optional method for schedulers that need state updates (like ACO)."""
        pass
        
    def __str__(self):
        return self.__class__.__name__