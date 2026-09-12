# WhoopShop Test Suite

These tests run with **no flight controller attached**. Every serial exchange
goes through `tools/fake_fc.py`, an in-memory stand-in that speaks the
Betaflight CLI and records what it was sent.

```bash
python -m unittest discover -s tests        # quiet
python -m unittest discover -s tests -v     # per-test names
python -m tools.check_presets               # validate canned command lists
```

Only `pyserial` is required, matching the project's zero-dependency promise.
The suite uses the standard library's `unittest`, so there is nothing extra to
install in CI.

## What is covered

| Area | File | Why it matters |
| :--- | :--- | :--- |
| CLI exit discipline | `test_fc_session.py` | A session that fails to exit locks the FC out of MSP until USB is replugged |
| Session output | `test_fc_session.py` | Captured text must carry no echo or prompt, or backups cannot be replayed |
| Variable names | `test_bf_vars.py` | Betaflight answers a bad name with `Invalid name` and carries on silently |

## Fixtures

`fixtures/` holds recorded Betaflight replies (`status`, `diff all`, a `get`
response, and an error). To add a board's real output, capture it with
`python tools/bf_cli.py "status"` and save the body as a new fixture.

## Speed

`CliSession` takes a `delay_scale` argument. Tests pass `0` to collapse the
serial settle delays and the prompt quiet period, which keeps the suite under
a second. Real hardware uses the default of `1.0`.
