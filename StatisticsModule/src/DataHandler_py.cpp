#include "../include/DataHandler.hpp"
#include "../include/StatOp.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

// ----------------
// Python interface
// ----------------

namespace py = pybind11;
using namespace MODULEA;

// Wrap as Python module

PYBIND11_MODULE(moduleA, m) {
    m.doc() = "pybind11 moduleA plugin";

    py::class_<CSVHandler, std::shared_ptr<CSVHandler>>(m, "CSVHandler")
        .def(py::init<const std::string>(), py::arg("input_path")) // Constructor
        .def("get_input_file_path", &CSVHandler::get_input_file_path)
        .def("get_input_file_name", &CSVHandler::get_input_file_name);
        // The implemented C++ methods readData, getHeader, create_output_path, writeResults
        // are not be used because Python will provide them in the main.
        // read_header would have been needed for calculateClassification,
        // which is also not used.

    py::class_<StatOp>(m, "StatOp")
        .def(py::init<const std::shared_ptr<CSVHandler>>(), py::arg("CSVfile")) // Constructor
        .def("calculateMean", &StatOp::calculateMean)
        .def("calculateMedian", &StatOp::calculateMedian)
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation)
        .def("calculateFrequency", &StatOp::calculateFrequency)
        .def("calculateVariance", &StatOp::calculateVariance)
        .def("calculateCorrelation", &StatOp::calculateCorrelation)
        // The implemented C++ method getColumn - which was used in main.cpp -
        // is not used because data will be processed with Python.
        .def("begin", &StatOp::begin)
        .def("end", &StatOp::end);
}