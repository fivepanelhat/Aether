#!/usr/bin/env python3
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
Aether CLI - Professional Command Line Interface
"""

import argparse
import sys
from aether import __version__
from aether.orchestrator import AetherOrchestrator
from aether.logging_config import setup_logging
from aether.init_cmd import run_init


def print_header(text: str):
    print("\n" + "=" * 72)
    print(text.center(72))
    print("=" * 72)


def run_task(goal: str, max_steps: int = 8, memory_path: str = None, auto_remediate: bool = False):
    if not goal or goal.strip() == "":
        print("Error: Please provide a goal.\nExample:\n  aether run \"Audit the API routes for security issues\"")
        sys.exit(1)

    print_header("AETHER")

    print(f"Goal: {goal}")
    print(f"Max Steps: {max_steps}")
    if auto_remediate:
        print("Auto-remediate: ON (high-risk actions authorized for this run)")
    print("-" * 72)
    print("Note: High-risk actions (writing files, git operations) require approval "
          "unless --auto-remediate is set.\n")

    try:
        aether = AetherOrchestrator(memory_path=memory_path)
        state = aether.run_react_loop(goal=goal, max_steps=max_steps, auto_remediate=auto_remediate)

        print("\n[Summary]")
        print(state.summarize())

        if hasattr(state, "skill_execution_results") and state.skill_execution_results:
            print("\n[Skills Used]")
            for result in state.skill_execution_results:
                print(f"  \u2022 {result.get('skill')}")

        print("\n[Recent Activity]")
        for entry in state.history[-8:]:
            print(f"  {entry}")

        errors = getattr(aether, "errors", None) or []
        if errors:
            print("\n[Errors Encountered]")
            for err in errors:
                print(f"  \u2022 {err}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Unexpected Error] {e}")
        print("Please check the logs or try again with a simpler goal.")
        sys.exit(1)

    print("\n" + "=" * 72)
    print("Task completed.")
    print("=" * 72 + "\n")


def list_skills():
    try:
        aether = AetherOrchestrator()
        print_header("AVAILABLE SKILLS")

        skills = aether.get_available_skills()

        if not skills:
            print("No skills found.")
            print("Create skills in the 'skills/' directory to extend Aether's capabilities.")
            return

        for name in sorted(skills):
            info = aether.get_skill_info(name) or {}
            desc = info.get("description", "No description available")
            print(f"  {name}")
            try:
                print(f"    {desc}\n")
            except UnicodeEncodeError:
                clean_desc = desc.encode("ascii", "ignore").decode("ascii")
                print(f"    {clean_desc}\n")

    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)


def _interactive_approver(action, args):
    """Prompt on a TTY before an actuating computer-use step; deny otherwise."""
    try:
        if not sys.stdin.isatty():
            return False
        print(f"\n[APPROVAL] Computer action '{action}' with {args}")
        answer = input("Proceed? [y/N] ").strip().lower()
        return answer in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def run_computer_agent(goal, model, max_steps, auto_approve, base_url, dry_run):
    """Vision computer-use loop over a local Ollama multimodal model."""
    from aether.computer.agent import ComputerUseAgent, DEFAULT_VISION_MODEL
    from aether.computer.backend import get_backend

    get_backend(force_new=True, dry_run=dry_run)

    print_header("AETHER COMPUTER USE")
    print(f"Goal: {goal}")
    print(f"Vision model: {model or DEFAULT_VISION_MODEL} @ {base_url}")
    print(f"Max steps: {max_steps} | auto-approve: {auto_approve} | dry-run: {dry_run}")
    print("-" * 72)
    if not auto_approve:
        print("Actuating steps require approval (interactive y/N on a TTY).\n")

    agent = ComputerUseAgent(
        model=model or DEFAULT_VISION_MODEL,
        base_url=base_url,
        auto_approve=auto_approve,
        approver=None if auto_approve else _interactive_approver,
    )
    try:
        result = agent.run(goal=goal, max_steps=max_steps)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)

    print("\n[Result]")
    print(result.render())
    print("\n" + "=" * 72)
    sys.exit(0 if (result.completed or not result.halted_reason) else 2)


def run_computer_direct(args):
    """Deterministic, model-free desktop control (screenshot / click / type / key / scroll)."""
    from aether.computer.backend import get_backend, BackendUnavailable

    be = get_backend(force_new=True, dry_run=getattr(args, "dry_run", False))
    if not be.available():
        print(f"Error: {be.unavailable_reason()}")
        sys.exit(1)

    op = args.computer_op
    try:
        if op == "shot":
            grab = be.screenshot(path=getattr(args, "path", None) or "aether_screenshot.png")
            print(f"Saved {grab.width}x{grab.height} screenshot to {grab.path}")
        elif op == "info":
            w, h = be.screen_size()
            cx, cy = be.cursor_position()
            print(f"Screen {w}x{h}; cursor at ({cx},{cy})")
        elif op == "click":
            x, y = be.click(args.x, args.y, button=args.button, clicks=args.clicks)
            print(f"Clicked {args.button} x{args.clicks} at ({x},{y})")
        elif op == "move":
            x, y = be.move(args.x, args.y)
            print(f"Moved to ({x},{y})")
        elif op == "type":
            n = be.type_text(args.text)
            print(f"Typed {n} characters")
        elif op == "key":
            keys = [k for k in args.keys.replace(" ", "").split("+") if k]
            pressed = be.press(keys)
            print(f"Pressed {'+'.join(pressed)}")
        elif op == "scroll":
            be.scroll(args.amount)
            print(f"Scrolled {args.amount}")
        else:
            print("Unknown computer operation.")
            sys.exit(1)
    except BackendUnavailable as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    sys.exit(0)


def run_doctor():
    """Environment readiness check for edge AI + computer use."""
    from aether.computer.backend import backend_status
    from aether.llm import OllamaClient, DEFAULT_MODEL

    print_header("AETHER DOCTOR")

    print("[Computer-use backend]")
    status = backend_status()
    print(f"  Platform : {status['platform']} (Python {status['python']})")
    if status["available"]:
        print(f"  Backend  : OK — screen {status['screen']}")
    else:
        print("  Backend  : UNAVAILABLE")
        print(f"             {status['reason']}")
    print(f"  Dry-run  : {status['dry_run']}")

    print("\n[Local LLM / edge AI]")
    text_client = OllamaClient()
    reachable = text_client.is_available()
    print(f"  Ollama   : {'reachable' if reachable else 'NOT reachable'} at {text_client.base_url}")
    print(f"  Text model target : {DEFAULT_MODEL}")
    if reachable:
        try:
            import urllib.request
            req = urllib.request.Request(f"{text_client.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                import json as _json
                tags = _json.loads(resp.read().decode("utf-8"))
                names = [m.get("name", "?") for m in tags.get("models", [])]
                print(f"  Installed models  : {', '.join(names) if names else '(none pulled yet)'}")
        except Exception as e:
            print(f"  Could not list models: {e}")
    else:
        print("  Start Ollama (https://ollama.com) and pull a vision model, e.g.:")
        print("      ollama pull qwen2.5-vl:7b")

    ready = status["available"] and reachable
    print("\n" + "=" * 72)
    print("READY for computer use." if ready else "NOT fully ready — see notes above.")
    print("=" * 72 + "\n")
    sys.exit(0 if ready else 1)


def start_webhook_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the GitHub webhook server.

    SECURITY: Defaults to localhost (127.0.0.1) to avoid unintended network exposure.
    Use --host 0.0.0.0 explicitly if you need to expose it (with proper authentication).
    """
    try:
        import uvicorn
        from aether.webhooks.github_webhook import app, create_app
    except ImportError:
        print('Error: webhook dependencies missing. Run: pip install -e ".[webhook]"')
        sys.exit(1)

    application = app if app is not None else create_app()

    if host in ("0.0.0.0", "::"):
        print("\n[WARNING] Webhook server is binding to all interfaces (0.0.0.0).")
        print("This exposes the server on the network. Ensure you have strong authentication.")
        print("Consider using a reverse proxy or firewall rules in production.\n")

    print(f"\nStarting Aether GitHub Webhook server on http://{host}:{port}")
    print("Set GITHUB_WEBHOOK_SECRET for signature verification.")
    print("Dev only: AETHER_WEBHOOK_INSECURE=1 skips signature checks.")
    print(
        "Default is propose-only. "
        "Set AETHER_WEBHOOK_AUTO_REMEDIATE=1 to authorize high-risk writes.\n"
    )

    uvicorn.run(application, host=host, port=port)


