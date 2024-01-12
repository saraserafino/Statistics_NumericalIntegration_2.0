cmake_minimum_required(VERSION 3.12)

project(homework2 VERSION 1.0
    DESCRIPTION "Homework3_Serafino"
    )

# Search for Boost
find_package(Boost 1.83 REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

# In python non si può fare quella cosa di module ON/OFF che io abbia visto
# Search for muparserx
find_package(muparserx 4.0 REQUIRED)
include_directories(${muparserx_INCLUDE_DIRS})

# Search for Pybind
find_package(pybind11 REQUIRED)
include_directories(SYSTEM ${pybind11_INCLUDE_DIRS})

#uso un unico cmakelists.txt o come prima? che in caso devo fare
#add_subdirectory(NumericalIntegrationModule)
#add_subdirectory(StatisticsModule)
# e i moduli pybind immagino li aggiungo negli altri due

# se sì separati allora questi li metto là
# Add the Python modules
pybind11_add_module(moduleC
    NumericalIntegrationModule/src/IntegrationMethods.cpp
    NumericalIntegrationModule/include/IntegrationMethods_py.hpp
    NumericalIntegrationModule/include/moduleCfunctions.tpl.hpp
    NumericalIntegrationModule/src/moduleCfunctions_py.cpp
    )

pybind11_add_module(moduleA
    StatisticsModule/src/DataHandler_py.cpp
    StatisticsModule/src/DataHandler.cpp
    StatisticsModule/src/StatOp.cpp
    )

target_include_directories(moduleA PRIVATE StatisticsModule/include)
target_include_directories(moduleC PRIVATE NumericalIntegration/include)


# e qua dovrei fare come in passato?
#add_executable(homework main.py)

#target_include_directories(homework
 #   PUBLIC
  #  ${PROJECT_BINARY_DIR}/NumericalIntegrationModule/include
   # ${PROJECT_BINARY_DIR}/NumericalIntegrationModule/src
   # ${PROJECT_BINARY_DIR}/StatisticsModule/include
   # ${PROJECT_BINARY_DIR}/StatisticsModule/src
    #${MUPARSERX_ROOT}/include
    #)

#target_link_directories(homework
 #   PUBLIC
  #  ${MUPARSERX_ROOT}/lib
   # )

#target_link_libraries(homework PUBLIC ${Boost_LIBRARIES} muparserx)

#endif()
