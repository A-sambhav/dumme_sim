cmake_minimum_required(VERSION 3.8)
project(dumme_firmware)

find_package(ament_cmake REQUIRED)

# The PlatformIO project under firmware/dumme_control/ (platformio.ini +
# src/main.cpp) is built and uploaded separately via PlatformIO (VS Code
# extension or `pio run -t upload`) - it is not built by colcon. This just
# keeps it tracked as part of the workspace.
install(
  DIRECTORY firmware
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
