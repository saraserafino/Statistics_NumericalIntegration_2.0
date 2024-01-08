#ifndef MODULE_C_FUNCTIONS_HPP_
#define MODULE_C_FUNCTIONS_HPP_

#include "muparserx/mpParser.h"
#include "IntegrationMethods.hpp"
#include <iostream>

using namespace MODULEC;

// Function to evaluate in point a
mup::Value evaluate(double y, mup::ParserX& parser);

// Function to integrate for whichever method
template<typename T>
double Integrate(const std::string& function, const T& method);

// When T is GaussLegendre, this version is invoked
template<>
double Integrate<GaussLegendre>(const std::string& function, const GaussLegendre& method);

template <typename QuadratureMethod>
void computeConvergenceOrder(const std::string& function, const double exactIntegral);

// Analize the results
void analysis (const double integration_value, const double true_value);

// Function that prints the results of integration and analysis for whichever method
template<typename T>
void print_results (const std::string& function, const T& method, const double true_value);

#include "moduleCfunctions.tpl.hpp"

#endif // MODULE_C_FUNCTIONS_HPP_