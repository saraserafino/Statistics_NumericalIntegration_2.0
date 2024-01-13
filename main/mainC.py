# Numerical Integration module
# Import the module created with pybind11
import moduleC

import numpy as np
import math
import scipy.integrate as integrate
from scipy.integrate import trapezoid, simpson, quad, fixed_quad
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time # for the wrapper execution_time
import os

# Decorator for computing the execution time
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        executionTime = time.time() - start
        return result, executionTime
    return wrapper

# Like in C++, define these functions to compute the analysis of the result and print it

def analysis(integrationValue, trueValue):
    print("True value: {:.6e}".format(trueValue))
    error = abs(trueValue - integrationValue)
    abserror = abs(error / trueValue) * 100
    tolerance = 10**(-15)

    if error < tolerance:
        print("Error: 0.000000e+00")
        print("Absolute relative error: 0.000000e+00 %\n")
    else:
        print("Error: {:.6e}".format(error))
        print("Absolute relative error: {:.6e} %\n".format(abserror))

def print_results(integrationValue, trueValue):
    print("\nIntegration with SciPy.")
    print("Result: {:.6e}".format(integrationValue))
    analysis(integrationValue, trueValue)

# Definitions of the integration methods both in C++ and in Python

# Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
def Midpoint_cpp(function, trueValue, a, b, nBins):
    M = moduleC.Midpoint(a, b, nBins)
    moduleC.print_resultsMidpoint(function, M, trueValue)

@execution_time
def test_Trapezoidal_cpp(function, trueValue, a, b, nBins):
    T = moduleC.Trapezoidal(a, b, nBins)
    moduleC.print_resultsTrapezoidal(function, T, trueValue)

@execution_time
def test_Trapezoidal_py(function, trueValue, nodes):
    result = integrate.trapezoid(function, nodes)
    print_results(result, trueValue)

@execution_time
def test_Simpson_cpp(function, trueValue, a, b, nBins):
    S = moduleC.Simpson(a, b, nBins)
    moduleC.print_resultsSimpson(function, S, trueValue)

@execution_time
def test_Simpson_py(function, trueValue, nodes):
    result = integrate.simpson(function, nodes)
    print_results(result, trueValue)

# Even though it's not Gauss, scipy.integrate.quad integrates between two points, so it's worth a comparison
@execution_time
def test_twopointGauss_cpp(function, trueValue, a, b):
    S = moduleC.twopointGauss(a, b, 2)
    moduleC.print_resultstwopointGauss(function, S, trueValue)

@execution_time
def test_twopoint_py(function, trueValue, a, b):
    result, _ = integrate.quad(function, a, b)
    print_results(result, trueValue)

# For Gauss-Legendre, the interval is fixed to [-1,1] due to numpy.polynomial.legendre.leggaus's
# definition which was overloaded in the C++ method (see IntegrationMethods.py for the overload)
@execution_time
def test_GaussLegendre_cpp(function, trueValue, nBins):
    GL = moduleC.GaussLegendre(-1, 1, nBins)
    moduleC.print_resultsGaussLegendre(function, GL, trueValue)

@execution_time
def test_GaussLegendre_py(function, trueValue, nBins):
    result, _ = integrate.fixed_quad(function, -1, 1, n = nBins)
    print_results(result, trueValue)


# Methods for computing the convergence order in C++ and in Python, decorated with execution time.
# Notice that they return the subintervals and the errors, in this way a plot with Matplotlib can be made

def computeConvergenceOrderMidpoint_cpp(function, exactIntegral):
    moduleC.computeConvergenceOrderMidpoint(function, exactIntegral)

@execution_time
def computeConvergenceOrderTrapezoidal_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderTrapezoidal(function, exactIntegral)
    return subintervals, errors

@execution_time
def computeConvergenceOrderSimpson_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderSimpson(function, exactIntegral)
    return subintervals, errors

