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

// Wrap C++ function with NumPy
py_readData() {
    return py::genfromtxt('Advanced Programming/Homework3_Serafino/data/player_data_03_22.csv', delimiter = ',', dtype = std::string)
}


// Wrap as Python module

PYBIND11_MODULE(moduleA, m) {
    m.doc() = "pybind11 moduleA plugin";

    py::class_<StatOp>(m, "StatOp")
        .def(py::init<const std::shared_ptr<>>(), py::arg("CSVfile"));
        .def("calculateMean", &StatOp::calculateMean);
        .def("calculateMedian", &StatOp::calculateMedian);
        .def("calculateStandardDeviation", &StatOp::calculateStandardDeviation);
        .def("calculateFrequency", &StatOp::calculateFrequency);
        .def("calculateClassification", &StatOp::calculateClassification);
        .def("calculateCorrelation", &StatOp::calculateCorrelation);
        // in realtà questi // li voglio cambiare con python
        .def("getColumn", &StatOp::getColumn);//
        .def("readSpecificColumn", &StatOp::readSpecificColumn);//
        .def("begin", &StatOp::begin);// verrà tolto
        .def("end", &StatOp::end);// verrà tolto

    py::class_<CSVHandler>(m, "CSVHandler")
        .def(py::init<const std::string>(), py::arg("input_path"));
        .def("create_output_path", &CSVHandler::create_output_path);
        .def("get_input_file_path", &CSVHandler::get_input_file_path);
        .def("get_input_file_name", &CSVHandler::get_input_file_name);
        .def("read_header", py::overload_cast<int, double>(&CSVHandler::read_header, py::const_)); // così fai overload e dici che è metodo costante
        .def("readData", &CSVHandler::readData); //
        .def("getHeader", &CSVHandler::getHeader); //
        .def("writeResults", &CSVHandler::writeResults);
}