# SPDX-License-Identifier: MIT
"""Reject unsupported SO-101 capabilities before any motion is started.

Sketch only. Does not implement the manipulation server.
"""

from __future__ import annotations

from pathlib import Path

import yaml

FALSE_MEANS_REJECT = {
    "contact",
    "move_until_contact",
    "force",
    "compliance",
    "payload_estimate",
    "bimanual",
    "openarm_hardware",
    "gripper_command_force",
}

UNSUPPORTED = "UNSUPPORTED_CAPABILITY"


def load_capabilities(path: Path | None = None) -> dict:
    path = path or Path(__file__).with_name("capabilities.yaml")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def discover(manifest: dict | None = None) -> dict:
    manifest = manifest or load_capabilities()
    return dict(manifest["capabilities"])


def reject_if_unsupported(capability: str, manifest: dict | None = None) -> str | None:
    """Return UNSUPPORTED_CAPABILITY or None if the call may proceed."""
    caps = discover(manifest)
    if capability not in caps:
        return UNSUPPORTED
    value = caps[capability]
    if value is False or (capability in FALSE_MEANS_REJECT and value is not True):
        return UNSUPPORTED
    return None
