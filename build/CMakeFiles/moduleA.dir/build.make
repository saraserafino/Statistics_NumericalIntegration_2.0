# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.27.8/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.27.8/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build"

# Include any dependencies generated for this target.
include CMakeFiles/moduleA.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/moduleA.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/moduleA.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/moduleA.dir/flags.make

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o: CMakeFiles/moduleA.dir/flags.make
CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o: /Users/sara/Desktop/Advanced\ Programming/Homework3_Serafino/StatisticsModule/src/DataHandler_py.cpp
CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o: CMakeFiles/moduleA.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir="/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o -MF CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o.d -o CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o -c "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler_py.cpp"

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler_py.cpp" > CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.i

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler_py.cpp" -o CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.s

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o: CMakeFiles/moduleA.dir/flags.make
CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o: /Users/sara/Desktop/Advanced\ Programming/Homework3_Serafino/StatisticsModule/src/DataHandler.cpp
CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o: CMakeFiles/moduleA.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir="/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o -MF CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o.d -o CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o -c "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler.cpp"

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler.cpp" > CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.i

CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/DataHandler.cpp" -o CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.s

CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o: CMakeFiles/moduleA.dir/flags.make
CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o: /Users/sara/Desktop/Advanced\ Programming/Homework3_Serafino/StatisticsModule/src/StatOp.cpp
CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o: CMakeFiles/moduleA.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir="/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o -MF CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o.d -o CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o -c "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/StatOp.cpp"

CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/StatOp.cpp" > CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.i

CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/StatisticsModule/src/StatOp.cpp" -o CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.s

# Object files for target moduleA
moduleA_OBJECTS = \
"CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o" \
"CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o" \
"CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o"

# External object files for target moduleA
moduleA_EXTERNAL_OBJECTS =

moduleA.cpython-312-darwin.so: CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler_py.cpp.o
moduleA.cpython-312-darwin.so: CMakeFiles/moduleA.dir/StatisticsModule/src/DataHandler.cpp.o
moduleA.cpython-312-darwin.so: CMakeFiles/moduleA.dir/StatisticsModule/src/StatOp.cpp.o
moduleA.cpython-312-darwin.so: CMakeFiles/moduleA.dir/build.make
moduleA.cpython-312-darwin.so: CMakeFiles/moduleA.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir="/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX shared module moduleA.cpython-312-darwin.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/moduleA.dir/link.txt --verbose=$(VERBOSE)
	/Library/Developer/CommandLineTools/usr/bin/strip -x /Users/sara/Desktop/Advanced\ Programming/Homework3_Serafino/build/moduleA.cpython-312-darwin.so

# Rule to build all files generated by this target.
CMakeFiles/moduleA.dir/build: moduleA.cpython-312-darwin.so
.PHONY : CMakeFiles/moduleA.dir/build

CMakeFiles/moduleA.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/moduleA.dir/cmake_clean.cmake
.PHONY : CMakeFiles/moduleA.dir/clean

CMakeFiles/moduleA.dir/depend:
	cd "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino" "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino" "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build" "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build" "/Users/sara/Desktop/Advanced Programming/Homework3_Serafino/build/CMakeFiles/moduleA.dir/DependInfo.cmake" "--color=$(COLOR)"
.PHONY : CMakeFiles/moduleA.dir/depend
