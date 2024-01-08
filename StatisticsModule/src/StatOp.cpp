#include "../include/StatOp.hpp"
#include "../include/DataHandler.hpp"
#include <iostream>
#include <fstream> // for std::ifstream and std::ofstream
#include <vector>
#include <sstream>
#include <string>
#include <map>
#include <limits>
#include <algorithm>
#include <optional> // for std::optional
#include <variant> // for std::variant
#include <stdexcept>
#include <iomanip>
#include "boost/optional.hpp"
#include "boost/variant.hpp"
#include "boost/accumulators/accumulators.hpp"
#include "boost/accumulators/statistics.hpp"

#define assertm(exp, msg) assert(((void)msg, exp))

namespace MODULEA {

    namespace ba = boost::accumulators;

    // Constructor
    StatOp::StatOp(const std::shared_ptr<CSVHandler> CSVfile) : CSVfile(CSVfile), data(CSVfile->readData()) {};

    std::vector<csvType> StatOp::readSpecificColumn(const std::shared_ptr<CSVHandler> CSVfile, const std::string &targetColumn) {
        // Get the name of the input file
        const std::string file_name = CSVfile->get_input_file_path();
        // Open the CSV file in input mode
        std::fstream file(file_name, std::ios::in);

        std::vector<std::optional<std::variant<double, std::string>>> content;
        std::string line, word;

        int index = CSVfile->read_header(targetColumn);
        if (index == -1) // Handle the case where the header row is not found
            return content;

        // Ignore the header line
        getline(file, line);

        while (getline(file, line)) {
            std::stringstream str(line);
            int j = 0;
            while (getline(str, word, ',')) {
                if (j == index) {
                    // Try to convert the word to double,
                    try { // add as double if successful
                        content.push_back(std::stod(word));
                    } catch (const std::invalid_argument &) {
                        // otherwise add as string
                        content.push_back(word);
                    }
                }
                j++;
            }
        }
        return content;
    };

    double StatOp::calculateMean(const std::vector<std::optional<std::variant<double, std::string>>> &data) {
        ba::accumulator_set<double, ba::stats<ba::tag::mean>> acc;

        for (const auto &value: data) {
            // value.index()==0 means the first element of std::variant i.e. double
            if (value && value.value().index() == 0) {
                acc(std::get<double>(value.value()));
            } else {
                // If the index of value is a string, throw an exception
                throw std::invalid_argument("Cannot calculate mean for a string.");
            }
        }

        // If there are no valid double values, return an exception
        if (data.empty()) {
            throw std::invalid_argument("Data is empty.");
        } else { // otherwise compute the mean
            return ba::mean(acc);
        }
    };

// The function calculateMedian computes the median of a vector of optional variants, where each variant
// can hold either a double or a string. The function filters out the empty optionals and creates a sorted
// vector (sortedData) based on the index of the variants. If the size of the sorted data is even, it checks
// whether the two middle elements are both of type double, and if so, returns their average. Otherwise,
// it returns the middle element. If the size is odd, it directly returns the middle element.
    std::variant<double, std::string>
    StatOp::calculateMedian(const std::vector<std::optional<std::variant<double, std::string>>> &data) {

        // Creating a copy of the original data to sort
        std::vector<std::variant<double, std::string>> sortedData;

        // Filtering out empty optionals and copying the rest to sortedData
        for (const auto &item: data) {
            if (item)
                sortedData.push_back(item.value());
        }

        // Sorting the data based on the index of the variant
        std::sort(sortedData.begin(), sortedData.end(), [](const auto &a, const auto &b) {
            if (a.index() == 0 && b.index() == 0) {
                return std::get<double>(a) < std::get<double>(b);
            } else if (a.index() == 1 && b.index() == 1) {
                return std::get<std::string>(a) < std::get<std::string>(b);
            } else {
                // If they're different types, sort by index
                return a.index() < b.index();
            }
        });

        size_t size = sortedData.size();

        if (size % 2 == 0) {
            if (sortedData[size / 2 - 1].index() == 0 && sortedData[size / 2].index() == 0) {
                return (std::get<double>(sortedData[size / 2 - 1]) + std::get<double>(sortedData[size / 2])) / 2.0;
            } else {
                return sortedData[size / 2];
            }
        } else {
            return sortedData[size / 2];
        }
    };

