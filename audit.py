#!/usr/bin/env python3
"""Generate a lightweight website revenue-leak audit using only the standard library."""

from __future__ import annotations

import argparse
import json
import ssl
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class PageSignals(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.descriptions: list[str] = []
        self.viewports: list[str] = []
        self.h1_count = 0
        self.tel_links = 0
        self.forms = 0
        self.images = 0
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = values.get("name", "").lower()
            if name == "description" and values.get("content", "").strip():
                self.descriptions.append(values["content"].strip())
            elif name == "viewport":
                self.viewports.append(values.get("content", ""))
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "a" and values.get("href", "").lower().startswith("tel:"):
            self.tel_links += 1
        elif tag == "form":
            self.forms += 1
        elif tag == "img":
            self.images += 1
            if not values.get("alt", "").strip():
                self.images_without_alt += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def finding(code: str, severity: str, title: str, action: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "title": title, "action": action}


def analyze_html(html: str, url: str) -> list[dict[str, str]]:
    signals = PageSignals()
    signals.feed(html)
    findings: list[dict[str, str]] = []

    if urlparse(url).scheme.lower() != "https":
        findings.append(finding("no_https", "critical", "Site is not using HTTPS", "Redirect every page to HTTPS and update canonical URLs."))
    if not signals.title.strip():
        findings.append(finding("missing_title", "critical", "Page title is missing", "Add a specific title describing the service and location."))
    elif not 20 <= len(signals.title.strip()) <= 65:
        findings.append(finding("weak_title_length", "warning", "Page title length is weak", "Keep the title between 20 and 65 characters."))
    if not signals.descriptions:
        findings.append(finding("missing_description", "warning", "Meta description is missing", "Write a persuasive 120–160 character search snippet."))
    if not signals.viewports:
        findings.append(finding("missing_viewport", "critical", "Mobile viewport is not configured", "Add a responsive viewport meta tag."))
    if signals.h1_count == 0:
        findings.append(finding("missing_h1", "warning", "Primary heading is missing", "Add one clear H1 stating the customer outcome."))
    elif signals.h1_count > 1:
        findings.append(finding("multiple_h1", "warning", "Multiple primary headings compete", "Use one primary H1 and structure the rest with H2/H3."))
    if signals.tel_links == 0 and signals.forms == 0:
        findings.append(finding("missing_cta", "critical", "No direct conversion path detected", "Add a tap-to-call link or short contact form above the fold."))
    if signals.images_without_alt:
        findings.append(finding("missing_alt", "warning", "Images are missing alternative text", "Add useful alt text to informative images."))
    return findings


def score_findings(findings: list[dict[str, str]]) -> int:
    penalties = {"critical": 15, "warning": 7, "note": 2}
    return max(0, 100 - sum(penalties.get(item["severity"], 0) for item in findings))


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "RevenueLeakAudit/0.1"})
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=15, context=context) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read(2_000_000).decode(charset, errors="replace")


def render_markdown(url: str, findings: list[dict[str, str]]) -> str:
    lines = [f"# Website Revenue Leak Audit", "", f"**Website:** {url}", f"**Score:** {score_findings(findings)}/100", ""]
    if not findings:
        lines.extend(["## Summary", "No high-confidence structural leaks were detected by the automated scan."])
    else:
        lines.append("## Prioritized findings")
        for item in findings:
            lines.extend(["", f"### [{item['severity'].upper()}] {item['title']}", item["action"]])
    lines.extend(["", "---", "Automated screening only. Manual review should confirm messaging, visual hierarchy, speed, local SEO, and the end-to-end contact flow."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--output", type=Path, default=Path("audit-report.md"))
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    findings = analyze_html(fetch(args.url), args.url)
    content = json.dumps({"url": args.url, "score": score_findings(findings), "findings": findings}, indent=2) if args.as_json else render_markdown(args.url, findings)
    args.output.write_text(content + ("\n" if args.as_json else ""), encoding="utf-8")
    print(f"Wrote {args.output} ({score_findings(findings)}/100)")


if __name__ == "__main__":
    main()
