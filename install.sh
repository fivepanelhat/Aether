#!/usr/bin/env bash
# Aether - Sovereign Edge AI + Computer Use installer (Linux / macOS)
#
# One-line install:
# curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh | bash
#
# Or from a clone:
# ./install.sh
#
# Creates an isolated virtualenv, installs Aether with the computer-use extras,
# exposes the `aether` command, and checks for a local Ollama runtime. Nothing
# leaves the machine - Aether runs entirely on-device.
set -euo pipefail

REPO_URL="${AETHER_REPO_URL:-https://github.com/fivepanelhat/Aether.git}"
INSTALL_DIR="${AETHER_HOME:-$HOME/.aether-app}"
VENV_DIR="$INSTALL_DIR/venv"
BIN_DIR="${AETHER_BIN_DIR:-$HOME/.local/bin}"

info() { printf '\033[36m[aether]\033[0m %s\n' "$1"; }
warn() { printf '\033[33m[aether]\033[0m %s\n' "$1"; }
err() { printf '\033[31m[aether]\033[0m %s\n' "$1" >&2; }

# ---- 1. Python ----
PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
 err "Python 3.10+ is required but was not found. Install Python and re-run."
 exit 1
fi
PY_VER="$("$PYTHON_BIN" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"

# Python version gate
PY_MAJOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[0])')"
PY_MINOR="$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[1])')"
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
 err "Python 3.10+ is required (found ${PY_MAJOR}.${PY_MINOR})."
 exit 1
fi
info "Using Python $PY_VER ($PYTHON_BIN)"

# ---- 2. Source: clone or in-place ----
if [[ -f "pyproject.toml" ]] && grep -q 'name = "aether"' pyproject.toml 2>/dev/null; then
 SRC_DIR="$(pwd)"
 info "Installing from current checkout: $SRC_DIR"
else
 if ! command -v git >/dev/null 2>&1; then
 err "git is required to fetch Aether. Install git or run this script from a clone."
 exit 1
 fi
 mkdir -p "$INSTALL_DIR"
 SRC_DIR="$INSTALL_DIR/src"
 if [[ -d "$SRC_DIR/.git" ]]; then
 info "Updating existing checkout in $SRC_DIR"
 git -C "$SRC_DIR" pull --ff-only || warn "Could not fast-forward; using existing checkout."
 else
 info "Cloning $REPO_URL"
 git clone --depth 1 "$REPO_URL" "$SRC_DIR"
 fi
fi

# ---- 3. Virtualenv ----
info "Creating virtualenv at $VENV_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null

# ---- 4. Install with computer-use extras ----
info "Installing aether[computer] (edge AI + desktop control)"
pip install "$SRC_DIR[computer]"

# ---- 5. Bundle skills ----
info "Installing bundled skills"
aether init --user-only || warn "Skill install skipped (non-fatal)."

# ---- 6. Launcher on PATH ----
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/aether" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/aether" "\$@"
EOF
chmod +x "$BIN_DIR/aether"
info "Installed launcher: $BIN_DIR/aether"
case ":$PATH:" in
 *":$BIN_DIR:"*) : ;;
 *) warn "Add $BIN_DIR to your PATH: echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.bashrc" ;;
esac

# ---- 7. Ollama check (edge AI runtime) ----
if command -v ollama >/dev/null 2>&1; then
 info "Ollama detected: $(ollama --version 2>/dev/null | head -n1)"
else
 warn "Ollama not found. Install the local model runtime from https://ollama.com"
 warn "Then pull models: ollama pull qwen2.5-coder:7b && ollama pull qwen2.5-vl:7b"
fi

echo
info "Done. Verify your setup with:"
echo " aether doctor"
echo
info "Try computer use:"
echo " aether computer run \"Open the calculator and compute 12 * 9\""
echo " aether computer shot screen.png # deterministic, no model needed"
