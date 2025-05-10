import pandas as pd
import os
def Age_to_year(age_str):
    try:
        years, days = map(float, str(age_str).split('-'))
        return years + (days / 365)
    except:
        return pd.NA
def print_leader(df, stat):
    if stat not in df.columns:
        print(f"- WARNING: Column '{stat}' not found in data")
        return
    best_value = df[stat].max()
    
    leaders = df[df[stat] == best_value]['Team'].unique().tolist()
    print(f"- {stat.upper()}: {', '.join(leaders)} ({best_value})")

df = pd.read_csv('I/results.csv')
df_cleaned = df.copy()


df_cleaned.replace('N/a', pd.NA, inplace=True)
df_cleaned['Age'] = df_cleaned['Age'].apply(Age_to_year)

if 'Minutes' in df_cleaned.columns:
    df_cleaned['Minutes'] = pd.to_numeric(
        df_cleaned['Minutes'].astype(str).str.replace(",", ""), 
        errors='coerce'
    )

stats = [col for col in df_cleaned.columns 
        if col not in ['Player', 'Nation', 'Team', 'Position']]
df_cleaned[stats] = df_cleaned[stats].apply(pd.to_numeric, errors='coerce')


print("\nLEADING TEAMS FOR EACH STATISTIC:")
for stat in stats:
    print_leader(df_cleaned, stat)
df_2 = pd.read_csv('II/results2.csv')
if df_2.loc[0, 'Team'] == 'All':
    df_2 = df_2.iloc[1:]

mean_cols = [col for col in df_2.columns if col.startswith('Mean')]

lower_is_better = [
    'Mean of Goals Against per 90 minutes',
    'Mean of Red Cards',
    'Mean of Yellow Cards',
    'Mean of Offsides',
    'Mean of Miscontrols',
    'Mean of Dispossessed',
    'Mean of Fouls Committed',
    'Mean of Offsides',
    'Mean of Takeled During Take-Ons Percentage',
    'Mean of Arials Lost',
]

# Dictionary to count points for each team
team_points = {}

for col in mean_cols:
    df_2[col] = pd.to_numeric(df_2[col], errors='coerce')
    df_col = df_2[col].dropna()  # Changed df to df_2 here
    if col in lower_is_better:
        idx = df_2[col].idxmin()
    else:
        idx = df_2[col].idxmax()
    team = df_2.loc[idx, 'Team']
    team_points[team] = team_points.get(team, 0) + 1
df_2.replace('N/a', pd.NA, inplace=True)

# Find the team with the most points
try:
    best_team = max(team_points, key=team_points.get)
except ValueError as e:
    print (f"\nERROR: {str(e)}")    
print("Team points:", team_points)
print(f"\nThe best performing team is: {best_team}")