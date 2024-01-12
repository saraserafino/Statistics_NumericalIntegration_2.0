#ifndef INTEGRATION_METHODS_PY_HPP_
#define INTEGRATION_METHODS_PY_HPP_

#include "IntegrationMethods.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// porta queste cose nel file di pybind

// ----------------------------------
// Python interface - fake trampoline
// ----------------------------------

class PyQuadrature : public MODULEC::Quadrature {
public:
    // Inherit the constructors
    using MODULEC::Quadrature::Quadrature;

    // Each virtual function needs a trampoline, but there isn't any
};

// Use template for defining the derived classes
/*
template <class QuadratureMethod> : public MODULEC::Quadrature {
public:
    // Inherit the constructors of the base class
    using MODULEC::Quadrature::Quadrature;
};
template <class PyQuadratureMethod> : public QuadratureMethod {
public:
    // Inherit the constructors of each derived class
    using QuadratureMethod::QuadratureMethod;
};
*/
#endif // INTEGRATION_METHODS_PY_HPP_