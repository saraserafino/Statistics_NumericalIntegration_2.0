# Statistics module

# Import the module created with pybind11
import moduleA

import numpy as np
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time # for the wrapper execution_time
import os
from typing import List, Optional, Union

# Decorator for computing the execution time
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        executionTime = time.time() - start
        return result, executionTime
    return wrapper

# Definitions of the statistics methods both in C++ and in Python

@execution_time
def test_calculateMean_cpp(StatOpInstance, data):
    return StatOpInstance.calculateMean(data)

@execution_time
def test_calculateMean_py(data):
    # If there's even a string
    if any(isinstance(value, str) for value in data):
        raise TypeError("Cannot calculate mean for a string.")
    # Otherwise compute it with NumPy
    return np.mean(data)

@execution_time
def test_calculateMedian_cpp(StatOpInstance, data):
    return StatOpInstance.calculateMedian(data)

@execution_time
def test_calculateMedian_py(data):
    if any(isinstance(value, str) for value in data):
        sorted_values = data.sort_values()
        median_index = len(sorted_values) // 2
        median = sorted_values.iloc[median_index]
    else: # If it's an int (like Age) return an int because it's cuter
        median = np.median(data)
    return median

@execution_time
def test_calculateStandardDeviation_cpp(StatOpInstance, data):
    return StatOpInstance.calculateStandardDeviation(data)

@execution_time
def test_calculateStandardDeviation_py(data):
    # If there's even a string
    if any(isinstance(value, str) for value in data):
        raise TypeError("Cannot calculate standard deviation for a string.")
    # Otherwise compute it with NumPy
    return np.std(data)

@execution_time
def test_calculateVariance_cpp(StatOpInstance, data):
    return StatOpInstance.calculateVariance(data)

@execution_time
def test_calculateVariance_py(data):
    # If there's even a string
    if any(isinstance(value, str) for value in data):
        raise TypeError("Cannot calculate variance for a string.")
    # Otherwise compute it with NumPy
    return np.var(data)

@execution_time
def test_calculateFrequency_cpp(StatOpInstance, data):
    return StatOpInstance.calculateFrequency(data)

@execution_time
def test_calculateFrequency_py(data):
    return data.value_counts()

# This function selects a column and retrieves players (elements from the first column)
# that meet a specified condition. For example, if the column represents age and the
# condition is 23, it selects players with the age of 23
# It's only implemented in Python because for some reason in C++ it didn't give anything
def calculateClassification_py(df, data, condition):
    # Convert the condition to the same data type of targetColumnData
    condition = type(data.iloc[0])(condition)
    # Filter the DataFrame based on the specified condition
    filtered_df = df[data == condition]
    if filtered_df.empty:
        return "No players found."

    # Return the players (1st column) from the column that met the condition
    players_list = filtered_df.iloc[:, 1].tolist()
    # Convert the list of players to a string (otherwise it can't be written in the output file)
    players_str = ', '.join(map(str, players_list))
    return players_str

@execution_time
def test_calculateCorrelation_cpp(StatOpInstance, data1, data2):
    return StatOpInstance.calculateCorrelation(data1, data2)

@execution_time
def test_calculateCorrelation_py(data1, data2):
    # Check there are valid data
    if np.isnan(data1).all() or np.isnan(data2).all():
        raise ValueError("Data is empty or contains non-numeric values.")
    return np.corrcoef(data1, data2)[0, 1]


# Plot the frequency with a bar plot
def barplotFrequency(frequency, name):
    # Create a DataFrame for Seaborn
    df_sns = pd.DataFrame({'Values': frequency.index, 'Counts': frequency.values})
    
    # Sort the DataFrame by 'Values' in ascending order
    df_sns = df_sns.sort_values(by = 'Values')
    
    # Use Seaborn to create a bar plot with rainbow colors
    plt.figure(figsize=(10, 6))
    sns.barplot(x = 'Values', y = 'Counts', hue = 'Values', data = df_sns, palette = 'rainbow', legend = False)
    plt.xlabel(name)
    plt.ylabel('Frequency')
    plt.title(f'Frequency of {name}')
    # Rotate x-axis labels for better readability in case some values are longer
    plt.xticks(rotation = 45, ha = 'right')

    # Annotate each bar with its count
    for idx, count in enumerate(df_sns['Counts']):
        plt.text(idx, count, f'{count}', ha = 'center', va = 'bottom')

    plt.show()

