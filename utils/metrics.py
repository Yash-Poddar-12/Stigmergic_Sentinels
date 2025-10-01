# utils/metrics.py
import numpy as np
from config import THERMAL_HOTSPOT_THRESHOLD, METRICS_LOG_INTERVAL

class Metrics:
    def __init__(self, num_cores, simulation_duration):
        self.num_cores = num_cores
        self.simulation_duration = simulation_duration
        self.total_busy_time = 0
        self.thermal_hotspot_counts = np.zeros(num_cores)
        self.threat_isolation_times = []
        
        # New attributes for time-series data
        self.time_steps = []
        self.avg_temp_history = []
        self.cpu_util_history = []
        self.active_threats_history = []
        self.last_log_time = -1
        self.interval_busy_time = 0

    def update(self, cores, task_queue, current_time):
        # Aggregate metrics (for final bar charts)
        for core in cores:
            if not core.is_idle():
                self.total_busy_time += 1
                self.interval_busy_time += 1
            if core.temperature > THERMAL_HOTSPOT_THRESHOLD:
                self.thermal_hotspot_counts[core.id] += 1
        
        # Time-series logging
        if current_time - self.last_log_time >= METRICS_LOG_INTERVAL:
            self.last_log_time = current_time
            self.time_steps.append(current_time)

            # Log average temperature
            avg_temp = np.mean([core.temperature for core in cores])
            self.avg_temp_history.append(avg_temp)

            # Log instantaneous CPU utilization
            current_util = (self.interval_busy_time / (self.num_cores * METRICS_LOG_INTERVAL)) * 100
            self.cpu_util_history.append(current_util)
            self.interval_busy_time = 0 # Reset for next interval

            # Log active threats
            running_threats = sum(1 for core in cores if not core.is_idle() and core.current_task.is_malicious)
            queued_threats = sum(1 for task in task_queue if task.is_malicious)
            self.active_threats_history.append(running_threats + queued_threats)
    
    def record_isolation(self, task, current_time):
        if task.detection_time > 0:
            isolation_time = current_time - task.detection_time
            self.threat_isolation_times.append(isolation_time)

    def calculate_results(self):
        # This remains the same, for the summary bar charts
        cpu_utilization = (self.total_busy_time / (self.num_cores * self.simulation_duration)) * 100
        total_hotspots = np.sum(self.thermal_hotspot_counts)
        avg_isolation_time = np.mean(self.threat_isolation_times) if self.threat_isolation_times else float('inf')
        
        return {
            "CPU Utilization (%)": cpu_utilization,
            "Thermal Hotspots": total_hotspots,
            "Avg Isolation Time (ms)": avg_isolation_time,
        }