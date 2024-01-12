#include "../include/DataHandler.hpp"
#include "../include/StatOp_py.hpp"
#include "../include/StatOp.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

// Wrap C++ functions with NumPy

py::array_t<py::array_t<std::string>> py_readData() { // o str? Cioè dopo che scrivo py:: uso python o c++?
    const std::string input_path = StatOp::get_input_file_path();
    return py::genfromtxt(input_path, delimiter = ',', dtype = str);
}

py::array_t<std::string> py_getHeader() {
    py::array_t<py::array_t<std::string>> csvarrays = py_readData();
    py::array_t<std::string> header = csvarrays[0,:];
    return header;
}

// Wrap as Python module

PYBIND11_MODULE(moduleA, m) {
    m.doc() = "pybind11 moduleA plugin";

    // This class is the same as in C++, except for the smart pointer
    py::class_<StatOp>(m, "StatOp")
    // il costruttore sarebbe 
    //     StatOp::StatOp(const std::shared_ptr<CSVHandler> CSVfile) : CSVfile(CSVfile), data(CSVfile->readData()) {};
    // ma in python non ci sono puntatori, come si scrive?
        .def(py::init<const std::shared_ptr<>>(), py::arg("CSVfile"));
        .def("calculateMean", &StatOp::calculateMean);
        .def("calculateMedian", &StatOp::calculateMedian);
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation);
        .def("calculateFrequency", &StatOp::calculateFrequency);
        .def("calculateClassification", &StatOp::calculateClassification);
        .def("calculateCorrelation", &StatOp::calculateCorrelation);
        .def("getColumn", &StatOp::getColumn, py::const_); // const method
        .def("begin", &StatOp::begin);
        .def("end", &StatOp::end);

    py::class_<CSVHandler>(m, "CSVHandler")
        .def(py::init<const std::string>(), py::arg("input_path"));
        .def("create_output_path", &CSVHandler::create_output_path);
        .def("get_input_file_path", &CSVHandler::get_input_file_path);
        .def("get_input_file_name", &CSVHandler::get_input_file_name);
        .def("writeResults", &CSVHandler::writeResults);
        .def("read_header", &CSVHandler::read_header, py::const_);
        // Overload and define as constant the following two methods
        .def("readData", py::overload_cast<py::array_t<py::array_t<std::string>>>(&CSVHandler::readData, py::const_));
        .def("getHeader", py::overload_cast<py::array_t<std::string>>(&CSVHandler::getHeader, py::const_));
        .def(py::del<>()); // come si scrive il distruttore? (questo non è default come gli altri)
}