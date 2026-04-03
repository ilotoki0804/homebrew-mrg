from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import time
import urllib.request


def fetch_json(url: str, github_token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "User-Agent": "homebrew-mrg-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "homebrew-mrg-sync"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the mrg Homebrew formula from the latest release.")
    parser.add_argument("--formula-path", default=os.environ.get("FORMULA_PATH", "Formula/mrg.rb"))
    parser.add_argument("--source-repo", default=os.environ.get("SOURCE_REPO", "ilotoki0804/mrg"))
    parser.add_argument("--package-name", default=os.environ.get("PACKAGE_NAME", "mrg"))
    parser.add_argument("--event-path", default=os.environ.get("GITHUB_EVENT_PATH"))
    parser.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT"))
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--wait", default=os.environ.get("WAIT_BEFORE_STARTING", "0"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.github_token:
        raise SystemExit("GITHUB_TOKEN is required")

    if wait := float(args.wait):
        print(f"Waiting for {wait}s before starting (it could waste Actions running time)")
        time.sleep(wait)

    formula_path = pathlib.Path(args.formula_path)
    event_payload: dict[str, object] = {}
    if args.event_path:
        event_payload = json.loads(pathlib.Path(args.event_path).read_text(encoding="utf-8"))

    dispatched_version = None
    client_payload = event_payload.get("client_payload")
    if isinstance(client_payload, dict):
        dispatched_version = client_payload.get("version") or client_payload.get("tag")

    if dispatched_version:
        version = str(dispatched_version).lstrip("v")
    else:
        latest = fetch_json(f"https://api.github.com/repos/{args.source_repo}/releases/latest", args.github_token)
        version = str(latest["tag_name"]).lstrip("v")

    source_url = (
        f"https://files.pythonhosted.org/packages/source/{args.package_name[0]}/"
        f"{args.package_name}/{args.package_name}-{version}.tar.gz"
    )
    source_sha256 = hashlib.sha256(fetch_bytes(source_url)).hexdigest()

    original = formula_path.read_text(encoding="utf-8")
    updated = re.sub(r'^  url ".*"$', f'  url "{source_url}"', original, flags=re.MULTILINE)
    updated = re.sub(r'^  sha256 .*$', f'  sha256 "{source_sha256}"', updated, flags=re.MULTILINE)

    changed = updated != original
    if changed:
        formula_path.write_text(updated, encoding="utf-8")

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
            fh.write(f"version={version}\n")

    print(f"Target version: {version}")
    print(f"Formula changed: {changed}")


if __name__ == "__main__":
    main()