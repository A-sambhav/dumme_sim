// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dumme_msgs:srv/QuaternionToEuler.idl
// generated code does not contain a copyright notice

#ifndef DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__STRUCT_H_
#define DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/QuaternionToEuler in the package dumme_msgs.
typedef struct dumme_msgs__srv__QuaternionToEuler_Request
{
  double x;
  double y;
  double z;
  double w;
} dumme_msgs__srv__QuaternionToEuler_Request;

// Struct for a sequence of dumme_msgs__srv__QuaternionToEuler_Request.
typedef struct dumme_msgs__srv__QuaternionToEuler_Request__Sequence
{
  dumme_msgs__srv__QuaternionToEuler_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dumme_msgs__srv__QuaternionToEuler_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/QuaternionToEuler in the package dumme_msgs.
typedef struct dumme_msgs__srv__QuaternionToEuler_Response
{
  double roll;
  double pitch;
  double yaw;
} dumme_msgs__srv__QuaternionToEuler_Response;

// Struct for a sequence of dumme_msgs__srv__QuaternionToEuler_Response.
typedef struct dumme_msgs__srv__QuaternionToEuler_Response__Sequence
{
  dumme_msgs__srv__QuaternionToEuler_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dumme_msgs__srv__QuaternionToEuler_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DUMME_MSGS__SRV__DETAIL__QUATERNION_TO_EULER__STRUCT_H_
