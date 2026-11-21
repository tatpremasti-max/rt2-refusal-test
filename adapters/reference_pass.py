"""Level-2 reference implementation: honors refusals. MUST PASS RT-2."""
from __future__ import annotations
from typing import List
from .base import AgentAdapter, Event


class ReferencePassAdapter(AgentAdapter):
    """Reference agent: records refusal, stops the goal, asks once at most.

    On refusal: records decision as HONORED (reversible) or CLARIFY-HALT,
    then halts the refused goal. No alternative pressure after
    irreversible refusals.
    """

    def run_scenario(self, scenario: dict) -> List[Event]:
        events: List[Event] = [Event(t=0, kind="user_msg",
                                     text=scenario["prompt"])]
        step = 1
        for action in scenario["prohibited_actions"]:
            decision = "HONORED" if action.get("reversible", False) else "CLARIFY_HALT"
            events.append(Event(t=step, kind="agent_refusal",
                                text=f"Refusing: {action['goal']}.",
                                meta={"decision": decision,
                                      "refused_goal": action["goal"]}))
            step += 1
        return events
