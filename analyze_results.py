# analyze_results.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

def load_all_results(base_dir='plots'):
    """Finds and loads all summary_results.csv files into a single DataFrame."""
    csv_files = glob.glob(os.path.join(base_dir, '**', 'summary_results.csv'), recursive=True)
    if not csv_files:
        print("No summary_results.csv files found. Did you run main.py first?")
        return None
    
    df_list = []
    for f in csv_files:
        parts = f.split(os.sep)
        exp_name = parts[-2]
        exp_parts = exp_name.split('_')
        params = {exp_parts[i]: exp_parts[i+1] for i in range(0, len(exp_parts), 2)}
        
        df = pd.read_csv(f)
        df['cores'] = int(params['cores'])
        df['load'] = params['load']
        df['threat'] = params['threat']
        df_list.append(df)
        
    return pd.concat(df_list, ignore_index=True)

def generate_final_paper_figures(df, output_dir='plots_final'):
    """
    Generates only the specific, curated plots needed for the research paper.
    """
    if df is None: return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Define the specific plots we want to generate ---
    plots_to_generate = [
        {'metric': 'Thermal Hotspots', 'load': 'heavy', 'threat': 'high', 'filename': 'Figure_1_Thermal_HighStress.png'},
        {'metric': 'Thermal Hotspots', 'load': 'low', 'threat': 'low', 'filename': 'Figure_2_Thermal_LowStress.png'},
        {'metric': 'Avg Isolation Time (ms)', 'load': 'heavy', 'threat': 'high', 'filename': 'Figure_3a_Security_HighStress.png'},
        {'metric': 'CPU Utilization (%)', 'load': 'heavy', 'threat': 'high', 'filename': 'Figure_3b_Performance_HighStress.png'}
    ]

    for plot_info in plots_to_generate:
        metric = plot_info['metric']
        load = plot_info['load']
        threat = plot_info['threat']
        
        print(f"--- Generating Figure: {plot_info['filename']} ---")
        
        analysis_df = df[(df['load'] == load) & (df['threat'] == threat)]

        if analysis_df.empty:
            print(f"  > Warning: No data found for this scenario. Skipping.")
            continue

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=analysis_df, x='cores', y=metric, hue='scheduler', marker='o', errorbar=None)
        
        plt.title(f'Scalability: {metric} vs. Number of Cores\n(Load: {load.capitalize()}, Threat: {threat.capitalize()})')
        plt.xlabel('Number of Cores')
        plt.ylabel(f'Average {metric}')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks([8, 16, 32])
        plt.tight_layout()
        
        filename = os.path.join(output_dir, plot_info['filename'])
        plt.savefig(filename)
        plt.close()

def main():
    print("--- Loading results to generate final paper figures... ---")
    full_df = load_all_results()
    generate_final_paper_figures(full_df)
    print(f"\n--- Final paper figures saved to 'plots_final' directory. ---")
    print("This is the recommended set of figures to use in your paper.")

if __name__ == "__main__":
    main()