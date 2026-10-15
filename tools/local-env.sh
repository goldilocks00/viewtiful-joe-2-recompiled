#!/usr/bin/env bash
# Source this file to use the optional unpacked Ubuntu development packages.
VJ2_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VJ2_SDK="$VJ2_ROOT/build/deps/root"
export PATH="$VJ2_SDK/usr/bin:$PATH"
export LD_LIBRARY_PATH="$VJ2_SDK/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LIBRARY_PATH="$VJ2_SDK/usr/lib/x86_64-linux-gnu${LIBRARY_PATH:+:$LIBRARY_PATH}"
export CPATH="$VJ2_SDK/usr/include:$VJ2_SDK/usr/include/x86_64-linux-gnu${CPATH:+:$CPATH}"
export PKG_CONFIG_PATH="$VJ2_SDK/usr/lib/x86_64-linux-gnu/pkgconfig:$VJ2_SDK/usr/share/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export PKG_CONFIG_SYSROOT_DIR="$VJ2_SDK"
export CMAKE_PREFIX_PATH="$VJ2_SDK/usr${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
export CC="$VJ2_SDK/usr/bin/gcc"
export CXX="$VJ2_SDK/usr/bin/g++"
