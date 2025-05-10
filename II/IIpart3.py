import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os  # Thêm thư viện xử lý thư mục

output_dir = "II/Histogram img"
os.makedirs(output_dir, exist_ok=True)

# Phần code xử lý data giữ nguyên
df = pd.read_csv('I/results.csv')
df_cleaned = df.copy()
df_cleaned.replace('N/a', pd.NA, inplace=True)

attack = ['Goals', 'Assists', 'Expected Goals']
defense = ['Tackles', 'Interceptions', 'Blocks']

for stat in attack + defense:
    df_cleaned[stat].fillna(0, inplace=True)
    df_cleaned[stat] = pd.to_numeric(df_cleaned[stat], errors='coerce')
plt.figure(figsize=(15, 5))
for i, stat in enumerate(attack, 1):
    plt.subplot(1, 3, i)
    plt.hist(df_cleaned[stat], bins=15, color='blue', edgecolor='black')
    plt.title(f'Distribution {stat}')
    plt.xlabel(stat)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(f"{output_dir}/All player_attack.png")
plt.figure(figsize=(15, 5))
for i, stat in enumerate(defense, 1):
    plt.subplot(1, 3, i)
    plt.hist(df_cleaned[stat], bins=15, color='red', edgecolor='black')
    plt.title(f'Distribution {stat}')
    plt.xlabel(stat)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(f"{output_dir}/All player_defense.png")
df_teams = df_cleaned.dropna(subset=['Team'])
teams = df_teams['Team'].unique()

for team in teams:
    team_data = df_teams[df_teams['Team'] == team]
    team_data[attack + defense] = team_data[attack + defense].fillna(0)
    plt.figure(figsize=(15, 6))
    plt.suptitle(f'TEAM PERFORMANCE ANALYSIS: {team.upper()}', 
                fontsize=16, 
                fontweight='bold', 
                y=1.05,
                color='navy')
    
    for i, stat in enumerate(attack, 1):
        plt.subplot(1, 3, i)
        n, bins, patches = plt.hist(team_data[stat], 
                                  bins=12, 
                                  color='royalblue', 
                                  edgecolor='white',
                                  alpha=0.8)
        plt.gca().text(0.95, 0.95, 
                      f'Total players: {len(team_data)}\n'
                      f'Medium: {team_data[stat].mean():.1f}\n'
                      f'Max: {team_data[stat].max()}',
                      transform=plt.gca().transAxes,
                      verticalalignment='top',
                      horizontalalignment='right',
                      bbox=dict(facecolor='white', alpha=0.8))
        
        plt.title(f'{stat}\n', fontsize=12, fontweight='bold')
        plt.xlabel('Value', fontsize=9)
        plt.ylabel('Number of players', fontsize=9)
        plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{team}_attack.png")  
    plt.close()  
    
    plt.figure(figsize=(15, 6))
    plt.suptitle(f'TEAM PERFORMANCE ANALYSIS: {team.upper()}', 
                fontsize=16, 
                fontweight='bold', 
                y=1.05,
                color='darkred')
    
    for i, stat in enumerate(defense, 1):
        plt.subplot(1, 3, i)
        n, bins, patches = plt.hist(team_data[stat], 
                                  bins=12, 
                                  color='firebrick', 
                                  edgecolor='white',
                                  alpha=0.8)
        plt.axvline(team_data[stat].mean(), 
                   color='gold', 
                   linestyle='dashed', 
                   linewidth=2,
                   label=f'Medium: {team_data[stat].mean():.1f}')
        plt.title(f'{stat}\n', fontsize=12, fontweight='bold')
        plt.xlabel('Value', fontsize=9)
        plt.ylabel('Number of players', fontsize=9)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)  
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{team}_defense.png")  
    plt.close() 