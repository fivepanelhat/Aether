"""
Pytest-native smoke and unit tests for Aether.
Run: pytest tests/ -v
"""

from aether import __version__
from aether.orchestrator import AetherOrchestrator, _resolve_skills_directory
from aether.guardrails import Guardrails
from aether.threat_modeling import ThreatModeler
from aether.tools.file_writer import FileWriterTool
from aether.tools.file_reader import FileReaderTool
from aether.tools.directory_lister import DirectoryListerTool
from aether.tools.codebase_search import CodebaseSearchTool
from aether.paths import bundled_skills_dir, is_within_allowed_root
from aether.init_cmd import run_init
import os


def test_version_is_single_sourced():
 assert __version__, "aether.__version__ must be set"
 import aether.cli as cli_mod
 assert cli_mod.__version__ == __version__


def test_orchestrator_initialises_without_skills(tmp_path, monkeypatch):
 monkeypatch.chdir(tmp_path)
 monkeypatch.delenv("AETHER_SKILLS_DIR", raising=False)
 empty = tmp_path / "empty_skills"
 empty.mkdir()
 orch = AetherOrchestrator(skills_directory=str(empty))
 assert orch.get_available_skills() == []
 assert "file_writer" in orch.get_available_tools()
 assert isinstance(orch.errors, list)


def test_orchestrator_loads_bundled_skills_by_default(tmp_path, monkeypatch):
 """Outside a project skills/ folder, packaged bundled_skills still load."""
 from pathlib import Path

 monkeypatch.chdir(tmp_path)
 monkeypatch.delenv("AETHER_SKILLS_DIR", raising=False)
 # Isolate from a pre-existing ~/.aether/skills (Linux HOME + Windows USERPROFILE)
 fake_home = tmp_path / "home"
 fake_home.mkdir()
 monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
 orch = AetherOrchestrator()
 skills = orch.get_available_skills()
 assert len(skills) >= 10
 assert "kiwi-edge-architecture" in skills or "git-workflow" in skills


def test_skills_directory_resolution_env_var(tmp_path, monkeypatch):
 skills_dir = tmp_path / "my-skills"
 skills_dir.mkdir()
 monkeypatch.setenv("AETHER_SKILLS_DIR", str(skills_dir))
 assert _resolve_skills_directory() == str(skills_dir.resolve())


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
 result = FileReaderTool(allowed_root=str(tmp_path)).run(file_path=str(f), max_lines=100)
 assert result.success is True
 assert result.output == "one\ntwo\n"


def test_file_reader_blocks_path_traversal(tmp_path):
 tool = FileReaderTool(allowed_root=str(tmp_path))
 result = tool.run(file_path="../../etc/passwd")
 assert result.success is False
 assert "outside allowed root" in result.error


def test_directory_lister_accepts_directory_alias(tmp_path):
 (tmp_path / "a.txt").write_text("x")
 result = DirectoryListerTool(allowed_root=str(tmp_path)).run(
 directory=str(tmp_path), max_depth=1
 )
 assert result.success is True
 assert "a.txt" in result.output


def test_guardrails_hitl_for_file_writer():
 g = Guardrails()
 assert g.enforce_hitl("file_writer") is True


def test_guardrails_cultural_sensitivity():
 g = Guardrails()
 assert g.assess_cultural_sensitivity("update the marae garden dashboard for whanau") == "high"


def test_read_tools_do_not_require_hitl_from_threat_model():
 tm = ThreatModeler()
 for action in ("file_reader", "codebase_search", "memory_query", "directory_lister"):
 model = tm.analyze_action(action)
 assert model.requires_hitl is False, f"{action} should not force HITL"


def test_orchestrator_allows_read_tools_without_approval(tmp_path, monkeypatch):
 monkeypatch.chdir(tmp_path)
 orch = AetherOrchestrator(use_llm=False)
 for action in ("file_reader", "codebase_search", "memory_query", "directory_lister"):
 assert orch._requires_approval(action) is False, f"{action} unexpectedly requires approval"
 assert orch._requires_approval("file_writer") is True


def test_skill_requires_hitl_from_frontmatter(tmp_path, monkeypatch):
 monkeypatch.chdir(tmp_path)
 orch = AetherOrchestrator(use_llm=False)
 orch.register_skill(
 "sensitive-playbook",
 {
 "name": "sensitive-playbook",
 "description": "needs human",
 "requires_hitl": True,
 "cultural_sensitivity": "low",
 "body": "# Do carefully\nStep 1: review",
 },
 )
 assert orch._requires_approval("sensitive-playbook") is True
 assert orch._requires_approval("directory_lister") is False


def test_skill_high_cultural_sensitivity_requires_approval(tmp_path, monkeypatch):
 monkeypatch.chdir(tmp_path)
 orch = AetherOrchestrator(use_llm=False)
 orch.register_skill(
 "sovereignty-check",
 {
 "name": "sovereignty-check",
 "description": "data sovereignty",
 "requires_hitl": False,
 "cultural_sensitivity": "high",
 "body": "Respect Te Mana Raraunga",
 },
 )
 assert orch._requires_approval("sovereignty-check") is True


