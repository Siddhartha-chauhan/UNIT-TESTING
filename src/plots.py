# src/plots.py
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Save directory
PLOT_PRINTS_DIR = Path(__file__).parent.parent / "plot_prints"
PLOT_PRINTS_DIR.mkdir(exist_ok=True)

# Import functions
try:
    from .main import (
        get_wins_per_team_per_year,
        get_extra_runs_2016,
        get_top_economical_bowlers_2015
    )
except ImportError:
    from main import (
        get_wins_per_team_per_year,
        get_extra_runs_2016,
        get_top_economical_bowlers_2015
    )

def _save_fig(fig, filename):
    path = PLOT_PRINTS_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Saved: {path}")

def plot_wins_stacked(matches: pd.DataFrame, show=True, save=True):
    data = get_wins_per_team_per_year(matches)
    df = pd.DataFrame(data).fillna(0).T

    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Matches Won by Teams Over Years (Stacked)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Wins')
    ax.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    if save:
        _save_fig(fig, "wins_stacked.png")
    if show:
        plt.show()
    else:
        plt.close(fig)

def plot_extra_runs_2016(matches: pd.DataFrame, deliveries: pd.DataFrame, show=True, save=True):
    data = get_extra_runs_2016(matches, deliveries)
    teams = list(data.keys())
    extras = list(data.values())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(teams, extras, color='skyblue')
    ax.set_title('Extra Runs Conceded per Team in 2016')
    ax.set_ylabel('Extra Runs')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    if save:
        _save_fig(fig, "extra_runs_2016.png")
    if show:
        plt.show()
    else:
        plt.close(fig)

def plot_top_economical_bowlers_2015(matches: pd.DataFrame, deliveries: pd.DataFrame, top_n=3, show=True, save=True):
    bowlers = get_top_economical_bowlers_2015(matches, deliveries, top_n)
    names, rates = zip(*bowlers)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, rates, color='salmon')
    ax.set_title(f'Top {top_n} Economical Bowlers in 2015')
    ax.set_ylabel('Economy Rate (runs/over)')
    plt.tight_layout()

    if save:
        _save_fig(fig, f"top_economical_bowlers_2015_top{top_n}.png")
    if show:
        plt.show()
    else:
        plt.close(fig)