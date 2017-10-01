cmake_minimum_required(VERSION 3.7)
project(GC_C___)

set(CMAKE_CXX_STANDARD 11)
#set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


SET(CMAKE_CXX_FLAGS "-g -O2")
SET(CMAKE_EXE_LINKER_FLAGS "-lntl -lgmp -lm")

set(SOURCE_FILES main.cpp Decoder.cpp Decoder.h Encoder.cpp Encoder.h GF.cpp GF.h)
add_executable(GC_C___ ${SOURCE_FILES})