# SO-101 portability fixture — first sketch

Status: sketch only. Not a Device Package. Not a frozen folder schema.
Owners to review: Mohamed Sayed, Om Jagtap (A5/I2 schema).
Source of joint/control facts: https://github.com/adoodevv/so101_ros2 (sim / fake-hardware).
Physical hardware and contact behaviour are **not** claimed.

This folder must stay out of `integration/openarm_*`.

## What SO-101 can actually do (sim / fake)

- 5-DoF arm + 1 gripper jaw, position control
- `ros2_control` with `arm_controller` (JointTrajectory) and a gripper controller
- MoveIt 2 groups `arm` and `gripper`; named state `home`
- Gazebo Harmonic bring-up and fake-hardware path
- Optional D435 mesh exists in the description; not treated as a required fixture capability

## Joints / gripper / control

Arm joints (MoveIt group `arm`):

- `shoulder_pan`
- `shoulder_lift`
- `elbow_flex`
- `wrist_flex`
- `wrist_roll`

Gripper joint: `gripper` (group `gripper`, parent link `gripper_frame_link`).

Command interfaces in the description: **position** only.

Controllers observed in `so101_ros2`:

| Controller | Type (sim) | Topic / action |
|---|---|---|
| `arm_controller` | `joint_trajectory_controller/JointTrajectoryController` | `/arm_controller/joint_trajectory` |
| `gripper_controller` | JTC in `ros2_controllers.yaml`; also documented as ForwardCommand | `/gripper_controller/commands` or follow_joint_trajectory |

Mount frame for a future combined model: `base_link` (parent of `shoulder_pan`). OpenAMRobot mast transform is **not** defined here.

## Supported vs unsupported

See `capabilities.yaml`. Supported means “this stack can be asked to do it in sim/fake.” Unsupported must be rejected, not faked.

Unsupported on purpose:

- contact / `move_until_contact`
- force, compliance, payload estimate
- bimanual
- OpenArm CAN / `openarm_hardware`
- GripperCommand force grasp

## Rejection rule (proposed, not an I2 contract)

If a caller asks for a capability whose flag is `false`, return a typed failure `UNSUPPORTED_CAPABILITY` and do not start motion. See `reject.py`.

## What the Device Package will need to describe (notes for Om)

Do not treat this list as a schema freeze.

1. Device id (`so101`) and DoF
2. Joint name list + MoveIt group names
3. Control interfaces present (`position`)
4. Capability flags (contact/force/gripper-mode/bimanual)
5. Controller names and action types
6. Mount frame (`base_link`) and EE frame (`gripper_frame_link`)
7. Provenance: sim / fake / real
8. Rejection code for unsupported flags

## Out of scope this pass

Combined URDF, I1 manipulation server, PR #9 OpenArm files, hardware bring-up, folder layout freeze.