    double
    StatOp::calculateStandardDeviation(const std::vector<std::optional<std::variant<double, std::string>>> &data) {
        return std::sqrt(calculateVariance(data));
    };

// Calculate the variance of a vector containing variants of double or string
    double StatOp::calculateVariance(const std::vector<std::optional<std::variant<double, std::string>>> &data) {
        ba::accumulator_set<double, ba::stats<ba::tag::variance>> acc;

        // Iterate through the data
        for (const auto &value: data) {
            if (value) {
                // Check if the variant holds a double value
                if (value.value().index() == 0) {
                    // Extract the double value
                    acc(std::get<double>(value.value()));
                } else if (value.value().index() == 1) {
                    // If the index of value is a string, throw an exception
                    throw std::invalid_argument("Variance can't be calculatedfor a string.");
                }
            }
        }

        // Check if there are valid double values in the data
        if (data.empty()) {
            // If there are no valid double values, return an exception
            throw std::invalid_argument("Data is empty.");
        } else {
            return ba::variance(acc); //variance
        }
    };

/*
 * Calculate the frequency of values in a vector of std::variant<double, std::string>.
 *
 * This function takes a vector of std::variant<double, std::string> and calculates
 * the frequency of each unique value in the vector.
 *
 * The input vector containing std::variant values.
 * A string representation of the frequencies, formatted as "value: frequency times".
 */
    std::string StatOp::calculateFrequency(const std::vector<std::optional<std::variant<double, std::string>>> &data) {
        // Map to store the frequency of each unique value
        std::map<std::optional<std::variant<double, std::string>>, size_t> frequencyMap;

        // Count the frequency of each value in the input vector
        for (const auto &value: data) {
            frequencyMap[value]++;
        }

        // String to store the result
        std::ostringstream result;

        // Iterate through the frequency map and construct the result string
        for (const auto &entry: frequencyMap) {
            // Check the type of the variant and construct the output accordingly
            if (entry.first && entry.first.value().index() == 0) {
                // If the variant holds a double, convert and append to the result
                result << std::setw(5) << std::setprecision(std::numeric_limits<double>::digits10)
                       << std::get<double>(entry.first.value()) << ":" << std::setw(10) << entry.second << " times\n";
            } else if (entry.first && entry.first.value().index() == 1) {
                // If the variant holds a string, append to the result
                result << std::get<std::string>(entry.first.value()) << ":" << std::setw(10) << entry.second << " times\n";
            }
        }

        // Return the final result string
        return result.str();
    };

// This function is a program that selects a column and retrieves players
// (elements from the first column) that meet a specified condition. 
// For example, if the column represents age and the condition is 23,
// the program selects players with the age of 23.
    std::string
    StatOp::calculateClassification(const std::string &targetColumn,
                                    const std::string &condition) {
        // Get the name of the input file
        const std::string file_name = CSVfile->get_input_file_name();
        // Open the CSV file in input mode
        std::fstream file(file_name, std::ios::in);

        // Variables to read lines and words from the file
        std::string line, word;

        // Get the index of the target column (header row)
        int index = CSVfile->read_header(this->targetColumn);

        // String to store the result
        std::ostringstream result;

        // Check if the target column is found in the header
        if (index == -1) {
            // Handle the case where the header row is not found
            throw std::invalid_argument("Target not found.");
        }

        // Ignore the header line
        getline(file, line);

        // Loop through each line in the CSV file
        while (getline(file, line)) {
            // Use a string stream to parse each line
            std::stringstream str(line);

            // Variables to store player name and column index
            std::string player_name;
            int j = 0;

            // Loop through each word (cell) in the line
            while (getline(str, word, ',')) {

                // If it's the second column, store player_name
                if (j == 1)
                    player_name = word;

                // Check if it's the target column
                if (j == index) {
                    // If the condition is met, append player_name to result
                    if (word == condition)
                        result << player_name << "\n";
                }
                j++;
            }
        }

        // Return the result as a string
        return result.str();
    };

    double StatOp::calculateCorrelation(const std::vector<std::optional<std::variant<double, std::string>>> &data1,
                                        const std::vector<std::optional<std::variant<double, std::string>>> &data2) {
        if (data1.empty() || data2.empty()) {
            throw std::invalid_argument("Data is empty.");
        }
        // Check of vector dimension
        if (data1.size() != data2.size()) {
            throw std::invalid_argument("Vectors don't have the same dimension.");
        }

        double mean1 = calculateMean(data1);
        double mean2 = calculateMean(data2);

        double numerator = 0;

        // Compute the numerator
        for (size_t i = 0; i < data1.size(); i++) {
            if (data1[i] && data2[i]) {
                if (data1[i].value().index() == 0 && data2[i].value().index() == 0) {
                    // If the indices of both the values are of type double
                    numerator +=
                            (std::get<double>(data1[i].value()) - mean1) * (std::get<double>(data2[i].value()) - mean2);
                } else {
                    // If the index of value is a string, throw an exception
                    throw std::invalid_argument("Correlation can't be calculated for a string.");
                }
            }
        }

        double dev1 = calculateStandardDeviation(data1);
        double dev2 = calculateStandardDeviation(data2);

        // Check that divisor are not null
        if (dev1 == 0 || dev2 == 0) {
            std::cerr << "Error: standard deviation is zero. Impossible to compute the correlation." << std::endl;
            throw std::invalid_argument("Error: zero deviation standard. Impossible to compute the correlation.");
        }

        // Compute correlation
        return numerator / (dev1 * dev2 * data1.size());
    };

    const std::vector<std::optional<std::variant<double, std::string>>>& StatOp::getColumn(const std::string columnName) const {
        int index = CSVfile->read_header(columnName);
        if(index == -1){
            return data[0];
        }
        return data[index];
    }

    std::vector<std::vector<csvType>>::const_iterator StatOp::begin() {
        return data.begin();
    }

    std::vector<std::vector<csvType>>::const_iterator StatOp::end() {
        return data.end();
    }

} // end of namespace