#ifndef INTEGRATION_METHODS_HPP_
#define INTEGRATION_METHODS_HPP_

#include <iostream>
#include <vector>

#pragma once
namespace MODULEC {

// Abstract class to initializing quadrature methods and returning weights and nodes
class Quadrature {
public:
    Quadrature(double a, double b, unsigned int nBins); // Constructor
    const std::vector<double>& get_weights() const;
    const std::vector<double>& get_nodes() const;
    virtual ~Quadrature() {}; // Virtual destructor

protected:
std::vector<double> weights;
std::vector<double> nodes;
double a; // starting point
double b; // ending point
unsigned int nBins; // number of bins i.e. of sub-intervals
};

// Midpoint method

class Midpoint : public Quadrature {
public:
    Midpoint (double a, double b, unsigned int nBins);
    ~Midpoint() {}; // Default destructor
};

// Trapezoidal method

class Trapezoidal : public Quadrature {
public:
    Trapezoidal (double a, double b, unsigned int nBins);
    ~Trapezoidal() {}; // Default destructor
};

// Simpson's method

class Simpson : public Quadrature {
public:
    Simpson (double a, double b, unsigned int nBins);
    ~Simpson() {}; // Default destructor
};

// Two point Gauss quadrature formula

class twopointGauss : public Quadrature {
public:
    twopointGauss (double a, double b, unsigned int nBins);
    ~twopointGauss() {}; // Default destructor
};

// Gauss-Legendre quadrature formula

class GaussLegendre : public Quadrature {
public:
    GaussLegendre (double a, double b, unsigned int nBins);
    ~GaussLegendre() {}; // Default destructor
    // For Gauss-Legendre integration we also need these
    const double& get_a() const;
    const double& get_b() const;

    struct Result {
        double value;
        double derivative;
        Result(): value(0), derivative(0) {}
        Result(double val, double deriv) : value(val), derivative(deriv) {}
    };

    Result calculatePolynomialValueAndDerivative(double x, unsigned int nBins);

private:
    const double EPSILON = 1e-15;
};

} // end of namespace
#endif // INTEGRATION_METHODS_HPP_
