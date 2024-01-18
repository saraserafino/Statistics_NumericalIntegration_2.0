#include "IntegrationMethods.hpp"
#include "moduleCfunctions.hpp"
#include <iostream>
#include <typeinfo> // for typeid, otherwise the program is ill-formed
#include "boost/type_index.hpp" // for boost::typeindex::type_id<T>().pretty_name()
#include <cmath>
#include <functional>
#include <iomanip>

using namespace MODULEC;

// Define the function to evaluate in point y
mup::Value evaluate(double y, mup::ParserX& parser) {
    // Remove any existing variable x to ensure a clean slate
    parser.RemoveVar("x");
    // Create variable x with value a
	mup::Value x(y);
    parser.DefineVar("x", mup::Variable(&x));
    // Evaluate the expression
    return parser.Eval();
};

// Function to integrate for whichever method
template<typename T>
double Integrate(const std::string& function, const T& method) {
    static_assert(std::is_base_of<Quadrature, T>::value, "T must be derived from Quadrature.");

    // Create the parser instance
    mup::ParserX parser;
    // Set the expression
    parser.SetExpr(function);

    double sum = 0;
    // Get nodes and weights of the used Numerical Integration method
    const std::vector<double> weights = method.get_weights();
    const std::vector<double> nodes = method.get_nodes();
    // Evaluate the expression at the current node
    for (unsigned int i = 0; i < weights.size(); ++i) {
        double ev = evaluate(nodes[i], parser);
        sum += ev * weights[i];
    }
    return sum;
};

// When T is GaussLegendre, this version is invoked
template<>
double Integrate<GaussLegendre>(const std::string& function, const GaussLegendre& method) {
    // Create the parser instance
    mup::ParserX parser;
    // Set the expression
    parser.SetExpr(function);

    double sum = 0;
    // Get nodes and weights of the Gauss-Legendre method
    const std::vector<double> weights = method.get_weights();
    const std::vector<double> nodes = method.get_nodes();

    // Get the integration extremes of the Gauss-Legendre method
    const double a = method.get_a();
    const double b = method.get_b();

    const double width = (b - a) * 0.5;
    const double mean = (a + b) * 0.5;
    // Evaluate the expression at the current node until the number
    // of subintervals nodes.size() = weights.size() = n
    for(unsigned int i = 0; i <= weights.size(); i++) {
        double ev = evaluate(width * nodes[i] + mean, parser);
        sum += weights[i] * ev;
    }
    return sum * width;
}
    
template <typename QuadratureMethod>
std::tuple<std::vector<double>, std::vector<double>> computeConvergenceOrder(const std::string& function, const double exactIntegral) {
    static_assert(std::is_base_of<Quadrature, QuadratureMethod>::value, "QuadratureMethod must be derived from Quadrature.");
    // Vectors for collecting convergence data
    std::vector<double> errors;
    std::vector<double> orders;

    // Create the parser instance
    mup::ParserX parser;
    // Set the expression
    parser.SetExpr(function);
    const double a = 0.0;  // Lower limit of integration
    const double b = M_PI / 2.0;  // Upper limit of integration

    //std::cout << "Convergence order:\n";
    // Initialize outside the loop
    double previousError = 1.0;

    for (unsigned int nBins = 2; nBins <= 1024; nBins *= 2) {
        QuadratureMethod method(a, b, nBins);
        double numericalIntegral = Integrate(function, method);

        // Compare with the exact integral
        double error = std::abs(numericalIntegral - exactIntegral);

        // Compute convergence order
        auto log_error = log(error);
        auto log_previous_error = log(previousError);
        auto order = (log_error - log_previous_error) / (log(2));

        // Collect convergence data
        errors.push_back(error);
        orders.push_back(-order);

        // Output the error and convergence order
        //std::cout << "  Subintervals: " << std::setw(4) << nBins
        //          << "  Error: " << std::scientific << std::setprecision(6) << error;

        //if (nBins > 2) {
        //    std::cout << "  Order: " << std::fixed << std::setprecision(2) << -order;
        //}
        //std::cout << "\n";

        previousError = error;
    }
    //std::cout << "\n";
    return std::make_tuple(errors, orders);
};

// When using np.polynomial.leggauss, the integration interval is [-1,1] so this is different:
template <>
std::tuple<std::vector<double>, std::vector<double>> computeConvergenceOrder<GaussLegendre>(const std::string& function, const double exactIntegral) {
    // Vectors for collecting convergence data
    std::vector<double> errors;
    std::vector<double> orders;

    // Create the parser instance
    mup::ParserX parser;
    // Set the expression
    parser.SetExpr(function);

    double previousError = 1.0;

    for (unsigned int nBins = 2; nBins <= 1024; nBins *= 2) {
        GaussLegendre method(-1, 1, nBins);
        double numericalIntegral = Integrate(function, method);

        // Compare with the exact integral
        double error = std::abs(numericalIntegral - exactIntegral);

        // Compute convergence order
        auto log_error = log(error);
        auto log_previous_error = log(previousError);
        auto order = (log_error - log_previous_error) / (log(2));

        // Collect convergence data
        errors.push_back(error);
        orders.push_back(-order);

        previousError = error;
    }
    //std::cout << "\n";
    return std::make_tuple(errors, orders);
};

// Analize the results
void analysis (const double integration_value, const double true_value) {
    std::cout << "True value: " << true_value << std::endl;
    const double error = std::abs(true_value - integration_value);
    const double abserror = std::abs(error / true_value) * 100;
    const double tolerance = std::pow(10, -15);
    if (error < tolerance) {
        std::cout << "Error: 0.000000e+00" << std::endl;
        std::cout << "Absolute relative error: 0.000000e+00 %\n\n";
    } else {
        std::cout <<"Error: " << std::scientific << std::setprecision(6) << error << std::endl;
        std::cout << "Absolute relative error: " <<std::scientific << std::setprecision(6) << abserror << " %\n\n";
    }
};

// Function that prints the results of integration and analysis for whichever method
template<typename T>
void print_results (const std::string& function, const T& method, const double true_value) {
    try {
        const double integration_value = Integrate(function, method);
        std::cout << "Integration with the "
        << boost::typeindex::type_id<T>().pretty_name() << " method." << std::endl;

        std::cout << "Result: " << std::scientific << std::setprecision(6) << integration_value << std::endl;

        analysis(integration_value, true_value);
    } catch (const mup::ParserError& e) {
        std::cout << "Parser error: " << e.GetMsg() << std::endl;
    }
};