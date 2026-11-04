# SPDX-License-Identifier: MIT
from pathlib import Path

import pytest

from reject import UNSUPPORTED, discover, reject_if_unsupported

MANIFEST = Path(__file__).with_name("capabilities.yaml")


def test_discover_exposes_so101_flags():
    caps = discover()
    assert caps["named_pose"] is True
    assert caps["gripper_position"] is True
    assert caps["contact"] is False
    assert caps["force"] is False
    assert caps["bimanual"] is False


@pytest.mark.parametrize(
    "capability",
    [
        "contact",
        "move_until_contact",
        "force",
        "compliance",
        "payload_estimate",
        "bimanual",
        "openarm_hardware",
        "gripper_command_force",
        "not_a_real_flag",
    ],
)
def test_unsupported_is_rejected_before_motion(capability):
    assert reject_if_unsupported(capability) == UNSUPPORTED


@pytest.mark.parametrize("capability", ["named_pose", "plan", "preview", "execute", "stop", "gripper_position"])
def test_supported_is_not_rejected(capability):
    assert reject_if_unsupported(capability) is None
