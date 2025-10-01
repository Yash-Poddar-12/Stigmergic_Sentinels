# utils/plotter.py
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = "plots"

def plot_summary_results(results):
    """Plots the final summary bar charts."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    scheduler_names = list(results.keys())
    metrics = list(results[scheduler_names[0]].keys())
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for metric in metrics:
        values = [results[name][metric] for name in scheduler_names]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(scheduler_names, values, color=colors)
        
        ax.set_ylabel(metric)
        ax.set_title(f"Scheduler Comparison: {metric}")
        ax.set_xticklabels(scheduler_names, rotation=15, ha="right")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom', ha='center')

        plt.tight_layout()
        filename = os.path.join(OUTPUT_DIR, f"summary_{metric.replace(' ', '_').replace('%', 'perc').replace('/', 'per')}.png")
        plt.savefig(filename)
        print(f"Saved summary plot to {filename}")
    plt.close('all')

def plot_time_series_results(all_metrics):
    """Plots the time-series line graphs."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    scheduler_names = list(all_metrics.keys())
    
    # Plot 1: Average Temperature Over Time
    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        metrics = all_metrics[name]
        plt.plot(metrics.time_steps, metrics.avg_temp_history, label=name)
    plt.xlabel("Simulation Time (ms)")
    plt.ylabel("Average Core Temperature (°C)")
    plt.title("Temperature Dynamics Over Time")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "timeseries_temperature.png"))
    print("Saved time-series plot to plots/timeseries_temperature.png")

    # Plot 2: CPU Utilization Over Time
    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        metrics = all_metrics[name]
        plt.plot(metrics.time_steps, metrics.cpu_util_history, label=name, alpha=0.8)
    plt.xlabel("Simulation Time (ms)")
    plt.ylabel("Interval CPU Utilization (%)")
    plt.title("CPU Utilization Dynamics Over Time")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "timeseries_cpu_utilization.png"))
    print("Saved time-series plot to plots/timeseries_cpu_utilization.png")

    # Plot 3: Active Threats Over Time
    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        metrics = all_metrics[name]
        plt.plot(metrics.time_steps, metrics.active_threats_history, label=name)
    plt.xlabel("Simulation Time (ms)")
    plt.ylabel("Number of Active Malicious Tasks")
    plt.title("Threat Landscape Over Time")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "timeseries_active_threats.png"))
    print("Saved time-series plot to plots/timeseries_active_threats.png")

    plt.show()