#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__EulerToQuaternion_Request() -> *const std::ffi::c_void;
}

#[link(name = "dumme_msgs__rosidl_generator_c")]
extern "C" {
    fn dumme_msgs__srv__EulerToQuaternion_Request__init(msg: *mut EulerToQuaternion_Request) -> bool;
    fn dumme_msgs__srv__EulerToQuaternion_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Request>, size: usize) -> bool;
    fn dumme_msgs__srv__EulerToQuaternion_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Request>);
    fn dumme_msgs__srv__EulerToQuaternion_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EulerToQuaternion_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Request>) -> bool;
}

// Corresponds to dumme_msgs__srv__EulerToQuaternion_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EulerToQuaternion_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub roll: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pitch: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub yaw: f64,

}



impl Default for EulerToQuaternion_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dumme_msgs__srv__EulerToQuaternion_Request__init(&mut msg as *mut _) {
        panic!("Call to dumme_msgs__srv__EulerToQuaternion_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EulerToQuaternion_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EulerToQuaternion_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EulerToQuaternion_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dumme_msgs/srv/EulerToQuaternion_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__EulerToQuaternion_Request() }
  }
}


#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__EulerToQuaternion_Response() -> *const std::ffi::c_void;
}

#[link(name = "dumme_msgs__rosidl_generator_c")]
extern "C" {
    fn dumme_msgs__srv__EulerToQuaternion_Response__init(msg: *mut EulerToQuaternion_Response) -> bool;
    fn dumme_msgs__srv__EulerToQuaternion_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Response>, size: usize) -> bool;
    fn dumme_msgs__srv__EulerToQuaternion_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Response>);
    fn dumme_msgs__srv__EulerToQuaternion_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EulerToQuaternion_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<EulerToQuaternion_Response>) -> bool;
}

// Corresponds to dumme_msgs__srv__EulerToQuaternion_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EulerToQuaternion_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub w: f64,

}



impl Default for EulerToQuaternion_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dumme_msgs__srv__EulerToQuaternion_Response__init(&mut msg as *mut _) {
        panic!("Call to dumme_msgs__srv__EulerToQuaternion_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EulerToQuaternion_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__EulerToQuaternion_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EulerToQuaternion_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EulerToQuaternion_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dumme_msgs/srv/EulerToQuaternion_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__EulerToQuaternion_Response() }
  }
}


#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__QuaternionToEuler_Request() -> *const std::ffi::c_void;
}

#[link(name = "dumme_msgs__rosidl_generator_c")]
extern "C" {
    fn dumme_msgs__srv__QuaternionToEuler_Request__init(msg: *mut QuaternionToEuler_Request) -> bool;
    fn dumme_msgs__srv__QuaternionToEuler_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Request>, size: usize) -> bool;
    fn dumme_msgs__srv__QuaternionToEuler_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Request>);
    fn dumme_msgs__srv__QuaternionToEuler_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QuaternionToEuler_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Request>) -> bool;
}

// Corresponds to dumme_msgs__srv__QuaternionToEuler_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QuaternionToEuler_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub w: f64,

}



impl Default for QuaternionToEuler_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dumme_msgs__srv__QuaternionToEuler_Request__init(&mut msg as *mut _) {
        panic!("Call to dumme_msgs__srv__QuaternionToEuler_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QuaternionToEuler_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QuaternionToEuler_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QuaternionToEuler_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dumme_msgs/srv/QuaternionToEuler_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__QuaternionToEuler_Request() }
  }
}


#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__QuaternionToEuler_Response() -> *const std::ffi::c_void;
}

#[link(name = "dumme_msgs__rosidl_generator_c")]
extern "C" {
    fn dumme_msgs__srv__QuaternionToEuler_Response__init(msg: *mut QuaternionToEuler_Response) -> bool;
    fn dumme_msgs__srv__QuaternionToEuler_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Response>, size: usize) -> bool;
    fn dumme_msgs__srv__QuaternionToEuler_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Response>);
    fn dumme_msgs__srv__QuaternionToEuler_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QuaternionToEuler_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<QuaternionToEuler_Response>) -> bool;
}

// Corresponds to dumme_msgs__srv__QuaternionToEuler_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QuaternionToEuler_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub roll: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pitch: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub yaw: f64,

}



impl Default for QuaternionToEuler_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dumme_msgs__srv__QuaternionToEuler_Response__init(&mut msg as *mut _) {
        panic!("Call to dumme_msgs__srv__QuaternionToEuler_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QuaternionToEuler_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dumme_msgs__srv__QuaternionToEuler_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QuaternionToEuler_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QuaternionToEuler_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dumme_msgs/srv/QuaternionToEuler_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dumme_msgs__srv__QuaternionToEuler_Response() }
  }
}






#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dumme_msgs__srv__EulerToQuaternion() -> *const std::ffi::c_void;
}

// Corresponds to dumme_msgs__srv__EulerToQuaternion
#[allow(missing_docs, non_camel_case_types)]
pub struct EulerToQuaternion;

impl rosidl_runtime_rs::Service for EulerToQuaternion {
    type Request = EulerToQuaternion_Request;
    type Response = EulerToQuaternion_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dumme_msgs__srv__EulerToQuaternion() }
    }
}




#[link(name = "dumme_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dumme_msgs__srv__QuaternionToEuler() -> *const std::ffi::c_void;
}

// Corresponds to dumme_msgs__srv__QuaternionToEuler
#[allow(missing_docs, non_camel_case_types)]
pub struct QuaternionToEuler;

impl rosidl_runtime_rs::Service for QuaternionToEuler {
    type Request = QuaternionToEuler_Request;
    type Response = QuaternionToEuler_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dumme_msgs__srv__QuaternionToEuler() }
    }
}


