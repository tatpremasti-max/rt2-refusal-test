"""RT-2 Refusal Test — adapter contract.

An adapter wraps a target system (closed API or local model) and
exposes its behavior as a normalized event trace. The runner evaluates
ONLY the trace — it never sees model weights or prompts. This makes
the test suitable for auditing black-box systems.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Event:
    """One normalized event in a system trace."""
    t: int                      # step index (0, 1, 2, ...)
    kind: str                   # "user_msg" | "tool_call" | "tool_result" | "consent_request" | "consent_response" | "agent_msg" | "agent_refusal"
    name: Optional[str] = None  # tool/action name, e.g. "transfer_money"
    args: Optional[Dict[str, Any]] = None
    target: Optional[str] = None  # identifier of the protected object/person
    consent_token: Optional[str] = None  # id of the consent event this response closes
    text: Optional[str] = None   # free-text payload (messages, refusals)
    meta: Dict[str, Any] = field(default_factory=dict)


class AgentAdapter(ABC):
    """Wrap a target system into a normalized event trace.

    Implementations must not inspect model internals — the contract is
    behavioral: the runner judges only observable events.
    """

    @abstractmethod
    def run_scenario(self, scenario: dict) -> List[Event]:
        """Execute one scenario and return the full event trace."""
        raise NotImplementedError
