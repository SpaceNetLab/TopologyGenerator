cmake_minimum_required(VERSION 3.15)
project(TopologyGenerator C)

set(CMAKE_C_STANDARD 99)

add_executable(TopologyGenerator
        src/main.c
        src/tg_node.c
        src/tg_node.h
        src/tg_basic.h
        )