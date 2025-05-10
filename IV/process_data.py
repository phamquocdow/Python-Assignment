import pandas as pd
import numpy as np
def main():
    # Read the CSV files
    results_df = pd.read_csv('results.csv')
    transfer_df = pd.read_csv('result_final.csv')
    
    # Merge the dataframes on 'Player', 'Nation', and 'Team'
    merged_df = pd.merge(
        results_df, 
        transfer_df[['Player', 'Nation', 'Team', 'Transfer Fee']], 
        on=['Player', 'Nation', 'Team'], 
        how='left'
    )
    
    # Filter to keep only players with transfer fees
    filtered_df = merged_df.dropna(subset=['Transfer Fee'])
    
    # Save the result to a new CSV file
    filtered_df.to_csv('merged_players_with_fees.csv', index=False)
    
    print(f"Merged data saved to merged_players_with_fees.csv")
    print(f"Total players in original data: {len(results_df)}")
    print(f"Players with transfer fees: {len(filtered_df)}")


    # Load the data
    df = pd.read_csv('merged_players_with_fees.csv')

    # Print basic info
    print("DataFrame info:")
    print(df.info())

    # Check Transfer Fee column
    print("\nTransfer Fee column (first 10 rows):")
    print(df['Transfer Fee'].head(10))

    # Try converting Transfer Fee to numeric
    print("\nConverting Transfer Fee to numeric:")
    try:
        df['Transfer Fee'] = df['Transfer Fee'].str.replace('€', '').str.replace('M', '').astype(float)
        print("Conversion successful")
        print(df['Transfer Fee'].head(10))
    except Exception as e:
        print(f"Error: {e}")

    # Check shape after conversion
    print(f"\nDataFrame shape: {df.shape}")

    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"\nNumber of numeric columns: {len(numeric_cols)}")
    print("First 10 numeric columns:", numeric_cols[:10])

    # Check if Transfer Fee is in numeric columns
    print(f"\nIs 'Transfer Fee' in numeric columns? {'Transfer Fee' in numeric_cols}")

    # Create X and y
    X = df[numeric_cols].drop(['Transfer Fee'], axis=1, errors='ignore')
    y = df['Transfer Fee']

    print(f"\nX shape: {X.shape}")
    print(f"y shape: {y.shape}")
    print(f"y type: {type(y)}")
    print(f"y first 5 values: {y.head()}")

    # Check if y is a Series or DataFrame
    print(f"\ny is Series: {isinstance(y, pd.Series)}")
    print(f"y is DataFrame: {isinstance(y, pd.DataFrame)}")

    if isinstance(y, pd.DataFrame):
        print(f"y columns: {y.columns}") 

if __name__ == "__main__":
    main()
