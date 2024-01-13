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

def test_calculateClassification_cpp(StatOpInstance, targetColumn, condition):
    return StatOpInstance.calculateClassification(targetColumn, condition)

def test_calculateCorrelation_cpp(StatOpInstance, data1, data2):
    return StatOpInstance.calculateCorrelation(data1, data2)


# Plot the frequency with a bar plot
def barplotFrequency(frequency, name):
    # Create a DataFrame for Seaborn
    dfsns = pd.DataFrame({'Values': frequency.index, 'Counts': frequency.values})
    
    # Sort the DataFrame by 'Values' in ascending order
    dfsns = dfsns.sort_values(by = 'Values')
    
    # Use Seaborn to create a bar plot with rainbow colors
    plt.figure(figsize=(10, 6))
    sns.barplot(x = 'Values', y = 'Counts', hue = 'Values', data = dfsns, palette = 'rainbow', legend = False)
    plt.xlabel(name)
    plt.ylabel('Frequency')
    plt.title(f'Frequency of {name}')
    # Rotate x-axis labels for better readability in case some values are longer
    plt.xticks(rotation = 45, ha = 'right')

    # Annotate each bar with its count
    for idx, count in enumerate(dfsns['Counts']):
        plt.text(idx, count, f'{count}', ha = 'center', va = 'bottom')

    plt.show()

# Plot the frequency with a pie chart
def pieplotFrequency(frequency, name):
    # Use Seaborn to create a pie chart with pastel colors
    plt.figure(figsize=(8, 8))  # make it bigger
    sns.set_palette('pastel')
    plt.title(f'Distribution of {name}')
    plt.pie(frequency, labels = frequency.index, autopct = '%1.1f%%', startangle=90)
    plt.show()

# main of Statistics module

# Create an instance for CSVHandler in order to use its methods
csvFile = moduleA.CSVHandler("data/player_data_03_22.csv")

# Create an instance for StatOp, otherwise the C++ methods can't work
StatOpInstance = moduleA.StatOp(csvFile)

# Read data from CSV file into NumPy arrays,
df = pd.read_csv('data/player_data_03_22.csv', delimiter=',')

headerNames = df.columns

# Now you can access each column by its name
#Age = df['Age']
#Team = df['Team']
#print(f"Prova che stampa la colonna Age: {Age}")
#print(f"Mean: {test_calculateMean_py(Age)}")
#print(f"Median: {test_calculateMedian_py(Age)}")
#AgeFrequency = test_calculateFrequency_py(Age)
#print(f"Frequency: {AgeFrequency}")
#print(f"Idem per Team: {Team}")
#print(f"Median: {test_calculateMedian_py(Team)}")
#TeamFrequency = test_calculateFrequency_py(Team)
#print(f"Frequency: {TeamFrequency}")

#print(f"Let's see the frequency of teams in which the players play:\n")

# Plot the frequency of Team with a bar plot and pie chart plot
#pieplotFrequency(TeamFrequency, 'Team frequency')
#barplotFrequency(TeamFrequency, 'Team')

# Analysis of which programming language is faster. Chosen column: Age o magari generalizza

# Plot the frequency of Age with a bar plot and pie chart plot
#pieplotFrequency(AgeFrequency, 'Age frequency')
#barplotFrequency(AgeFrequency, 'Age')

print("Now you can analyze statistics operations in columns of your choice.")

print(f"\nThe name of the columns are {headerNames[1:]}")
# Without [1:], it prints '0' as first value because the first column is the enumeration of rows

# Create the output path outside the loop, otherwise it gets cleaned every time
output_file_path = "results.txt"

# Check if the file already exists, if so, write the title
if os.path.exists(output_file_path):
    with open(output_file_path, 'w') as file:
            file.write('Statistics operations with NBA players\n\n')

# Since in Python do-while doesn't exist, set this condition continueChoice
# in order to run the while loop at least once
continueChoice = 1
while continueChoice == 1:
    try:
        targetColumn = input("What is the name of the column you want to analyze? : ")
        targetColumnData = df[targetColumn]
    except RuntimeError as e:
        print("This column does not exist.", str(e))

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
    choice = input("Enter the corresponding number: ")

    # Switch case for Python
    match choice:
        case "0": # Exit loop if the user chooses 0
            break

        # description, result and timeExecution are defined in every case in order to write them in the output file
        case "1":
            try:
                description = f"Mean of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateMean_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateMean_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating mean.", str(e))

        case "2":
            try:
                description = f"Median of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateMedian_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateMedian_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating median.", str(e))

        case "3":
            try:
                description = f"Standard deviation of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateStandardDeviation_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateStandardDeviation_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating standard deviation.", str(e))

        case "4":
            try:
                description = f"Variance of {targetColumn}:\n"
                res_cpp, time_cpp = test_calculateVariance_cpp(StatOpInstance, targetColumnData)
                res_py, time_py = test_calculateVariance_py(targetColumnData)
                result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
                timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"
            except RuntimeError as e:
                print("Error calculating variance.", str(e))

        case "5":
            description = f"Frequency count of {targetColumn}:\n"
            res_cpp, time_cpp = test_calculateFrequency_cpp(StatOpInstance, targetColumnData)
            res_py, time_py = test_calculateFrequency_py(targetColumnData)
            result = f"C++ result: {res_cpp} \nPython result: {res_py}\n"
            timeExecution = f"C++ executed it in {time_cpp} s, Python in {time_py} s.\n"

            plotta = int(input("Do you want to see it with a bar plot? (1 for Yes, 0 for No): "))
            if plotta == 1:
                barplotFrequency(res_py, targetColumn)
                
            plotta = int(input("Do you want to see it with a pie chart plot? (1 for Yes, 0 for No): "))
            if plotta == 1:
                pieplotFrequency(res_py, targetColumn)

        case "6":
            condition : str = (input("Enter the name of the feature you want to classify: "))
            try:
                description = f"Classification of {targetColumn}:\n"
                result = test_calculateClassification_cpp(StatOpInstance, targetColumn, condition)
                timeExecution = '' # The function didn't have a time decorator
            except RuntimeError as e:
                print("Error calculating classification.", str(e))

        case "7":
            targetColumn2 = input("Enter the name of the target column for correlation: ")
            targetColumnData2 = df[targetColumn2]
            try:
                description = f"Correlation between {targetColumn} and {targetColumn2}:\n"
                result = str(test_calculateCorrelation_cpp(StatOpInstance, targetColumnData, targetColumnData2))
                timeExecution = '' # The function didn't have a time decorator
            except RuntimeError as e:
                print("Error calculating correlation.", str(e))

        case _: # default case
            print("Invalid choice. Please choose a number between 1 and 7.")
            continue # Skip the rest of the loop and ask the user for a new choice

    # Open the output file in append mode (so it doesn't overwrite)
    with open(output_file_path, 'a') as file:
        file.write(description + result + timeExecution + '\n')

    print(f"Analysis completed:\n{result}{timeExecution}")
    continueChoice = int(input("\nDo you want to perform another analysis? (1 for Yes, 0 for No): "))

print(f"All analyses completed. Results written to {output_file_path}")