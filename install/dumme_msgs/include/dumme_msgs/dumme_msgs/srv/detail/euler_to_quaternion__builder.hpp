// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dumme_msgs:srv/EulerToQuaternion.idl
// generated code does not contain a copyright notice

#ifndef DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__BUILDER_HPP_
#define DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dumme_msgs/srv/detail/euler_to_quaternion__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dumme_msgs
{

namespace srv
{

namespace builder
{

class Init_EulerToQuaternion_Request_yaw
{
public:
  explicit Init_EulerToQuaternion_Request_yaw(::dumme_msgs::srv::EulerToQuaternion_Request & msg)
  : msg_(msg)
  {}
  ::dumme_msgs::srv::EulerToQuaternion_Request yaw(::dumme_msgs::srv::EulerToQuaternion_Request::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Request msg_;
};

class Init_EulerToQuaternion_Request_pitch
{
public:
  explicit Init_EulerToQuaternion_Request_pitch(::dumme_msgs::srv::EulerToQuaternion_Request & msg)
  : msg_(msg)
  {}
  Init_EulerToQuaternion_Request_yaw pitch(::dumme_msgs::srv::EulerToQuaternion_Request::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_EulerToQuaternion_Request_yaw(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Request msg_;
};

class Init_EulerToQuaternion_Request_roll
{
public:
  Init_EulerToQuaternion_Request_roll()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EulerToQuaternion_Request_pitch roll(::dumme_msgs::srv::EulerToQuaternion_Request::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_EulerToQuaternion_Request_pitch(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dumme_msgs::srv::EulerToQuaternion_Request>()
{
  return dumme_msgs::srv::builder::Init_EulerToQuaternion_Request_roll();
}

}  // namespace dumme_msgs


namespace dumme_msgs
{

namespace srv
{

namespace builder
{

class Init_EulerToQuaternion_Response_w
{
public:
  explicit Init_EulerToQuaternion_Response_w(::dumme_msgs::srv::EulerToQuaternion_Response & msg)
  : msg_(msg)
  {}
  ::dumme_msgs::srv::EulerToQuaternion_Response w(::dumme_msgs::srv::EulerToQuaternion_Response::_w_type arg)
  {
    msg_.w = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Response msg_;
};

class Init_EulerToQuaternion_Response_z
{
public:
  explicit Init_EulerToQuaternion_Response_z(::dumme_msgs::srv::EulerToQuaternion_Response & msg)
  : msg_(msg)
  {}
  Init_EulerToQuaternion_Response_w z(::dumme_msgs::srv::EulerToQuaternion_Response::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_EulerToQuaternion_Response_w(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Response msg_;
};

class Init_EulerToQuaternion_Response_y
{
public:
  explicit Init_EulerToQuaternion_Response_y(::dumme_msgs::srv::EulerToQuaternion_Response & msg)
  : msg_(msg)
  {}
  Init_EulerToQuaternion_Response_z y(::dumme_msgs::srv::EulerToQuaternion_Response::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_EulerToQuaternion_Response_z(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Response msg_;
};

class Init_EulerToQuaternion_Response_x
{
public:
  Init_EulerToQuaternion_Response_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EulerToQuaternion_Response_y x(::dumme_msgs::srv::EulerToQuaternion_Response::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_EulerToQuaternion_Response_y(msg_);
  }

private:
  ::dumme_msgs::srv::EulerToQuaternion_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dumme_msgs::srv::EulerToQuaternion_Response>()
{
  return dumme_msgs::srv::builder::Init_EulerToQuaternion_Response_x();
}

}  // namespace dumme_msgs

#endif  // DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__BUILDER_HPP_
