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

    // This class is the same as in C++, except for the smart pointer
    py::class_<StatOp>(m, "StatOp")
    // il costruttore sarebbe 
    //     StatOp::StatOp(const std::shared_ptr<CSVHandler> CSVfile) : CSVfile(CSVfile), data(CSVfile->readData()) {};
    // ma in python non ci sono puntatori, come si scrive?
        .def(py::init<const &CSVHandler(), py::arg("CSVfile"))
        .def("calculateMean", &StatOp::calculateMean)
        .def("calculateMedian", &StatOp::calculateMedian)
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation)
        .def("calculateFrequency", &StatOp::calculateFrequency)
        .def("calculateClassification", &StatOp::calculateClassification)
        .def("calculateCorrelation", &StatOp::calculateCorrelation)
        //.def("getColumn", &StatOp::getColumn, py::const_) // const method
        .def("begin", &StatOp::begin)
        .def("end", &StatOp::end);

    py::class_<CSVHandler>(m, "CSVHandler")
        .def(py::init<const std::string>(), py::arg("input_path"))
        .def("create_output_path", &CSVHandler::create_output_path)
        .def("get_input_file_path", &CSVHandler::get_input_file_path)
        .def("get_input_file_name", &CSVHandler::get_input_file_name)
        .def("writeResults", &CSVHandler::writeResults);
        //.def("read_header", &CSVHandler::read_header, py::const_);
}