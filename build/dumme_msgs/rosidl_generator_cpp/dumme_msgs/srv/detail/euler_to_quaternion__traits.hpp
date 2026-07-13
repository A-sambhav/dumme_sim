// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dumme_msgs:srv/EulerToQuaternion.idl
// generated code does not contain a copyright notice

#ifndef DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__TRAITS_HPP_
#define DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dumme_msgs/srv/detail/euler_to_quaternion__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dumme_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const EulerToQuaternion_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: roll
  {
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << ", ";
  }

  // member: pitch
  {
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EulerToQuaternion_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: roll
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "roll: ";
    rosidl_generator_traits::value_to_yaml(msg.roll, out);
    out << "\n";
  }

  // member: pitch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pitch: ";
    rosidl_generator_traits::value_to_yaml(msg.pitch, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EulerToQuaternion_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace dumme_msgs

namespace rosidl_generator_traits
{

[[deprecated("use dumme_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dumme_msgs::srv::EulerToQuaternion_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dumme_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dumme_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const dumme_msgs::srv::EulerToQuaternion_Request & msg)
{
  return dumme_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dumme_msgs::srv::EulerToQuaternion_Request>()
{
  return "dumme_msgs::srv::EulerToQuaternion_Request";
}

template<>
inline const char * name<dumme_msgs::srv::EulerToQuaternion_Request>()
{
  return "dumme_msgs/srv/EulerToQuaternion_Request";
}

template<>
struct has_fixed_size<dumme_msgs::srv::EulerToQuaternion_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dumme_msgs::srv::EulerToQuaternion_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dumme_msgs::srv::EulerToQuaternion_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dumme_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const EulerToQuaternion_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: w
  {
    out << "w: ";
    rosidl_generator_traits::value_to_yaml(msg.w, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EulerToQuaternion_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: w
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w: ";
    rosidl_generator_traits::value_to_yaml(msg.w, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EulerToQuaternion_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace dumme_msgs

namespace rosidl_generator_traits
{

[[deprecated("use dumme_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dumme_msgs::srv::EulerToQuaternion_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dumme_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dumme_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const dumme_msgs::srv::EulerToQuaternion_Response & msg)
{
  return dumme_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dumme_msgs::srv::EulerToQuaternion_Response>()
{
  return "dumme_msgs::srv::EulerToQuaternion_Response";
}

template<>
inline const char * name<dumme_msgs::srv::EulerToQuaternion_Response>()
{
  return "dumme_msgs/srv/EulerToQuaternion_Response";
}

template<>
struct has_fixed_size<dumme_msgs::srv::EulerToQuaternion_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dumme_msgs::srv::EulerToQuaternion_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dumme_msgs::srv::EulerToQuaternion_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dumme_msgs::srv::EulerToQuaternion>()
{
  return "dumme_msgs::srv::EulerToQuaternion";
}

template<>
inline const char * name<dumme_msgs::srv::EulerToQuaternion>()
{
  return "dumme_msgs/srv/EulerToQuaternion";
}

template<>
struct has_fixed_size<dumme_msgs::srv::EulerToQuaternion>
  : std::integral_constant<
    bool,
    has_fixed_size<dumme_msgs::srv::EulerToQuaternion_Request>::value &&
    has_fixed_size<dumme_msgs::srv::EulerToQuaternion_Response>::value
  >
{
};

template<>
struct has_bounded_size<dumme_msgs::srv::EulerToQuaternion>
  : std::integral_constant<
    bool,
    has_bounded_size<dumme_msgs::srv::EulerToQuaternion_Request>::value &&
    has_bounded_size<dumme_msgs::srv::EulerToQuaternion_Response>::value
  >
{
};

template<>
struct is_service<dumme_msgs::srv::EulerToQuaternion>
  : std::true_type
{
};

template<>
struct is_service_request<dumme_msgs::srv::EulerToQuaternion_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dumme_msgs::srv::EulerToQuaternion_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__TRAITS_HPP_
