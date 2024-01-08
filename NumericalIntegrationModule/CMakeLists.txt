cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Creating the library for the module C"
    LANGUAGES CXX)

# Use C++17 standard for compiling
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# Set the use of this module as an option with default value on
option(USE_MODULEC "Use the Numerical Integration Module")

if(USE_MODULEC)
    add_library(NumericalIntegrationModule SHARED src/IntegrationMethods.cpp)
    
    # Search for muparserx
    find_package(muparserx 4.0 REQUIRED)

    include_directories(${muparserx_INCLUDE_DIRS})

    target_include_directories(NumericalIntegrationModule
        PUBLIC
        ${MUPARSERX_ROOT}/include
        )
    
    target_link_directories(NumericalIntegrationModule
        PUBLIC
        ${MUPARSERX_ROOT}/lib
        )

    target_link_libraries(NumericalIntegrationModule muparserx)
    
    target_compile_definitions(NumericalIntegrationModule PUBLIC USE_MODULEC)
endif()
