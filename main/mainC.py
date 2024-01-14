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
from tabulate import tabulate # for a cute table of results

# Decorator for computing the execution time
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        executionTime = time.time() - start
        return result, executionTime
    return wrapper

# Definitions of the integration methods both in C++ and in Python

# Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
@execution_time
def Midpoint_cpp(function, trueValue, a, b, nBins):
    M = moduleC.Midpoint(a, b, nBins)
    integrationValue = moduleC.IntegrateMidpoint(function, M)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_Trapezoidal_cpp(function, trueValue, a, b, nBins):
    T = moduleC.Trapezoidal(a, b, nBins)
    integrationValue = moduleC.IntegrateTrapezoidal(function, T)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_Trapezoidal_py(function, trueValue, nodes):
    integrationValue = integrate.trapezoid(function, nodes)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_Simpson_cpp(function, trueValue, a, b, nBins):
    S = moduleC.Simpson(a, b, nBins)
    integrationValue = moduleC.IntegrateSimpson(function, S)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_Simpson_py(function, trueValue, nodes):
    integrationValue = integrate.simpson(function, nodes)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

# Even though it's not Gauss, scipy.integrate.quad integrates between two points, so it's worth a comparison
@execution_time
def test_twopointGauss_cpp(function, trueValue, a, b):
    T = moduleC.twopointGauss(a, b, 2)
    integrationValue = moduleC.IntegratetwopointGauss(function, T)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_twopoint_py(function, trueValue, a, b):
    integrationValue, _ = integrate.quad(function, a, b)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

# For Gauss-Legendre, the interval is fixed to [-1,1] due to numpy.polynomial.legendre.leggaus's
# definition which was overloaded in the C++ method (see IntegrationMethods.py for the overload)
@execution_time
def test_GaussLegendre_cpp(function, trueValue, nBins):
    GL = moduleC.GaussLegendre(-1, 1, nBins)
    integrationValue = moduleC.IntegrateGaussLegendre(function, GL)
    error = abs(trueValue - integrationValue)
    return integrationValue, error

@execution_time
def test_GaussLegendre_py(function, trueValue, nBins):
    integrationValue, _ = integrate.fixed_quad(function, -1, 1, n = nBins)
    error = abs(trueValue - integrationValue)
    return integrationValue, error


# Methods for computing the convergence order in C++ and in Python, decorated with execution time.
# They return the errors and the orders of convergence, so that a plot with Matplotlib can be made

@execution_time
def computeConvergenceOrderMidpoint_cpp(function, exactIntegral):
    errors, orders = moduleC.computeConvergenceOrderMidpoint(function, exactIntegral)
    return errors, orders

@execution_time
def computeConvergenceOrderTrapezoidal_cpp(function, exactIntegral):
    errors, orders = moduleC.computeConvergenceOrderTrapezoidal(function, exactIntegral)
    return errors, orders

@execution_time
def computeConvergenceOrderSimpson_cpp(function, exactIntegral):
    errors, orders = moduleC.computeConvergenceOrderSimpson(function, exactIntegral)
    return errors, orders

@execution_time
def computeConvergenceOrderGaussLegendre_cpp(function, exactIntegral):
    errors, orders = moduleC.computeConvergenceOrderGaussLegendre(function, exactIntegral)
    return errors, orders

# Since the Trapezoidal and the Simpson method have in common the arguments, write just one function
@execution_time
def computeConvergenceOrderTrapezoidal_Simpson_py(function, exactIntegral, method):
    # Lists for collecting convergence data
    errors = []
    orders = []
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
        order = (log_error - log_previousError) / math.log(2)

        # Collect convergence data
        errors.append(error)
        orders.append(-order)

        previousError = error
        nBins *= 2
    return errors, orders

@execution_time
def computeConvergenceOrderGaussLegendre_py(function, exactIntegral):
    # Lists for collecting convergence data
    errors = []
    orders = []
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
        order = (log_error - log_previousError) / math.log(2)

        # Collect convergence data
        errors.append(error)
        orders.append(-order)

        previousError = error
        nBins *= 2
    return errors, orders


# ----------------
# main of module C
# ----------------

# Create a folder in which to store plot images
if not os.path.exists("NumericalIntegrationModule/images"):
    os.mkdir("NumericalIntegrationModule/images")
