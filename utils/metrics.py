# utils/metrics.py
import numpy as np
from config import METRICS_LOG_INTERVAL, THERMAL_HOTSPOT_THRESHOLD

class Metrics:
    def __init__(self, num_cores, simulation_duration):
        self.num_cores = num_cores
        self.simulation_duration = simulation_duration
        self.total_busy_time = 0
        self.thermal_hotspot_counts = 0
        self.threat_isolation_times = []
        
        self.time_steps = []
        self.avg_temp_history = []
        self.cpu_util_history = []
        self.active_threats_history = []
        self.last_log_time = -1
        self.interval_busy_time = 0

    def update(self, cores, task_queue, current_time):
        busy_cores_in_step = 0
        for core in cores:
            if not core.is_idle():
                busy_cores_in_step += 1
                if core.temperature > THERMAL_HOTSPOT_THRESHOLD:
                    self.thermal_hotspot_counts += 1

        self.total_busy_time += busy_cores_in_step
        self.interval_busy_time += busy_cores_in_step
        
        self.time_steps.append(current_time)
        avg_temp = np.mean([core.temperature for core in cores])
        self.avg_temp_history.append(avg_temp)
        
        current_util = (self.interval_busy_time / (self.num_cores * METRICS_LOG_INTERVAL)) * 100
        self.cpu_util_history.append(current_util)
        self.interval_busy_time = 0
        
        active_threats = sum(1 for core in cores if not core.is_idle() and core.current_task.is_malicious) + \
                         sum(1 for task in task_queue if task.is_malicious)
        self.active_threats_history.append(active_threats)
    
    def record_isolation(self, task, current_time):
        if task.detection_time > 0:
            isolation_time = current_time - task.detection_time
            self.threat_isolation_times.append(isolation_time)

    def calculate_results(self):
        cpu_utilization = (self.total_busy_time / (self.num_cores * self.simulation_duration)) * 100
        avg_isolation_time = np.mean(self.threat_isolation_times) if self.threat_isolation_times else float('inf')
        
        return {
            "CPU Utilization (%)": cpu_utilization,
            "Thermal Hotspots": self.thermal_hotspot_counts,
            "Avg Isolation Time (ms)": avg_isolation_time,
        }