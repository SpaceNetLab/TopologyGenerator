cmake_minimum_required(VERSION 3.15)
project(TopologyGenerator C)

set(CMAKE_C_STANDARD 99)

if(WIN32)
    add_definitions(-D WIN_OS)
    #add_definitions(-D HAVE_WINDOWS_H)
    #add_definitions(-D HAVE_GETSYSTEMTIMEASFILETIME)
elseif(APPLE)
    add_definitions(-D Mac_OS)
endif()

include_directories(
        third-party/libuv/include
        third-party/klib
        third-party/c-logger/src
)
add_executable(TopologyGenerator
        src/main.c
        src/tg_node.c
        src/tg_node.h
        src/tg_basic.h
        )

target_link_libraries(TopologyGenerator
        uv_a
        logger_static
        )

add_subdirectory(third-party/libuv)
add_subdirectory(third-party/c-logger)