@execution_time
def computeConvergenceOrderGaussLegendre_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderGaussLegendre(function, exactIntegral)
    return subintervals, errors

# Since the Trapezoidal and the Simpson method have in common the arguments, write just one function
@execution_time
def computeConvergenceOrderTrapezoidal_Simpson_py(function, exactIntegral, method):
    # Lists for collecting convergence data
    subintervals = []
    errors = []
    
    print(f"\nConvergence order with Python:\n")
    # Initialize outside the loop
    previousError = 1.0
    upperbound = math.pi / 2.0
    nBins = 2
    while nBins <= 1024:
        nodes = np.linspace(0, upperbound, num = nBins)
        f = function(nodes)
        numericalIntegral = method(f, nodes)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        # Compute convergence order
        log_error = math.log(error)
        log_previousError = math.log(previousError)
        p = (log_error - log_previousError) / math.log(2)

        # Collect convergence data
        errors.append(error)
        subintervals.append(nBins)

        # Output the error and convergence order
        print(f"  Subintervals: {nBins:4d}  Error: {error:.6e}  Order: {-p:.2f}")

        previousError = error
        nBins *= 2

    print("\n")
    return subintervals, errors

@execution_time
def computeConvergenceOrderGaussLegendre_py(function, exactIntegral):
    # Lists for collecting convergence data
    subintervals = []
    errors = []
    
    print(f"Convergence order for Gauss-Legendre method with Python:\n")
    # Initialize outside the loop
    previousError = 1.0
    nBins = 2
    while nBins <= 1024:
        numericalIntegral, _ = integrate.fixed_quad(function, -1, 1, n = nBins)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        # Compute convergence order
        log_error = math.log(error)
        log_previousError = math.log(previousError)
        p = (log_error - log_previousError) / math.log(2)

        # Collect convergence data
        errors.append(error)
        subintervals.append(nBins)

        # Output the error and convergence order
        print(f"  Subintervals: {nBins:4d}  Error: {error:.6e}  Order: {-p:.2f}")

        previousError = error
        nBins *= 2

    print("\n")
    return subintervals, errors

# TOGLILO SE ALLA FINE NON LO USI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Plot a nested barplot by method and language to compare execution times and absolute error
def catplotCompare(results, AbsError):
    results_df = pd.DataFrame(results)
    # Use catplot by seaborn. The pairs are made based on the language (C++ or Python)
    g = sns.catplot(data = results_df, kind = 'bar', x = 'Method', y = 'ExecutionTime', hue = 'Language', height = 6, aspect = 1.5)
    g.set_axis_labels('', 'Time (s)')
    g.legend.set_title('')
    # Annotate each couple of bars with the absolute error between C++ and Python (if present)
    for idx, err in enumerate(AbsError):
        plt.text(idx, err, f'{err}', ha = 'center', fontsize = 'medium', weight = 'bold')
    plt.show()

# ----------------
# main of module C
# ----------------

# Create the output path outside the loop, otherwise it gets cleaned every time
output_file_path = "IntegrationResults.txt"

# Check if the file already exists, if so, overwrite it
if os.path.exists(output_file_path):
    with open(output_file_path, 'w') as file:
        file.write('Numerical Integration analysis\n\n')


