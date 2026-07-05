# Copyright 2026 Aether Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Aether Memory Module
Simple but effective memory system for tasks, decisions, and context.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os


@dataclass
class MemoryEntry:
    timestamp: str
    type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class AetherMemory:
    def __init__(self, persist_path: Optional[str] = None):
        self.entries: List[MemoryEntry] = []
        self.project_context: Dict[str, Any] = {}
        self.persist_path = persist_path

        if persist_path and os.path.exists(persist_path):
            self._load_from_file()

    def add_entry(self, entry_type: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            type=entry_type,
            content=content,
            metadata=metadata or {}
        )
        self.entries.append(entry)

        if self.persist_path:
            self._save_to_file()

    def get_recent_history(self, limit: int = 10) -> List[MemoryEntry]:
        return self.entries[-limit:]

    def _save_to_file(self):
        try:
            data = {
                "entries": [
                    {
                        "timestamp": e.timestamp,
                        "type": e.type,
                        "content": e.content,
                        "metadata": e.metadata
                    } for e in self.entries
                ],
                "project_context": self.project_context
            }
            with open(self.persist_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _load_from_file(self):
        try:
            with open(self.persist_path, "r") as f:
                data = json.load(f)
                self.entries = [MemoryEntry(**entry) for entry in data.get("entries", [])]
                self.project_context = data.get("project_context", {})
        except Exception:
            pass
