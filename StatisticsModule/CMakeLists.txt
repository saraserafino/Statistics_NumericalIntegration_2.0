cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Creating the library for the module A"
    LANGUAGES CXX)

# Use C++17 standard for compiling
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# Set the use of this module as an option with default value on
option(USE_MODULEA "Use the Statistics Module")

if(USE_MODULEA)
    add_library(StatisticsModule SHARED src/StatOp.cpp src/DataHandler.cpp)
    target_compile_definitions(StatisticsModule PUBLIC USE_MODULEA)
endif()
