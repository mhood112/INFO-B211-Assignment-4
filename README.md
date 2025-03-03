# INFO-B211-Assignment-4

This program analyzes NBA players statistics from a CSV file provided, that contains player stats. by the season. The overrall goal is to identify the player who has played the most seasons and perform various statistical analyses on their performance. 

## File Structure
  - import - pandas as pd
  - import - os
  - import - numpy as np
  - import - scipy.stats as stats
  - import - matplotlib.pyplot as plt
  - import - quad from scipy.integrate
  - input - players_stats_by_season_full_details.csv

## Class design and Implementation

  This program does not use any classes, but it will rely on two main user defined fucnctions.

### Importing the Necessary Libraries
  - pandas - used for data manipulation
  - os - provides a way for using operating system dependent functions
  - NumPy - used for numerical operations
  - scipy.stats - used for statistical functions
  - matplotlib.pyplot - used for plotting graphs
  - scipy.integrate.quad - used for integration

### Functions
  - #### load_dataset(file_path)
      - **Purpose**
          - Loads the csv into a pandas DataFrame
      - **Parameters**
          - file_path - path to the CSV file
      - **Returns**
          - df(DataFrame) - returns the loaded DataFrame or none if an error arises

  - #### main()
      - **Purpose**
          - This is the main function that will perform all of the data analysis.

    ### Explanation of Each Section
      - ##### Main
        - This is where the base path and CSV file is defined. Then they are both combine to get the full fiel path. Then the dataset is loaded in as a dataframe.

      - ##### Data Filtering & Prep
        - This is where the data is going to be filtered. It starts by filtering for the NBA regular season. This it will group the data by the player and keep count of the number of seasons that each player has played. Then it will find the player with the most seasons played.
          
      - ##### Data Cleaning & Transformation
        - The columns are then converted in to numerical values for error handling just incase there are any missing values, it will deal with those by putting in 0s.

      - ##### Handling Missing Seasons & Interpolation
        - This block identifies any missing seasons and interpolates the missing values.

      - ##### Linear Regression & Integration
        - This block is where the linear regression and the integration will happen. The line of best fit is created here. The over the played seasons is integrated. And the averages for the accuracies are calculated.

      - ##### Plotting
        - This is where the data is plotted and displayed.

      - ##### Stats. Metric Calculation
        - This is where the mean, variance, skewness, and kurtosis for FGM and FGA is calculated.

      - ##### T-Tests
        - This is where the T-Tests are performed for FGM and FGA.

## Limitations
  - This program assums that there is a linear relationship between the seasons and three-point accuracy.
  - Missing values are filled with 0, but that might not be the best for this data.

  ## Conclusion 
      The mean for the FGA is higher than the mean for the FGM meaning that more field goals are attemped than made. The variance of FGA is higher than the FGM, meaning that the attempts are more spread out compared to the made field goals. FGA has a higher skewness than FGM, meaning that the distribution of attempts is more skewed. The kurtosis values for FGM is higher than FGA, so this means that the distribution of attempts has heavier tails. 
    