def main():
    try:
        from aether.paths import ensure_utf8_stdio

        ensure_utf8_stdio()
    except Exception:
        # Best-effort UTF-8 stdio before logging is configured; non-fatal and
        # nothing to log to yet — intentionally silent.
        pass  # nosec B110
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Aether - Sovereign Agentic Development System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aether run "Audit the API routes for security issues"
  aether run "Improve context handling in agents" --max-steps 10
  aether remediate "CI failed on main with test error in user.test.ts"
  aether skills
  aether doctor
  aether computer run "Open the calculator and compute 12 * 9"
  aether computer shot screen.png
  aether computer click 640 480 --button left
  aether webhook --port 9000
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show Aether version"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === Run Command ===
    run_parser = subparsers.add_parser(
        "run",
        help="Run a task using the ReAct reasoning loop"
    )
    run_parser.add_argument(
        "goal",
        type=str,
        help="The goal or task you want Aether to work on"
    )
    run_parser.add_argument(
        "--max-steps",
        type=int,
        default=8,
        help="Maximum number of reasoning steps (default: 8)"
    )
    run_parser.add_argument(
        "--memory",
        type=str,
        default=None,
        help="Path to persist memory across runs"
    )
    run_parser.add_argument(
        "--auto-remediate",
        action="store_true",
        help="Authorize high-risk actions (file writes) for this run without interactive halt"
    )

    # === Skills Command ===
    subparsers.add_parser(
        "skills",
        help="List all available skills"
    )

    # === Init Command ===
    init_parser = subparsers.add_parser(
        "init",
        help="Install bundled skills to ~/.aether/skills and ./skills",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing skill directories",
    )
    init_parser.add_argument(
        "--user-only",
        action="store_true",
        help="Only install to ~/.aether/skills",
    )
    init_parser.add_argument(
        "--project-only",
        action="store_true",
        help="Only install to ./skills in the current directory",
    )

    # === Remediate Command ===
    remediate_parser = subparsers.add_parser(
        "remediate",
        help="Trigger the error remediation workflow on a CI failure or error"
    )
    remediate_parser.add_argument(
        "error",
        type=str,
        help="The error or CI failure to remediate"
    )

    # === Webhook Command ===
    webhook_parser = subparsers.add_parser(
        "webhook",
        help="Start the GitHub webhook server (requires: pip install -e \".[webhook]\")"
    )
    webhook_parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1 for security)")
    webhook_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")

    # === Doctor Command ===
    subparsers.add_parser(
        "doctor",
        help="Check edge-AI + computer-use readiness (Ollama, display, backend)",
    )

    # === Computer Command (edge AI + computer use) ===
    computer_parser = subparsers.add_parser(
        "computer",
        help="Operate the desktop: agentic vision loop, or direct control "
             '(requires: pip install "aether[computer]")',
    )
    computer_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Rehearse without actuating the mouse/keyboard (AETHER_COMPUTER_DRY_RUN)",
    )
    computer_sub = computer_parser.add_subparsers(dest="computer_op", help="Computer operation")

    cu_run = computer_sub.add_parser("run", help="Agentic vision loop: pursue a goal on the desktop")
    cu_run.add_argument("goal", type=str, help="What Aether should accomplish on screen")
    cu_run.add_argument("--model", default=None, help="Ollama vision model (default: qwen2.5-vl:7b)")
    cu_run.add_argument("--base-url", default="http://localhost:11434", help="Ollama base URL")
    cu_run.add_argument("--max-steps", type=int, default=12, help="Max screenshot->act cycles")
    cu_run.add_argument(
        "--auto-approve",
        action="store_true",
        help="Authorize actuating steps without interactive confirmation",
    )

    cu_shot = computer_sub.add_parser("shot", help="Save a screenshot")
    cu_shot.add_argument("path", nargs="?", default=None, help="Output PNG path")
    computer_sub.add_parser("info", help="Print screen size and cursor position")

    cu_click = computer_sub.add_parser("click", help="Click at absolute pixel (x, y)")
    cu_click.add_argument("x", type=int)
    cu_click.add_argument("y", type=int)
    cu_click.add_argument("--button", default="left", choices=["left", "right", "middle"])
    cu_click.add_argument("--clicks", type=int, default=1)

    cu_move = computer_sub.add_parser("move", help="Move pointer to absolute pixel (x, y)")
    cu_move.add_argument("x", type=int)
    cu_move.add_argument("y", type=int)

    cu_type = computer_sub.add_parser("type", help="Type literal text at the current focus")
    cu_type.add_argument("text", type=str)

    cu_key = computer_sub.add_parser("key", help="Press a key or chord, e.g. 'enter' or 'ctrl+s'")
    cu_key.add_argument("keys", type=str)

    cu_scroll = computer_sub.add_parser("scroll", help="Scroll wheel (positive up, negative down)")
    cu_scroll.add_argument("amount", type=int)

    try:
        args = parser.parse_args()

        if not getattr(args, "command", None):
            parser.print_help()
            sys.exit(1)

        if args.command == "run":
            run_task(args.goal, args.max_steps, args.memory, getattr(args, "auto_remediate", False))
        elif args.command == "skills":
            list_skills()
        elif args.command == "init":
            user = not getattr(args, "project_only", False)
            project = not getattr(args, "user_only", False)
            if getattr(args, "user_only", False) and getattr(args, "project_only", False):
                print("Error: --user-only and --project-only are mutually exclusive.")
                sys.exit(1)
            rc = run_init(
                project=project,
                user=user,
                force=getattr(args, "force", False),
            )
            sys.exit(rc)
        elif args.command == "remediate":
            if not getattr(args, "error", "") or args.error.strip() == "":
                print("Error: Please provide an error.\nExample: aether remediate \"CI failed on main branch\"")
                sys.exit(1)
            goal = f"Remediate the following error using error-remediation-orchestrator: {args.error}"
            run_task(goal, max_steps=10, auto_remediate=True)
        elif args.command == "webhook":
            start_webhook_server(
                host=getattr(args, "host", "127.0.0.1"),
                port=getattr(args, "port", 8000)
            )
        elif args.command == "doctor":
            run_doctor()
        elif args.command == "computer":
            op = getattr(args, "computer_op", None)
            if not op:
                computer_parser.print_help()
                sys.exit(1)
            if op == "run":
                if not getattr(args, "goal", "") or args.goal.strip() == "":
                    print('Error: provide a goal.\nExample: aether computer run "Open the calculator and compute 12*9"')
                    sys.exit(1)
                run_computer_agent(
                    goal=args.goal,
                    model=getattr(args, "model", None),
                    max_steps=getattr(args, "max_steps", 12),
                    auto_approve=getattr(args, "auto_approve", False),
                    base_url=getattr(args, "base_url", "http://localhost:11434"),
                    dry_run=getattr(args, "dry_run", False),
                )
            else:
                run_computer_direct(args)
        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
