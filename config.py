# config.py

# --- Number of simulation runs to average for EACH experiment ---
NUM_RUNS = 30

# --- Default simulation settings (can be overridden in main.py) ---
SIMULATION_DURATION = 20000
NUM_CORES = 8
TASK_ARRIVAL_RATE = 20
THREAT_PROBABILITY = 0.05

# --- Static Task Properties ---
TASK_CPU_BURST_RANGE = (50, 200)
TASK_PRIORITY_RANGE = (1, 5)

# --- Static Model Parameters ---
# Thermal Model
THERMAL_AMBIENT = 40.0
THERMAL_ACTIVE_INCREASE = 0.5
THERMAL_IDLE_DECREASE = 0.1
THERMAL_NEIGHBOR_INFLUENCE = 0.01
THERMAL_HOTSPOT_THRESHOLD = 85.0

# Security Monitor
THREAT_DETECTION_PROBABILITY = 0.9
FALSE_POSITIVE_PROBABILITY = 0.001

# Stigmergic Sentinels Pheromones
RHO_T = 0.1
RHO_E = 0.05
RHO_C = 0.08
ALPHA = 1.0
BETA = 1.0
GAMMA = 2.0
DELTA = 1.5
EPSILON = 1.0

# Single-Pheromone ACO
RHO_SINGLE_ACO = 0.1
ALPHA_SINGLE_ACO = 1.0
BETA_SINGLE_ACO = 1.0

# Plotting
METRICS_LOG_INTERVAL = 200
MOVING_AVERAGE_WINDOW = 10