cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Homework3_Serafino"
    )

add_compile_options(-std=c++17)

# Search for Boost
find_package(Boost 1.83 REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

# Search for muparserx
find_package(muparserx 4.0 REQUIRED)
include_directories(${muparserx_INCLUDE_DIRS})

# Search for Pybind
find_package(pybind11 REQUIRED)
include_directories(SYSTEM ${pybind11_INCLUDE_DIRS})

# Add the Python modules
pybind11_add_module(moduleC
    NumericalIntegrationModule/src/IntegrationMethods.cpp
    NumericalIntegrationModule/include/moduleCfunctions.tpl.hpp
    NumericalIntegrationModule/src/moduleCfunctions_py.cpp
    )

pybind11_add_module(moduleA
    StatisticsModule/src/DataHandler_py.cpp
    StatisticsModule/src/DataHandler.cpp
    StatisticsModule/src/StatOp.cpp
    )

target_link_libraries(moduleC PRIVATE ${MUPARSERX_LIBRARY})
target_include_directories(moduleA PRIVATE StatisticsModule/include)
target_include_directories(moduleC PRIVATE NumericalIntegration/include)
#endif()