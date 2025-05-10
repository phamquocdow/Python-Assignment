import pandas as pd
import os
def Age_to_year(age_str):
    years, days = map(float, age_str.split('-'))
    days = float(days / 365)
    years = years + days
    return years
df = pd.read_csv('I/results.csv')
df_cleaned = df.copy()
stats = [col for col in df_cleaned.columns 
        if col not in ['Player', 'Nation', 'Team', 'Position']]
df_cleaned['Age'] = df_cleaned['Age'].apply(Age_to_year)
df_cleaned["Minutes"] = df_cleaned["Minutes"].str.replace(",", "")
df_cleaned.replace('N/a', pd.NA, inplace=True)
for stat in stats:
    df_cleaned[stat] = pd.to_numeric(df_cleaned[stat], errors='coerce')
results = []
all_stats = {'Team': 'All'}
for attr in stats:
    all_stats[f'Median of {attr}'] = df_cleaned[attr].median()
    all_stats[f'Mean of {attr}'] = df_cleaned[attr].mean()
    all_stats[f'Std of {attr}'] = df_cleaned[attr].std()
results.append(all_stats)
for team, team_df in df_cleaned.groupby('Team'):
    team_stats = {'Team': team}
    for attr in stats:
        team_stats[f'Median of {attr}'] = team_df[attr].median()
        team_stats[f'Mean of {attr}'] = team_df[attr].mean()
        team_stats[f'Std of {attr}'] = team_df[attr].std()
    results.append(team_stats)
results_df = pd.DataFrame(results)
columns_order = ['Team']
for attr in stats:
    columns_order.extend([f'Median of {attr}', f'Mean of {attr}', f'Std of {attr}'])
results_df = results_df[columns_order]
results_df.to_csv('II/results2.csv', na_rep='N/a', index=True)
