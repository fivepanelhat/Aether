"""
Aether Memory Module (hardened)

Changes over previous revision:
- Append-only JSONL persistence: one entry per line, no full-file rewrite per add
- No silent exception swallowing - all failures logged with context
- Bounded in-memory load (max_entries) so long-lived memory files don't blow RAM
- Keyword search for the memory_query tool
- Corrupt lines are skipped and reported, never crash the load
"""

import json
import logging
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("AetherMemory")


@dataclass
class MemoryEntry:
 timestamp: str
 type: str
 content: str
 metadata: Dict[str, Any] = field(default_factory=dict)


class AetherMemory:
 def __init__(self, persist_path: Optional[str] = None, max_entries: int = 5000):
 self.entries: List[MemoryEntry] = []
 self.project_context: Dict[str, Any] = {}
 self.persist_path = persist_path
 self.max_entries = max_entries

 if persist_path and os.path.exists(persist_path):
 self._load_from_file()

 # ---------------- write path ----------------

 def add_entry(self, entry_type: str, content: str, metadata: Optional[Dict[str, Any]] = None):
 entry = MemoryEntry(
 timestamp=datetime.now(timezone.utc).isoformat(),
 type=entry_type,
 content=content,
 metadata=metadata or {},
 )
 self.entries.append(entry)

 # Keep in-memory list bounded
 if len(self.entries) > self.max_entries:
 self.entries = self.entries[-self.max_entries:]

 if self.persist_path:
 self._append_to_file(entry)

 def _append_to_file(self, entry: MemoryEntry):
 """Append a single JSONL line - O(1) per write, crash-safe."""
 try:
 parent = os.path.dirname(os.path.abspath(self.persist_path))
 os.makedirs(parent, exist_ok=True)
 with open(self.persist_path, "a", encoding="utf-8") as f:
 f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
 except OSError as e:
 logger.error(f"Memory persistence failed ({self.persist_path}): {e}")

 # ---------------- read path ----------------

 def _load_from_file(self):
 loaded, skipped = 0, 0
 try:
 with open(self.persist_path, "r", encoding="utf-8") as f:
 for line_no, line in enumerate(f, start=1):
 line = line.strip()
 if not line:
 continue
 try:
 data = json.loads(line)
 self.entries.append(MemoryEntry(
 timestamp=data.get("timestamp", ""),
 type=data.get("type", "unknown"),
 content=data.get("content", ""),
 metadata=data.get("metadata", {}) or {},
 ))
 loaded += 1
 except (json.JSONDecodeError, TypeError) as e:
 skipped += 1
 logger.warning(f"Skipping corrupt memory line {line_no}: {e}")
 except OSError as e:
 logger.error(f"Failed to read memory file {self.persist_path}: {e}")
 return

 # Bound after load
 if len(self.entries) > self.max_entries:
 self.entries = self.entries[-self.max_entries:]

 logger.info(f"Memory loaded: {loaded} entries ({skipped} corrupt lines skipped)")

 def get_recent_history(self, limit: int = 10) -> List[MemoryEntry]:
 return self.entries[-limit:]

 def search(self, keyword: str, limit: int = 10, entry_type: Optional[str] = None) -> List[MemoryEntry]:
 """Simple keyword recall - case-insensitive substring over content."""
 kw = keyword.lower()
 hits: List[MemoryEntry] = []
 # Newest-first, stop as soon as we have `limit` hits instead of
 # scanning the entire memory every query.
 for e in reversed(self.entries):
 if kw in e.content.lower() and (entry_type is None or e.type == entry_type):
 hits.append(e)
 if len(hits) >= limit:
 break
 return hits

 # ---------------- maintenance ----------------

 def compact(self):
 """Rewrite the JSONL file with only the bounded in-memory entries."""
 if not self.persist_path:
 return
 tmp_path = self.persist_path + ".tmp"
 try:
 with open(tmp_path, "w", encoding="utf-8") as f:
 for e in self.entries:
 f.write(json.dumps(asdict(e), ensure_ascii=False) + "\n")
 os.replace(tmp_path, self.persist_path)
 logger.info(f"Memory compacted to {len(self.entries)} entries")
 except OSError as e:
 logger.error(f"Memory compaction failed: {e}")
