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
def test_GaussLegendre_cpp(function, a, b):
    return moduleC.IntegrateGaussLegendre(function, method)

@execution_time
def test_GaussLegendre_py(function, a, b):
    return integrate.fixed_quad(function, method)

n = 1000
A = np.random.randint(0, 1001, size=(n, n))
B = np.random.randint(0, 1001, size=(n, n))

test_GaussLegendre_cpp(function, a, b)
test_GaussLegendre_py(function, a, b)

# ex2 lab12
#try:
#    root = solver_complex.solve()
#    print(f"Approximate root: {root}")
#except RuntimeError as e:
#    print("Error: ", str(e))