# simulation/security_monitor.py
import numpy as np
from config import THREAT_DETECTION_PROBABILITY, FALSE_POSITIVE_PROBABILITY

class SecurityMonitor:
    def check_task(self, task):
        if task.detected_malicious:
            return True, True # Already detected

        detected = False
        is_correct = False
        if task.is_malicious:
            if np.random.rand() < THREAT_DETECTION_PROBABILITY:
                detected = True
                is_correct = True
        else: # Benign task
            if np.random.rand() < FALSE_POSITIVE_PROBABILITY:
                detected = True
                is_correct = False
        
        return detected, is_correct