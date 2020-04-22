cmake_minimum_required(VERSION 3.16)
project(region_growing C)

set(CMAKE_C_STANDARD 11)

set(SOURCE_FILES region_growing.c stack.c)
set(HEADER_FILES region_growing.h stack.h)

add_executable(region_growing main.c ${SOURCE_FILES} ${HEADER_FILES})
add_library(region_growing_lib SHARED ${SOURCE_FILES} ${HEADER_FILES})