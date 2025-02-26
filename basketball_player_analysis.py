import pandas as pd
import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.integrate import quad

def load_dataset(file_path):
    # This functions loads the csv into a dataframe
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        # Handle the case where the file is empty
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        # Handle the case where the file could not be parsed
        print("Error: The file could not be parsed.")
        return None

def main():
    
# This is the main function that will be called when the script is run
    
    # Define the base path (you can change this to any directory you want)
    base_path = os.path.expanduser('~/Desktop/assignment 4')
    file_name = 'players_stats_by_season_full_details.csv'
    file_path = os.path.join(base_path, file_name)

    # Load the dataset
    df = load_dataset(file_path)
    if df is None:
        # Exit the program if the dataset could not be loaded
        return

    """
    #Check for missing values in the dataset
    print("Missing values in the dataset:")
    print(df.isnull().sum())
    """
    
    
# Data Filitering And Preparation for use. 
    
    # Filter the dataset for NBA regular season data
    nba_regular_season_df = df[(df['League'] == 'NBA') & (df['Stage'] == 'Regular_Season')]

    # Group by player and count the number of unique seasons each player has played
    player_season_counts = nba_regular_season_df.groupby('Player')['Season'].nunique()

    # Find the player with the most regular seasons
    most_regular_seasons_player = player_season_counts.idxmax() # Get the player with the most regular seasons
    most_regular_seasons_count = player_season_counts.max() # Get the maximum count of regular seasons

    print(f"The player who has played the most regular seasons is {most_regular_seasons_player} with {most_regular_seasons_count} seasons.")

    # Filter the dataset for the player with the most regular seasons & makes a copy
    player_data = nba_regular_season_df[nba_regular_season_df['Player'] == most_regular_seasons_player].copy()


# Data Cleaning and Tranformation
    
    # Convert numerical columns to numeric data types
    player_data['3PM'] = pd.to_numeric(player_data['3PM'], errors='coerce') 
    player_data['3PA'] = pd.to_numeric(player_data['3PA'], errors='coerce')
    player_data['FGM'] = pd.to_numeric(player_data['FGM'], errors='coerce')
    player_data['FGA'] = pd.to_numeric(player_data['FGA'], errors='coerce')

    """
    # Check for missing values in the player's data
    print(f"Missing values in {most_regular_seasons_player}'s data:")
    print(player_data.isnull().sum())
    """
    
    # Fill missing values, nan,  with 0 for numerical columns
    player_data.fillna(0, inplace=True)

    # Calculate three-point accuracy for each season
    player_data['3P_accuracy'] = player_data['3PM'] / player_data['3PA'] # Calculate the accuracy
    player_data['3P_accuracy'] = player_data['3P_accuracy'].replace([np.inf, -np.inf], np.nan) # Replace infinite values with NaN
    player_data['3P_accuracy'] = player_data['3P_accuracy'].fillna(0) # Fill NaN values with 0


# Handling Missing Values and Interpolation

    # Add missing seasons with NaN values for three-point accuracy
    missing_seasons = ['2002 - 2003', '2015 - 2016'] # Define the missing seasons
    for season in missing_seasons:
        # Check if the season is missing
        if season not in player_data['Season'].values:
            # Add a missing row with NaN values for three-point accuracy
            missing_row = pd.DataFrame({'Season': [season], '3P_accuracy': [np.nan]}) # Create a DataFrame with the missing row
            player_data = pd.concat([player_data, missing_row], ignore_index=True) # Concatenate the missing row to the player's data

    # Sort by season and interpolate missing values
    player_data = player_data.sort_values(by='Season') # Sort the data by season
    player_data['3P_accuracy'] = player_data['3P_accuracy'].interpolate() # Interpolate missing values

    """
    # Check for missing values after interpolation
    print(f"Missing values in {most_regular_seasons_player}'s data after interpolation:")
    print(player_data.isnull().sum())
    """
    
    
# Perform linear regression & Integration

    try: 
        years = np.arange(len(player_data)) # Create an array of years
        three_point_accuracy = player_data['3P_accuracy'].values # Get the three-point accuracy values
        slope, intercept, r_value, p_value, std_err = stats.linregress(years, three_point_accuracy) # Perform linear regression
    except ValueError as e:
        # Handle the case where linear regression fails
        print(f"Error performing linear regression: {e}")
        return

    # Create a line of best fit
    line_of_best_fit = slope * years + intercept

    # Integrate the fit line over the played seasons
    try:
        integral, _ = quad(lambda x: slope * x + intercept, 0, len(years) - 1) # Integrate the line of best fit
        average_fit_accuracy = integral / (len(years) - 1) # Calculate the average accuracy
    except Exception as e:
        # Handle the case where integration fails
        print(f"Error performing integration: {e}")
        return

    # Calculate the actual average three-point accuracy
    actual_average_accuracy = player_data['3P_accuracy'].mean()

    # Compare the two values
    print(f"\nThree-Point Accuracy Comparison for {most_regular_seasons_player}:")
    print(f"Average from the fit line: {average_fit_accuracy:.4f}")
    print(f"Actual average: {actual_average_accuracy:.4f}")


