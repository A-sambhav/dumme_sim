// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dumme_msgs:srv/EulerToQuaternion.idl
// generated code does not contain a copyright notice
#include "dumme_msgs/srv/detail/euler_to_quaternion__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
dumme_msgs__srv__EulerToQuaternion_Request__init(dumme_msgs__srv__EulerToQuaternion_Request * msg)
{
  if (!msg) {
    return false;
  }
  // roll
  // pitch
  // yaw
  return true;
}

void
dumme_msgs__srv__EulerToQuaternion_Request__fini(dumme_msgs__srv__EulerToQuaternion_Request * msg)
{
  if (!msg) {
    return;
  }
  // roll
  // pitch
  // yaw
}

bool
dumme_msgs__srv__EulerToQuaternion_Request__are_equal(const dumme_msgs__srv__EulerToQuaternion_Request * lhs, const dumme_msgs__srv__EulerToQuaternion_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // roll
  if (lhs->roll != rhs->roll) {
    return false;
  }
  // pitch
  if (lhs->pitch != rhs->pitch) {
    return false;
  }
  // yaw
  if (lhs->yaw != rhs->yaw) {
    return false;
  }
  return true;
}

bool
dumme_msgs__srv__EulerToQuaternion_Request__copy(
  const dumme_msgs__srv__EulerToQuaternion_Request * input,
  dumme_msgs__srv__EulerToQuaternion_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // roll
  output->roll = input->roll;
  // pitch
  output->pitch = input->pitch;
  // yaw
  output->yaw = input->yaw;
  return true;
}

dumme_msgs__srv__EulerToQuaternion_Request *
dumme_msgs__srv__EulerToQuaternion_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Request * msg = (dumme_msgs__srv__EulerToQuaternion_Request *)allocator.allocate(sizeof(dumme_msgs__srv__EulerToQuaternion_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dumme_msgs__srv__EulerToQuaternion_Request));
  bool success = dumme_msgs__srv__EulerToQuaternion_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dumme_msgs__srv__EulerToQuaternion_Request__destroy(dumme_msgs__srv__EulerToQuaternion_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dumme_msgs__srv__EulerToQuaternion_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__init(dumme_msgs__srv__EulerToQuaternion_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Request * data = NULL;

  if (size) {
    data = (dumme_msgs__srv__EulerToQuaternion_Request *)allocator.zero_allocate(size, sizeof(dumme_msgs__srv__EulerToQuaternion_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dumme_msgs__srv__EulerToQuaternion_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dumme_msgs__srv__EulerToQuaternion_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__fini(dumme_msgs__srv__EulerToQuaternion_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      dumme_msgs__srv__EulerToQuaternion_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

dumme_msgs__srv__EulerToQuaternion_Request__Sequence *
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Request__Sequence * array = (dumme_msgs__srv__EulerToQuaternion_Request__Sequence *)allocator.allocate(sizeof(dumme_msgs__srv__EulerToQuaternion_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dumme_msgs__srv__EulerToQuaternion_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__destroy(dumme_msgs__srv__EulerToQuaternion_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dumme_msgs__srv__EulerToQuaternion_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__are_equal(const dumme_msgs__srv__EulerToQuaternion_Request__Sequence * lhs, const dumme_msgs__srv__EulerToQuaternion_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dumme_msgs__srv__EulerToQuaternion_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dumme_msgs__srv__EulerToQuaternion_Request__Sequence__copy(
  const dumme_msgs__srv__EulerToQuaternion_Request__Sequence * input,
  dumme_msgs__srv__EulerToQuaternion_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dumme_msgs__srv__EulerToQuaternion_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dumme_msgs__srv__EulerToQuaternion_Request * data =
      (dumme_msgs__srv__EulerToQuaternion_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dumme_msgs__srv__EulerToQuaternion_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dumme_msgs__srv__EulerToQuaternion_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dumme_msgs__srv__EulerToQuaternion_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
dumme_msgs__srv__EulerToQuaternion_Response__init(dumme_msgs__srv__EulerToQuaternion_Response * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  // w
  return true;
}

void
dumme_msgs__srv__EulerToQuaternion_Response__fini(dumme_msgs__srv__EulerToQuaternion_Response * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
  // w
}

bool
dumme_msgs__srv__EulerToQuaternion_Response__are_equal(const dumme_msgs__srv__EulerToQuaternion_Response * lhs, const dumme_msgs__srv__EulerToQuaternion_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // w
  if (lhs->w != rhs->w) {
    return false;
  }
  return true;
}

bool
dumme_msgs__srv__EulerToQuaternion_Response__copy(
  const dumme_msgs__srv__EulerToQuaternion_Response * input,
  dumme_msgs__srv__EulerToQuaternion_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // w
  output->w = input->w;
  return true;
}

dumme_msgs__srv__EulerToQuaternion_Response *
dumme_msgs__srv__EulerToQuaternion_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Response * msg = (dumme_msgs__srv__EulerToQuaternion_Response *)allocator.allocate(sizeof(dumme_msgs__srv__EulerToQuaternion_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dumme_msgs__srv__EulerToQuaternion_Response));
  bool success = dumme_msgs__srv__EulerToQuaternion_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dumme_msgs__srv__EulerToQuaternion_Response__destroy(dumme_msgs__srv__EulerToQuaternion_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dumme_msgs__srv__EulerToQuaternion_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__init(dumme_msgs__srv__EulerToQuaternion_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Response * data = NULL;

  if (size) {
    data = (dumme_msgs__srv__EulerToQuaternion_Response *)allocator.zero_allocate(size, sizeof(dumme_msgs__srv__EulerToQuaternion_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dumme_msgs__srv__EulerToQuaternion_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dumme_msgs__srv__EulerToQuaternion_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__fini(dumme_msgs__srv__EulerToQuaternion_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      dumme_msgs__srv__EulerToQuaternion_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

dumme_msgs__srv__EulerToQuaternion_Response__Sequence *
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dumme_msgs__srv__EulerToQuaternion_Response__Sequence * array = (dumme_msgs__srv__EulerToQuaternion_Response__Sequence *)allocator.allocate(sizeof(dumme_msgs__srv__EulerToQuaternion_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dumme_msgs__srv__EulerToQuaternion_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__destroy(dumme_msgs__srv__EulerToQuaternion_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dumme_msgs__srv__EulerToQuaternion_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__are_equal(const dumme_msgs__srv__EulerToQuaternion_Response__Sequence * lhs, const dumme_msgs__srv__EulerToQuaternion_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dumme_msgs__srv__EulerToQuaternion_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dumme_msgs__srv__EulerToQuaternion_Response__Sequence__copy(
  const dumme_msgs__srv__EulerToQuaternion_Response__Sequence * input,
  dumme_msgs__srv__EulerToQuaternion_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dumme_msgs__srv__EulerToQuaternion_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dumme_msgs__srv__EulerToQuaternion_Response * data =
      (dumme_msgs__srv__EulerToQuaternion_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dumme_msgs__srv__EulerToQuaternion_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dumme_msgs__srv__EulerToQuaternion_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dumme_msgs__srv__EulerToQuaternion_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
