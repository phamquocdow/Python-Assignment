import requests
import bs4
import time
import pandas as pd
import os
import random   
table_ids = ['div_stats_standard_9', 'div_stats_keeper_9', 'div_stats_shooting_9', 
             'div_stats_passing_9', 'div_stats_gca_9', 'div_stats_defense_9', 
             'div_stats_possession_9', 'div_stats_misc_9']

data_stats = [
    [
        'nationality',
        'position',
        'age', 
        'games',
        'games_starts',
        'minutes',
        'goals',
        'assists',
        'cards_yellow',
        'cards_red',
        'xg',
        'xg_assist',
        'progressive_carries',
        'progressive_passes',
        'progressive_passes_received',
        'goals_per90',
        'assists_per90',
        'xg_per90',
        'xg_assist_per90'
    ],
    [
        'gk_goals_against_per90',
        'gk_save_pct',
        'gk_clean_sheets_pct',
        'gk_pens_save_pct'
    ], 
    [
        'shots_on_target_pct',
        'shots_on_target_per90',
        'goals_per_shot',
        'average_shot_distance'
    ],
    [
        'passes_completed',
        'passes_pct',
        'passes_total_distance',
        'passes_pct_short',
        'passes_pct_medium',
        'passes_pct_long',
        'assisted_shots',
        'passes_into_final_third',
        'passes_into_penalty_area',
        'crosses_into_penalty_area',
        'progressive_passes'
    ],
    [
        'sca',
        'sca_per90',
        'gca',
        'gca_per90'
    ],
    [
        'tackles',
        'tackles_won',
        'challenges',
        'challenges_lost',
        'blocks',
        'blocked_shots',
        'blocked_passes',
        'interceptions'
    ],
    [
        'touches',
        'touches_def_pen_area',
        'touches_def_3rd',
        'touches_mid_3rd',
        'touches_att_3rd',
        'touches_att_pen_area',
        'take_ons',
        'take_ons_won_pct',
        'take_ons_tackled_pct',
        'carries',
        'carries_progressive_distance',
        'progressive_carries',
        'carries_into_final_third',
        'carries_into_penalty_area',
        'miscontrols',
        'dispossessed',
        'passes_received',
        'progressive_passes_received'
    ],
    [
        'fouls',
        'fouled',
        'offsides',
        'crosses',
        'ball_recoveries',
        'aerials_won',
        'aerials_lost',
        'aerials_won_pct'
    ]
]



def get_infor_of_each_team():
    url = 'https://fbref.com/en/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', {'id': "all_results2024-202591"})
    tds = div.find_all('td', {'data-stat': "team"})

    link_and_name_of_team = []
    for td in tds:
        a = td.find('a')
        if a and 'href' in a.attrs: 
            link = "https://fbref.com" + a['href']  
            team_name = td.get_text()
            link_and_name_of_team.append((link, team_name))  
            
    return link_and_name_of_team

def get_infor_of_each_player(url, team_name):
    for attempt in range(5):
        time.sleep(random.uniform(1, 6))
        response = requests.get(url)
        if response.status_code == 429:
            print("Rate limited. Waiting before retrying...")
            time.sleep(10 * (attempt + 1))
            continue
        break
    else:
        print("Failed due to repeated rate limiting.")
        return []
    
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    table = soup.find('div', id='div_stats_standard_9')
    if not table:
        return []
    tbody = table.find('tbody')
    players = {}
    for tr in tbody.find_all('tr'):
        th = tr.find('th')
        name = th.get_text()
        td = tr.find('td', {'data-stat': 'minutes_90s'})
        minutes_90s = float('0' + td.get_text()) if td else 0
        if minutes_90s > 1:
            players[name] = [name]
        
    for table_id, dstats in zip(table_ids, data_stats):
        visited = set()
        table = soup.find('div', id=table_id)
        if not table:
            continue
            
        tbody = table.find('tbody')
        if not tbody:
            continue
            
        for tr in tbody.find_all('tr'):
            th = tr.find('th')
            name = th.get_text()
            if name not in players:
                continue
            
            visited.add(name)    
            for dstat in dstats:
                if dstat == 'nationality':
                    td = tr.find('td', {'data-stat': dstat})
                    if td:
                        if td.find('a'):
                            nation = td.find('a').get_text()
                            na1, na2 = nation.split()
                            nation = na2
                            del na1
                        else:
                            nation = 'N/a'
                        players[name].append(nation)
                        players[name].append(team_name)
                else:
                    td = tr.find('td', {'data-stat': dstat})
                    if td.get_text() == '':
                        value = 'N/a'
                    else:
                        value = td.get_text()
                    players[name].append(value)       
                
        for name in players: 
            if name not in visited:  
                players[name].extend(['N/a'] * len(dstats))
                
    return list(players.values())
def main():
    teams = get_infor_of_each_team()
    all_players = []
    for url, team_name in teams:
        print(f"Processing team: {team_name}")
        players = get_infor_of_each_player(url, team_name)
        all_players.extend(players)
        time.sleep(2) 
    columns = ['Player', 'Nation', 'Team', 'Position', 'Age', 'Matches played', 'Starts', 'Minutes','Goals',
                'Assists', 'Yellow Cards', 'Red Cards', 'Expected Goals',
                'Expedted Assist Goals', 'Progressive Carries in Progression', 'Progressive Passes in Progression',
                'Progressive Passes Received in Progression', 'Goals Scored per 90 minutes','Assists per 90 minutes',
                'Expected Goals per 90 minutes', 'Expected Assists Goals per 90 minutes',
                'Goals Against per 90 minutes', 'Save Percentage', 'Clean Sheets Percentage',
                'Penalty Save Percentage', 'Percentage of shots that are on target', 'Shots on target per 90 minutes',
                'Goals per shot', 'Average Shot Distance', 'Passes Completed', 'Pass Completion Percentage',
                'Total Passing Distance','Passes Completion Percentage (Short)','Passes Completion Percentage (Medium)',
                'Passes Completion Percentage (Long)', 'Key Passes', 'Passes into Final Third', 'Passes into Penalty Area',
                'Crosses into Penalty Area', 'Progressive Passes in Expected','Shot-Creating Actions','Shot-Creating Actions per 90 minutes',
                'Goal-Creating Actions','Goal-Creating Actions per 90 minutes','Tackles','Tackles Won','Dribblers Tackled',
                'Dribbles Challenged', 'Blocks', 'Shots Blocked','Passes Blocked', 'Interceptions','Touches','Touches(Defensive Penalty Area)','Touches(Defensive Third)',
                'Touches(Mid Third)', 'Touches(Attacking Third)','Touches(Attacking Penalty Area)','Take-Ons Attempted(Take-Ons)','Percentage of Take-Ons Completed Successfully',
                'Tackled During Take-Ons Percentage','Carries','Progressive Carrying Distance','Progressive Carries in Carries', 'Carries into Final Third','Carries into Penalty Area',
                'Miscontrols', 'Dispossessed','Passes Received', 'Progressive Passes Received in Receiving', 'Fouls Committed',
                'Fouls Drawn', 'Offsides', 'Crosses','Ball Recoveries','Aerials Won','Aerials Lost','Aerials Won Percentage']
    df = pd.DataFrame(all_players, columns=columns) 
    df = df.sort_values('Player')  
    folder_path = 'I'
    os.makedirs(folder_path, exist_ok=True)
    output_file = os.path.join(folder_path, 'results.csv')
    df.to_csv(output_file, index=False)
if __name__ == "__main__":
    main()