import moduleC # module created with pybind11
import numpy as np
import scipy.integrate as integrate
from scipy.integrate import trapezoid, simpson, quad, fixed_quad
import time # for the wrapper execution_time

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
            moduleC.computeConvergenceOrderMidpoint("cos(x)", 1.0)
            moduleC.computeConvergenceOrderTrapezoidal("cos(x)", 1.0)
            moduleC.computeConvergenceOrderSimpson("cos(x)", 1.0)
            moduleC.computeConvergenceOrderGaussLegendre("cos(x)", 1.0)
            break

        case "2":
            # Nota per me stessa: quelli con Py li ho controllati tutti con jupyter notebook e vanno bene

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