def test_codebase_search_blocks_path_traversal(tmp_path):
 (tmp_path / "ok.py").write_text("secret_token = 1\n")
 tool = CodebaseSearchTool(allowed_root=str(tmp_path))
 result = tool.run(query="secret", directory="../../")
 assert result.success is False
 assert "outside allowed root" in result.error


def test_directory_lister_blocks_path_traversal(tmp_path):
 tool = DirectoryListerTool(allowed_root=str(tmp_path))
 result = tool.run(directory="../../")
 assert result.success is False
 assert "outside allowed root" in result.error


def test_is_within_allowed_root_portable(tmp_path):
 """Sandbox checks work with mixed separators and sibling path tricks."""
 root = tmp_path / "proj"
 root.mkdir()
 inside = root / "src" / "a.py"
 inside.parent.mkdir()
 inside.write_text("x\n", encoding="utf-8")
 sibling = tmp_path / "proj_evil"
 sibling.mkdir()

 assert is_within_allowed_root(str(inside), str(root)) is True
 assert is_within_allowed_root(str(root), str(root)) is True
 assert is_within_allowed_root(str(sibling), str(root)) is False
 assert is_within_allowed_root(str(tmp_path), str(root)) is False

 # Forward slashes work on Windows too
 forward = str(inside).replace("\\", "/")
 assert is_within_allowed_root(forward, str(root)) is True

 # Relative traversal out of root must fail when resolved against CWD
 monkey_cwd = root
 old = os.getcwd()
 try:
 os.chdir(monkey_cwd)
 assert is_within_allowed_root("..", str(root)) is False
 assert is_within_allowed_root("src", str(root)) is True
 finally:
 os.chdir(old)


def test_path_tools_accept_forward_slashes(tmp_path):
 """Tools accept POSIX-style paths on Windows and Linux."""
 (tmp_path / "nested").mkdir()
 f = tmp_path / "nested" / "note.txt"
 f.write_text("kia ora\n", encoding="utf-8")
 rel = "nested/note.txt"
 reader = FileReaderTool(allowed_root=str(tmp_path))
 # resolve relative to allowed_root via chdir
 old = os.getcwd()
 try:
 os.chdir(tmp_path)
 result = reader.run(file_path=rel)
 assert result.success is True
 assert "kia ora" in result.output
 finally:
 os.chdir(old)


def test_codebase_search_works_inside_root(tmp_path):
 (tmp_path / "app.py").write_text("def login(): pass\n")
 tool = CodebaseSearchTool(allowed_root=str(tmp_path))
 result = tool.run(query="login", directory=str(tmp_path))
 assert result.success is True
 assert any("login" in str(m.get("content", "")) for m in result.output)


def test_bundled_skills_dir_present():
 b = bundled_skills_dir()
 assert b is not None
 assert (b / "git-workflow" / "SKILL.md").is_file() or any(b.iterdir())


def test_aether_init_copies_skills(tmp_path, monkeypatch):
 from pathlib import Path

 monkeypatch.chdir(tmp_path)
 fake_home = tmp_path / "home"
 fake_home.mkdir()
 monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
 from aether import paths as paths_mod
 monkeypatch.setattr(paths_mod, "user_skills_dir", lambda: fake_home / ".aether" / "skills")

 rc = run_init(project=True, user=True, force=False, cwd=str(tmp_path))
 assert rc == 0
 assert (tmp_path / "skills").is_dir()
 assert any((tmp_path / "skills").iterdir())
 assert (fake_home / ".aether" / "skills").is_dir()
 assert any((fake_home / ".aether" / "skills").iterdir())


def test_execute_skill_injects_playbook_into_state(tmp_path, monkeypatch):
 monkeypatch.chdir(tmp_path)
 orch = AetherOrchestrator(use_llm=False)
 orch.register_skill(
 "demo-skill",
 {
 "name": "demo-skill",
 "description": "demo",
 "requires_hitl": False,
 "cultural_sensitivity": "low",
 "version": "1.2.0",
 "body": "## Steps\n1. search\n2. report",
 },
 )
 orch.start_task("demo goal")
 result = orch._execute_skill("demo-skill", "demo goal")
 assert result["applied"] is True
 assert "demo-skill" in orch.state.loaded_skills
 assert len(orch.state.skill_execution_results) == 1
 assert orch.state.skill_execution_results[0]["skill"] == "demo-skill"
 assert any("ACTIVE SKILL PLAYBOOK: demo-skill" in b for b in orch.state.active_skill_instructions)
 summary = orch.state.summarize()
 assert "BINDING SKILL PLAYBOOKS" in summary
 assert "1. search" in summary
