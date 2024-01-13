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
        .def(py::init<const std::string>(), py::arg("input_path"))
        //.def("create_output_path", &CSVHandler::create_output_path)
        .def("get_input_file_path", &CSVHandler::get_input_file_path)
        .def("get_input_file_name", &CSVHandler::get_input_file_name)
        // The implemented C++ methods readData and getHeader will not be used because the data will
        // be read with Python. read_header is needed though, because it's used in Classification.
        // It needs input_file_name and targetColumn as inputs, so it's ok
        .def("read_header", &CSVHandler::read_header);

    py::class_<StatOp>(m, "StatOp")
        .def(py::init<const std::shared_ptr<CSVHandler>>(), py::arg("CSVfile"))
        .def("calculateMean", &StatOp::calculateMean)
        .def("calculateMedian", &StatOp::calculateMedian)
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation)
        .def("calculateFrequency", &StatOp::calculateFrequency)
        .def("calculateVariance", &StatOp::calculateVariance)
        .def("calculateClassification", &StatOp::calculateClassification)
        .def("calculateCorrelation", &StatOp::calculateCorrelation)
        // The implemented C++ method getColumn - which was used in main.cpp -
        // will not be used because data will be processed with Python.
        .def("begin", &StatOp::begin)
        .def("end", &StatOp::end);
}