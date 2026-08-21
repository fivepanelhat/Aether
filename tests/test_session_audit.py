"""Smoke tests for SessionEvent audit bridge (Sprint A)."""

from aether.session_audit import NullSessionEventStore, make_session_store, new_session_id


def test_null_store_emit_is_noop():
    store = NullSessionEventStore()
    assert store.emit(session_id="s", event_type="session_start", actor="t") is None
    assert store.list_session("s") == []


def test_new_session_id_is_uuid_like():
    sid = new_session_id()
    assert isinstance(sid, str) and len(sid) >= 32


def test_make_session_store_default_without_core_or_with():
    store = make_session_store(storage_path="/tmp/aether_test_events.jsonl")
    # Either Null or real store; emit must not raise
    store.emit(session_id="s1", event_type="session_start", actor="test", payload={})
