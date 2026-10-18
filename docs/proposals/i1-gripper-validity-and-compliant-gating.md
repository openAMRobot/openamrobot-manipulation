# Proposal: I1 gripper observation validity and CompliantHold gating

> **Status: Proposed, for the I1 contract owner.** This is not a contract change. It changes no I1
> or I2 field, schema or code. It answers the two open I1 questions recorded in issue #19 and in
> the PR #20 reviews, so that the I1 owner can accept, adapt or reject them.
> Owner of the decision: I1 contract owner. Consumers: A5/I2 Device Package (PR #20),
> A12 contact and compliance path (issue #14), A13 end-effector and TCP contract (issue #15).

## Public context

- Issue #19 records that the referenced I1 revision defines `final_effort_valid` and
  `effort_or_load_valid` for gripper results, while `contact_detected` and `object_detected` are
  plain booleans with no validity field. Unavailable detection could therefore be read as a
  measured "no contact".
- The 15 October review of PR #20 asks for (1) a representation of unavailable gripper
  contact/object observations that is distinguishable from a valid negative observation and
  (2) CompliantHold gating that rejects unsupported compliant control before motion, with a
  success / unsupported / unavailable case table.
- The I2 manifest already declares per-device capability flags: `gripper.contact_detection`,
  `gripper.object_detection`, `capabilities.has_compliant_control` and
  `capabilities.force_torque_sensing`, each of which may be `PENDING`.

## (a) Unavailable gripper contact and object data

**Proposal.** Add two booleans to the I1 gripper result and feedback, next to the existing pattern:

| Field | Meaning |
|---|---|
| `contact_detected_valid` | `true` only when the device measured contact state for this result |
| `object_detected_valid` | `true` only when the device measured object presence for this result |

Rules:

1. When a `*_valid` field is `false`, the paired value is `false` and carries no meaning.
   Consumers must not read it as "no contact" or "no object".
2. A device whose I2 flag is `false` or `PENDING` always reports `*_valid: false`. Only a device
   whose flag is `true` may report `*_valid: true`, and only for an observation it measured.
3. A consumer that needs contact data (for example move-until-contact in A12) treats
   `contact_detected_valid: false` as "data unavailable", never as success.

**Why validity fields.** They repeat the pattern I1 already uses for effort, they keep the
existing booleans and message layout, and older consumers see the same field types.

**Alternative.** A tri-state enum per observation (`UNKNOWN`, `NOT_DETECTED`, `DETECTED`)
replacing the booleans. It is harder to misread, but it changes field types and every consumer.

## (b) CompliantHold gating

**Proposal.** The common server dispatches CompliantHold to a device only when all of these hold:

1. `capabilities.has_compliant_control` is `true` (not `false`, not `PENDING`);
2. `capabilities.actions.compliant_hold` is `supported`, or `experimental` with development/test
   enablement;
3. `capabilities.force_torque_sensing` is not `UNKNOWN` and not `PENDING`.

Otherwise the request ends with `ACTION_REJECTED` before any device call and before any motion.
The message names the capability (`has_compliant_control`, `compliant_hold` or
`force_torque_sensing`). There is no silent downgrade to a position hold.

**Consequence for I2 (proposed, not implemented).** The I2 validator would reject a manifest that
declares `compliant_hold` as `supported` or `experimental` while `has_compliant_control` is not
`true`, and `resolve_request()` would return `ACTION_REJECTED` with `device_invoked: false` and
`motion: false` in that case. On the PR #20 head (`ab12941`) such a manifest validates and
`resolve_request("compliant_hold")` dispatches to the device; the review of PR #20 records this.

## Case table

`ACTION_REJECTED` is the rejection result already used by I2. Success and in-motion failure codes
are left to the I1 owner and are written here as "success" and "typed failure".

| # | Request | Device declaration | Observation at run time | Result | Device invoked | Motion |
|---|---|---|---|---|---|---|
| 1 | GripperCommand CLOSE | `contact_detection: true` | contact measured | success; `contact_detected: true`, `contact_detected_valid: true` | yes | yes |
| 2 | GripperCommand CLOSE | `contact_detection: true` | no contact measured | success; `contact_detected: false`, `contact_detected_valid: true` | yes | yes |
| 3 | GripperCommand CLOSE | `contact_detection: false` or `PENDING` | not measured | success; `contact_detected: false`, `contact_detected_valid: false` (unavailable, not "no contact") | yes | yes |
| 4 | MoveUntilContact | `force_torque_sensing: UNKNOWN` or `PENDING` | none | `ACTION_REJECTED` naming `force_torque_sensing` | no | no |
| 5 | MoveUntilContact | sensing declared | contact data becomes unavailable during motion | typed failure, motion stopped; never success | yes | stopped |
| 6 | CompliantHold | `has_compliant_control: true`, `compliant_hold: supported`, sensing declared | as declared | success | yes | yes |
| 7 | CompliantHold | `has_compliant_control: false` | none | `ACTION_REJECTED` naming `has_compliant_control` | no | no |
| 8 | CompliantHold | `has_compliant_control: PENDING` | none | `ACTION_REJECTED` naming `has_compliant_control` | no | no |
| 9 | CompliantHold | `compliant_hold: experimental`, no enablement | none | `ACTION_REJECTED` naming `compliant_hold` | no | no |
| 10 | CompliantHold | `has_compliant_control: true`, `force_torque_sensing: UNKNOWN` | none | `ACTION_REJECTED` naming `force_torque_sensing` | no | no |

## Recording the decision

1. The I1 owner records accept, adapt or reject for (a) and (b) in the I1 source document and
   gives it an unambiguous revision label and date.
2. A public-safe acceptance record (revision label, date, decision, no private link or content)
   goes to `openAMRobot/openamrobot-interfaces`, the owning repository for shared contracts, and
   is linked from PR #20.
3. Only then does the A5/I2 owner change the I2 schema, validator and tests in this repository,
   with a test for each row of the case table.

This proposal is a text artefact. It does not validate contact sensing, force control,
compliance, payload or physical safety on any device.
