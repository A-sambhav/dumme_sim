// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dumme_msgs:srv/EulerToQuaternion.idl
// generated code does not contain a copyright notice

#ifndef DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__STRUCT_H_
#define DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/EulerToQuaternion in the package dumme_msgs.
typedef struct dumme_msgs__srv__EulerToQuaternion_Request
{
  double roll;
  double pitch;
  double yaw;
} dumme_msgs__srv__EulerToQuaternion_Request;

// Struct for a sequence of dumme_msgs__srv__EulerToQuaternion_Request.
typedef struct dumme_msgs__srv__EulerToQuaternion_Request__Sequence
{
  dumme_msgs__srv__EulerToQuaternion_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dumme_msgs__srv__EulerToQuaternion_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/EulerToQuaternion in the package dumme_msgs.
typedef struct dumme_msgs__srv__EulerToQuaternion_Response
{
  double x;
  double y;
  double z;
  double w;
} dumme_msgs__srv__EulerToQuaternion_Response;

// Struct for a sequence of dumme_msgs__srv__EulerToQuaternion_Response.
typedef struct dumme_msgs__srv__EulerToQuaternion_Response__Sequence
{
  dumme_msgs__srv__EulerToQuaternion_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dumme_msgs__srv__EulerToQuaternion_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DUMME_MSGS__SRV__DETAIL__EULER_TO_QUATERNION__STRUCT_H_
