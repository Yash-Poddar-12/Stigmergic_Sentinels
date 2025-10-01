# main.py
from simulation.environment import Environment
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.cfs_scheduler import CFSScheduler
from schedulers.single_aco_scheduler import SingleACOScheduler
from schedulers.stigmergic_sentinel import StigmergicSentinelsScheduler
from utils.plotter import plot_summary_results, plot_time_series_results # Updated import
from config import NUM_CORES
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def main():
    schedulers_to_run = [
        CFSScheduler(NUM_CORES),
        PriorityScheduler(NUM_CORES),
        SingleACOScheduler(NUM_CORES),
        StigmergicSentinelsScheduler(NUM_CORES),
    ]

    all_summary_results = {}
    all_metrics_objects = {}

    for scheduler in schedulers_to_run:
        env = Environment(scheduler)
        metrics_obj = env.run() # This now returns the whole object
        
        # Store results for both types of plots
        all_summary_results[str(scheduler)] = metrics_obj.calculate_results()
        all_metrics_objects[str(scheduler)] = metrics_obj
        
        print(f"Final results for {scheduler}: {all_summary_results[str(scheduler)]}\n")

    # Plotting both summary and time-series results
    print("--- Generating Plots ---")
    plot_summary_results(all_summary_results)
    plot_time_series_results(all_metrics_objects)
    print("Simulation complete. All plots saved to the 'plots' directory.")


if __name__ == "__main__":
    main()