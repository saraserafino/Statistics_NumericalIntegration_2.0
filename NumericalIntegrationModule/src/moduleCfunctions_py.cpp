#include "../include/IntegrationMethods.hpp"
#include "../include/IntegrationMethods_py.hpp"
#include "../include/moduleCfunctions.hpp"
#include <iostream>
#include <typeinfo> // for typeid, otherwise the program is ill-formed
#include "boost/type_index.hpp" // for boost::typeindex::type_id<T>().pretty_name()
#include <cmath>
#include <functional>
#include <iomanip>

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

// Qui cambia GaussLegendre

// Wrap the GaussLegendre method in C++ with SciPy

// Import SciPy
/* questo era quanto detto sul sito di pybind
py::object scipy = py::module_::import("scipy");
return scipy.attr("__version__");
*/

// Import the scipy.integrate module
py::module scipyInt = py::module::import("scipy.integrate");
// Access the specific function for Gauss-Legendre
py::object GaussL = scipyInt.attr("fixed_quad");
// Call it with some example arguments
py::object result = GaussL(function, a, b);
// calcolo direttamente senza passare per pesi e nodi



PYBIND11_MODULE(moduleCfunctions, m) {
    m.doc() = "pybind11 moduleCfunctions plugin";

    m.def("evaluate", &evaluate);
    
    // Explicit instantion of the template methods for each derived class
    m.def("IntegrateMidpoint", &Integrate<Midpoint>);
    m.def("IntegrateTrapezoidal", &Integrate<Trapezoidal>);
    m.def("IntegrateSimpson", &Integrate<Simpson>);
    m.def("IntegratetwopointGauss", &Integrate<twopointGauss>);
    m.def("IntegrateGaussLegendre", &Integrate<GaussLegendre>);

    m.def("computeConvergenceOrderMidpoint", &computeConvergenceOrder<Midpoint>);
    m.def("computeConvergenceOrderTrapezoidal", &computeConvergenceOrder<Trapezoidal>);
    m.def("computeConvergenceOrderSimpson", &computeConvergenceOrder<Simpson>);
    m.def("computeConvergenceOrdertwopointGauss", &computeConvergenceOrder<twopointGauss>);
    m.def("computeConvergenceOrderGaussLegendre", &computeConvergenceOrder<GaussLegendre>)

    m.def("analysis", &analysis);

    m.def("print_resultsMidpoint", &print_results<Midpoint>);
    m.def("print_resultsTrapezoidal", &print_results<Trapezoidal>);
    m.def("print_resultsSimpson", &print_results<Simpson>);
    m.def("print_resultstwopointGauss", &print_results<twopointGauss>);
    m.def("print_resultsGaussLegendre", &print_results<GaussLegendre>);
}
