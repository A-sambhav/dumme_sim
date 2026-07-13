#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to dumme_msgs__srv__EulerToQuaternion_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EulerToQuaternion_Request::default())
  }
}

impl rosidl_runtime_rs::Message for EulerToQuaternion_Request {
  type RmwMsg = super::srv::rmw::EulerToQuaternion_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        roll: msg.roll,
        pitch: msg.pitch,
        yaw: msg.yaw,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
    }
  }
}


// Corresponds to dumme_msgs__srv__EulerToQuaternion_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EulerToQuaternion_Response::default())
  }
}

impl rosidl_runtime_rs::Message for EulerToQuaternion_Response {
  type RmwMsg = super::srv::rmw::EulerToQuaternion_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
        w: msg.w,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      w: msg.w,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      w: msg.w,
    }
  }
}


// Corresponds to dumme_msgs__srv__QuaternionToEuler_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::QuaternionToEuler_Request::default())
  }
}

impl rosidl_runtime_rs::Message for QuaternionToEuler_Request {
  type RmwMsg = super::srv::rmw::QuaternionToEuler_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
        w: msg.w,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      w: msg.w,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      w: msg.w,
    }
  }
}


// Corresponds to dumme_msgs__srv__QuaternionToEuler_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::QuaternionToEuler_Response::default())
  }
}

impl rosidl_runtime_rs::Message for QuaternionToEuler_Response {
  type RmwMsg = super::srv::rmw::QuaternionToEuler_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        roll: msg.roll,
        pitch: msg.pitch,
        yaw: msg.yaw,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      roll: msg.roll,
      pitch: msg.pitch,
      yaw: msg.yaw,
    }
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


