cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Homework3_Serafino"
    )

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
    NumericalIntegrationModule/include/IntegrationMethods_py.hpp
    NumericalIntegrationModule/include/moduleCfunctions.tpl.hpp
    NumericalIntegrationModule/src/moduleCfunctions_py.cpp)

# Example that shows how to pass a value from Python to C++.
target_compile_definitions(moduleC PRIVATE VERSION_INFO=${MODULEC_VERSION_INFO})

#target_include_directories(moduleC
 #   PUBLIC
  #  ${PROJECT_BINARY_DIR}/NumericalIntegrationModule/include
   # ${PROJECT_BINARY_DIR}/NumericalIntegrationModule/src
    #${MUPARSERX_ROOT}/include
    #)

#target_link_directories(moduleC
 #   PUBLIC
  #  ${MUPARSERX_ROOT}/lib
   # )

#target_link_libraries(moduleC PUBLIC ${Boost_LIBRARIES} muparserx)

# Add the subdirectories for the modules if necessary
#if(USE_MODULEA)
 #   add_subdirectory(StatisticsModule)
#
 #   target_include_directories(homework
  #  PUBLIC
   # ${PROJECT_BINARY_DIR}/StatisticsModule/include
    #)

    #target_link_libraries(homework PUBLIC StatisticsModule)
#endif()
