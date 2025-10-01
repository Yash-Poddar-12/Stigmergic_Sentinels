# schedulers/cfs_scheduler.py
from .base_scheduler import BaseScheduler

class CFSScheduler(BaseScheduler):
    def schedule(self, tasks, cores, current_time):
        idle_cores = [core for core in cores if core.is_idle()]
        if not tasks or not idle_cores:
            return

        # Sort tasks by virtual runtime (lower is better)
        sorted_tasks = sorted(tasks, key=lambda t: t.vruntime)

        for task in sorted_tasks:
            if not idle_cores:
                break
            core = idle_cores.pop(0)
            core.current_task = task
            tasks.remove(task)