# openamrobot-manipulation

Shared arm-integration framework for the OpenAMRobot ecosystem. Consumed by both the mobile manipulator (`openamr-upperbody-*`) and the future humanoid (`openamh-humanoid-*`).

**Status:** planning / early development (v0.2 cycle).

## What lives here
- **Manipulation server:** one arm-agnostic API to move any supported arm (named poses, plan, preview, execute, stop, gripper).
- **Device Package format:** a self-contained folder that adds an arm or device (description, controllers, MoveIt config, UI panel, blocks, manifest).
- **Reference arm packages:** Franka (Panda / FR3) and ReBot (Seeed Studio).

Software only. Physical arms are vendor hardware; the lift and mounts live in `openamr-upperbody-hw`.

## What we are building (v0.2)
1. Manipulation server exposing a small, stable action API over MoveIt.
2. Device Package specification, extracted from the first real integration, then proven on a second arm.
3. Two reference arm packages (Franka, ReBot) that pass the same integration path with no core-file edits.

## Contracts owned elsewhere
- API message / service / action definitions live in `openamrobot-interfaces`.
- Device Package UI panels and blocks are loaded by `openamrobot-ui`.

## Design rule
Arm-agnostic by construction. The framework commits to an interface, not to an arm. Any supported arm is one Device Package plus one docs page.

Part of the OpenAMRobot ecosystem: https://github.com/openAMRobot
