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
        .def("create_output_path", &CSVHandler::create_output_path)
        .def("get_input_file_path", &CSVHandler::get_input_file_path)
        .def("get_input_file_name", &CSVHandler::get_input_file_name)
        .def("writeResults", &CSVHandler::writeResults)
        // read_header è usato in getColumn e nella classificazione
        // necessita di input_file_name e targetColumn
        // Lo terrei solo per la classificazione ma per il resto farei con python
        .def("read_header", &CSVHandler::read_header);

    // This class is the same as in C++, except for the smart pointer which is removed
    py::class_<StatOp>(m, "StatOp")
        .def(py::init<const std::shared_ptr<CSVHandler>>(), py::arg("CSVfile"))
        .def("calculateMean", &StatOp::calculateMean)
        .def("calculateMedian", &StatOp::calculateMedian)
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation)
        .def("calculateFrequency", &StatOp::calculateFrequency)
        .def("calculateClassification", &StatOp::calculateClassification)
        .def("calculateCorrelation", &StatOp::calculateCorrelation)
        // getColumn usa read_header, restituisce data
        // viene usato in main.cpp per ottenere i valori di data ogni volta
        // quindi potrei non usare getColumn e farlo con python
        //.def("getColumn", &StatOp::getColumn)
        .def("begin", &StatOp::begin)
        .def("end", &StatOp::end);
}