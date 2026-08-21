"""Smoke tests for SessionEvent audit bridge (Sprint A)."""

from aether.session_audit import NullSessionEventStore, get_store


def test_null_store_emit_is_noop():
    store = NullSessionEventStore()
    assert store.emit(session_id="s", event_type="session_start", actor="t") is None
    assert store.list_session("s") == []
    assert store.resume_from("s", after_event_id="x") == []


def test_get_store_force_null():
    store = get_store(force_null=True)
    assert isinstance(store, NullSessionEventStore)
    store.emit(session_id="s1", event_type="session_start", actor="test", payload={})


def test_get_store_default_emit_does_not_raise(tmp_path):
    # Without Core installed → Null; with Core → real store. Either way emit is safe.
    path = tmp_path / "session_events.jsonl"
    store = get_store(storage_path=path)
    store.emit(session_id="s1", event_type="session_start", actor="test", payload={})
