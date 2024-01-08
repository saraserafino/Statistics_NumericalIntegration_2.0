# Homework3_Serafino

## Code organization
For each module there is a folder which separates source files from header files; the main file is in its folder called main; a cmake is provided for each of them and will be explained later on.

## Main
The `main.cpp` was written using switch cases to allow the user to decide what to compute.
* For the Statistics module, it is asked which column of the CSV file to analyse and which analysis perform.
* For the Numerical Integration module, it is asked for convergence tests, polynomial tests and if the user wants to compute the integral of a function from input.  
Being compilable as standalone libraries, a `#if USE_MODULEX` and `#endif` delimit their includes and code in main.cpp.

## Statistics module
This module computes mean, median, standard deviation, variance, frequency count, classification, and correlation analyses on the data taken from a CSV file on [NBA Players from 2003 to 2022](https://www.kaggle.com/datasets/dhruvsuryavanshi/nba-player-data-from-2003-to-2022/) and outputs them on a file named `player_data_03_22_analysis.txt` in a folder named results.

### Analysis and observations
* Various statistical calculations are provided, including mean, median, variance, standard deviation, frequency, and correlation.
These calculations can handle data stored in a vector of std::optional<std::variant<double, std::string>>. The definition of median is a bit altered in the case of strings in order to adapt it to strings.
* Assertions (assertm) are used to check the validity of input arguments and file operations. They provide a means of catching errors during development.
Exceptions are thrown for cases such as invalid arguments, missing columns, or incompatible data types.
* The Boost library is used for accumulators.

## Numerical integration module
This module approximates integrals with the methods midpoint, trapezoidal, Simpson's, two-point Gauss and Gauss-Legendre.  
For this last integration method we used the code provided [here](https://thoughts-on-coding.com/2019/04/25/numerical-methods-in-cpp-part-2-gauss-legendre-integration/) with some edits. For example we defined some constants, like `const double k = M_PI / (n + 0.5)` at line 120 of `IntegrationMethods.cpp`, in order to compute the node as `nodes[i] = cos(k * (i - 0.25))`, avoiding one calculus for each iteration of the for-cycle as in the code of the website. We tested it and unfortunately it has some memory leaks, so we also provided the implementation of twoPointGauss.   
This module is divided in `IntegrationMethods.cpp` and `moduleCfunctions.tpl.hpp` with their headers. The first one has an abstract class `Quadrature` and one derived class for each method. These classes take the integration extremes a and b and the number of subintervals n; in the constructor they calculate relative weights and nodes and through two const methods return them. Moreover the Gauss-Legendre class returns the integration extremes which are necessary to compute the integration, since it's a bit different from the other methods (as you can see from the above linked website). For this reason, in `moduleCfunctions.tpl.hpp` we defined two templates of Integrate. They differ in the use of width and mean (where integration extremes are needed) and for the fact that the function isn't simply evaluated in the node but in $width*\{x_i\} + mean$. In order to evaluate the function, the library muparserx was used. In this file we also calculated the order of convergence (consulting [this website](https://lucia-gastaldi.unibs.it/did2015/automazione/lezioni/quadratura.pdf)), analized and print the relative results. Creating these functions, we can just recall them from the main, providing a clearer design.

### Analysis and observations
* The MuParserx library has been employed to facilitate the input of functions as strings, enabling users to calculate integrals interactively.

* Static asserts have been utilized (compile-time checks) to verify that in the functions Integrate and computeConvergenceOrder, the templates are restricted to classes derived from the abstract class Quadrature. Additionally, runtime asserts have been employed to ensure that the input files are well-defined.

* As in the analysis conducted on slide 11 of the [material](https://lucia-gastaldi.unibs.it/did2015/automazione/lezioni/quadratura.pdf), the approach involved assuming the error to conform to the Cn^p form. Subsequently, through the calculation of error across an increasing number of intervals, proportionate to 2^n, and the subsequent comparison with the preceding error on a logarithmic scale, the research determined the value of -p. This value represents the angular coefficient of the line connecting the points (2^n, E(2^n)) and (2^(n+1), E(2^(n+1))). Importantly, this coefficient is defined as the convergence order.

* It was further verified that the Midpoint and Trapezoidal formulas are exact up to polynomials of degree 1, the Simpson formula up to polynomials of degree 3, and the Gauss formula with 2n+1 nodes up to polynomials of degree n.

## CMake and libraries
Three CMake are provided: one for each of the two modules and one to actually compile. The two modules have their own namespaces (called MODULEA and MODULEC) and can be compiled both together or independently, setting the option ON from terminal when compiling. The Statistics module also uses the namespace ba for boost::accumulators inside the StatOp.cpp.  
Since the library Boost is shared, it's linked in the CMake to compile; while the library muparserx is only used in the second module and therefore only linked if that module is compiled.  
Everyone in this field should have these libraries installed, if not so, Boost can be downloaded from [the original webpage](https://www.boost.org/) and muparserx from [this zip file on GitHub](https://github.com/beltoforion/muparserx/archive/refs/tags/v4.0.12.tar.gz).  
Since most Boost libraries are header-only, often there is nothing to build; this is our case. While for muparserx it's required to create a folder in which to run the cmake.  
The hardest part was understanding how the three CMake must be written and actually doing it.

## How to compile
A `CMake` is provided in the main directory.
Create and enter the folder `build`:
```bash
mkdir build
cd build
```
Then run the cmake specifying, if necessary, where the libraries `boost` and `muparserx` are installed. This last one is only needed if you want to compile the module C. By default both modules are set OFF; if you want to set one ON, add the flag `-DUSE_MODULEX=ON` where X is A for the Statistics module and C for the Numerical Integration module. So for example write:
```bash
cmake -DUSE_MODULEA=ON -DUSE_MODULEC=ON ../ -DBOOST_ROOT=/cartella/di/installazione/boost -Dmuparserx_DIR=/opt/muparserx/share/cmake/muparserx
```
Being careful that while for Boost the root folder is enough, for muparserx you must specify the directory containing the file `muparserxConfig.cmake` so it must end with `/share/cmake/muparserx`.  
Lastly write:
```bash
make
```
After a successful building you'll be prompt to write `./homework`.