# Create the output path for the results outside the loop, otherwise it gets cleaned every time
output_file_path = "NumericalIntegrationModule/IntegrationResults.txt"

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
    1. Convergence order tests
    2. Polynomial tests
    0. Exit
    """)
    choice = int(input("Enter the corresponding number: "))
    
    match choice:
        case 0: # Exit loop if the user chooses 0
            print("Exiting...")
            break

        # description, result and timeExecution are defined in every case for writing them in the output file
        case 1:
            description = "Compute the average of convergence order and time of execution for each method (except for the two-point that would be mathematically inconsistent to compute).\n\n"
            # Define the function for the computation of the convergence order
            cos = np.vectorize(np.cos)

            # Create a dictionary for each of the results computed in the for-cycle. Lastly we'll compute their average
            methods = ['Midpoint', 'Trapezoidal', 'PyTrapezoidal', 'Simpson', 'PySimpson', 'Gauss-Legendre', 'PyGauss-Legendre']
            results = {method: {'avg_errors': [], 'avg_orders': [], 'avg_time': []} for method in methods}

            for i in range(11):
                # The execution time given by the decorator will be used to plot the speeds, thus the actual result must be written between []

                # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
                [errors_mid_cpp, orders_mid_cpp], time_mid_cpp = computeConvergenceOrderMidpoint_cpp("cos(x)", 1.0)

                [errors_trap_cpp, orders_trap_cpp], time_trap_cpp = computeConvergenceOrderTrapezoidal_cpp("cos(x)", 1.0)
                [errors_trap_py, orders_trap_py], time_trap_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.trapezoid)
                
                [errors_simp_cpp, orders_simp_cpp], time_simp_cpp = computeConvergenceOrderSimpson_cpp("cos(x)", 1.0)
                [errors_simp_py, orders_simp_py], time_simp_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.simpson)
                
                [errors_gl_cpp, orders_gl_cpp], time_gl_cpp = computeConvergenceOrderGaussLegendre_cpp("cos(x)", 1.0)
                [errors_gl_py, orders_gl_py], time_gl_py = computeConvergenceOrderGaussLegendre_py(cos, 1.0)
                
                # Append each result
                results['Midpoint']['avg_errors'].append(errors_mid_cpp)
                results['Midpoint']['avg_orders'].append(orders_mid_cpp)
                results['Midpoint']['avg_time'].append(time_mid_cpp)

                results['Trapezoidal']['avg_errors'].append(errors_trap_cpp)
                results['Trapezoidal']['avg_orders'].append(orders_trap_cpp)
                results['Trapezoidal']['avg_time'].append(time_trap_cpp)
                
                results['PyTrapezoidal']['avg_errors'].append(errors_trap_py)
                results['PyTrapezoidal']['avg_orders'].append(orders_trap_py)
                results['PyTrapezoidal']['avg_time'].append(time_trap_py)
                
                results['Simpson']['avg_errors'].append(errors_simp_cpp)
                results['Simpson']['avg_orders'].append(orders_simp_cpp)
                results['Simpson']['avg_time'].append(time_simp_cpp)
                
                results['PySimpson']['avg_errors'].append(errors_simp_py)
                results['PySimpson']['avg_orders'].append(orders_simp_py)
                results['PySimpson']['avg_time'].append(time_simp_py)
                
                results['Gauss-Legendre']['avg_errors'].append(errors_gl_cpp)
                results['Gauss-Legendre']['avg_orders'].append(orders_gl_cpp)
                results['Gauss-Legendre']['avg_time'].append(time_gl_cpp)
                
                results['PyGauss-Legendre']['avg_errors'].append(errors_gl_py)
                results['PyGauss-Legendre']['avg_orders'].append(orders_gl_py)
                results['PyGauss-Legendre']['avg_time'].append(time_gl_py)

            # Compute their averages
            averages = {method: {'avg_errors': np.mean(results[method]['avg_errors'], axis = 0),
                        'avg_orders': np.mean(results[method]['avg_orders'], axis = 0),
                        'avg_time': np.mean(results[method]['avg_time'])} for method in methods}

            # Recreate the subintervals of the above results (2, 4, 8, 16, 32, 64, ..., 1024)
            subintervals = [int(math.pow(2, i)) for i in range(int(math.log2(2)), int(math.log2(1024)) + 1)]

            # Plot convergence for each compared method
            plt.plot(subintervals, averages['Midpoint']['avg_errors'], label = 'Midpoint Rule with C++', color = 'purple')
            plt.plot(subintervals, averages['Trapezoidal']['avg_errors'], label = 'Trapezoidal Rule with C++', color = 'aquamarine')
            plt.plot(subintervals, averages['PyTrapezoidal']['avg_errors'], label = 'Trapezoidal Rule with Python', color = 'orchid')
            plt.plot(subintervals, averages['Simpson']['avg_errors'], label = 'Simpson\'s Rule with C++', color = 'orange')
            plt.plot(subintervals, averages['PySimpson']['avg_errors'], label = 'Simpson\'s Rule with Python', color = 'mediumseagreen')
            plt.plot(subintervals, averages['Gauss-Legendre']['avg_errors'], label = 'Gauss-Legendre Quadrature with a mixture', color = 'red')
            plt.plot(subintervals, averages['PyGauss-Legendre']['avg_errors'], label = 'Gauss-Legendre Quadrature with Python', color = 'fuchsia')
            # Use logarithmic scale for a better visibility
            plt.xscale('log')
            plt.yscale('log')
            # Name the axis, give a title and show the legend
            plt.xlabel('Subintervals')
            plt.ylabel('Error')
            plt.title('Average Convergence Order of Numerical Integration Methods')
            plt.legend()
            # Show a grid and the actual plot
            plt.grid(True)
            input("\nPress enter to visualize a plot of the convergence order for each compared method.")
            # Save the plot
            plt.savefig('NumericalIntegrationModule/images/AverageConvergenceOrder.png')
            plt.show()

            # Plot execution times for each compared method
            ExecutionTimes = {averages[method]['avg_time'] for method in methods}
            plt.bar(methods, ExecutionTimes, color = ['purple', 'aquamarine', 'orchid', 'orange', 'mediumseagreen', 'red', 'fuchsia'])
            plt.xlabel('Integration Method')
            plt.ylabel('Execution Time (s)')
            plt.title('Average Execution Time of Numerical Integration Methods')
            # Rotate x-axis labels for better readability
            plt.xticks(rotation = 45, ha = 'right')
            # Annotate each bar with its execution time
            for idx, times in enumerate(ExecutionTimes):
                plt.text(idx, times, f'{times:.4f}', ha = 'center', va = 'bottom')
            input("\nPress enter to visualize a plot of the execution times for each compared method.")
            # Save the plot
            plt.savefig('NumericalIntegrationModule/images/AverageExecutionTime.png')
            plt.show()

            # Prepare the results to be printed
            # Convert sets to lists
            averageErrors = {method : averages[method]['avg_errors'] for method in methods}
            averageOrders = {method : averages[method]['avg_orders'] for method in methods}
            averageTimes = {method : averages[method]['avg_time'] for method in methods}
            result = ''
            for method in methods:
                result += f"Average Convergence for {method}:\n"
                for i, subint in enumerate(subintervals):
                    result += f"  Subintervals: {subint:4d}  Error: {averageErrors[method][i]:.6e}  Order: {averageOrders[method][i]:.2f}\n"
                result += f"\nExecuted in {averageTimes[method]:.4f} s.\n\n\n"
            
        case 2:
            description = "Compute some integrals for each method.\n"
            result = ''
            # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in C++
            TrueValue = 2.5
            result = f"\nIntegration of 3x+1 in [0,1] with Midpoint Rule.\nTrue value: {TrueValue:.6e}\n"
            [res_mid_cpp, err_mid_cpp], time_mid_cpp = Midpoint_cpp("3*x+1", TrueValue, 0, 1, 2)
            result += f"Result with C++: {res_mid_cpp:.6e} \nError: {err_mid_cpp:.6e}\n"
            abserr_mid_cpp = abs(err_mid_cpp / TrueValue) * 100
            result += f"Absolute relative error: {abserr_mid_cpp:.6e}\nExecuted in {time_mid_cpp:.4f} s."

            # In both SciPy's Trapezoidal and Simpson methods, you can optionally provide
            # the array over which the function is sampled i.e. the nodes

            TrueValue = 0.25
            result += f"\n\nCompare the integration of x^3 in [0,1] with Trapezoidal Rule.\nTrue value: {TrueValue:.6e}\n\n"
            [res_trap_cpp, err_trap_cpp], time_trap_cpp = test_Trapezoidal_cpp("x^3", TrueValue, 0, 1, 5) # nBins = 5
            abserr_trap_cpp = abs(err_trap_cpp / TrueValue) * 100
            nodesT = np.linspace(0, 1, num = 5) # array in [0,1] of size 5 like the above nBins
            [res_trap_py, err_trap_py], time_trap_py = test_Trapezoidal_py(nodesT**3, TrueValue, nodesT)
            abserr_trap_py = abs(err_trap_py / TrueValue) * 100
            
            # Prepare the results to be printed in a more uniform way with tabulate
            header = ["", "C++", "Python"]
            data_trap = [
                    ["Result", res_trap_cpp, res_trap_py],
                    ["Error", err_trap_cpp, err_trap_py],
                    ["Absolute relative error (%)", abserr_trap_cpp, abserr_trap_py],
                    ["Execution time (s)", time_trap_cpp, time_trap_py]
                ]
            result += tabulate(data_trap, header, tablefmt = "fancy_grid")

            TrueValue = 21.0
            result += f"\n\nCompare the integration of x^2 in [1,4] with Simpson's Rule.\nTrue value: {TrueValue:.6e}\n\n"
            [res_simp_cpp, err_simp_cpp], time_simp_cpp = test_Simpson_cpp("x^2", TrueValue, 1, 4, 3) # nBins = 3
            abserr_simp_cpp = abs(err_simp_cpp / TrueValue) * 100
            nodesS = np.array([1, 3, 4]) # array in [1,4] of size 3 like the above nBins
            [res_simp_py, err_simp_py], time_simp_py = test_Simpson_py(nodesS**2, TrueValue, nodesS)
            abserr_simp_py = abs(err_simp_py / TrueValue) * 100

            data_simp = [
                        ["Result", res_simp_cpp, res_simp_py],
                        ["Error", err_simp_cpp, err_simp_py],
                        ["Absolute relative error (%)", abserr_simp_cpp, abserr_simp_py],
                        ["Execution time (s)", time_simp_cpp, time_simp_py]
                    ]
            result += tabulate(data_simp, header, tablefmt = "fancy_grid")

            TrueValue = 64.0/3.0 # = 21.333 with 3 periodic
            result += f"\n\nCompare the integration of x^2 in [0,4] with two-point Gauss.\nTrue value: {TrueValue:.6e}\n\n"
            [res_tp_cpp, err_tp_cpp], time_tp_cpp = test_twopointGauss_cpp("x^2", TrueValue, 0, 4)
            abserr_tp_cpp = abs(err_tp_cpp / TrueValue) * 100
            x2 = lambda x: x**2
            [res_tp_py, err_tp_py], time_tp_py = test_twopoint_py(x2, TrueValue, 0, 4) # uses integrate.quad, see def above for more
            abserr_tp_py = abs(err_tp_py / TrueValue) * 100

            data_tp = [
                        ["Result", res_tp_cpp, res_tp_py],
                        ["Error", err_tp_cpp, err_tp_py],
                        ["Absolute relative error (%)", abserr_tp_cpp, abserr_tp_py],
                        ["Execution time (s)", time_tp_cpp, time_tp_py]
                    ]
            result += tabulate(data_tp, header, tablefmt = "fancy_grid")

            TrueValue = 2.0/5.0 # = 0.4
            result += f"\n\nCompare the integration of x^4 in [-1,1] with Gauss-Legendre.\nTrue value: {TrueValue:.6e}\n\n"
            [res_gl_cpp, err_gl_cpp], time_gl_cpp = test_GaussLegendre_cpp("x^4", 2.0/5.0, 11) # nBins = 11
            abserr_gl_cpp = abs(err_gl_cpp / TrueValue) * 100
            x4 = lambda x: x**4
            [res_gl_py, err_gl_py], time_gl_py = test_GaussLegendre_py(x4, 2.0/5.0, 11)
            abserr_gl_py = abs(err_gl_py / TrueValue) * 100

            data_gl = [
                        ["Result", res_gl_cpp, res_gl_py],
                        ["Error", err_gl_cpp, err_gl_py],
                        ["Absolute relative error (%)", abserr_gl_cpp, abserr_gl_py],
                        ["Execution time (s)", time_gl_cpp, time_gl_py]
                    ]
            result += tabulate(data_gl, header, tablefmt = "fancy_grid")

        case _: # default case
            print("Invalid choice. Please choose a number between 0 and 2.")
            continue

    # Open the output file in append mode (so it doesn't overwrite)
    with open(output_file_path, 'a') as file:
        file.write(description + result + '\n\n')

    print(f"{description}Analysis completed:\n{result}")
    continueChoice = int(input("Do you want to perform another analysis? (1 for Yes): "))

print(f"All analyses completed. Results written to {output_file_path}")