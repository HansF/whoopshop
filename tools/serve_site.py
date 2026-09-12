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


def parse_markdown_to_html(md_text):
    """Pure-Python markdown converter with Callout Boxes, Tables, Headers, Code, Links."""
    title = "WhoopShop Page"
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            md_text = parts[2]
            for line in frontmatter.splitlines():
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"').strip("'")

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

    return title, HTML_TEMPLATE.format(title=title, content=body_html)


def generate_section_index(dir_path, section_title):
    """Generate HTML index page listing markdown articles in a section folder."""
    items = []
    for file in sorted(os.listdir(dir_path)):
        if file.endswith(".md") and file not in ("_index.md", "index.md"):
            filepath = os.path.join(dir_path, file)
            title = file.replace(".md", "").replace("-", " ").title()
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                for line in content.splitlines():
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
                        break

            html_filename = file.replace(".md", ".html")
            items.append(f'<li><a href="{html_filename}">📄 {title}</a> <span>→</span></li>')

    list_html = "\n".join(items) if items else "<li>No log entries or documents created yet.</li>"

    html_content = f"""<h1>{section_title}</h1>
<p>Explore articles, recordings, and guides in this section:</p>
<ul class="page-list">
{list_html}
</ul>
"""
    return HTML_TEMPLATE.format(title=section_title, content=html_content)


def build_site(base_dir, output_dir):
    """Scan content/ directory, rendering HTML files and section index pages."""
    os.makedirs(output_dir, exist_ok=True)
    content_dir = os.path.join(base_dir, "content")

    for root, _, files in os.walk(content_dir):
        rel_root = os.path.relpath(root, content_dir)
        target_root = os.path.join(output_dir, rel_root) if rel_root != "." else output_dir
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            if file.endswith(".md"):
                src_path = os.path.join(root, file)
                filename_base = "index.html" if file in ("_index.md", "index.md") else file.replace(".md", ".html")
                dst_path = os.path.join(target_root, filename_base)

                with open(src_path, "r", encoding="utf-8") as f:
                    md_text = f.read()

                _, html_output = parse_markdown_to_html(md_text)
                with open(dst_path, "w", encoding="utf-8") as f:
                    f.write(html_output)

        # Generate automated index listing if section index exists
        if rel_root != "." and "_index.md" in files:
            section_title = rel_root.title() + " Directory"
            idx_dst = os.path.join(target_root, "index.html")
            idx_html = generate_section_index(root, section_title)
            with open(idx_dst, "w", encoding="utf-8") as f:
                f.write(idx_html)

    print(f"[+] Local website successfully built in `{output_dir}`.")


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
