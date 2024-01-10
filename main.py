import moduleC # module created with pybind11
import numpy as np
import math # for pi
import scipy.integrate as integrate
from scipy.integrate import trapezoid, simpson, quad, fixed_quad
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

# Methods for computing the convergence order in Python

@execution_time
def computeConvergenceOrderTrapezoidal_py(function, exactIntegral):
    # Initialize previous error outside the loop
    previousError = 1.0
    upperbound = math.pi / 2.0
    nBins = 2
    while nBins <= 1024:
        nodes = np.linspace(0, upperbound, num = nBins)
        f = function(nodes)
        numericalIntegral = integrate.trapezoid(f, nodes)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        log_error = math.log(error)
        log_previousError = math.log(previousError)

        p = (log_error - log_previousError) / math.log(2)
        # Output the error and convergence order
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")

@execution_time
def computeConvergenceOrderSimpson_py(function, exactIntegral):
    # Initialize previous error outside the loop
    previousError = 1.0
    upperbound = math.pi / 2.0
    nBins = 2
    while nBins <= 1024:
        nodes = np.linspace(0, upperbound, num = nBins)
        f = function(nodes)
        numericalIntegral = integrate.simpson(f, nodes)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        log_error = math.log(error)
        log_previousError = math.log(previousError)

        p = (log_error - log_previousError) / math.log(2)
        # Output the error and convergence order
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")

@execution_time
def computeConvergenceOrderTwopoint_py(function, exactIntegral):
    # Lower and upper bounds
    a = 0.0
    b = math.pi / 2.0
    # Initialize previous error outside the loop
    previousError = 1.0
    nBins = 2
    while nBins <= 1024:
        numericalIntegral, _ = integrate.quad(function, a, b)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        log_error = math.log(error)
        log_previousError = math.log(previousError)

        p = (log_error - log_previousError) / math.log(2)
        # Output the error and convergence order
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")

@execution_time
def computeConvergenceOrderGaussLegendre_py(function, exactIntegral):
    # Initialize previous error outside the loop
    previousError = 1.0
    nBins = 2
    while nBins <= 1024:
        numericalIntegral, _ = integrate.fixed_quad(function, -1, 1, n = nBins)

        # Compare with the exact integral
        error = abs(numericalIntegral - exactIntegral)

        log_error = math.log(error)
        log_previousError = math.log(previousError)

        p = (log_error - log_previousError) / math.log(2)
        # Output the error and convergence order
        print(f"    Subintervals: {nBins:4d}    Error: {error:.6e}", end='')

        if nBins > 2:
            print(f"    Order: {-p:.2f}", end='')
        
        print("\n")

        previousError = error
        nBins *= 2

    print("\n")

# Wrap the computation of the convergence order in C++ for its execution time
    
@execution_time
def computeConvergenceOrderTrapezoidal_cpp(function, exactIntegral):
    return moduleC.computeConvergenceOrderTrapezoidal("cos(x)", 1.0)

@execution_time
def computeConvergenceOrderSimpson_cpp(function, exactIntegral):
    return moduleC.computeConvergenceOrderSimpson("cos(x)", 1.0)

@execution_time
def computeConvergenceOrderTwopointGauss_cpp(function, exactIntegral):
    return moduleC.computeConvergenceOrderTwopointGauss("cos(x)", 1.0)

@execution_time
def computeConvergenceOrderGaussLegendre_cpp(function, exactIntegral):
    return moduleC.computeConvergenceOrderGaussLegendre("cos(x)", 1.0)

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

            cos = np.vectorize(np.cos)

            computeConvergenceOrderTrapezoidal_cpp("cos(x)", 1.0)
            computeConvergenceOrderTrapezoidal_py(cos, 1.0)
            
            computeConvergenceOrderSimpson_cpp("cos(x)", 1.0)
            computeConvergenceOrderSimpson_py(cos, 1.0)
            
            computeConvergenceOrderTwopointGauss_cpp("cos(x)", 1.0)
            computeConvergenceOrderTwopoint_py(cos, 1.0)
            
            computeConvergenceOrderGaussLegendre_cpp("cos(x)", 1.0)
            computeConvergenceOrderGaussLegendre_py(cos, 1.0)
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
