cmake_minimum_required(VERSION 3.10)
set(CMAKE_PROJECT_NAME "raygui")
project(${CMAKE_PROJECT_NAME} LANGUAGES C)

set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_C_STANDARD 17)

add_subdirectory(raylib)

add_executable(${CMAKE_PROJECT_NAME} main.c)
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE raylib/src)
target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE raylib)
