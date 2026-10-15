#!/usr/bin/env python3
"""Nodexys custom kernel config overlay.

  apply  <gki_defconfig> <file> [extra]   overlay entries on top of the defconfig
  verify <.config>       <file> [extra]   warn about entries that did not survive Kconfig

Accepted syntax (file or the `extra` string, which is whitespace separated):
  CONFIG_FOO=y            enable
  CONFIG_FOO=m            module
  CONFIG_FOO=n            disable  (written as "# CONFIG_FOO is not set")
  # CONFIG_FOO is not set disable
  CONFIG_FOO=1024         number
  CONFIG_FOO="text"       string (only in the file; the inline `extra` splits on spaces)
Anything else starting with # is a comment. Last entry for a symbol wins.
"""
import os
import re
import sys
import glob


def parse(text):
    out = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = re.match(r'^#\s*(CONFIG_[A-Za-z0-9_]+)\s+is not set$', line)
        if m:
            out[m.group(1)] = None
            continue
        if line.startswith('#'):
            continue
        m = re.match(r'^(CONFIG_[A-Za-z0-9_]+)\s*=\s*(.*)$', line)
        if not m:
            print(f"::warning::custom config: ignoring unrecognized line: {line}")
            continue
        key, val = m.group(1), m.group(2).strip()
        if not val.startswith('"'):
            val = re.split(r'\s+#', val)[0].strip()
        if val == '':
            print(f"::warning::custom config: {key} has no value, ignoring")
            continue
        out[key] = None if val == 'n' else val
    return out


def load(path, extra):
    entries = {}
    if path and os.path.isfile(path):
        entries.update(parse(open(path, encoding='utf-8').read()))
    if extra and extra.strip():
        entries.update(parse("\n".join(extra.split())))
    return entries


def line_for(key, val):
    return f"# {key} is not set" if val is None else f"{key}={val}"


def apply(defconfig, entries):
    lines = open(defconfig, encoding='utf-8').read().splitlines()
    for key, val in entries.items():
        pat = re.compile(rf'^(# {re.escape(key)} is not set|{re.escape(key)}=.*)$')
        lines = [l for l in lines if not pat.match(l)]
        lines.append(line_for(key, val))
    open(defconfig, 'w', encoding='utf-8').write("\n".join(lines) + "\n")
    print(f"Applied {len(entries)} custom config entries to {defconfig}:")
    for key, val in entries.items():
        print("   " + line_for(key, val))


def verify(config, entries):
    cfg = {}
    for l in open(config, encoding='utf-8', errors='replace').read().splitlines():
        m = re.match(r'^(CONFIG_[A-Za-z0-9_]+)=(.*)$', l)
        if m:
            cfg[m.group(1)] = m.group(2)
    rows, bad = [], 0
    for key, want in entries.items():
        got = cfg.get(key)
        ok = (got is None) if want is None else (got == want)
        if not ok:
            bad += 1
            print(f"::warning::{key}: pediste {line_for(key, want)} pero el kernel final tiene "
                  f"{'(sin definir)' if got is None else key + '=' + got} "
                  f"(probablemente una dependencia no se cumple)")
        rows.append((key, line_for(key, want), 'OK' if ok else f"DIFERENTE ({got})"))
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary and rows:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write("\n### Configs personalizadas\n\n| Config | Pedido | Resultado |\n|---|---|---|\n")
            for k, w, r in rows:
                f.write(f"| `{k}` | `{w}` | {r} |\n")
    print(f"Custom configs checked: {len(rows)} total, {bad} differ.")


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    mode, target, path = sys.argv[1:4]
    extra = sys.argv[4] if len(sys.argv) > 4 else ''
    entries = load(path, extra)
    if not entries:
        print("No custom configs defined - nothing to do.")
        return
    if mode == 'apply':
        apply(target, entries)
    elif mode == 'verify':
        if target == 'auto':
            cands = ['/home/runner/out/.config'] + glob.glob('/home/runner/out/**/.config', recursive=True)
            target = next((c for c in cands if os.path.isfile(c)), '')
        if not target or not os.path.isfile(target):
            print("::warning::custom config: could not locate the final .config to verify")
            return
        verify(target, entries)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == '__main__':
    main()
