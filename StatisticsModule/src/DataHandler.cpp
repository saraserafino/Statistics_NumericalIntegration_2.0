#include "../include/DataHandler.hpp"

#include <typeinfo>
#include <exception>
#include <cassert>
#include <iostream>
#define assertm(exp, msg) assert(((void)msg, exp))

// Constructor
CSVHandler::CSVHandler(const std::string &input_path) : input_path(input_path), input_file_name(std::filesystem::path(input_path).stem().string()) {
  // Check if the file extension is .csv
  std::string extension = std::filesystem::path(this->input_path).extension();
  if (extension != ".csv") {
    throw std::invalid_argument("Invalid file type. Supported type: csv");
  }

  // Open input file
  input_file.open(this->input_path, std::ifstream::in);
  // Throw an error if it fails
  if (!input_file.is_open()) {
    throw std::runtime_error("Could not open the input file: " + this->input_path);
  }

  // Create the output path
  create_output_path();
};

// Method for creating destination and file for the output result
const std::filesystem::path CSVHandler::create_output_path() {
  // Create the path for the folder "results" in which to insert the output file
  const std::string results_folder = "../results";
  const std::filesystem::path results_path(results_folder);

  // If it already exists, remove it recursively
  if (std::filesystem::exists(results_path))
    std::filesystem::remove_all(results_path);
  // Create the folder for the results
  std::filesystem::create_directories(results_path);

  // Create output file path
  output_file_path = results_path / (this->input_file_name + "_analysis.txt");

  return output_file_path;
};

const std::string CSVHandler::get_input_file_path() const {
    return input_path;
};

const std::string CSVHandler::get_input_file_name() const {
    return input_file_name;
};

// Functions for reading the input file
int CSVHandler::read_header(const std::string &targetColumn) const {
  // Check if the input arguments are valid
  assertm(!this->input_file_name.empty() && !targetColumn.empty(), "Invalid input arguments.");

  std::fstream file(this->input_path, std::ios::in);
  std::string line;

  // Check if the file is open
  assertm(file.is_open(), "Failed to open file.");
    
  if (file.is_open()) {
    getline(file, line);

    size_t found = line.find(targetColumn);
    assertm(found !=std::string::npos, "Coloumn not found.");
    // To give the column index
    return std::count(line.begin(), line.begin() + found, ',');
  }
  return -1;
};

std::vector<std::vector<csvType>> CSVHandler::readData() const {
    // Open the CSV file in input mode
    std::fstream file(input_path, std::ios::in);
    std::string line, word;
    std::vector<std::vector<csvType>> data;

    getline(file, line);
    std::stringstream header(line);
    while(getline(header,word,',')){
        data.push_back(std::vector<csvType>());
    }

    while (getline(file, line)) {
        std::stringstream record(line);
        int j = 0;
        while (getline(record, word, ',')) {
            // Try to convert the word to double,
            try { // add as double if successful
                data[j].push_back(std::stod(word));
            } catch (const std::invalid_argument &) {
                // otherwise add as string
                data[j].push_back(word);
            }
            j++;
        }
    }
    return data;
};

std::vector<std::string> CSVHandler::getHeader() const {
  std::fstream file(this->input_path, std::ios::in);
  std::string line, word;
  std::vector<std::string> headerNames;
  // Check if the file is open
  assertm(file.is_open(), "Failed to open file.");
    
  if (file.is_open()) {
    getline(file, line);

    std::stringstream header(line);
    while(getline(header,word,',')) {
      headerNames.push_back(word);
    }
  }
  return headerNames;
};

// Method for writing the results
void CSVHandler::writeResults(const std::string &result) {
  // Open output file in append mode (so it doesn't overwrite)
  output_file.open(this->output_file_path, std::ios::app);
  // Throw an error if it fails
  if (!output_file.is_open()) {
    throw std::runtime_error("Could not open the output file.");
  }
  // Write the result of the analysis to the file
  output_file << result << "\n\n";

  // Check if writing to the file failed
  assertm(!output_file.fail(),"Error writing to the output file.");

  // Close the file explicitly
  output_file.close();
};