import moduleC # module created with pybind11
import numpy as np
import math
import scipy.integrate as integrate
from scipy.integrate import trapezoid, simpson, quad, fixed_quad
import matplotlib.pyplot as plt
import time # for the wrapper execution_time

# Nota per me stessa: tutte le parti in Python (def funzioni e loro esecuzione)
# le ho già controllate con jupyter notebook e sono corrette

# Decorator for computing the execution time
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start} seconds.")
        return result
    return wrapper

# Statistics module



# Numerical Integration module

# Definitions of the integration methods both in cpp and in python

def Midpoint_cpp(function, trueValue, a, b, nBins):
    M = moduleC.Midpoint(a, b, nBins)
    moduleC.print_resultsMidpoint(function, M, trueValue)

@execution_time
def test_Trapezoidal_cpp(function, trueValue, a, b, nBins):
    T = moduleC.Trapezoidal(a, b, nBins)
    moduleC.print_resultsTrapezoidal(function, T, trueValue)

@execution_time
def test_Trapezoidal_py(function, nodes):
    result = integrate.trapezoid(function, nodes)
    print(f"The integration with SciPy gives {result}")

@execution_time
def test_Simpson_cpp(function, trueValue, a, b, nBins):
    S = moduleC.Simpson(a, b, nBins)
    moduleC.print_resultsSimpson(function, S, trueValue)

@execution_time
def test_Simpson_py(function, nodes):
    result = integrate.simpson(function, nodes)
    print(f"The integration with SciPy gives {result}")

# Even though it's not Guass, scipy.integrate.quad integrates between two points, so it's worth a comparison
@execution_time
def test_twopointGauss_cpp(function, trueValue, a, b):
    S = moduleC.twopointGauss(a, b, 2)
    moduleC.print_resultstwopointGauss(function, S, trueValue)

@execution_time
def test_twopoint_py(function, a, b):
    result, _ = integrate.quad(function, a, b)
    print(f"The integration with SciPy gives {result}")

# For Gauss-Legendre the interval is fixed to [-1,1] due to numpy.polynomial.legendre.leggaus's definition
@execution_time
def test_GaussLegendre_cpp(function, trueValue, nBins):
    GL = moduleC.GaussLegendre(-1, 1, nBins)
    moduleC.print_resultsGaussLegendre(function, GL, trueValue)

@execution_time
def test_GaussLegendre_py(function, nBins):
    result, _ = integrate.fixed_quad(function, -1, 1, n = nBins)
    print(f"The integration with SciPy gives {result}")


# Methods for computing the convergence order in C++ and in Python, decorated with execution time.
# Notice that they return the subintervals and the errors, in this way a plot with Matplotlib can be made

@execution_time
def computeConvergenceOrderTrapezoidal_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderTrapezoidal("cos(x)", 1.0)
    return subintervals, errors

@execution_time
def computeConvergenceOrderSimpson_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderSimpson("cos(x)", 1.0)
    return subintervals, errors

@execution_time
def computeConvergenceOrderGaussLegendre_cpp(function, exactIntegral):
    subintervals, errors = moduleC.computeConvergenceOrderGaussLegendre("cos(x)", 1.0)
    return subintervals, errors

# Since the Trapezoidal and the Simpson method have in common the arguments, write just one function
@execution_time
def computeConvergenceOrderTrapezoidal_Simpson_py(function, exactIntegral, method):
    # Lists for collecting convergence data
    subintervals = []
    errors = []
    
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
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")
    return subintervals, errors

@execution_time
def computeConvergenceOrderGaussLegendre_py(function, exactIntegral):
    # Lists for collecting convergence data
    subintervals = []
    errors = []
    
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
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")
    return subintervals, errors

# ex2 lab12
#try:
#    root = solver_complex.solve()
#    print(f"Approximate root: {root}")
#except RuntimeError as e:
#    print("Error: ", str(e))

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
    choice = input("Enter the corresponding number: ")

    # Switch case for Python
    match choice:
        case "0": # Exit loop if the user chooses 0
            break

        case "1":
            # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in cpp 
            moduleC.computeConvergenceOrderMidpoint("cos(x)", 1.0)

            # Define the function for the computation of the convergence order
            cos = np.vectorize(np.cos)

            subintervals_trap_cpp, errors_trap_cpp = computeConvergenceOrderTrapezoidal_cpp("cos(x)", 1.0)
            subintervals_trap_py, errors_trap_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.trapezoid)
            
            subintervals_simp_cpp, errors_simp_cpp = computeConvergenceOrderSimpson_cpp("cos(x)", 1.0)
            subintervals_simp_py, errors_simp_py = computeConvergenceOrderTrapezoidal_Simpson_py(cos, 1.0, integrate.simpson)
            
            # The order of convergence of two point methods is not computed: being 2 points it would be mathematically inconsistent
            
            subintervals_gl_cpp, errors_gl_cpp = computeConvergenceOrderGaussLegendre_cpp("cos(x)", 1.0)
            subintervals_gl_py, errors_gl_py = computeConvergenceOrderGaussLegendre_py(cos, 1.0)

            # Plot convergence for each method in both C++ and Python
            plt.plot(subintervals_trap_cpp, errors_trap_cpp, label = 'Trapezoidal Rule')
            plt.plot(subintervals_trap_py, errors_trap_py, label = 'PyTrapezoidal Rule')
            plt.plot(subintervals_simp_cpp, errors_simp_cpp, label = 'Simpson\'s Rule')
            plt.plot(subintervals_simp_py, errors_simp_py, label = 'PySimpson\'s Rule')
            plt.plot(subintervals_gl_cpp, errors_gl_cpp, label = 'Gauss-Legendre Quadrature')
            plt.plot(subintervals_gl_py, errors_gl_py, label = 'PyGauss-Legendre Quadrature')
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
            plt.show()

            break

        case "2":
            # Neither in SciPy nor in NumPy there's a midpoint integration method, so just compute it as in cpp 
            Midpoint_cpp("3*x+1", 2.5, 0, 1, 2)

            # In both SciPy's Trapezoidal and Simpson methods, you can provide the array
            # over which the function is sampled i.e. the nodes
            print("Compare the integration of x^3 in [0,1]")
            test_Trapezoidal_cpp("x^3", 0.25, 0, 1, 5) # trueValue = 0.25, nBins = 5
            nodesT = np.linspace(0, 1, num = 10) # array in [0,1] of size 5 like nBins of cpp
            test_Trapezoidal_py(nodesT**3, nodesT)

            print("Compare the integration of x^2 in [1,4]")
            test_Simpson_cpp("x^2", 21.0, 1, 4, 3) # trueValue = 21, nBins = 3
            nodesS = np.array([1, 3, 4]) # array in [1,4] of size 3 like nBins of cpp
            test_Simpson_py(nodesS**2, nodesS)

            print("Compare the integration of x^2 in [0,4]")
            test_twopointGauss_cpp("x^2", 64.0/3.0, 0, 4) # trueValue = 64/3 = 21.333
            test_twopoint_py(x2, 0, 4) # uses integrate.quad, see def above for more

            print("Compare the integration of x^4 in [-1,1]")
            test_GaussLegendre_cpp("x^4", 2.0/5.0, 11) # trueValue = 2/5 = 0.4, nBins = 11
            x4 = lambda x: x**4
            test_GaussLegendre_py(x4, 11)
            break

        case "3":
            #compute integrals
            break

        case _: # default case
            print("Invalid choice. Please choose a number between 1 and 3.")
            continue

    continueChoice = input("Do you want to perform another analysis? (1 for Yes, 0 for No): ")
