# utils/plotter.py
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

def plot_summary_boxplots(all_runs_summary, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    scheduler_names = list(all_runs_summary.keys())
    metric_keys = all_runs_summary[scheduler_names[0]][0].keys()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for metric in metric_keys:
        data_to_plot = [[run[metric] for run in all_runs_summary[name]] for name in scheduler_names]
        
        fig, ax = plt.subplots(figsize=(10, 7))
        bp = ax.boxplot(data_to_plot, patch_artist=True, labels=scheduler_names)
        
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            
        ax.set_ylabel(metric)
        ax.set_title(f"Performance Distribution: {metric} (over {len(data_to_plot[0])} runs)")
        ax.tick_params(axis='x', rotation=15)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        filename = os.path.join(output_dir, f"boxplot_{metric.replace(' ', '_').replace('%', 'perc').replace('/', 'per')}.png")
        plt.savefig(filename)
    plt.close('all')

def get_averaged_series(metrics_list, series_name):
    all_series = []
    for metrics in metrics_list:
        df = pd.DataFrame({
            'time': metrics.time_steps,
            series_name: getattr(metrics, f"{series_name}_history")
        }).set_index('time')
        all_series.append(df)
    
    combined_df = pd.concat(all_series, axis=1).interpolate(method='linear', limit_direction='both')
    mean_series = combined_df.mean(axis=1)
    return mean_series

def plot_time_series_results(all_runs_metrics, window_size, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    scheduler_names = list(all_runs_metrics.keys())
    
    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        mean_s = get_averaged_series(all_runs_metrics[name], 'avg_temp')
        mean_s_smooth = mean_s.rolling(window=window_size, min_periods=1).mean()
        plt.plot(mean_s_smooth.index, mean_s_smooth, label=name)
    plt.title("Average Temperature Dynamics Over Time")
    plt.ylabel("Average Core Temperature (°C)")
    plt.xlabel("Simulation Time (ms)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(output_dir, "avg_timeseries_temperature.png"))
    plt.close()

    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        mean_s = get_averaged_series(all_runs_metrics[name], 'cpu_util')
        mean_s_smooth = mean_s.rolling(window=window_size, min_periods=1).mean()
        plt.plot(mean_s_smooth.index, mean_s_smooth, label=name)
    plt.title("Average CPU Utilization Dynamics Over Time")
    plt.ylabel("Average Interval CPU Utilization (%)")
    plt.xlabel("Simulation Time (ms)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(output_dir, "avg_timeseries_cpu_utilization.png"))
    plt.close()
    
    plt.figure(figsize=(12, 7))
    for name in scheduler_names:
        mean_s = get_averaged_series(all_runs_metrics[name], 'active_threats')
        plt.plot(mean_s.index, mean_s, label=name)
    plt.title("Average Active Threats Over Time")
    plt.ylabel("Average Number of Active Malicious Tasks")
    plt.xlabel("Simulation Time (ms)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(output_dir, "avg_timeseries_active_threats.png"))
    plt.close()