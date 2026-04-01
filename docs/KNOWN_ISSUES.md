# Known Issues & Stabilization Roadmap (v8.0.0+)

The v8.0.0 release is explicitly focused on stabilizing the plugin marketplace experience and decoupling storage semantics. Below are the currently identified operational constraints and known issues being tracked for future iterations:

## Data Storage
- **Local Fallback Persistence:** If the plugin operates outside of an initialized Claude Code environment (where `${CLAUDE_PLUGIN_DATA}` is undefined), data is saved sequentially into `.claude-patterns/` within the Current Working Directory (CWD). Switching directories without injecting the environment variable can lead to fragmented patterns.
- **Concurrency Locks on Windows:** High-volume sequential tasks on Windows currently use `msvcrt` locks in `pattern_storage.py`. There may be a 1-5ms delay during massive multi-agent asynchronous logging events.

## Sub-Agent Execution
- **Long-Running Process Limits:** Certain long-running Python validation scripts (like headless browser testing) might timeout under Claude Code's default step execution timer if they exceed ~180 seconds.
- **Terminal Parsing Variations:** Powershell/CMD output parsing differs slightly per system. Workarounds have been included but rely heavily on standard `$stderr`.

## Future Tracking
If you encounter exceptions, ensure you are running the `v8.0.0+` codebase seamlessly via standard marketplace initialization `claude plugin install`. Development anomalies are usually remedied by running `python -m lib.exec_plugin_script pattern_storage.py check`.
