#ifndef INTEGRATION_METHODS_PY_HPP_
#define INTEGRATION_METHODS_PY_HPP_

#include "IntegrationMethods.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// ----------------------------------
// Python interface - fake trampoline
// ----------------------------------

class PyQuadrature : public Quadrature {
public:
    // Inherit the constructors
    using Quadrature::Quadrature;

    // Each virtual function needs a trampoline, but there isn't any
};

// Use template for defining the derived classes

template <class QuadratureMethod> : public Quadrature {
public:
    // Inherit the constructors of the base class
    using Quadrature::Quadrature;
};
template <class PyQuadratureMethod> : public QuadratureMethod {
public:
    // Inherit the constructors of each derived class
    using QuadratureMethod::QuadratureMethod;
};

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

class Quadrature:
    def __init__(self, a, b, nBins):
        self.weights = [0.0] * (nBins + 1)
        self.nodes = [0.0] * (nBins + 1)
        self.a = a
        self.b = b
        self.nBins = nBins

// When defining a custom constructor in a derived Python class,
// you must explicitly call the bound C++ constructor using __init__

class Midpoint(Quadrature):
    def __init__(self, a, b, nBins):
        Quadrature.__init__(self) // Without this, a TypeError is raised

class Trapezoidal(Quadrature):
    def __init__(self, a, b, nBins):
        Quadrature.__init__(self)

class Simpson(Quadrature):
    def __init__(self, a, b, nBins):
        Quadrature.__init__(self)

class twopointGauss(Quadrature):
    def __init__(self, a, b, nBins):
        Quadrature.__init__(self)
        self.nBins = 2 // because it's "two point"

// GaussLegendre is better implemented with NumPy
// Import the numpy.polynomial.legendre module
py::module npLeg = py::module::import("numpy.polynomial.legendre");
// Access the specific function for Gauss-Legendre
py::object npGaussLeg = npLeg.attr("leggauss");
// Note: it can only compute nodes and weights in [-1,1]

class GaussLegendre(Quadrature):
    def __init__(self, a, b, nBins):
        Quadrature.__init__(self)
        // Call numpy.polynomial.legendre.leggauss
        py::object nodes_weights = npGaussLeg(nBins - 1);
        self.nodes,self.weights = nodes_weights

    def get_a(self):
        return a

    def get_b(self):
        return b

#endif // INTEGRATION_METHODS_PY_HPP_