cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
project(activity_detection)
find_package(PCL 1.6 REQUIRED COMPONENTS common io search visualization)
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

set(CMAKE_BUILD_TYPE Debug)

add_executable (segment src/get_skel_segments.cpp)
add_executable (extractOPC src/extractObjectPointclouds.cpp)
add_executable (featgenSeg src/featureGenerationForSegments.cpp)
add_executable (frameFeatgen src/featureGenerationForFrames.cpp)
add_executable (skelViewer src/skeletonViewer.cpp)
add_executable (getTraj src/getObjHandTrajectories.cpp)


FIND_PACKAGE( OpenCV REQUIRED )

TARGET_LINK_LIBRARIES(segment ${PCL_LIBRARIES})
TARGET_LINK_LIBRARIES(extractOPC ${PCL_LIBRARIES} ${OpenCV_LIBS})
TARGET_LINK_LIBRARIES(featgenSeg ${PCL_LIBRARIES} ${OpenCV_LIBS})
TARGET_LINK_LIBRARIES(frameFeatgen ${PCL_LIBRARIES} ${OpenCV_LIBS})
TARGET_LINK_LIBRARIES(skelViewer ${PCL_LIBRARIES})
TARGET_LINK_LIBRARIES(getTraj ${PCL_LIBRARIES} ${OpenCV_LIBS} )

#TARGET_LINK_LIBRARIES(segment ${PCL_LIBRARIES}  ${OpenCV_LIBS})
