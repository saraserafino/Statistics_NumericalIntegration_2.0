#include "../include/IntegrationMethods.hpp"
#include "../include/IntegrationMethods_py.hpp"
#include "../include/moduleCfunctions.hpp"

#include <pybind11/pybind11.h>

// Wrap as Python module

PYBIND11_MODULE(moduleCfunctions, m) {
    m.doc() = "pybind11 moduleCfunctions plugin";

    m.def("evaluate", &evaluate, "Evaluate muparserx expression");
    
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

    m.def("analysis", &analysis, "Compute the analysis of the datas");

    m.def("print_resultsMidpoint", &print_results<Midpoint>);
    m.def("print_resultsTrapezoidal", &print_results<Trapezoidal>);
    m.def("print_resultsSimpson", &print_results<Simpson>);
    m.def("print_resultstwopointGauss", &print_results<twopointGauss>);
    m.def("print_resultsGaussLegendre", &print_results<GaussLegendre>);
}
