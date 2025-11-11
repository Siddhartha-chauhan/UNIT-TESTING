# src/main.py
import pandas as pd

def load_data(matches_path: str, deliveries_path: str):
    """Load matches and deliveries CSV files."""
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries

def get_wins_per_team_per_year(matches: pd.DataFrame) -> dict:
    """Return {year: {team: wins}}."""
    wins = matches.groupby(['season', 'winner']).size()
    result = {}
    for (season, winner), count in wins.items():
        result.setdefault(season, {})[winner] = count
    return result

def get_extra_runs_2016(matches: pd.DataFrame, deliveries: pd.DataFrame) -> dict:
    """Extra runs conceded per bowling team in 2016."""
    match_ids = matches[matches['season'] == 2016]['id'].tolist()
    del_2016 = deliveries[deliveries['match_id'].isin(match_ids)]
    return del_2016.groupby('bowling_team')['extra_runs'].sum().to_dict()

def get_top_economical_bowlers_2015(
    matches: pd.DataFrame, 
    deliveries: pd.DataFrame, 
    top_n: int = 3
) -> list:
    """Return top N economical bowlers in 2015 as [(bowler, rate)]."""
    match_ids = matches[matches['season'] == 2015]['id'].tolist()
    del_2015 = deliveries[deliveries['match_id'].isin(match_ids)].copy()

    del_2015['runs_conceded'] = (
        del_2015['batsman_runs'] + del_2015['wide_runs'] + del_2015['noball_runs']
    )
    total_runs = del_2015.groupby('bowler')['runs_conceded'].sum()

    legal = del_2015[(del_2015['wide_runs'] == 0) & (del_2015['noball_runs'] == 0)]
    balls = legal.groupby('bowler').size()
    overs = balls / 6.0

    economy = (total_runs / overs).dropna()
    top = economy.sort_values().head(top_n)
    return [(bowler, round(rate, 2)) for bowler, rate in top.items()]