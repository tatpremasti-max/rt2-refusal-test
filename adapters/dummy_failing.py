"""Level-1 stub: parrots compliance, then acts anyway. MUST FAIL RT-2."""
from __future__ import annotations
from typing import List
from .base import AgentAdapter, Event


class DummyFailingAdapter(AgentAdapter):
    """Simulates a 'polite yes' agent that ignores refusals.

    Acknowledges every refusal verbally, then performs the refused
    action regardless — the classic parrot-compliance failure.
    """

    def run_scenario(self, scenario: dict) -> List[Event]:
        events: List[Event] = [Event(t=0, kind="user_msg",
                                     text=scenario["prompt"])]
        step = 1
        for action in scenario["prohibited_actions"]:
            events.append(Event(t=step, kind="agent_refusal",
                                text="I understand your concern, but proceeding anyway.",
                                meta={"refused_goal": action["goal"]}))
            step += 1
            events.append(Event(t=step, kind="tool_call",
                                name=action["tool"],
                                args=action["args"],
                                target=action["target"]))
            step += 1
        return events
