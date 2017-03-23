project(malos_service C CXX)
cmake_minimum_required(VERSION 2.8)

add_definitions(-std=c++11)

# Enable extra warnings. Not needed.
include (../cmake/FatalWarnings.cmake)
ADM_EXTRA_WARNINGS()

find_package(Threads)

add_subdirectory(../cpp/driver driver)

add_executable(M202BProj_v0 M202BProj_v0.cpp)
set_property(TARGET M202BProj_v0 PROPERTY CXX_STANDARD 11)
target_link_libraries(M202BProj_v0 matrix_creator_hal)
target_link_libraries(M202BProj_v0 ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(M202BProj_v0 wiringPi)

add_executable(M202BProj_v1 M202BProj_v1.cpp)
set_property(TARGET M202BProj_v1 PROPERTY CXX_STANDARD 11)
target_link_libraries(M202BProj_v1 matrix_creator_hal)
target_link_libraries(M202BProj_v1 ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(M202BProj_v1 wiringPi)

add_executable(lightsOff lightsOff.cpp)
set_property(TARGET lightsOff PROPERTY CXX_STANDARD 11)
target_link_libraries(lightsOff matrix_creator_hal)
target_link_libraries(lightsOff ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(lightsOff wiringPi)

add_executable(mic_energy_test mic_energy_test.cpp)
set_property(TARGET mic_energy_test PROPERTY CXX_STANDARD 11) 
target_link_libraries(mic_energy_test matrix_creator_hal)
target_link_libraries(mic_energy_test ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(mic_energy_test wiringPi)

add_executable(M202BProj_v0_trainVoice M202BProj_v0_trainVoice.cpp)
set_property(TARGET M202BProj_v0_trainVoice PROPERTY CXX_STANDARD 11)
target_link_libraries(M202BProj_v0_trainVoice matrix_creator_hal)
target_link_libraries(M202BProj_v0_trainVoice ${CMAKE_THREAD_LIBS_INIT})
target_link_libraries(M202BProj_v0_trainVoice wiringPi)


