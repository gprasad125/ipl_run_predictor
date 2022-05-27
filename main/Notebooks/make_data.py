import pandas as pd
import numpy as np

def make_data(bat, bowl, full):
    
    bad = {"-":0}
    bat.replace(bad, inplace = True)
    bowl.replace(bad, inplace = True)
    
    bat["strikeRate"] = bat["strikeRate"].astype(float)
    bowl["economyRate"] = bowl["economyRate"].astype(float)
    
    bat_stats = ["runs", "ballsFaced", "fours", "sixes", "strikeRate"]
    avg_bat_stats = bat.groupby("fullName")[bat_stats].mean().reset_index()
    total_bat_stats = bat.groupby("fullName")[bat_stats].sum().reset_index()

    overall_batsman = pd.merge(avg_bat_stats, total_bat_stats, on = "fullName")
    cols = ["batsman_name", "avg_runs", "avg_bf", "avg_fours", "avg_sixes", "avg_sr", "total_runs", "total_bf", "total_fours", 
            "total_sixes", "total_sr"]
    overall_batsman.columns = cols
    useless = ["total_sr"]
    overall_batsman = overall_batsman.drop(columns = useless)
    
    bowl_stats = ["overs", "maidens", "conceded", "wickets", "economyRate", "dots", "foursConceded", "sixesConceded", "wides", 
                  "noballs"]
    avg_bowl_stats = bowl.groupby("fullName")[bowl_stats].mean().reset_index()
    total_bowl_stats = bowl.groupby("fullName")[bowl_stats].sum().reset_index()

    overall_bowler = pd.merge(avg_bowl_stats, total_bowl_stats, on = "fullName")
    cols = ["bowler_name", "avg_overs", "avg_maidens", "avg_conceded", "avg_wickets", "avg_er", "avg_dots", "avg_fours_c", "avg_sixes_c", "avg_wides", "avg_noballs",
            "total_overs", "total_maidens", "total_conceded", "total_wickets", "total_er", "total_dots", "total_fours_c", "total_sixes_c", "total_wides", "total_noballs"]
    overall_bowler.columns = cols
    useless = ["avg_overs", "total_er"]
    overall_bowler = overall_bowler.drop(columns = useless)
    
    important = ["season", "match_id", "batsman1_name", "bowler1_name", "home_team", "away_team", "current_innings", "ball", 
                 "runs"]
    full = full.loc[(full["isWide"] != True) & (full["isNoball"] != True)]
    full = full[important]

    index_cols = ["season", "match_id", "batsman1_name", "bowler1_name", "home_team", "away_team", "current_innings"]
    runs_df = pd.pivot_table(full, index = index_cols, values = ["runs"], aggfunc = "sum")
    balls_df = pd.pivot_table(full, index = index_cols, values = ["ball"], aggfunc = len)
    
    versus_df = pd.concat([runs_df, balls_df], axis = 1).reset_index()
    
    areas = bat[["match_id", "venue", "city", "country"]]
    versus_df = pd.merge(versus_df, areas, on = "match_id")
    
    df = pd.merge(versus_df, overall_batsman, left_on = "batsman1_name", right_on = "batsman_name")
    df = pd.merge(df, overall_bowler, left_on = "bowler1_name", right_on = "bowler_name")
    df = df.drop_duplicates()
    
    return df