# Plotting the Data and Line of Best Fit

    plt.figure(figsize=(10, 6)) # Set the figure size
    plt.plot(player_data['Season'], three_point_accuracy, 'o', label='Three-Point Accuracy') # Plot the three-point accuracy
    plt.plot(player_data['Season'], line_of_best_fit, 'r', label='Line of Best Fit') # Plot the line of best fit
    plt.xlabel('Season') # Set the x-axis label
    plt.ylabel('Three-Point Accuracy') # Set the y-axis label
    plt.title(f'Three-Point Accuracy Over Seasons for {most_regular_seasons_player}') # Set the title
    plt.legend() # Show the legend
    plt.xticks(rotation=45) # Rotate the x-axis labels
    plt.tight_layout() # Adjust the layout
    plt.show() # Show the plot


# Calculate statistical metrics for FGM and FGA

    try:
        fgm_mean = player_data['FGM'].mean() # Calculate the mean for FGM
        fgm_variance = player_data['FGM'].var() # Calculate the variance for FGM
        fgm_skew = stats.skew(player_data['FGM'].dropna()) # Calculate the skewness for FGM
        fgm_kurtosis = stats.kurtosis(player_data['FGM'].dropna()) # Calculate the kurtosis for FGM 

        fga_mean = player_data['FGA'].mean() # Calculate the mean for FGA
        fga_variance = player_data['FGA'].var() # Calculate the variance for FGA
        fga_skew = stats.skew(player_data['FGA'].dropna()) # Calculate the skewness for FGA
        fga_kurtosis = stats.kurtosis(player_data['FGA'].dropna()) # Calculate the kurtosis for FGA
    except KeyError as e:
        # Handle the case where the columns are not found
        print(f"Error calculating statistical metrics: {e}")
        return

    # Print the statistical metrics
    print(f"\nStatistical Metrics for {most_regular_seasons_player}:")
    print(f"{'Metric':<15} {'FGM':<15} {'FGA':<15}")
    print(f"{'Mean':<15} {fgm_mean:<15.4f} {fga_mean:<15.4f}")
    print(f"{'Variance':<15} {fgm_variance:<15.4f} {fga_variance:<15.4f}")
    print(f"{'Skew':<15} {fgm_skew:<15.4f} {fga_skew:<15.4f}")
    print(f"{'Kurtosis':<15} {fgm_kurtosis:<15.4f} {fga_kurtosis:<15.4f}")

    # Compare the statistics from FGM to FGA
    print(f"\nComparison of FGM and FGA statistics:")
    print(f"{'Metric':<15} {'Difference':<15}")
    print(f"{'Mean':<15} {fga_mean - fgm_mean:<15.4f}")
    print(f"{'Variance':<15} {fga_variance - fgm_variance:<15.4f}")
    print(f"{'Skew':<15} {fga_skew - fgm_skew:<15.4f}")
    print(f"{'Kurtosis':<15} {fga_kurtosis - fgm_kurtosis:<15.4f}")

# T-Test Analysis

    # Perform a paired t-test on FGM and FGA
    try:
        # Perform a paired t-test on FGM and FGA
        t_stat_paired, p_value_paired = stats.ttest_rel(player_data['FGM'].dropna(), player_data['FGA'].dropna())
    except ValueError as e:
        # Handle the case where the t-test fails
        print(f"Error performing paired t-test: {e}")
        return

    # Perform individual t-tests on FGM and FGA
    try:
        t_stat_fgm, p_value_fgm = stats.ttest_1samp(player_data['FGM'].dropna(), 0) 
        t_stat_fga, p_value_fga = stats.ttest_1samp(player_data['FGA'].dropna(), 0)
    except ValueError as e:
        # Handle the case where the t-tests fail
        print(f"Error performing individual t-tests: {e}")
        return

    # Print the t-test results
    print(f"\nPaired t-test results for FGM and FGA:")
    print(f"t-statistic: {t_stat_paired:.4f}, p-value: {p_value_paired:.4f}")

    print(f"\nIndividual t-test results for FGM:")
    print(f"t-statistic: {t_stat_fgm:.4f}, p-value: {p_value_fgm:.4f}")

    print(f"\nIndividual t-test results for FGA:")
    print(f"t-statistic: {t_stat_fga:.4f}, p-value: {p_value_fga:.4f}")

    # Compare the results of the individual t-tests to the paired t-test
    print(f"\nComparison of individual t-tests to paired t-test:")
    print(f"{'Test':<25} {'p-value':<15}")
    print(f"{'Paired t-test':<25} {p_value_paired:<15.4f}")
    print(f"{'Individual t-test for FGM':<25} {p_value_fgm:<15.4f}")
    print(f"{'Individual t-test for FGA':<25} {p_value_fga:<15.4f}")

if __name__ == "__main__":
    # Call the main function
    main()
