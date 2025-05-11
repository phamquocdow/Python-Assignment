import pandas as pd
import numpy as np
import os  # Thêm thư viện quản lý thư mục

def age_to_days(age_str):
    try:
        years, days = map(int, age_str.split('-'))
        return years * 365 + days
    except:
        return np.nan

def days_to_age(days_total):
    years = days_total // 365
    days = days_total % 365
    return f"{int(years)}-{int(days)}"


os.makedirs("II", exist_ok=True)

df = pd.read_csv('I/results.csv')  
df_cleaned = df.copy()

stats = [col for col in df_cleaned.columns if col not in ['Player', 'Nation', 'Team', 'Position']]

# Xử lý dữ liệu Age và Minutes
df_cleaned['Age'] = df_cleaned['Age'].apply(age_to_days)
df_cleaned["Minutes"] = df_cleaned["Minutes"].str.replace(",", "")
df_cleaned.replace('N/a', pd.NA, inplace=True)


for stat in stats:
    df_cleaned[stat] = pd.to_numeric(df_cleaned[stat], errors='coerce')

with open('II/top3.txt', 'w', encoding='utf-8', errors='ignore') as f:  
    for stat in stats:
        f.write(f"--- {stat} ---\n")
        valid = df_cleaned.dropna(subset=[stat])
        
        top3 = valid.nlargest(3, stat)
        bot3 = valid.nsmallest(3, stat)

        
        if stat == 'Age':
            for df_ in (top3, bot3):
                df_['Age'] = df_['Age'].apply(days_to_age)
        
        display_cols = ['Player','Nation','Team','Position', stat]

        f.write("Top 3:\n")
        f.write(top3[display_cols].to_string(
            index=False,          
            justify='left',     
            col_space=15
        ))
        f.write("\n\nBottom 3:\n")
        f.write(bot3[display_cols].to_string(
            index=False,          
            justify='left',    
            col_space=15
        ))
        f.write("\n\n")
