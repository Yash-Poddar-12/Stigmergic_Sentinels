# Stigmergic Sentinels: A Simulation Framework

[cite_start]This repository contains the Python simulation of the "Stigmergic Sentinels" framework, a novel multi-pheromone Ant Colony Optimization (ACO) approach for resilient OS task scheduling[cite: 1]. [cite_start]The simulation validates the paper's claims by comparing the proposed scheduler against traditional and single-pheromone schedulers across three key areas: performance, thermal management, and security response[cite: 15].

---

## 🚀 Features

- **Stigmergic Sentinels Scheduler**: Full implementation of the multi-pheromone scheduler, featuring:
  - [cite_start]**Repulsive Threat Pheromones** for dynamic security isolation[cite: 13, 27].
  - [cite_start]**Environmental Pheromones** for proactive thermal management[cite: 14, 28].
  - [cite_start]**Contention Pheromones** for resource bottleneck avoidance[cite: 14].
- [cite_start]**Baseline Schedulers**: Includes implementations of CFS (simplified), Priority-based, and a standard Single-Pheromone ACO scheduler for comprehensive comparison[cite: 86].
- [cite_start]**Dynamic Simulation Environment**: A discrete-event simulation modeling a multi-core system with a task generator, security monitor, and thermal model[cite: 73].
- **Rich Visualization**: Automatically generates and saves summary bar charts and detailed time-series line graphs to compare scheduler performance visually.

---

## 🛠️ Setup and Installation

Follow these steps to set up the simulation environment.

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd stigmergic-sentinels-sim
    ```

2.  **Create and activate a Python virtual environment:**

    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ How to Run

To run the full suite of simulations and generate the result plots, execute the main script from the root directory of the project:

```bash
python main.py
```
