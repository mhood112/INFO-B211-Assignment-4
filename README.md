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

      - 
    
      
    
