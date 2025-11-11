# run_plots.py
from src.main import load_data
from src.plots import (
    plot_wins_stacked,
    plot_extra_runs_2016,
    plot_top_economical_bowlers_2015
)

if __name__ == "__main__":
    # Load mock data
    matches, deliveries = load_data('data/mock_matches.csv', 'data/mock_deliveries.csv')

    # Generate all 3 plots
    print("Generating plots...")
    plot_wins_stacked(matches)
    plot_extra_runs_2016(matches, deliveries)
    plot_top_economical_bowlers_2015(matches, deliveries, top_n=3)
    print("All plots displayed!")