# Since in Python do-while doesn't exist, set this condition continueChoice
# in order to run the while loop at least once
continueChoice = 1
while continueChoice == 1:
    print("""
    Select the analysis type:
    1. Convergence tests
    2. Polynomial tests
    3. Compute integrals
    0. Exit
    """)
    choice = int(input("Enter the corresponding number: "))
    
    match choice:
        case 0: # Exit loop if the user chooses 0
            print("Exiting...")
            break

        # description, result and timeExecution are defined in every case for writing them in the output file
        case 1:
            # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
            computeConvergenceOrderMidpoint_cpp("cos(x)", 1.0)

            # Sarebbe più bello computare più volte e fare la media, ma dovrei cambiare le funzioni iniziali visto che dentro stampano

            # Define the function for the computation of the convergence order
            cos = np.vectorize(np.cos)

            # The execution time given by the decorator will be used to plot the speeds, thus the actual result must be written between []
            [subintervals_trap_cpp, errors_trap_cpp], time_trap_cpp = computeConvergenceOrderTrapezoidal_cpp("cos(x)", 1.0)
            [subintervals_trap_py, errors_trap_py], time_trap_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.trapezoid)
            
            [subintervals_simp_cpp, errors_simp_cpp], time_simp_cpp = computeConvergenceOrderSimpson_cpp("cos(x)", 1.0)
            [subintervals_simp_py, errors_simp_py], time_simp_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.simpson)
            
            # The order of convergence of two point methods is not computed: being 2 points it would be mathematically inconsistent
            
            [subintervals_gl_cpp, errors_gl_cpp], time_gl_cpp = computeConvergenceOrderGaussLegendre_cpp("cos(x)", 1.0)
            [subintervals_gl_py, errors_gl_py], time_gl_py = computeConvergenceOrderGaussLegendre_py(cos, 1.0)

            # Plot convergence for each compared method
            plt.plot(subintervals_trap_cpp, errors_trap_cpp, label = 'Trapezoidal Rule with C++', color = 'aquamarine')
            plt.plot(subintervals_trap_py, errors_trap_py, label = 'Trapezoidal Rule with Python', color = 'orchid')
            plt.plot(subintervals_simp_cpp, errors_simp_cpp, label = 'Simpson\'s Rule with C++', color = 'orange')
            plt.plot(subintervals_simp_py, errors_simp_py, label = 'Simpson\'s Rule with Python', color = 'mediumseagreen')
            plt.plot(subintervals_gl_cpp, errors_gl_cpp, label = 'Gauss-Legendre Quadrature with a mixture', color = 'red')
            plt.plot(subintervals_gl_py, errors_gl_py, label = 'Gauss-Legendre Quadrature with Python', color = 'fuchsia')
            # Use logarithmic scale for a better visibility
            plt.xscale('log')
            plt.yscale('log')
            # Name the axis, give a title and show the legend
            plt.xlabel('Subintervals')
            plt.ylabel('Error')
            plt.title('Convergence of Numerical Integration Methods in C++ and Python')
            plt.legend()
            # Show a grid and the actual plot
            plt.grid(True)
            input("\nPress enter to visualize a plot for the convergence of each compared method.")
            plt.show()

            # Plot execution times for each compared method
            methods = ['Trapezoidal', 'PyTrapezoidal', 'Simpson', 'PySimpson', 'Gauss-Legendre', 'PyGauss-Legendre']
            executionTimes = [time_trap_cpp, time_trap_py, time_simp_cpp, time_simp_py, time_gl_cpp, time_gl_py]
            plt.bar(methods, executionTimes, color = ['aquamarine', 'orchid', 'orange', 'mediumseagreen', 'red', 'fuchsia'])
            plt.xlabel('Integration Method')
            plt.ylabel('Execution Time (s)')
            plt.title('Execution Time of Numerical Integration Methods in C++ and Python')
            # Rotate x-axis labels for better readability
            plt.xticks(rotation = 45, ha = 'right')
            # Annotate each bar with its execution time
            for idx, times in enumerate(executionTimes):
                plt.text(idx, times, f'{times:.4f}', ha = 'center', va = 'bottom')
            input("\nPress enter to visualize a plot for the execution times of each compared method.")
            plt.show()

            # Create a list with the absolute errors between C++ and Python. For computing it, they must have the same type
            # And we're interested only in the last error (so [-1])
            errors_trap_cpp[-1] = float(errors_trap_cpp[-1])
            errors_simp_cpp[-1] = float(errors_simp_cpp[-1])
            errors_gl_cpp[-1] = float(errors_gl_cpp[-1])
            AbsErrorConvergence = [abs(errors_trap_cpp[-1] - errors_trap_py[-1]), abs(errors_simp_cpp[-1] - errors_simp_py[-1]), abs(errors_gl_cpp[-1] - errors_gl_py[-1])]
            # Create the base for a DataFrame with the results
            resultsConvergence = {
                'Language': ['C++', 'Python', 'C++', 'Python', 'C++', 'Python'],
                'Method': ['Trapezoidal', 'Trapezoidal', 'Simpson', 'Simpson', 'Gauss-Legendre', 'Gauss-Legendre'],
                'Error': [errors_trap_cpp[-1], errors_trap_py[-1], errors_simp_cpp[-1], errors_simp_py[-1], errors_gl_cpp[-1], errors_gl_py[-1]],
                'ExecutionTime': [time_trap_cpp, time_trap_py, time_simp_cpp, time_simp_py, time_gl_cpp, time_gl_py]
            }
            #input("\nPress enter to visualize a plot for the execution times of each compared method.")
            #catplotCompare(resultsConvergence, AbsErrorConvergence)

        case 2:
            # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
            print("\nIntegration of 3x+1 in [0,1]:")
            Midpoint_cpp("3*x+1", 2.5, 0, 1, 2)

            # In both SciPy's Trapezoidal and Simpson methods, you can optionally provide
            # the array over which the function is sampled i.e. the nodes
            print("Compare the integration of x^3 in [0,1].\n")
            res_trap_cpp, time_trap_cpp = test_Trapezoidal_cpp("x^3", 0.25, 0, 1, 5) # trueValue = 0.25, nBins = 5
            nodesT = np.linspace(0, 1, num = 5) # array in [0,1] of size 5 like the above nBins
            res_trap_py, time_trap_py = test_Trapezoidal_py(nodesT**3, 0.25, nodesT)
            print(f"C++ executed it in {time_trap_cpp} s, Python in {time_trap_py} s.")

            print("\nCompare the integration of x^2 in [1,4].\n")
            res_simp_cpp, time_simp_cpp = test_Simpson_cpp("x^2", 21.0, 1, 4, 3) # trueValue = 21, nBins = 3
            nodesS = np.array([1, 3, 4]) # array in [1,4] of size 3 like the above nBins
            res_simp_py, time_simp_py = test_Simpson_py(nodesS**2, 21.0, nodesS)
            print(f"C++ executed it in {time_simp_cpp} s, Python in {time_simp_py} s.")

            print("\nCompare the integration of x^2 in [0,4].\n")
            res_tp_cpp, time_tp_cpp = test_twopointGauss_cpp("x^2", 64.0/3.0, 0, 4) # trueValue = 64/3 = 21.333
            x2 = lambda x: x**2
            res_tp_py, time_tp_py = test_twopoint_py(x2, 64.0/3.0, 0, 4) # uses integrate.quad, see def above for more
            print(f"C++ executed it in {time_tp_cpp} s, Python in {time_tp_py} s.")

            print("\nCompare the integration of x^4 in [-1,1].\n")
            res_gl_cpp, time_gl_cpp = test_GaussLegendre_cpp("x^4", 2.0/5.0, 11) # trueValue = 2/5 = 0.4, nBins = 11
            x4 = lambda x: x**4
            res_gl_py, time_gl_py = test_GaussLegendre_py(x4, 2.0/5.0, 11)
            print(f"C++ executed it in {time_gl_cpp} s, Python in {time_gl_py} s.")

        case 3:
            #compute integrals
            break

        case _: # default case
            print("Invalid choice. Please choose a number between 1 and 3.")
            continue

    # Open the output file in append mode (so it doesn't overwrite)
    #with open(output_file_path, 'a') as file:
        #file.write(description + result + timeExecution + '\n')

    #print(f"Analysis completed:\n{result}{timeExecution}")
    continueChoice = int(input("Do you want to perform another analysis? (1 for Yes): "))

print(f"All analyses completed. Results written to {output_file_path}")