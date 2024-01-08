#include "../include/IntegrationMethods.hpp"

#include <pybind11/pybind11.h>
//#include <pybind11/stl.h> // forse servirà?

// ----------------------------------
// Python interface - fake trampoline
// ----------------------------------

class PyQuadrature : public Quadrature {
public:
    // Inherit the constructors
    using Quadrature::Quadrature;

    // Each virtual function needs a trampoline, but there aren't
};

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

// Wrap C++ function with NumPy 
py::array_t<int>
py_multiply(const py::array_t<double, py::array::c_style | py::array::forcecast>
                &array) {
  // Allocate std::vector (to pass to the C++ function).
  std::vector<double> vector(array.size());

  // Copy py::array -> std::vector.
  std::memcpy(vector.data(), array.data(), array.size() * sizeof(double));

  // Call pure C++ function.
  std::vector<int> result_vec = multiply(vector);

  // Allocate py::array (to pass the result of the C++ function to Python).
  auto result = py::array_t<int>(array.size());
  auto result_buffer = result.request();
  int *result_ptr = (int *)result_buffer.ptr;

  // Copy std::vector -> py::array.
  std::memcpy(result_ptr, result_vec.data(), result_vec.size() * sizeof(int));

  return result;
}

// Wrap as Python module.
PYBIND11_MODULE(IntegrationMethods, m) {
    py::class_<Quadrature, PyQuadrature>(m, "Quadrature")
        .def(py::init<>());
        .def("get_weights", &get_weights, "Get the weights of the function to integrate");
        .def("get_nodes", &get_nodes, "Get the nodes of the function to integrate");

    py::class_<Midpoint, Quadrature>(m, "Midpoint")
        .def(py::init<double, double, unsigned int>(),
            py::arg("a"), py::arg("b"), py::arg("nBins"));

    py::class_<Trapezoidal, Quadrature>(m, "Trapezoidal").def(py::init<>());
        .def(py::init<double, double, unsigned int>(),
            py::arg("a"), py::arg("b"), py::arg("nBins"));

    py::class_<Simpson, Quadrature>(m, "Simpson").def(py::init<>());
        .def(py::init<double, double, unsigned int>(),
            py::arg("a"), py::arg("b"), py::arg("nBins"));

    py::class_<twopointGauss, Quadrature>(m, "twopointGauss").def(py::init<>());
        .def(py::init<double, double, unsigned int>(),
            py::arg("a"), py::arg("b"), py::arg("nBins"));

    py::class_<GaussLegendre, Quadrature>(m, "GaussLegendre").def(py::init<>());
        .def(py::init<double, double, unsigned int>(),
            py::arg("a"), py::arg("b"), py::arg("nBins"));
    // che in realtà ha più roba ma la voglio fare in python
}