# config.py

# Simulation settings
SIMULATION_DURATION = 10000  # in milliseconds
NUM_CORES = 8
TASK_ARRIVAL_RATE = 20  # tasks per 1000ms (lambda for Poisson)

# Task properties
TASK_CPU_BURST_RANGE = (50, 200)  # min/max ms
TASK_PRIORITY_RANGE = (1, 5)  # 1 is highest priority
THREAT_PROBABILITY = 0.05 # Probability a new task is malicious

# Thermal Model parameters
THERMAL_AMBIENT = 40.0  # Ambient temperature in Celsius
THERMAL_ACTIVE_INCREASE = 0.5  # Temp increase per ms when active
THERMAL_IDLE_DECREASE = 0.1 # Temp decrease per ms when idle
THERMAL_NEIGHBOR_INFLUENCE = 0.01  # How much neighbors affect temp
THERMAL_HOTSPOT_THRESHOLD = 85.0 # Temp in Celsius to be a hotspot

# Security Monitor parameters
THREAT_DETECTION_PROBABILITY = 0.9 # Prob of detecting a malicious task per ms
FALSE_POSITIVE_PROBABILITY = 0.001 # Prob of flagging a benign task

# Stigmergic Sentinels parameters (from paper)
# Pheromone evaporation rates
RHO_T = 0.1   # Threat pheromone
RHO_E = 0.05  # Environmental pheromone
RHO_C = 0.08  # Contention pheromone

# Decision formula weights (Equation 4)
ALPHA = 1.0   # attractive_pheromone
BETA = 1.0    # heuristic
GAMMA = 2.0   # threat_pheromone (repulsive, so higher weight)
DELTA = 1.5   # env_pheromone
EPSILON = 1.0 # contention_pheromone

# Single-Pheromone ACO parameters
RHO_SINGLE_ACO = 0.1
ALPHA_SINGLE_ACO = 1.0
BETA_SINGLE_ACO = 1.0

# NEW SETTING for time-series plotting
METRICS_LOG_INTERVAL = 200 # Log data every 200ms