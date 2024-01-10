from moduleC import * # module created with pybind11
import scipy.integrate as integrate
from integrate import fixed_quad, trapezoid, simpson
import time # for the wrapper execution_time

def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start} seconds.")
        return result
    return wrapper

@execution_time
def test_GaussLegendre_cpp(function, trueValue, nBins):
    GL = moduleC.GaussLegendre(-1, 1, nBins)
    moduleC.print_resultsGaussLegendre(function, GL, trueValue)

@execution_time
def test_GaussLegendre_py(function, nBins):
    result, _ = integrate.fixed_quad(function, -1, 1, n = nBins)
    return result

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

    if choice == 0:
        break # Exit loop if the user chooses 0

    # Switch case for Python
    match choice:
        case "1":
            #convergence tests
            break

        case "2":
            #polynomial tests
            test_GaussLegendre_cpp("x^4", 0, 7)
            x4 = lambda x: x**4
            test_GaussLegendre_py(x4, 7)
            break

        case "3":
            #compute integrals
            break

        case _: # default case
            print("Invalid choice. Please choose a number between 1 and 3.")
            continue

    continueChoice = input("Do you want to perform another analysis? (1 for Yes, 0 for No): ")
