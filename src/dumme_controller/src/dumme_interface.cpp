#include "dumme_controller/dumme_interface.hpp"
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>


namespace dumme_controller
{

std::string compensateZeros(const int value)
{
  std::string compensate_zeros = "";
  if(value < 10){
    compensate_zeros = "00";
  } else if(value < 100){
    compensate_zeros = "0";
  } else {
    compensate_zeros = "";
  }
  return compensate_zeros;
}

DummeInterface::DummeInterface()
{
}


DummeInterface::~DummeInterface()
{
  if (esp32_.IsOpen())
  {
    try
    {
      esp32_.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("DummeInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }
}


CallbackReturn DummeInterface::on_init(const hardware_interface::HardwareInfo &hardware_info)
{
  CallbackReturn result = hardware_interface::SystemInterface::on_init(hardware_info);
  if (result != CallbackReturn::SUCCESS)
  {
    return result;
  }

  try
  {
    port_ = info_.hardware_parameters.at("port");
  }
  catch (const std::out_of_range &e)
  {
    RCLCPP_FATAL(rclcpp::get_logger("DummeInterface"), "No Serial Port provided! Aborting");
    return CallbackReturn::FAILURE;
  }

  position_commands_.reserve(info_.joints.size());
  position_states_.reserve(info_.joints.size());
  prev_position_commands_.reserve(info_.joints.size());

  return CallbackReturn::SUCCESS;
}


std::vector<hardware_interface::StateInterface> DummeInterface::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  // Provide only a position interface
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_states_[i]));
  }

  return state_interfaces;
}


std::vector<hardware_interface::CommandInterface> DummeInterface::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  // Provide only a position interface
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_commands_[i]));
  }

  return command_interfaces;
}


CallbackReturn DummeInterface::on_activate(const rclcpp_lifecycle::State &previous_state)
{
  (void)previous_state;
  RCLCPP_INFO(rclcpp::get_logger("DummeInterface"), "Starting robot hardware ...");

  // Reset commands and states - order matches dumme_ros2_control.xacro:
  // [0] shoulder_rotation_plate_joint, [1] shoulder_joint, [2] elbow_joint, [3] wrist_joint
  position_commands_ = { 0.0, 0.0, 0.0, 0.0 };
  prev_position_commands_ = { 0.0, 0.0, 0.0, 0.0 };
  position_states_ = { 0.0, 0.0, 0.0, 0.0 };

  try
  {
    esp32_.Open(port_);
    esp32_.SetBaudRate(LibSerial::BaudRate::BAUD_115200);
  }
  catch (...)
  {
    RCLCPP_FATAL_STREAM(rclcpp::get_logger("DummeInterface"),
                        "Something went wrong while interacting with port " << port_);
    return CallbackReturn::FAILURE;
  }

  RCLCPP_INFO(rclcpp::get_logger("DummeInterface"),
              "Hardware started, ready to take commands");
  return CallbackReturn::SUCCESS;
}


CallbackReturn DummeInterface::on_deactivate(const rclcpp_lifecycle::State &previous_state)
{
  (void)previous_state;
  RCLCPP_INFO(rclcpp::get_logger("DummeInterface"), "Stopping robot hardware ...");

  if (esp32_.IsOpen())
  {
    try
    {
      esp32_.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("DummeInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }

  RCLCPP_INFO(rclcpp::get_logger("DummeInterface"), "Hardware stopped");
  return CallbackReturn::SUCCESS;
}


hardware_interface::return_type DummeInterface::read(const rclcpp::Time &time,
                                                       const rclcpp::Duration &period)
{
  (void)time;
  (void)period;
  // Open loop control - the MG995 servos have no position feedback, so we
  // assume the arm is wherever we last commanded it to be. This matches
  // open_loop_control: true in dumme_controllers.yaml.
  position_states_ = position_commands_;
  return hardware_interface::return_type::OK;
}


hardware_interface::return_type DummeInterface::write(const rclcpp::Time &time,
                                                        const rclcpp::Duration &period)
{
  (void)time;
  (void)period;
  if (position_commands_ == prev_position_commands_)
  {
    // Nothing changed, do not send any command
    return hardware_interface::return_type::OK;
  }

  // NOTE: conversion assumes each joint's 0 rad (URDF zero) corresponds to
  // the servo's 90 degree center position, with +/-PI/2 rad mapping to the
  // servo's 0-180 degree mechanical range. Verify this against the real
  // mounting of each servo - if a joint moves the wrong direction, negate
  // the (position_commands_.at(i)) term for that joint, the same way the
  // reference project inverts "shoulder" with a (180 - x) formula.
  std::string msg;

  int plate = static_cast<int>(((position_commands_.at(0) + (M_PI / 2)) * 180) / M_PI);
  msg.append("p");
  msg.append(compensateZeros(plate));
  msg.append(std::to_string(plate));
  msg.append(",");

  int shoulder = static_cast<int>(((position_commands_.at(1) + (M_PI / 2)) * 180) / M_PI);
  msg.append("s");
  msg.append(compensateZeros(shoulder));
  msg.append(std::to_string(shoulder));
  msg.append(",");

  int elbow = static_cast<int>(((position_commands_.at(2) + (M_PI / 2)) * 180) / M_PI);
  msg.append("e");
  msg.append(compensateZeros(elbow));
  msg.append(std::to_string(elbow));
  msg.append(",");

  int wrist = static_cast<int>(((position_commands_.at(3) + (M_PI / 2)) * 180) / M_PI);
  msg.append("w");
  msg.append(compensateZeros(wrist));
  msg.append(std::to_string(wrist));
  msg.append(",");

  try
  {
    RCLCPP_INFO_STREAM(rclcpp::get_logger("DummeInterface"), "Sending new command " << msg);
    esp32_.Write(msg);
  }
  catch (...)
  {
    RCLCPP_ERROR_STREAM(rclcpp::get_logger("DummeInterface"),
                        "Something went wrong while sending the message "
                            << msg << " to the port " << port_);
    return hardware_interface::return_type::ERROR;
  }

  prev_position_commands_ = position_commands_;

  return hardware_interface::return_type::OK;
}

}  // namespace dumme_controller

PLUGINLIB_EXPORT_CLASS(dumme_controller::DummeInterface, hardware_interface::SystemInterface)
