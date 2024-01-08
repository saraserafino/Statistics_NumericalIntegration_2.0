#include <iostream>
#include <vector>
#include <iomanip>

#if USE_MODULEA
    #include "../StatisticsModule/include/StatOp.hpp"
    #include "../StatisticsModule/include/DataHandler.hpp"
    #include <optional>
    #include <variant>
    #include <fstream>
    #include <algorithm>
    #include <string>
    using namespace MODULEA;
#endif

#if USE_MODULEC
    #include "../NumericalIntegrationModule/include/IntegrationMethods.hpp"
    #include "../NumericalIntegrationModule/include/moduleCfunctions.hpp"
    #include "muparserx/mpParser.h"
    #define assertm(exp, msg) assert(((void)msg, exp))
    using namespace MODULEC;
#endif

int main() {
    #if USE_MODULEA

    // File path
    const std::string input_file_path = "../data/player_data_03_22.csv";
    // Create shared pointer
    const std::shared_ptr<CSVHandler> CSVfile = std::make_shared<CSVHandler>(input_file_path);

    StatOp analysis(CSVfile);

    std::vector<std::string> headerNames = CSVfile->getHeader();

    std::cout << "Some statistics about the players:\n";
    std::cout << std::setw(14) << std::left << "Column name"
            << std::setw(8) << std::left << "Mean"
            << std::setw(8) << std::left << "Standard Deviation" << std::endl;
    unsigned int j = 0;
    for(auto& column : analysis) {
        if (column[0].value().index() == 0) {
            std::cout << std::setw(14) << std::left << headerNames[j]
                      << std::setw(10) << std::left << std::setprecision(4) << analysis.calculateMean(column)
                      << std::setw(8) << std::left << std::setprecision(4) << analysis.calculateStandardDeviation(column) << std::endl;
        }
        j++;
    }
    std::cout << std::endl;

    std::cout << "The name of the columns of the CSV file are: ";
    for(auto& name : headerNames)
        std::cout << name << " | ";
    std::cout << std::endl;

    // Create the output path outside the loop, otherwise it creates it for every cycle, overwriting the results
    CSVfile->create_output_path();

    std::string targetColumn;
    // Perform analyses one by one
    do {
        std::cout << "\nWhat is the name of the column you want to analyze? ";
        std::cin >> targetColumn;

        std::cout << "\nChoose the analysis type:\n"
                  << "1. Mean\n"
                  << "2. Median\n"
                  << "3. Standard Deviation\n"
                  << "4. Variance\n"
                  << "5. Frequency Count\n"
                  << "6. Classification\n"
                  << "7. Correlation\n"
                  << "0. Exit\n"
                  << "Enter the corresponding number: ";

        int analysisChoice;
        std::cin >> analysisChoice;

        if (analysisChoice == 0) {
            break; // Exit loop if user chooses 0
        }

        // Compute and append the selected analysis to the result string
        std::string result;
        switch (analysisChoice) {
            case 1:
                try {
                result = "Mean: " + std::to_string(analysis.calculateMean(analysis.getColumn(targetColumn)));
                } catch (const std::invalid_argument &e) {
                std::cerr << "Error calculating mean: " << e.what() << std::endl;
                }
            break;
            case 2:
                {
                    std::variant<double, std::string> medianVariant = analysis.calculateMedian(analysis.getColumn(targetColumn));
                    result = "Median: " + (medianVariant.index() == 1 ? std::get<std::string>(medianVariant) : std::to_string(std::get<double>(medianVariant)));
                }
                break;
            case 3:
                try {
                result = "Standard Deviation: " + std::to_string(analysis.calculateStandardDeviation(analysis.getColumn(targetColumn)));
                } catch (const std::invalid_argument &e) {
                std::cerr << "Error calculating standard deviation: " << e.what() << std::endl;
                }
                break;
            case 4:
                try {
                result = "Variance: " + std::to_string(analysis.calculateVariance(analysis.getColumn(targetColumn)));
                } catch (const std::invalid_argument &e) {
                std::cerr << "Error calculating variance: " << e.what() << std::endl;
                }
                break;
            case 5:
                result = "Frequency Count:\n" + analysis.calculateFrequency(analysis.getColumn(targetColumn));
                break;
            case 6:
            {
                std::string condition;
                std::cout << "Enter the name of the feature you want to classify: ";
                std::cin >> condition;
                try {
                    result = "Classification: " + analysis.calculateClassification(targetColumn, condition);
                } catch (const std::invalid_argument &e) {
                    std::cerr << "Error calculating classification: " << e.what() << std::endl;
                }
                break;
            }
            case 7:
            {
                std::string targetColumn2;
                std::cout << "Enter the name of the other target column for correlation: ";
                std::cin >> targetColumn2;
                try {
                    result = "Correlation: " + std::to_string(analysis.calculateCorrelation(analysis.getColumn(targetColumn), analysis.getColumn(targetColumn2)));
                } catch (const std::invalid_argument &e) {
                    std::cerr << "Error calculating correlation: " << e.what() << std::endl;
                }
            break;
            }
            default:
                std::cerr << "Invalid choice. Please choose a number between 0 and 7." << std::endl;
                continue; // Skip the rest of the loop and ask the user for a new choice
        }

        // Write the results to the output file
        CSVfile->writeResults(result);
        std::cout << "\nAnalysis completed: " << result << "\n";

        // Ask the user if they want to choose another analysis
        std::cout << "Do you want to choose another analysis? (1 for Yes, 0 for No): ";
        int continueChoice;
        std::cin >> continueChoice;

        if (continueChoice != 1) {
            break; // Exit the loop if the user does not want to continue
        }

    } while (true);

    std::cout << "\nAll analyses completed. Results written to results/player_data_03_22_analysis.txt\n\n";

    #endif // of Module A

    #if USE_MODULEC

    do {
        std::cout << "Select the analysis type:\n"
                  << "1. Convergence tests\n"
                  << "2. Polynomial tests\n"
                  << "3. Compute integrals\n"
                  << "0. Exit\n"
                  << "Enter the corresponding number: ";

        int choice;
        std::cin >> choice;

        if (choice == 0) {
            break; // Exit loop if the user chooses 0
        }

        switch (choice) {
            case 1:
                computeConvergenceOrder<Midpoint>("cos(x)", 1.0);
                computeConvergenceOrder<Trapezoidal>("cos(x)", 1.0);
                computeConvergenceOrder<Simpson>("cos(x)", 1.0);
                //computeConvergenceOrder<GaussLegendre>("cos(x)", 1.0);
                break;
            case 2: {
                Midpoint midpointRule(0, 1, 2);
                print_results("3*x+1", midpointRule, 2.5);

                Trapezoidal trapRule(0, 1, 5);
                print_results("3*x", trapRule, 1.5);

                Simpson simpRule(0, 1, 8); 
                print_results("3*x^3", simpRule, 0.75);

                twopointGauss twogaussRule(0, 1, 2);
                // In two-point Gauss n = 2 so it doesn't matter what it's written when initialized
                print_results("1", twogaussRule, 1);

                //GaussLegendre GaussLegendreInt(0, 1, 11);
                //print_results("6*x^5", GaussLegendreInt, 1);
                break;
            }
            case 3: {
                std::string function;
                double lowerBound, upperBound;
                int quadratureChoice, n;

                std::cout << "Enter the function to integrate: ";
                std::cin >> function;

                std::cout << "Enter the lower bound of integration: ";
                std::cin >> lowerBound;

                std::cout << "Enter the upper bound of integration: ";
                std::cin >> upperBound;

                std::cout << "Choose a quadrature method:\n"
                          << "1. Midpoint\n"
                          << "2. Trapezoidal\n"
                          << "3. Simpson\n"
                          << "4. Gauss-Legendre\n";
                std::cout << "Enter the number corresponding to the quadrature method: ";
                std::cin >> quadratureChoice;

                std::cout << "Enter the number of subintervals (n): ";
                std::cin >> n;

                if (std::cin.fail() || n <= 0) {
                    std::cerr << "Invalid input for the number of subintervals. Exiting...\n";
                    return 1;
                }

                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

                switch (quadratureChoice) {
                    case 1: {
                        Midpoint midpoint(lowerBound, upperBound, n);
                        double integral = Integrate<Midpoint>(function, midpoint);
                        std::cout << "Here the result: " << std::scientific << std::setprecision(6) << integral << " %\n\n";
                        break;
                    }
                    case 2: {
                        Trapezoidal trap(lowerBound, upperBound, n);
                        double integral = Integrate<Trapezoidal>(function, trap);
                        std::cout << "Here the result: " << std::scientific << std::setprecision(6) << integral << " %\n\n";
                        break;
                    }
                    case 3: {
                        while (n % 2 != 0) {
                        std::cerr << "Error: n must be even. Enter the number of subintervals (n): ";
                        std::cin >> n;
                    }
                        Simpson simp(lowerBound, upperBound, n);
                        double integral = Integrate<Simpson>(function, simp);
                        std::cout << "Here the result: " << std::scientific << std::setprecision(6) << integral << " %\n\n";
                        break;
                    }
                    case 4: {
                        GaussLegendre gauss(lowerBound, upperBound, n);
                        double integral = Integrate<GaussLegendre>(function, gauss);
                        std::cout << "Here the result: " << std::scientific << std::setprecision(6) << integral << " %\n\n";
                        break;
                    }
                    default:
                        std::cerr << "Invalid choice for quadrature method. Exiting...\n";
                        return 1;
                }
                break;
            }
            default:
                std::cerr << "Invalid choice. Please choose a number between 1 and 4." << std::endl;
                continue;
        }

        std::cout << "Do you want to perform another analysis? (1 for Yes, 0 for No): ";
        int continueChoice;
        std::cin >> continueChoice;

        if (continueChoice != 1) {
            break;
        }

    } while (true);

    #endif // of Module C
    return 0;
}