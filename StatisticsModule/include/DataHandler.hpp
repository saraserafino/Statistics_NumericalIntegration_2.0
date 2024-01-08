#ifndef DATAHANDLER_HPP
#define DATAHANDLER_HPP

#include <filesystem>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

typedef std::optional<std::variant<double,std::string>> csvType;

class CSVHandler {
public:
  // Declare StatOp as a friend class of CSVHandler in order to access its private members
  friend class StatOp;

  // Constructor for opening the input file
  CSVHandler(const std::string &input_path);

  // Method for creating destination and file for the output result
  // Since it creates from scratch, it gets called only once (in the constructor)
  // otherwise every time we continue the analysis, it would clear everything
  const std::filesystem::path create_output_path();

  const std::string get_input_file_path() const;
  const std::string get_input_file_name() const;

  // Functions for reading the input file
  int read_header(const std::string &targetColumn) const;
  std::vector<std::vector<csvType>> readData() const;
  std::vector<std::string> getHeader() const;

  // Function to write the results
  void writeResults(const std::string &result);

  // Destructor for both files
  ~CSVHandler() {
    this->input_file.close();
    this->output_file.close();
  }

  // To operate on input and output files we define them as public (if/of streams are not allowed to be r-values)
  std::ifstream input_file;
  std::ofstream output_file;

protected:  
  const std::string input_path;
  const std::string input_file_name;
  std::filesystem::path output_file_path;
  // Shared pointer between the two classes
  const std::shared_ptr<CSVHandler> CSVfile;
};

#endif