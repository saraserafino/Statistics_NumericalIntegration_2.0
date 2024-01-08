cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Homework2_sistemato_Serafino"
    LANGUAGES CXX)

# Use C++17 standard for compiling
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# Search for Boost
find_package(Boost 1.83 REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})

# Add the executable
add_executable(homework main/main.cpp)

target_link_libraries(homework PUBLIC ${Boost_LIBRARIES})

# Add the subdirectories for the modules if necessary
if(USE_MODULEA)
    add_subdirectory(StatisticsModule)

    target_include_directories(homework
    PUBLIC
    ${PROJECT_BINARY_DIR}/StatisticsModule/include
    )

    target_link_libraries(homework PUBLIC StatisticsModule)
endif()

if(USE_MODULEC)
    add_subdirectory(NumericalIntegrationModule)

    target_include_directories(homework
    PUBLIC
    ${PROJECT_BINARY_DIR}/NumericalIntegrationModule/include
    )

    target_link_libraries(homework PUBLIC NumericalIntegrationModule)
endif()