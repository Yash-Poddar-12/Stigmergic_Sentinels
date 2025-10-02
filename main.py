# main.py
import os
import numpy as np
import warnings
import pandas as pd
from simulation.environment import Environment
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.cfs_scheduler import CFSScheduler
from schedulers.single_aco_scheduler import SingleACOScheduler
from schedulers.stigmergic_sentinel import StigmergicSentinelsScheduler
from utils.plotter import plot_summary_boxplots, plot_time_series_results
import config as default_config

warnings.filterwarnings("ignore", category=RuntimeWarning)

def main():
    # --- DEFINE YOUR EXPERIMENTAL MATRIX HERE ---
    core_levels = [8, 16, 32]
    load_levels = {'low': 10, 'medium': 20, 'heavy': 40}
    threat_levels = {'low': 0.02, 'medium': 0.05, 'high': 0.10}

    # Generate all experiment configurations
    experiments = []
    for cores in core_levels:
        for load_name, load_val in load_levels.items():
            for threat_name, threat_val in threat_levels.items():
                exp_name = f"cores_{cores}_load_{load_name}_threat_{threat_name}"
                experiments.append({
                    'name': exp_name,
                    'NUM_CORES': cores,
                    'TASK_ARRIVAL_RATE': load_val,
                    'THREAT_PROBABILITY': threat_val,
                })

    scheduler_classes = {
        "CFSScheduler": CFSScheduler,
        "PriorityScheduler": PriorityScheduler,
        "SingleACOScheduler": SingleACOScheduler,
        "StigmergicSentinelsScheduler": StigmergicSentinelsScheduler,
    }

    # Main experiment loop
    for experiment_params in experiments:
        current_config = {
            'NUM_RUNS': default_config.NUM_RUNS,
            'SIMULATION_DURATION': default_config.SIMULATION_DURATION,
        }
        current_config.update(experiment_params)
        
        exp_name = current_config['name']
        print(f"\n{'='*60}\n--- Starting Experiment: {exp_name} ---\n{'='*60}")

        all_runs_summary = {name: [] for name in scheduler_classes.keys()}
        all_runs_metrics_objects = {name: [] for name in scheduler_classes.keys()}

        for i in range(current_config['NUM_RUNS']):
            print(f"\n--- Experiment '{exp_name}', Run {i + 1}/{current_config['NUM_RUNS']} ---")
            for name, scheduler_class in scheduler_classes.items():
                scheduler = scheduler_class(current_config['NUM_CORES'])
                env = Environment(scheduler, current_config)
                metrics_obj = env.run()
                
                all_runs_summary[name].append(metrics_obj.calculate_results())
                all_runs_metrics_objects[name].append(metrics_obj)
        
        print(f"\n--- Experiment '{exp_name}' complete. Processing and saving results... ---")
        
        output_directory = os.path.join('plots', exp_name)

        # --- SAVE NUMERICAL RESULTS TO CSV ---
        summary_df_data = []
        for scheduler_name, run_results in all_runs_summary.items():
            for i, run_result in enumerate(run_results):
                row = {'scheduler': scheduler_name, 'run': i + 1}
                row.update(run_result)
                summary_df_data.append(row)
        summary_df = pd.DataFrame(summary_df_data)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        summary_df.to_csv(os.path.join(output_directory, 'summary_results.csv'), index=False)
        print(f"  > Saved numerical summary to {os.path.join(output_directory, 'summary_results.csv')}")

        # --- GENERATE PLOTS FOR THIS EXPERIMENT ---
        plot_summary_boxplots(all_runs_summary, output_directory)
        plot_time_series_results(all_runs_metrics_objects, default_config.MOVING_AVERAGE_WINDOW, output_directory)
        print(f"--- Plots for '{exp_name}' saved to '{output_directory}' ---")

if __name__ == "__main__":
    main()