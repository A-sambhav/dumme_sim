# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target dumme_msgs::dumme_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${dumme_msgs_TARGETS}.
if(dumme_msgs_TARGETS AND NOT TARGET dumme_msgs::dumme_msgs)
  add_library(dumme_msgs::dumme_msgs INTERFACE IMPORTED)
  set_target_properties(dumme_msgs::dumme_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${dumme_msgs_TARGETS}")
endif()
