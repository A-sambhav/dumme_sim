#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <rclcpp_components/register_node_macro.hpp>
#include "dumme_msgs/action/dumme_task.hpp"
#include <moveit/move_group_interface/move_group_interface.h>

#include <memory>


using namespace std::placeholders;

namespace dumme_remote
{
class TaskServer : public rclcpp::Node
{
public:
  explicit TaskServer(const rclcpp::NodeOptions& options = rclcpp::NodeOptions())
    : Node("task_server", options)
  {
    RCLCPP_INFO(get_logger(), "Starting the Server");
    action_server_ = rclcpp_action::create_server<dumme_msgs::action::DummeTask>(
        this, "task_server", std::bind(&TaskServer::goalCallback, this, _1, _2),
        std::bind(&TaskServer::cancelCallback, this, _1),
        std::bind(&TaskServer::acceptedCallback, this, _1));
  }

private:
  rclcpp_action::Server<dumme_msgs::action::DummeTask>::SharedPtr action_server_;
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> arm_move_group;
  std::vector<double> arm_joint_goal;

  rclcpp_action::GoalResponse goalCallback(
      const rclcpp_action::GoalUUID& uuid,
      std::shared_ptr<const dumme_msgs::action::DummeTask::Goal> goal)
  {
    RCLCPP_INFO(get_logger(), "Received goal request with id %d", goal->task_number);
    (void)uuid;
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse cancelCallback(
      const std::shared_ptr<rclcpp_action::ServerGoalHandle<dumme_msgs::action::DummeTask>> goal_handle)
  {
    (void)goal_handle;
    RCLCPP_INFO(get_logger(), "Received request to cancel goal");
    auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
    arm_move_group.stop();
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void acceptedCallback(
      const std::shared_ptr<rclcpp_action::ServerGoalHandle<dumme_msgs::action::DummeTask>> goal_handle)
  {
    // this needs to return quickly to avoid blocking the executor, so spin up a new thread
    std::thread{ std::bind(&TaskServer::execute, this, _1), goal_handle }.detach();
  }

  void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<dumme_msgs::action::DummeTask>> goal_handle)
  {
    RCLCPP_INFO(get_logger(), "Executing goal");
    auto result = std::make_shared<dumme_msgs::action::DummeTask::Result>();

    // MoveIt 2 Interface
    if(!arm_move_group){
      arm_move_group = std::make_shared<moveit::planning_interface::MoveGroupInterface>(shared_from_this(), "arm");
    }

    // Joint order: shoulder_rotation_plate_joint, shoulder_joint, elbow_joint, wrist_joint
    if (goal_handle->get_goal()->task_number == 0)
    {
      arm_joint_goal = {0.0, 0.0, 0.0, 0.0};
    }
    else if (goal_handle->get_goal()->task_number == 1)
    {
      arm_joint_goal = {-1.14, -0.6, -0.07, 0.0};
    }
    else if (goal_handle->get_goal()->task_number == 2)
    {
      arm_joint_goal = {-1.57, 0.0, -0.9, 0.0};
    }
    else
    {
      RCLCPP_ERROR(get_logger(), "Invalid Task Number");
      return;
    }

    arm_move_group->setStartState(*arm_move_group->getCurrentState());

    bool arm_within_bounds = arm_move_group->setJointValueTarget(arm_joint_goal);
    if (!arm_within_bounds)
    {
      RCLCPP_WARN(get_logger(),
                  "Target joint position(s) were outside of limits, but we will plan and clamp to the limits ");
      return;
    }

    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;
    bool arm_plan_success = (arm_move_group->plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS);

    if(arm_plan_success)
    {
      RCLCPP_INFO(get_logger(), "Planner SUCCEED, moving the arm");
      arm_move_group->move();
    }
    else
    {
      RCLCPP_ERROR(get_logger(), "Planner failed!");
      return;
    }

    result->success = true;
    goal_handle->succeed(result);
    RCLCPP_INFO(get_logger(), "Goal succeeded");
  }
};
}  // namespace dumme_remote

RCLCPP_COMPONENTS_REGISTER_NODE(dumme_remote::TaskServer)
