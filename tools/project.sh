#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -x build/deps/root/usr/bin/cmake ]]; then
  source tools/local-env.sh
fi
export CMAKE_BUILD_PARALLEL_LEVEL="${CMAKE_BUILD_PARALLEL_LEVEL:-1}"
export XDG_CACHE_HOME="$ROOT/build/cache"
TEMPLATE="$ROOT/upstream/ModernGekko-Template"
MODERN="$TEMPLATE/lib/ModernGekko"
GAME="$ROOT/extracted/G2VP08"
mkdir -p build/logs
case "${1:-help}" in
  sources|tools|prepare|build|run)
    exec 9>build/.operation.lock
    if ! flock -n 9; then
      echo 'Another project operation is already running; refusing concurrent execution.' >&2
      exit 3
    fi
    ;;
esac
validate_game() {
    python3 - <<'PY'
import hashlib,json
from pathlib import Path
lock=json.loads(Path('config/sources.lock.json').read_text())
digest=hashlib.sha256(Path('extracted/G2VP08/sys/main.dol').read_bytes()).hexdigest()
if digest != lock['dol_sha256']:
    raise SystemExit('main.dol differs from the inspected revision; refusing to build')
PY
}
case "${1:-help}" in
  sources)
    python3 tools/fetch_sources.py
    ;;
  tools)
    cmake -S "$TEMPLATE/lib/DolRecomp" -B build/dolrecomp -G Ninja -DCMAKE_BUILD_TYPE=Release
    cmake --build build/dolrecomp --parallel "$CMAKE_BUILD_PARALLEL_LEVEL"
    ctest --test-dir build/dolrecomp --output-on-failure
    sdk_args=()
    if [[ -n "${VJ2_SDK:-}" ]]; then sdk_args+=("-DMODERNGEKKO_FRONTEND_SDK=$VJ2_SDK"); fi
    cmake -S "$MODERN" -B build/moderngekko -G Ninja -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTING=OFF -DENABLE_EGL=ON -DMODERNGEKKO_GAMECUBE_CONTROLLERS=ON \
      -DMODERNGEKKO_REQUIRED_DISC_ID=G2VP08 \
      '-DMODERNGEKKO_DEFAULT_WINDOW_TITLE=Viewtiful Joe 2 Recompiled' "${sdk_args[@]}"
    cmake --build build/moderngekko --target moderngekko-port --parallel "$CMAKE_BUILD_PARALLEL_LEVEL"
    ;;
  prepare)
    if [[ $# != 2 ]]; then echo 'Usage: tools/project.sh prepare /path/to/disc.ciso-or-iso' >&2; exit 2; fi
    python3 tools/inspect_disc.py "$2" > build/logs/input-metadata.json
    python3 - <<'PY'
import json
from pathlib import Path
m=json.loads(Path('build/logs/input-metadata.json').read_text())
if m['game_id']!='G2VP08' or m['revision']!=0:
    raise SystemExit('Only G2VP08 revision 0 is configured')
PY
    if [[ -e "$GAME" ]]; then echo "Refusing to overwrite existing extraction: $GAME" >&2; exit 2; fi
    image="$2"
    if [[ "${image,,}" == *.ciso ]]; then
      mkdir -p iso
      python3 tools/prepare_iso.py "$image" iso/ViewtifulJoe2-working.iso
      image=iso/ViewtifulJoe2-working.iso
    fi
    build/dolrecomp/dolrecomp extract "$image" "$GAME"
    ;;
  build)
    validate_game
    build/moderngekko/moderngekko-port build "$GAME" --backend c --toolchain gcc \
      --opt-level "${VJ2_OPT_LEVEL:-2}" --output "$ROOT/build/modules"
    ;;
  run)
    validate_game
    python3 tools/prepare_user.py
    pulse_socket="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/pulse/native"
    if [[ -S "$pulse_socket" && -z "${PULSE_SERVER:-}" ]]; then
      export PULSE_SERVER="unix:$pulse_socket"
      if [[ -z "${PULSE_RUNTIME_PATH:-}" ]]; then
        export PULSE_RUNTIME_PATH="$ROOT/build/pulse-runtime"
        mkdir -p "$PULSE_RUNTIME_PATH"
        chmod 700 "$PULSE_RUNTIME_PATH"
      fi
    fi
    shift
    build/moderngekko/moderngekko-port run "$GAME" --backend c --toolchain gcc \
      --opt-level "${VJ2_OPT_LEVEL:-2}" --output "$ROOT/build/modules" -- \
      --user-dir "$ROOT/build/user" -X11 --graphics OGL "$@"
    ;;
  *)
    echo 'Usage: tools/project.sh {sources|tools|prepare IMAGE|build|run [runner arguments]}'
    ;;
esac
