#ifndef STATOP_HPP_
#define STATOP_HPP_

#include "DataHandler.hpp"
#include <iostream>
#include <fstream> // for std::ifstream and std::ofstream
#include <vector>
#include <string>
#include <algorithm>
#include <optional> // for std::optional
#include <variant> // for std::variant

#pragma once
namespace MODULEA {

class StatOp {
public:
    // Constructor
    StatOp(const std::string &input_targetColumn);

    std::vector<std::optional<std::variant<double, std::string>>> readSpecificColumn(const std::shared_ptr<CSVHandler> CSVfile, const std::string &targetColumn);

    double calculateMean(const std::vector<std::optional<std::variant<double, std::string>>> &data);
    std::variant<double, std::string> calculateMedian(const std::vector<std::optional<std::variant<double, std::string>>> &data);
    double calculateStandardDeviation(const std::vector<std::optional<std::variant<double, std::string>>> &data);
    double calculateVariance(const std::vector<std::optional<std::variant<double, std::string>>> &data);
    std::string calculateFrequency(const std::vector<std::optional<std::variant<double, std::string>>> &data);
    std::string calculateClassification(const std::shared_ptr<CSVHandler> CSVfile, const std::string &targetColumn, const std::string &condition);
    double calculateCorrelation(const std::vector<std::optional<std::variant<double, std::string>>> &data1, const std::vector<std::optional<std::variant<double, std::string>>> &data2);

    // Destructor
    ~StatOp() {};
private:
    const std::string &targetColumn;
};
} // end of namespace

#endif // STATOP_HPP_