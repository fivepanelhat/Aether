# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Simple Tool Result Cache
Caches results from expensive or repetitive tool calls.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
import time


@dataclass
class CacheEntry:
    result: Any
    timestamp: float
    ttl: int  # Time to live in seconds


class ToolCache:
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl  # 5 minutes default
        self._last_sweep = time.time()

    def _make_key(self, tool_name: str, **kwargs) -> str:
        """Create a cache key from tool name and arguments."""
        sorted_args = sorted(kwargs.items())
        return f"{tool_name}:{str(sorted_args)}"

    def get(self, tool_name: str, **kwargs) -> Optional[Any]:
        key = self._make_key(tool_name, **kwargs)
        entry = self.cache.get(key)

        if entry:
            if time.time() - entry.timestamp < entry.ttl:
                return entry.result
            else:
                # Expired
                del self.cache[key]
        return None

    def set(self, tool_name: str, result: Any, ttl: Optional[int] = None, **kwargs):
        now = time.time()
        # Expired entries are otherwise only removed when their exact key is
        # re-read, so sweep periodically to bound long-lived processes.
        if now - self._last_sweep > self.default_ttl:
            self._last_sweep = now
            expired = [k for k, e in self.cache.items() if now - e.timestamp >= e.ttl]
            for k in expired:
                del self.cache[k]

        key = self._make_key(tool_name, **kwargs)
        self.cache[key] = CacheEntry(
            result=result,
            timestamp=now,
            ttl=ttl or self.default_ttl
        )

    def clear(self):
        self.cache.clear()

    def invalidate(self, tool_name: str):
        """Remove all cached entries for a specific tool."""
        keys_to_delete = [k for k in self.cache.keys() if k.startswith(f"{tool_name}:")]
        for key in keys_to_delete:
            del self.cache[key]