# Plot the frequency with a pie chart
def pieplotFrequency(frequency, name):
    # Use Seaborn to create a pie chart with pastel colors
    plt.figure(figsize=(8, 8))  # make it bigger
    sns.set_palette('pastel')
    plt.title(f'Distribution of {name} frequency')
    plt.pie(frequency, labels = frequency.index, autopct = '%1.1f%%', startangle=90)
    plt.show()

# Plot a nested barplot by operation and language to compare execution times and absolute error
def catplotCompare(results, AbsError):
    results_df = pd.DataFrame(results)
    # Use catplot by seaborn. The pairs are made based on the language (C++ or Python)
    g = sns.catplot(data = results_df, kind = 'bar', x = 'Operation', y = 'ExecutionTime', hue = 'Language', height = 6, aspect = 1.5)
    g.set_axis_labels('', 'Time (s)')
    g.legend.set_title('')
    # Annotate each couple of bars with the absolute error between C++ and Python (if present)
    for idx, err in enumerate(AbsError):
        plt.text(idx, err, f'{err}', ha = 'center', va = 'bottom', fontsize = 'medium', weight = 'bold')
    plt.show()


# ----------------
# main of module A
# ----------------

# Create an instance for CSVHandler and StatOp in order to use their methods
csvFile = moduleA.CSVHandler("data/player_data_03_22.csv")
StatOpInstance = moduleA.StatOp(csvFile)

# Read data from CSV file using pandas
df = pd.read_csv('data/player_data_03_22.csv', delimiter=',')
# Store the header i.e. the names of the columns
header = df.columns

print("Some statistics about the age of the players:\n")
# Save the datas in order to compute df[] just once
Age = df['Age']

# Compute the statistics to compare between C++ and Python
res_mean_cpp, time_mean_cpp = test_calculateMean_cpp(StatOpInstance, Age)
res_mean_py, time_mean_py = test_calculateMean_py(Age)

res_sd_cpp, time_sd_cpp = test_calculateStandardDeviation_cpp(StatOpInstance, Age)
res_sd_py, time_sd_py = test_calculateStandardDeviation_py(Age)

res_f_cpp, time_f_cpp = test_calculateFrequency_cpp(StatOpInstance, Age)
res_f_py, time_f_py = test_calculateFrequency_py(Age)

# Create a list with the absolute errors between C++ and Python. For computing it, they must have the same type
res_mean_cpp = float(res_mean_cpp)
res_sd_cpp = float(res_sd_cpp)
AbsErrorAge = [abs(res_mean_cpp - res_mean_py), abs(res_sd_cpp - res_sd_py)]
# Create the base for a DataFrame with the results
resultsAge = {
    'Language': ['C++', 'Python', 'C++', 'Python', 'C++', 'Python'],
    'Operation': ['Mean', 'Mean', 'StandardDeviation', 'StandardDeviation', 'Frequency', 'Frequency'],
    'Result': [res_mean_cpp, res_mean_py, res_sd_cpp, res_sd_py, res_f_cpp, res_f_py],
    'ExecutionTime': [time_mean_cpp, time_mean_py, time_sd_cpp, time_sd_py, time_f_cpp, time_f_py]
}

# In this way you don't get suddenly overwhelmed by datas and plots
input("\nPress enter to visualize a catplot to compare execution times and absolute error for Age.")
catplotCompare(resultsAge, AbsErrorAge)

input("\nPress enter to visualize a bar plot of its frequency count.")
barplotFrequency(res_f_py, 'Age')

input("\nPress enter to visualize a pie chart plot for its distribution.")
pieplotFrequency(res_f_py, 'Age')

# Same as before but with Team
print("\nSome statistics about the teams of the players:\n")
Team = df['Team']

res_median_cpp, time_median_cpp = test_calculateMedian_cpp(StatOpInstance, Team)
res_median_py, time_median_py = test_calculateMedian_py(Team)

res_f_cpp, time_f_cpp = test_calculateFrequency_cpp(StatOpInstance, Team)
res_f_py, time_f_py = test_calculateFrequency_py(Team)

AbsErrorTeam = []
resultsTeam = {
    'Language': ['C++', 'Python', 'C++', 'Python'],
    'Operation': ['Median', 'Median', 'Frequency', 'Frequency'],
    'Result': [res_median_cpp, res_median_py, res_f_cpp, res_f_py],
    'ExecutionTime': [time_median_cpp, time_median_py, time_f_cpp, time_f_py]
}

