// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dumme_msgs:srv/QuaternionToEuler.idl
// generated code does not contain a copyright notice

#ifndef DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__BUILDER_HPP_
#define DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dumme_msgs/srv/detail/quaternion_to_euler__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dumme_msgs
{

namespace srv
{

namespace builder
{

class Init_QuaternionToEuler_Request_w
{
public:
  explicit Init_QuaternionToEuler_Request_w(::dumme_msgs::srv::QuaternionToEuler_Request & msg)
  : msg_(msg)
  {}
  ::dumme_msgs::srv::QuaternionToEuler_Request w(::dumme_msgs::srv::QuaternionToEuler_Request::_w_type arg)
  {
    msg_.w = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Request msg_;
};

class Init_QuaternionToEuler_Request_z
{
public:
  explicit Init_QuaternionToEuler_Request_z(::dumme_msgs::srv::QuaternionToEuler_Request & msg)
  : msg_(msg)
  {}
  Init_QuaternionToEuler_Request_w z(::dumme_msgs::srv::QuaternionToEuler_Request::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_QuaternionToEuler_Request_w(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Request msg_;
};

class Init_QuaternionToEuler_Request_y
{
public:
  explicit Init_QuaternionToEuler_Request_y(::dumme_msgs::srv::QuaternionToEuler_Request & msg)
  : msg_(msg)
  {}
  Init_QuaternionToEuler_Request_z y(::dumme_msgs::srv::QuaternionToEuler_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_QuaternionToEuler_Request_z(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Request msg_;
};

class Init_QuaternionToEuler_Request_x
{
public:
  Init_QuaternionToEuler_Request_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QuaternionToEuler_Request_y x(::dumme_msgs::srv::QuaternionToEuler_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_QuaternionToEuler_Request_y(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dumme_msgs::srv::QuaternionToEuler_Request>()
{
  return dumme_msgs::srv::builder::Init_QuaternionToEuler_Request_x();
}

}  // namespace dumme_msgs


namespace dumme_msgs
{

namespace srv
{

namespace builder
{

class Init_QuaternionToEuler_Response_yaw
{
public:
  explicit Init_QuaternionToEuler_Response_yaw(::dumme_msgs::srv::QuaternionToEuler_Response & msg)
  : msg_(msg)
  {}
  ::dumme_msgs::srv::QuaternionToEuler_Response yaw(::dumme_msgs::srv::QuaternionToEuler_Response::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Response msg_;
};

class Init_QuaternionToEuler_Response_pitch
{
public:
  explicit Init_QuaternionToEuler_Response_pitch(::dumme_msgs::srv::QuaternionToEuler_Response & msg)
  : msg_(msg)
  {}
  Init_QuaternionToEuler_Response_yaw pitch(::dumme_msgs::srv::QuaternionToEuler_Response::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_QuaternionToEuler_Response_yaw(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Response msg_;
};

class Init_QuaternionToEuler_Response_roll
{
public:
  Init_QuaternionToEuler_Response_roll()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QuaternionToEuler_Response_pitch roll(::dumme_msgs::srv::QuaternionToEuler_Response::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_QuaternionToEuler_Response_pitch(msg_);
  }

private:
  ::dumme_msgs::srv::QuaternionToEuler_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dumme_msgs::srv::QuaternionToEuler_Response>()
{
  return dumme_msgs::srv::builder::Init_QuaternionToEuler_Response_roll();
}

}  // namespace dumme_msgs

#endif  // DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__BUILDER_HPP_
