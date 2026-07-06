"""
Pytest-native smoke and unit tests for Aether.
Run: pytest tests/ -v
"""


from aether import __version__
from aether.orchestrator import AetherOrchestrator, _resolve_skills_directory
from aether.guardrails import Guardrails
from aether.tools.file_writer import FileWriterTool
from aether.tools.file_reader import FileReaderTool


def test_version_is_single_sourced():
    assert __version__, "aether.__version__ must be set"


def test_orchestrator_initialises_without_skills(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("AETHER_SKILLS_DIR", raising=False)
    orch = AetherOrchestrator()
    assert orch.get_available_skills() == []
    assert "file_writer" in orch.get_available_tools()


def test_skills_directory_resolution_env_var(tmp_path, monkeypatch):
    skills_dir = tmp_path / "my-skills"
    skills_dir.mkdir()
    monkeypatch.setenv("AETHER_SKILLS_DIR", str(skills_dir))
    assert _resolve_skills_directory() == str(skills_dir)


def test_tool_calls_logged_exactly_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    orch = AetherOrchestrator()
    orch.start_task("test goal")
    orch.call_tool("directory_lister", directory=str(tmp_path))
    assert len(orch.state.tool_calls) == 1


def test_pipeline_max_steps_zero_does_not_crash(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    orch = AetherOrchestrator()
    state = orch.run_pipeline("do nothing", max_steps=0)
    assert state.current_phase == "pipeline_complete"


def test_file_writer_blocks_path_traversal(tmp_path):
    tool = FileWriterTool(allowed_root=str(tmp_path))
    result = tool.run(file_path="../../etc/evil.txt", content="x")
    assert result.success is False
    assert "outside allowed root" in result.error


def test_file_writer_handles_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tool = FileWriterTool(allowed_root=str(tmp_path))
    result = tool.run(file_path="notes.txt", content="kia ora")
    assert result.success is True
    assert (tmp_path / "notes.txt").read_text() == "kia ora"


def test_file_reader_max_lines_on_short_file(tmp_path):
    f = tmp_path / "short.txt"
    f.write_text("one\ntwo\n")
    result = FileReaderTool().run(file_path=str(f), max_lines=100)
    assert result.success is True
    assert result.output == "one\ntwo\n"


def test_guardrails_hitl_for_file_writer():
    g = Guardrails()
    assert g.enforce_hitl("file_writer") is True


def test_guardrails_cultural_sensitivity():
    g = Guardrails()
    assert g.assess_cultural_sensitivity("update the marae garden dashboard for whanau") == "high"
