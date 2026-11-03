#!/usr/bin/env python3
"""Patch script for libfprint Elan 0x0c4f support (elanpress driver)."""
import glob
import os
import re
import sys


def patch_old_elan_driver():
    """Disable 0x0c4f in the old 'elan' driver (swipe mode)."""
    elan_h = "libfprint/drivers/elan.h"
    if not os.path.exists(elan_h):
        return
    with open(elan_h, "r") as f:
        content = f.read()
    new_content, n = re.subn(r'0x0c4f', '0xffff', content, flags=re.IGNORECASE)
    with open(elan_h, "w") as f:
        f.write(new_content)
    print(f"[PATCH] elan.h: disabled {n} references to 0x0c4f in the old swipe driver.")


def get_elanpress_files():
    """Return the list of elanpress-related source files."""
    files = (
        glob.glob("libfprint/drivers/elanpress*")
        + glob.glob("libfprint/drivers/elan*/*.c")
        + glob.glob("libfprint/drivers/elan*/*.h")
    )
    return sorted(set(files))


def patch_elanpress_file(path):
    """Patch a single elanpress driver file."""
    with open(path, "r") as f:
        text = f.read()
    orig = text

    # Show relevant lines for transparent diagnostics in the build log
    keywords = ["0x0c6e", "0x0c63", "width", "height", "threshold", "match", "dim"]
    for i, line in enumerate(text.splitlines(), 1):
        if any(k in line.lower() for k in keywords):
            print(f"  [INFO {os.path.basename(path)}:{i}] {line.strip()}")

    # Map PID 0x0c6e -> 0x0c4f so it uses the tested main elanpress flow
    if re.search(r'0x0c6e', text, re.IGNORECASE):
        text = re.sub(r'0x0c6e', '0x0c4f', text, flags=re.IGNORECASE)
        print(f"[PATCH] {path}: mapped PID 0x0c6e -> 0x0c4f")

    # Adjust match/threshold from 12 to 8 (compensate for 80x80 = 6400px area)
    text = re.sub(r'(#define\s+\w*MATCH\w*\s+)12\b', r'\g<1>8', text)
    text = re.sub(r'(#define\s+\w*THRESHOLD\w*\s+)12\b', r'\g<1>8', text)

    if text != orig:
        with open(path, "w") as f:
            f.write(text)


def patch_hwdb_lists():
    """Update any C file in libfprint/ that filters by PID 0x0c6e."""
    for hwfile in glob.glob("libfprint/*.c"):
        with open(hwfile, "r") as f:
            t = f.read()
        if "0x0c6e" in t.lower():
            t2 = re.sub(r'0x0c6e', '0x0c4f', t, flags=re.IGNORECASE)
            with open(hwfile, "w") as f:
                f.write(t2)
            print(f"[PATCH] Updated {hwfile}")


def main():
    patch_old_elan_driver()

    ep_files = get_elanpress_files()
    print(f"[PATCH] Detected files: {ep_files}")

    if not ep_files:
        print("ERROR: No elanpress files found", file=sys.stderr)
        sys.exit(1)

    for path in ep_files:
        patch_elanpress_file(path)

    patch_hwdb_lists()


if __name__ == "__main__":
    main()
