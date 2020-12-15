cmake_minimum_required(VERSION 3.6)

project(AdventOfCode
    LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

add_executable(day15 main.cpp)