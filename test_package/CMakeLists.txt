project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()


# CONAN_PKG imported targets

add_executable(test_tidy_CONAN_PKG test71.cxx)
target_link_libraries(test_tidy_CONAN_PKG CONAN_PKG::tidy)
add_test(
    NAME test_tidy_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_tidy_CONAN_PKG
)


# Tidy imported targets

find_package(Tidy REQUIRED)

add_executable(test_tidy test71.cxx)
target_link_libraries(test_tidy Tidy::Tidy)
add_test(
    NAME test_tidy
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_tidy
)

