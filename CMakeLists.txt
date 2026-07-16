# For more information about build system see
# https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/build-system.html
# The following five lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)

set(PROJECT_VER "1.9.0")

# 强制关闭“将警告视为错误”，解决 freetype 等库的编译中断问题
add_compile_options("-Wno-error")
add_compile_options("-Wno-maybe-uninitialized")

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(xiaozhi)