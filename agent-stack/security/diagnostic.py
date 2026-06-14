from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SECURITY_HEADERS = [
    "strict-transport-security",
    "content-security-policy",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "permissions-policy",
]


def check_url(url: str) -> dict[str, Any]:
    parsed = urlparse(url)
    report: dict[str, Any] = {
        "url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checks": {},
        "summary": {"pass": 0, "warn": 0, "fail": 0},
    }

    if parsed.scheme != "https":
        report["checks"]["https"] = {"status": "fail", "message": "Use HTTPS for public websites."}
    else:
        report["checks"]["https"] = {"status": "pass", "message": "HTTPS is enabled."}

    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Tukuk-Security-Diagnostic/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            report["checks"]["reachable"] = {"status": "pass", "status_code": response.status}
    except (urllib.error.URLError, TimeoutError) as exc:
        report["checks"]["reachable"] = {"status": "warn", "message": str(exc)}
        headers = {}

    for header in SECURITY_HEADERS:
        status = "pass" if header in headers else "warn"
        message = "Header present." if status == "pass" else "Consider adding this defensive security header."
        report["checks"][header] = {"status": status, "message": message}

    if parsed.hostname:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((parsed.hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                    cert = ssock.getpeercert()
            report["checks"]["tls_certificate"] = {"status": "pass", "issuer": cert.get("issuer", {})}
        except Exception as exc:  # defensive diagnostic only
            report["checks"]["tls_certificate"] = {"status": "warn", "message": str(exc)}

    for item in report["checks"].values():
        report["summary"][item.get("status", "warn")] += 1

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Defensive web security diagnostic for Tukuk AI.")
    parser.add_argument("--url", required=True, help="Public website URL to diagnose")
    parser.add_argument("--output", default="diagnostic-report.json")
    args = parser.parse_args()

    report = check_url(args.url)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
