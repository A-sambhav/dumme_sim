cmake_minimum_required(VERSION 3.8)
project(dumme_vision)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  ${PROJECT_NAME}/spaghetti_detector.py
  ${PROJECT_NAME}/publish_image.py
  ${PROJECT_NAME}/person_detector.py
  ${PROJECT_NAME}/video_recorder.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