input("Press enter to visualize a catplot to compare execution times for Team.")
catplotCompare(resultsTeam, AbsErrorTeam)
print(f"Median with C++ is: {res_median_cpp} \nWith Python: {res_median_py}\n")

input("\nPress enter to visualize a bar plot of the frequency count for each Team.")
barplotFrequency(res_f_py, 'Team')

input("\nPress enter to visualize a pie chart plot for its distribution.")
pieplotFrequency(res_f_py, 'Team')


print("\nNow you can analyze statistics operations in columns of your choice.")

# Print the header so the user can see the options
print(f"\nThe names of the columns are {header[1:]}")
# Without [1:], it prints '0' as first value because the first column is the enumeration of rows

# Create the output path outside the loop, otherwise it gets cleaned every time
output_file_path = "NBAresults.txt"

# Check if the file already exists, if so, overwrite it
if os.path.exists(output_file_path):
    with open(output_file_path, 'w') as file:
        file.write('Statistics operations with NBA players\n\n')

# Since in Python do-while doesn't exist, set this condition continueChoice
# in order to run the while loop at least once
continueChoice = 1
while continueChoice == 1:
    targetColumn = input("What is the name of the column you want to analyze? ")
    while targetColumn not in header:
        targetColumn = input("This column does not exist. Please insert a valid name: ")
    targetColumnData = df[targetColumn]

    print("""
    Select the analysis type:
    1. Mean
    2. Median
    3. Standard Deviation
    4. Variance
    5. Frequency Count
    6. Classification
    7. Correlation
    0. Exit
    """)
    choice = int(input("Enter the corresponding number: "))
    # Exit loop if the user chooses 0
    if choice == 0:
        print("Exiting...")
        break

    # If there's even a string, some analysis can't be computed (it would not make sense)
    if any(isinstance(value, str) for value in targetColumnData):
        while choice not in [2, 5, 6]:
            print(f"{targetColumn} has no numerical values.")
            choice = int(input("Choose an analysis number between 2, 5 or 6: "))

    # Switch case for Python
    match choice:
        # description, result and timeExecution are defined in every case for writing them in the output file
        case 1:
            try:
                description = f"Mean of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateMean_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateMean_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating mean.", str(e))

        case 2:
            try:
                description = f"Median of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateMedian_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateMedian_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating median.", str(e))

        case 3:
            try:
                description = f"Standard deviation of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateStandardDeviation_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateStandardDeviation_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating standard deviation.", str(e))

        case 4:
            try:
                description = f"Variance of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateVariance_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateVariance_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating variance.", str(e))

        case 5:
            description = f"Frequency count of {targetColumn}:\n"
            res_cpp, time_cpp = test_calculateFrequency_cpp(StatOpInstance, targetColumnData)
            res_py, time_py = test_calculateFrequency_py(targetColumnData)
            result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
            timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"

            input("Press enter to see it with a bar plot.")
            barplotFrequency(res_py, targetColumn)
                
            input("Press enter to see its distribution with a pie chart plot.")
            pieplotFrequency(res_py, targetColumn)

        case 6:
            condition = input("Enter the name of the feature you want to classify: ")
            description = f"Players with {targetColumn} equal to {condition}:\n"
            result = (f"Python result: {calculateClassification_py(df, targetColumnData, condition)}")
            timeExecution = '' # The function doesn't have a time decorator

        case 7:
            targetColumn2 = input("Enter the name of the other target column for correlation: ")
            while targetColumn2 not in header:
                targetColumn2 = input("This column does not exist. Please insert a valid name: ")
            targetColumnData2 = df[targetColumn2]
            try:
                description = f"Correlation between {targetColumn} and {targetColumn2}:\n"
                res_cpp, time_cpp = test_calculateCorrelation_cpp(StatOpInstance, targetColumnData, targetColumnData2)
                res_py, time_py = test_calculateCorrelation_py(targetColumnData, targetColumnData2)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating correlation.", str(e))

        case _: # default case
            choice = int(input("Invalid choice. Please choose a number between 1 and 7."))
            continue # Skip the rest of the loop and ask the user for a new choice

    # Open the output file in append mode (so it doesn't overwrite)
    with open(output_file_path, 'a') as file:
        file.write(description + result + timeExecution + '\n')

    print(f"Analysis completed:\n{result}{timeExecution}")
    continueChoice = int(input("\nDo you want to perform another analysis? (1 for Yes): "))

print(f"All analyses completed. Results written to {output_file_path}")