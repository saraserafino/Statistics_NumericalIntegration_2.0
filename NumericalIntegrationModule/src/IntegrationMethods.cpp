#include "../include/IntegrationMethods.hpp"
#include <iostream>
#include <cmath>


namespace MODULEC {
// Constructor of the abstract class
Quadrature::Quadrature(double a, double b, unsigned int nBins) : weights(nBins + 1), nodes(nBins + 1), a(a), b(b), nBins(nBins) {}
// For all the methods except the midpoint one, the number of nodes and weights is equal to the number of sub-intervals + 1
// because it has to include the beginning and the end of the interval.
// For this reason, in Quadrature they are initialized with the + 1

// These two methods simply return the weights and nodes that are computed in the derived classes of Quadrature
const std::vector<double>& Quadrature::get_weights() const {
    return weights;
}

const std::vector<double>& Quadrature::get_nodes() const {
    return nodes;
}

// Midpoint method
// For this method, the number of nodes and weights is the same as the number of sub-intervals
// because the points in which the function will be computed are the midpoints of each sub-interval.
// Having initialized them in Quadrature with (nBins + 1), here we resize them with nBins
Midpoint::Midpoint (double a, double b, unsigned int nBins) : Quadrature(a, b, nBins) {
    const double h = (b - a) / nBins; // length of subintervals
    // In Midpoint method the weights are all equal to h
    weights.assign(nBins, h);
    // Compute the nodes
    nodes.assign(nBins, h);
    nodes[0] = a + h / 2;
    for (unsigned int i = 1; i < nBins; ++i)
        nodes[i] += nodes[i - 1];
}

// Trapezoidal method
Trapezoidal::Trapezoidal (double a, double b, unsigned int nBins) : Quadrature(a, b, nBins) {
    const double h = (b - a) / nBins; // length of subintervals
    // In Trapezoidal method the weights are all equal to h
    // except for the endpoints which are h/2
    weights.assign(nBins + 1, h);
    weights[0] /= 2.0;
    weights[nBins] /= 2.0;
    // Compute the nodes
    for (unsigned int i = 0; i <= nBins; ++i)
        nodes[i] = a + i * h;
}

// Simpson's method
Simpson::Simpson (double a, double b, unsigned int nBins) : Quadrature(a, b, nBins) {
    const double h = (b - a) / nBins; // length of subintervals
    nodes.assign(nBins + 1, a);
    // In Simpson method the weights are h/3 at the endpoints
    weights.assign(nBins + 1, h / 3.0);
    for (unsigned int i = 1; i < nBins; i += 2) {
        // While at the interior points
        // For even indices the weight is 4 * h/3
        weights[i] *= 4.0;
        // For odd indices the weight is 2 * h/3
        weights[i + 1] *= 2.0;
        // Compute nodes in the same for-cycle to optimize speed
        nodes[i] += (i * h);
        nodes[i + 1] += ( (i + 1) * h);
    }
    // When nBins odd, these nodes aren't computed in the above for-cycle
    nodes[nBins - 1] = b - h;
    nodes[nBins] = b;
    // When nBins even, the last weight is wrongly computed in the above for-cycle
    weights[nBins] = h / 3.0;
}

// Two point Gauss quadrature formula
// Since it's two points, nBins = 2 by default and there are only 2 nodes and 2 weights
twopointGauss::twopointGauss (double a, double b, unsigned int n) : Quadrature(a, b, 2) {
    // This method is valid for integrals over [-1,1] so
    // it must be rescaled for integrals over [a,b]
    if (a == -1 && b == 1) {
        // In [-1,1] the two weights have value 1
        // and the nodes -+ 1/sqrt(3)
        weights.assign(2, 1.0);
        nodes.assign(2, 1.0 / std::sqrt(3.0));
        nodes[0] *= -1;
    } else {
        // In [a,b] the two weights have value h
        // and the nodes -+ h/sqrt(3) + (a+b)/2
        const double h = (b - a) / 2.0; // length of subintervals
        weights.assign(2, h);
        // Compute nodes
        nodes.assign(2, (a + b) / 2.0);
        const double rescale = h / std::sqrt(3.0);
        nodes[0] += -rescale;
        nodes[1] += rescale;
    }
}

// Gauss-Legendre quadrature formula
GaussLegendre::GaussLegendre (double a, double b, unsigned int nBins) : Quadrature(a, b, nBins) {
    double NRratio; // Newton-Raphson ratio
    const double k = M_PI / (nBins + 0.5); // constant k
    for(unsigned int i = 0; i <= nBins; i++) {
        // Compute nodes
        nodes[i] = cos(k * (i - 0.25));
        Result result = calculatePolynomialValueAndDerivative(nodes[i], nBins);

        do {
            NRratio = result.value/result.derivative;
            nodes[i] -= NRratio;
            result = calculatePolynomialValueAndDerivative(nodes[i], nBins);
        } while (fabs(NRratio) > EPSILON);
        // fabs is float absolute value
        // EPSILON is defined as private in the header file
        
        // Compute weights
        weights[i] = 2.0 / ((1 - nodes[i] * nodes[i]) * result.derivative * result.derivative);
    }
}

// Since the computation of the approximate integral is different, we need these
GaussLegendre::Result GaussLegendre::calculatePolynomialValueAndDerivative(double x, unsigned int nBins) {
    Result result(x, 0);
    double value_minus_1 = 1;
    const double c = 1 / (x * x - 1);
    for(unsigned int i = 2; i <= nBins; i++) {
        const double value = ((2 * i - 1) * x * result.value - (i - 1) * value_minus_1) / i;
        result.derivative = i * c * (x * value - result.value);
        value_minus_1 = result.value;
        result.value = value;
    }
    return result;
}

const double& GaussLegendre::get_a() const {
    return a;
}

const double& GaussLegendre::get_b() const {
    return b;
}

} // end of namespace