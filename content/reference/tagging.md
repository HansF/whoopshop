---
title: "Tagging & Multi-Craft Organisation"
date: 2026-09-12T20:10:00Z
draft: false
tags: [reference, workflow]
---

# Tagging & Multi-Craft Organisation

The workshop holds more than one drone, so every page carries two pieces of
metadata: **which craft it is about**, and **what it is about**. The site builder
turns those into browsable collections, which means all drones can share a single
repository without the sections turning into a junk drawer.

---

## 1. The Two Axes

| Axis | Frontmatter | Answers | Site section |
| :--- | :--- | :--- | :--- |
| **Craft** | `craft:` or `craft_name:` | Which drone is this about? | `/craft/` |
| **Tags** | `tags:` | What is this about? | `/tags/` |

Craft is the vertical cut: one drone, everything ever written about it. Tags are
the horizontal cut: one topic, across every drone. A page can have a craft, tags,
both, or neither. Pages with no craft, such as this one, are general workshop
knowledge.

---

## 2. Frontmatter

Both list styles work, so existing pages do not need rewriting:

```yaml
---
title: "Air65 — Bench Setup & Preference Port"
date: 2026-09-12T19:30:00Z
craft_name: "AIR65 F"
draft: false
tags: [setup, modes, rates, osd, firmware]
---
```

```yaml
tags:
  - setup
  - modes
```

`craft_name` is accepted as a synonym for `craft` because flight log pages and
`tools/capture_log.py` already used it. Use whichever reads better; `craft_name` is
the safer default for log pages.

---

## 3. Tag Vocabulary

Keep the list short. A tag used once is a tag that helps nobody.

| Tag | Use for |
| :--- | :--- |
| `hardware` | Frames, motors, boards, weights, component choices |
| `setup` | Bringing a craft up to workshop standard |
| `modes` | Switch layout, aux channels, arming |
| `rates` | Rate curves, expo, throttle feel |
| `tuning` | PIDs, filters, anything flight-feel related |
| `blackbox` | Log capture, decoding, analysis |
| `osd` | On-screen display layout and drivers |
| `firmware` | Flashing, versions, board-specific firmware warnings |
| `cli` | Betaflight CLI usage and variables |
| `elrs` | Receiver binding, link settings, telemetry |
| `vtx` | Video transmitter power, bands, channels |
| `safety` | Anything that can hurt someone or brick a board |
| `flight-log` | Applied automatically by `tools/capture_log.py` |
| `telemetry` | Captured live values from the flight controller |
| `reference` | Lookup material rather than narrative |
| `generated` | Machine-written, do not hand-edit |
| `workflow` | How we work in this repo |

Before inventing a tag, check `/tags/` for one that already fits.

---

## 4. Adding a Craft

No configuration or registry is needed. Give a page a `craft_name`, and the craft
page appears on the next build.

The recommended shape for a new drone:

1. A build spec at `content/spec/<craft>-build.md` with `craft_name` and
   `tags: [hardware, setup]`.
2. A first log entry at `content/log/<date>-<craft>-setup.md` recording what was
   changed and why.
3. Shared preferences stay in `content/reference/`, tagged but with **no** craft, so
   they are not duplicated per drone. See
   [Pilot Preferences](/reference/pilot-preferences.html).

> [!TIP]
> Write the craft name exactly as `craft_name` appears in Betaflight. `AIR65 F` and
> `Air65 F` produce two separate craft pages.

---

## 5. Rebuilding

```bash
python tools/serve_site.py --build-only   # writes public_html/
python tools/serve_site.py                # ... and serves it on :8000
```

The build prints a count of pages, tags and craft. A tag count that jumps
unexpectedly usually means a typo created a near-duplicate tag.
