cmake_minimum_required(VERSION 3.8)
project(RankingGeneratorCpp)

set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs 3)

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

set(sources RankingGenerator.cpp RankingGenerator.h)

SET_SOURCE_FILES_PROPERTIES(RankingGeneratorCpp.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_LIBRARY(RankingGeneratorCpp
        TYPE SHARED
        LANGUAGE python
        SOURCES RankingGeneratorCpp.i ${sources})
SWIG_LINK_LIBRARIES(RankingGeneratorCpp ${PYTHON_LIBRARIES})

#set(SOURCE_FILES RankingGenerator.cpp RankingGenerator.h)
#add_library(cpp ${SOURCE_FILES})