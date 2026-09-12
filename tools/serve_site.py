#!/usr/bin/env python3
"""WhoopShop Local Workshop Site Generator & Web Server.

100% Pure Python, zero extra binaries required!
Converts markdown pages in `content/` and `workshop/` into a sleek, responsive
local website with modern styling, navigation, callout boxes, and flight log summaries.

Usage:
    python tools/serve_site.py          # Builds site and serves at http://localhost:8000
    python tools/serve_site.py --port 8080
    python tools/serve_site.py --build-only
"""
import argparse
import http.server
import os
import re
import socketserver
import sys

# Sleek modern dark mode HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — WhoopShop Workshop</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --code-bg: #090d16;
        }}
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .brand {{
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        nav a {{
            color: var(--text-muted);
            text-decoration: none;
            margin-left: 1.5rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        nav a:hover, nav a.active {{
            color: var(--accent);
        }}
        .container {{
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }}
        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }}
        h1, h2, h3 {{ color: var(--text-main); margin-top: 1.5rem; }}
        h1 {{ margin-top: 0; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }}
        a {{ color: var(--accent); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{
            background-color: var(--code-bg);
            color: #e2e8f0;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: var(--code-bg);
            border: 1px solid var(--border);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{ background: none; padding: 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}
        th, td {{
            border: 1px solid var(--border);
            padding: 0.75rem 1rem;
            text-align: left;
        }}
        th {{ background-color: rgba(56, 189, 248, 0.1); color: var(--accent); }}
        tr:nth-child(even) {{ background-color: rgba(255, 255, 255, 0.02); }}

        /* Alert Callout Styling */
        .callout {{
            padding: 1rem 1.25rem;
            border-left: 4px solid var(--accent);
            background-color: rgba(56, 189, 248, 0.08);
            border-radius: 6px;
            margin: 1.5rem 0;
        }}
        .callout-title {{
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }}
        .callout.note {{ border-color: #38bdf8; background-color: rgba(56, 189, 248, 0.08); }}
        .callout.note .callout-title {{ color: #38bdf8; }}
        .callout.tip {{ border-color: #34d399; background-color: rgba(52, 211, 153, 0.08); }}
        .callout.tip .callout-title {{ color: #34d399; }}
        .callout.warning {{ border-color: #fbbf24; background-color: rgba(251, 191, 36, 0.08); }}
        .callout.warning .callout-title {{ color: #fbbf24; }}
        .callout.caution, .callout.important {{ border-color: #f87171; background-color: rgba(248, 113, 113, 0.08); }}
        .callout.caution .callout-title, .callout.important .callout-title {{ color: #f87171; }}

        .meta-bar {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0 1.5rem;
        }}
        .chip {{
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            border: 1px solid var(--border);
            color: var(--text-muted);
            background-color: rgba(255, 255, 255, 0.02);
            white-space: nowrap;
        }}
        .chip:hover {{
            color: var(--accent);
            border-color: var(--accent);
            text-decoration: none;
        }}
        .chip.craft {{
            color: #34d399;
            border-color: rgba(52, 211, 153, 0.4);
            background-color: rgba(52, 211, 153, 0.08);
        }}
        .chip.craft:hover {{ color: #34d399; border-color: #34d399; }}
        .chip .count {{ opacity: 0.55; margin-left: 0.35rem; font-weight: 400; }}
        .chip-cloud {{ display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 1.5rem 0; }}
        .page-list .chips {{ display: flex; gap: 0.4rem; flex-wrap: wrap; }}
        .page-list {{
            list-style: none;
            padding: 0;
        }}
        .page-list li {{
            padding: 0.75rem 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 0.75rem;
            background-color: rgba(255, 255, 255, 0.01);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <header>
        <a href="/index.html" class="brand">🛸 WhoopShop Workshop</a>
        <nav>
            <a href="/index.html">Home</a>
            <a href="/log/index.html">Flight Logs</a>
            <a href="/spec/index.html">Build Specs</a>
            <a href="/docs/index.html">Docs</a>
            <a href="/reference/index.html">Reference</a>
            <a href="/craft/index.html">Craft</a>
            <a href="/tags/index.html">Tags</a>
        </nav>
    </header>
    <main class="container">
        <div class="card">
            {content}
        </div>
    </main>
    <footer>
        WhoopShop — Standalone Cross-Platform FPV Workshop & Telemetry Hub
    </footer>
</body>
</html>
"""


def _clean_scalar(value):
    """Strip surrounding whitespace and matching quotes from a frontmatter value."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        value = value[1:-1]
    return value.strip()


def parse_frontmatter(md_text):
    """Split YAML-ish frontmatter from a markdown document.

    Returns (meta, body). Supports scalars, inline lists (`tags: [a, b]`) and
    block lists. Deliberately small: the site only needs titles, dates, craft
    names and tags, so a full YAML parser would be a dependency for nothing.
    """
    meta = {}
    if not md_text.startswith("---"):
        return meta, md_text

    parts = md_text.split("---", 2)
    if len(parts) < 3:
        return meta, md_text

    pending_key = None
    for raw_line in parts[1].splitlines():
        if not raw_line.strip():
            continue

        block_item = re.match(r"^\s+-\s+(.*)$", raw_line)
        if block_item and pending_key:
            meta.setdefault(pending_key, []).append(_clean_scalar(block_item.group(1)))
            continue

        key_value = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw_line)
        if not key_value:
            continue

        key, value = key_value.group(1), key_value.group(2).strip()
        if not value:
            # A bare `tags:` introduces a block list on the following lines.
            pending_key = key
            meta.setdefault(key, [])
            continue

        pending_key = None
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [_clean_scalar(v) for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key] = _clean_scalar(value)

    return meta, parts[2]


def slugify(value):
    """Turn a tag or craft name into a safe, stable URL fragment."""
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return slug or "untagged"


def page_tags(meta):
    """Normalise the `tags` frontmatter field to a list of strings."""
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = tags.split(",")
    return [t.strip() for t in tags if str(t).strip()]


def page_craft(meta):
    """The craft a page belongs to.

    `craft` is the explicit field; `craft_name` is accepted because flight log
    pages and `tools/capture_log.py` already use it.
    """
    craft = meta.get("craft") or meta.get("craft_name") or ""
    if isinstance(craft, list):
        craft = craft[0] if craft else ""
    return str(craft).strip()


def render_chips(craft, tags, limit=None):
    """Render craft and tag chips as links to their collection pages."""
    chips = []
    if craft:
        chips.append(f'<a class="chip craft" href="/craft/{slugify(craft)}.html">&#128760; {craft}</a>')
    shown = tags if limit is None else tags[:limit]
    for tag in shown:
        chips.append(f'<a class="chip" href="/tags/{slugify(tag)}.html">#{tag}</a>')
    return "".join(chips)


def render_meta_bar(meta):
    """The chip strip shown under a page's title."""
    chips = render_chips(page_craft(meta), page_tags(meta))
    return f'<div class="meta-bar">{chips}</div>' if chips else ""


def inject_meta_bar(body_html, meta_bar):
    """Place the chip strip directly beneath the first heading."""
    if not meta_bar:
        return body_html
    closing = body_html.find("</h1>")
    if closing == -1:
        return meta_bar + body_html
    cut = closing + len("</h1>")
    return body_html[:cut] + "\n" + meta_bar + body_html[cut:]


def parse_markdown_to_html(md_text):
    """Pure-Python markdown converter with Callout Boxes, Tables, Headers, Code, Links."""
    meta, md_text = parse_frontmatter(md_text)
    title = meta.get("title") or "WhoopShop Page"

    lines = md_text.splitlines()
    html_lines = []
    in_code_block = False
    in_table = False
    in_callout = False

    for line in lines:
        # Fenced code blocks
        if line.strip().startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = line.strip().lstrip("`").strip()
                html_lines.append(f'<pre><code class="{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # GitHub Alert Callouts (> [!NOTE], > [!WARNING], > [!CAUTION], > [!TIP], > [!IMPORTANT])
        callout_match = re.match(r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)\]", line.strip(), re.IGNORECASE)
        if callout_match:
            ctype = callout_match.group(1).lower()
            if in_callout:
                html_lines.append("</div>")
            html_lines.append(f'<div class="callout {ctype}"><div class="callout-title">{ctype.upper()}</div>')
            in_callout = True
            continue
        elif in_callout and line.startswith("> "):
            html_lines.append(f"<p>{line[2:].strip()}</p>")
            continue
        elif in_callout and not line.startswith(">"):
            html_lines.append("</div>")
            in_callout = False

        # Tables
        if "|" in line and "-|-" in line:
            continue
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_table:
                html_lines.append("<table><thead><tr>")
                html_lines.append("".join(f"<th>{c}</th>" for c in cells))
                html_lines.append("</tr></thead><tbody>")
                in_table = True
            else:
                html_lines.append("<tr>")
                html_lines.append("".join(f"<td>{c}</td>" for c in cells))
                html_lines.append("</tr>")
            continue
        elif in_table:
            html_lines.append("</tbody></table>")
            in_table = False

        # Headers
        if line.startswith("# "):
            title = line[2:].strip()
            html_lines.append(f"<h1>{title}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")

    if in_table:
        html_lines.append("</tbody></table>")
    if in_callout:
        html_lines.append("</div>")

    body_html = "\n".join(html_lines)

    # Inline formatting (Bold, Code, Links)
    body_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", body_html)
    body_html = re.sub(r"`(.*?)`", r"<code>\1</code>", body_html)
    body_html = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', body_html)

    # Replace .md links with .html links
    body_html = body_html.replace(".md", ".html")

    body_html = inject_meta_bar(body_html, render_meta_bar(meta))

    return title, HTML_TEMPLATE.format(title=title, content=body_html)


def collect_pages(content_dir):
    """Read every markdown page under content/ once, with its frontmatter."""
    pages = []
    for root, _, files in os.walk(content_dir):
        rel_dir = os.path.relpath(root, content_dir)
        for file in sorted(files):
            if not file.endswith(".md"):
                continue

            src_path = os.path.join(root, file)
            with open(src_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            meta, body = parse_frontmatter(md_text)
            is_index = file in ("_index.md", "index.md")
            out_name = "index.html" if is_index else file[:-3] + ".html"
            url_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/") + "/"

            pages.append({
                "src_path": src_path,
                "file": file,
                "rel_dir": rel_dir,
                "url": "/" + url_dir + out_name,
                "markdown": md_text,
                "body": body,
                "meta": meta,
                "is_index": is_index,
                "title": meta.get("title") or file[:-3].replace("-", " ").title(),
                "date": meta.get("date", ""),
                "tags": page_tags(meta),
                "craft": page_craft(meta),
                "section": "" if rel_dir == "." else rel_dir.split(os.sep)[0],
            })
    return pages


def sort_pages(pages):
    """Newest first where a date exists, then alphabetical by title."""
    by_title = sorted(pages, key=lambda p: p["title"].lower())
    return sorted(by_title, key=lambda p: str(p["date"]), reverse=True)


def render_page_list(pages, empty_message="Nothing filed here yet."):
    """A list of page links, each showing its craft and tag chips."""
    if not pages:
        return f'<ul class="page-list"><li>{empty_message}</li></ul>'

    items = []
    for page in sort_pages(pages):
        chips = render_chips(page["craft"], page["tags"], limit=4)
        items.append(
            f'<li><a href="{page["url"]}">&#128196; {page["title"]}</a>'
            f'<span class="chips">{chips}</span></li>'
        )
    return '<ul class="page-list">\n' + "\n".join(items) + "\n</ul>"


def index_intro(pages, rel_dir):
    """The prose from a section's _index.md, so it survives index generation."""
    for page in pages:
        if page["rel_dir"] == rel_dir and page["is_index"]:
            body = page["body"].strip()
            if body:
                html = "\n".join(
                    f"<p>{line.strip()}</p>" for line in body.splitlines() if line.strip()
                )
                return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    return ""


def generate_section_index(pages, rel_dir, section_title):
    """Index page for one content section, listing its articles."""
    entries = [p for p in pages if p["rel_dir"] == rel_dir and not p["is_index"]]
    html_content = (
        f"<h1>{section_title}</h1>\n"
        f"{index_intro(pages, rel_dir)}\n"
        f"{render_page_list(entries, 'No log entries or documents created yet.')}\n"
    )
    return HTML_TEMPLATE.format(title=section_title, content=html_content)


def collect_tags(pages):
    """Map each tag to the pages carrying it."""
    tags = {}
    for page in pages:
        if page["is_index"]:
            continue
        for tag in page["tags"]:
            tags.setdefault(tag, []).append(page)
    return tags


def collect_craft(pages):
    """Map each craft name to the pages about it."""
    craft = {}
    for page in pages:
        if page["is_index"] or not page["craft"]:
            continue
        craft.setdefault(page["craft"], []).append(page)
    return craft


def generate_tag_page(tag, pages):
    """One page per tag, listing everything carrying it."""
    content = (
        f"<h1>#{tag}</h1>\n"
        f"<p>{len(pages)} page(s) tagged <code>{tag}</code>, across every section "
        f"of the workshop.</p>\n"
        f"{render_page_list(pages)}\n"
        f'<p><a href="/tags/index.html">&#8592; All tags</a></p>\n'
    )
    return HTML_TEMPLATE.format(title=f"#{tag}", content=content)


def generate_tag_index(tags):
    """The tag cloud, most used first."""
    ordered = sorted(tags.items(), key=lambda item: (-len(item[1]), item[0].lower()))
    cloud = "".join(
        f'<a class="chip" href="/tags/{slugify(tag)}.html">#{tag}'
        f'<span class="count">{len(pages)}</span></a>'
        for tag, pages in ordered
    )
    body = f'<div class="chip-cloud">{cloud}</div>' if cloud else "<p>No tags in use yet.</p>"
    content = (
        "<h1>Tags</h1>\n"
        "<p>Every topic used across build specs, flight logs, docs and reference "
        "pages. Tags are the cross-section view; use Craft to see one drone.</p>\n"
        f"{body}\n"
    )
    return HTML_TEMPLATE.format(title="Tags", content=content)


def generate_craft_page(craft, pages):
    """Everything about a single drone, grouped by section."""
    sections = {}
    for page in pages:
        sections.setdefault(page["section"] or "root", []).append(page)

    blocks = []
    for section in sorted(sections):
        label = {"spec": "Build Specs", "log": "Flight Logs",
                 "docs": "Documentation", "reference": "Reference"}.get(section, section.title())
        blocks.append(f"<h2>{label}</h2>\n{render_page_list(sections[section])}")

    content = (
        f"<h1>&#128760; {craft}</h1>\n"
        f"<p>{len(pages)} page(s) filed against this craft.</p>\n"
        + "\n".join(blocks)
        + f'\n<p><a href="/craft/index.html">&#8592; All craft</a></p>\n'
    )
    return HTML_TEMPLATE.format(title=craft, content=content)


def generate_craft_index(craft_map):
    """The fleet overview."""
    ordered = sorted(craft_map.items(), key=lambda item: item[0].lower())
    cloud = "".join(
        f'<a class="chip craft" href="/craft/{slugify(name)}.html">&#128760; {name}'
        f'<span class="count">{len(pages)}</span></a>'
        for name, pages in ordered
    )
    body = f'<div class="chip-cloud">{cloud}</div>' if cloud else "<p>No craft recorded yet.</p>"
    content = (
        "<h1>Craft</h1>\n"
        "<p>Every drone in the workshop. Each page gathers that craft's build "
        "spec, flight logs and notes in one place, no matter which section they "
        "live in.</p>\n"
        f"{body}\n"
    )
    return HTML_TEMPLATE.format(title="Craft", content=content)


def write_html(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def build_site(base_dir, output_dir):
    """Render content/ to HTML, plus the tag and craft collection pages."""
    os.makedirs(output_dir, exist_ok=True)
    content_dir = os.path.join(base_dir, "content")
    pages = collect_pages(content_dir)

    for page in pages:
        rel_dir = page["rel_dir"]
        target_root = output_dir if rel_dir == "." else os.path.join(output_dir, rel_dir)
        out_name = os.path.basename(page["url"])
        _, html_output = parse_markdown_to_html(page["markdown"])
        write_html(os.path.join(target_root, out_name), html_output)

    # Section indexes replace the rendered _index.md with a generated listing.
    for rel_dir in sorted({p["rel_dir"] for p in pages if p["rel_dir"] != "."}):
        if not any(p["rel_dir"] == rel_dir and p["is_index"] for p in pages):
            continue
        section_title = rel_dir.replace(os.sep, " ").title() + " Directory"
        write_html(
            os.path.join(output_dir, rel_dir, "index.html"),
            generate_section_index(pages, rel_dir, section_title),
        )

    tags = collect_tags(pages)
    for tag, tagged in tags.items():
        write_html(os.path.join(output_dir, "tags", f"{slugify(tag)}.html"),
                   generate_tag_page(tag, tagged))
    write_html(os.path.join(output_dir, "tags", "index.html"), generate_tag_index(tags))

    craft_map = collect_craft(pages)
    for craft, craft_pages in craft_map.items():
        write_html(os.path.join(output_dir, "craft", f"{slugify(craft)}.html"),
                   generate_craft_page(craft, craft_pages))
    write_html(os.path.join(output_dir, "craft", "index.html"), generate_craft_index(craft_map))

    print(f"[+] Local website successfully built in `{output_dir}`.")
    print(f"    {len(pages)} page(s), {len(tags)} tag(s), {len(craft_map)} craft.")


def serve_site(output_dir, port=8000):
    """Serve the built site using Python's built-in http.server."""
    os.chdir(output_dir)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n==================================================")
        print(f"  🛸 WhoopShop Local Workshop Site Live!")
        print(f"  URL: http://localhost:{port}/")
        print(f"  Press Ctrl+C to stop the server.")
        print(f"==================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down workshop server.")


def main():
    parser = argparse.ArgumentParser(description="WhoopShop Pure-Python Local Site Builder & Server.")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to serve site on (default: 8000)")
    parser.add_argument("--build-only", action="store_true", help="Build HTML files without starting web server")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "public_html")

    build_site(base_dir, output_dir)

    if not args.build_only:
        serve_site(output_dir, port=args.port)


if __name__ == "__main__":
    main()
