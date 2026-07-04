"""
Aether Tool System - Base Class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ToolResult:
    success: bool
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Tool(ABC):
    name: str = "base_tool"
    description: str = "Base tool description"
    input_schema: Dict[str, str] = {}

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        pass

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def __repr__(self):
        return f"<Tool name={self.name}>"
