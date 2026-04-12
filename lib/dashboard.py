#!/usr/bin/env python3
"""Autonomous Agent Dashboard - Web interface for learning metrics.

Reads JSON data from .claude-patterns/ and renders a 4-tab dashboard
with Chart.js visualizations. No local module dependencies.

Usage:
    python dashboard.py --port 5000 --patterns-dir .claude-patterns
"""

import argparse
import json
import socket
import webbrowser
from pathlib import Path
from typing import Any

from flask import Flask, jsonify

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_TTL = 5.0  # seconds


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------


def _load_json(path: str, filename: str) -> dict | list | None:
    """Load a JSON file with a short in-memory cache."""
    cache_key = f"{path}/{filename}"
    now = __import__("time").time()
    if cache_key in _CACHE:
        ts, data = _CACHE[cache_key]
        if now - ts < _CACHE_TTL:
            return data
    fp = Path(path) / filename
    if not fp.exists():
        return None
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
        _CACHE[cache_key] = (now, data)
        return data
    except (json.JSONDecodeError, OSError):
        return None


def get_overview_metrics(patterns_dir: str) -> dict:
    """Overview metrics from unified_data + dashboard_success_metrics."""
    ud = _load_json(patterns_dir, "unified_data.json") or {}
    sm = _load_json(patterns_dir, "dashboard_success_metrics.json") or {}
    patterns = ud.get("patterns", [])
    total_patterns = len(patterns)
    avg_success = 0.0
    if patterns:
        avg_success = sum(p.get("success_rate", 0) for p in patterns) / total_patterns
    return {
        "total_tasks": sm.get("total_tasks", 0),
        "successful_tasks": sm.get("successful_tasks", 0),
        "success_rate": round(
            sm.get("successful_tasks", 0) / max(1, sm.get("total_tasks", 1)) * 100, 1
        ),
        "avg_quality_score": round(sm.get("avg_quality_score", 0), 1),
        "avg_performance_index": round(sm.get("avg_performance_index", 0), 1),
        "total_patterns": total_patterns,
        "avg_pattern_success": round(avg_success * 100, 1),
        "last_updated": sm.get("last_updated", ""),
    }


def get_quality_trends(patterns_dir: str, days: int = 30) -> dict:
    """Quality trend data from quality_history."""
    qh = _load_json(patterns_dir, "quality_history.json") or {}
    assessments = qh.get("quality_assessments", [])
    recent = assessments[-days:] if len(assessments) > days else assessments
    return {
        "assessments": [
            {
                "timestamp": a.get("timestamp", ""),
                "task_type": a.get("task_type", "unknown"),
                "overall_score": a.get("overall_score", 0),
                "pass": a.get("pass", False),
            }
            for a in recent
        ],
        "statistics": qh.get("statistics", {}),
        "total_assessments": len(assessments),
    }


def get_skill_metrics(patterns_dir: str) -> dict:
    """Skill effectiveness from skill_metrics.json."""
    sm = _load_json(patterns_dir, "skill_metrics.json") or {}
    effectiveness = sm.get("skill_effectiveness", {})
    usage_history = sm.get("skill_usage_history", [])
    return {
        "effectiveness": effectiveness,
        "usage_history": usage_history[-20:],
        "total_events": sm.get("total_skill_usage_events", 0),
        "overall_success_rate": sm.get("overall_success_rate", 0),
        "last_updated": sm.get("last_updated", ""),
    }


def get_agent_performance(patterns_dir: str) -> dict:
    """Agent performance from agent_performance.json."""
    ap = _load_json(patterns_dir, "agent_performance.json") or {}
    return {
        "agent_metrics": ap.get("agent_metrics", {}),
        "task_history": ap.get("task_history", []),
        "last_updated": ap.get("last_updated", ""),
    }


def get_recent_activity(patterns_dir: str, limit: int = 20) -> dict:
    """Recent activity from performance_records.json."""
    pr = _load_json(patterns_dir, "performance_records.json") or {}
    records = pr.get("records", [])
    recent = records[-limit:] if len(records) > limit else records
    return {
        "records": [
            {
                "timestamp": r.get("timestamp", ""),
                "task_type": r.get("task_type", "unknown"),
                "quality_score": r.get("quality_score", 0),
                "success": r.get("success", False),
                "duration": r.get("duration", 0),
                "skills_used": r.get("skills_used", []),
            }
            for r in reversed(recent)
        ],
        "total_records": len(records),
    }


def get_current_model(patterns_dir: str) -> dict:
    """Current model info from current_session.json."""
    cs = _load_json(patterns_dir, "current_session.json") or {}
    return {
        "model": cs.get("current_model", "Unknown"),
        "session_start": cs.get("session_start", ""),
        "last_activity": cs.get("last_activity", ""),
        "detection_method": cs.get("detection_method", ""),
        "platform": cs.get("platform", ""),
    }


def get_model_quality_scores(patterns_dir: str) -> dict:
    """Model quality scores from quality_history.json."""
    qh = _load_json(patterns_dir, "quality_history.json") or {}
    return {
        "baselines": qh.get("baselines", {}),
        "statistics": qh.get("statistics", {}),
    }


def get_debugging_performance(patterns_dir: str) -> dict:
    """Debugging performance from debugging_performance.json."""
    dp = _load_json(patterns_dir, "debugging_performance.json") or {}
    return {
        "rankings": dp.get("performance_rankings", []),
        "detailed_metrics": dp.get("detailed_metrics", {}),
        "total_assessments": dp.get("total_debugging_assessments", 0),
    }


def get_token_overview(patterns_dir: str) -> dict:
    """Token analytics from token_analytics.json."""
    ta = _load_json(patterns_dir, "token_analytics.json") or {}
    return {
        "total_registered_content": ta.get("total_registered_content", 0),
        "total_tokens": ta.get("total_tokens", 0),
        "content_by_type": ta.get("content_by_type", {}),
        "access_frequency": ta.get("access_frequency", {}),
        "last_updated": ta.get("last_updated", ""),
    }


def get_kpi_overview(patterns_dir: str) -> dict:
    """KPI data from dashboard_success_metrics.json."""
    sm = _load_json(patterns_dir, "dashboard_success_metrics.json") or {}
    return {
        "total_tasks": sm.get("total_tasks", 0),
        "successful_tasks": sm.get("successful_tasks", 0),
        "avg_quality_score": sm.get("avg_quality_score", 0),
        "avg_performance_index": sm.get("avg_performance_index", 0),
        "learning_patterns": sm.get("learning_patterns", {}),
        "improvement_trends": sm.get("improvement_trends", {}),
    }


# ---------------------------------------------------------------------------
# HTML template (4-tab dashboard)
# ---------------------------------------------------------------------------

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Autonomous Agent Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  :root { --bg: #0f172a; --card: #1e293b; --border: #334155; --text: #e2e8f0; --muted: #94a3b8; --accent: #38bdf8; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); }
  .header { background: var(--card); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; }
  .header h1 { font-size: 1.25rem; font-weight: 600; }
  .header .model { color: var(--accent); font-size: 0.85rem; }
  .tabs { display: flex; background: var(--card); border-bottom: 1px solid var(--border); padding: 0 24px; gap: 0; }
  .tab { padding: 12px 20px; cursor: pointer; color: var(--muted); border-bottom: 2px solid transparent; font-size: 0.9rem; }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .content { max-width: 1200px; margin: 0 auto; padding: 24px; }
  .panel { display: none; }
  .panel.active { display: block; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
  .card .label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .card .value { font-size: 1.8rem; font-weight: 700; }
  .chart-box { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 24px; }
  .chart-box h3 { font-size: 0.95rem; margin-bottom: 12px; }
  table { width: 100%; border-collapse: collapse; }
  th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border); font-size: 0.85rem; }
  th { color: var(--muted); font-weight: 500; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
  .badge-pass { background: #065f46; color: #6ee7b7; }
  .badge-fail { background: #7f1d1d; color: #fca5a5; }
  .refresh-info { color: var(--muted); font-size: 0.8rem; }
  @media (max-width: 768px) { .grid { grid-template-columns: 1fr 1fr; } .content { padding: 12px; } }
</style>
</head>
<body>
<div class="header">
  <h1>Autonomous Agent Dashboard</h1>
  <span class="model" id="model-info">Loading...</span>
</div>
<div class="tabs">
  <div class="tab active" onclick="switchTab('overview')">Overview</div>
  <div class="tab" onclick="switchTab('quality')">Quality</div>
  <div class="tab" onclick="switchTab('skills')">Skills</div>
  <div class="tab" onclick="switchTab('agents')">Agents</div>
</div>
<div class="content">
  <!-- Overview -->
  <div id="panel-overview" class="panel active">
    <div class="grid" id="overview-cards"></div>
    <div class="chart-box"><h3>Quality Score Timeline</h3><canvas id="chart-quality-timeline"></canvas></div>
  </div>
  <!-- Quality -->
  <div id="panel-quality" class="panel">
    <div class="grid" id="quality-cards"></div>
    <div class="chart-box"><h3>Model Quality Scores</h3><canvas id="chart-model-scores"></canvas></div>
    <div class="chart-box"><h3>Debugging Performance</h3><div id="debugging-table"></div></div>
  </div>
  <!-- Skills -->
  <div id="panel-skills" class="panel">
    <div class="grid" id="skills-cards"></div>
    <div class="chart-box"><h3>Skill Effectiveness</h3><canvas id="chart-skills"></canvas></div>
    <div class="chart-box"><h3>Skill Usage History</h3><div id="skills-table"></div></div>
  </div>
  <!-- Agents -->
  <div id="panel-agents" class="panel">
    <div class="grid" id="agents-cards"></div>
    <div class="chart-box"><h3>Recent Activity</h3><div id="activity-table"></div></div>
  </div>
</div>
<div class="header" style="justify-content:center">
  <span class="refresh-info">Auto-refresh every 30s &middot; <span id="last-refresh"></span></span>
</div>
<script>
const PDIR = "{{PATTERNS_DIR}}";
let charts = {};

function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', ['overview','quality','skills','agents'][i]===name));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-'+name).classList.add('active');
}

async function api(endpoint) {
  const r = await fetch('/api/'+endpoint);
  return r.json();
}

function card(html, id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

function refreshTime() {
  document.getElementById('last-refresh').textContent = new Date().toLocaleTimeString();
}

async function loadOverview() {
  const d = await api('overview');
  card([
    mc('Total Tasks', d.total_tasks),
    mc('Success Rate', d.success_rate+'%'),
    mc('Avg Quality', d.avg_quality_score),
    mc('Patterns', d.total_patterns),
    mc('Pattern Success', d.avg_pattern_success+'%'),
  ].join(''), 'overview-cards');

  const qt = await api('quality-trends');
  const labels = qt.assessments.map(a => (a.timestamp||'').slice(5,16));
  const scores = qt.assessments.map(a => a.overall_score);
  if (charts.timeline) charts.timeline.destroy();
  charts.timeline = new Chart(document.getElementById('chart-quality-timeline'), {
    type:'line', data:{labels, datasets:[{label:'Quality Score',data:scores,borderColor:'#38bdf8',backgroundColor:'rgba(56,189,248,0.1)',fill:true,tension:0.3}]},
    options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,max:100}}}
  });
}

async function loadQuality() {
  const d = await api('quality-trends');
  const stats = d.statistics || {};
  card([
    mc('Total Assessments', d.total_assessments),
    mc('Avg Score', (stats.mean_score||0).toFixed(1)),
    mc('Pass Rate', ((stats.pass_rate||0)*100).toFixed(1)+'%'),
  ].join(''), 'quality-cards');

  const mq = await api('model-quality-scores');
  const baselines = mq.baselines || {};
  const blabels = Object.keys(baselines);
  const bscores = blabels.map(k => baselines[k].overall_score || baselines[k] || 0);
  if (charts.modelScores) charts.modelScores.destroy();
  charts.modelScores = new Chart(document.getElementById('chart-model-scores'), {
    type:'bar', data:{labels:blabels, datasets:[{label:'Score',data:bscores,backgroundColor:'#38bdf8'}]},
    options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,max:100}}}
  });

  const dp = await api('debugging-performance');
  const metrics = dp.detailed_metrics || {};
  let html = '<table><tr><th>Model</th><th>Score</th><th>Issues Resolved</th></tr>';
  for (const [m, v] of Object.entries(metrics)) {
    html += `<tr><td>${m}</td><td>${(v.overall_score||0).toFixed(1)}</td><td>${v.issues_resolved||0}</td></tr>`;
  }
  html += '</table>';
  document.getElementById('debugging-table').innerHTML = html;
}

async function loadSkills() {
  const d = await api('skills');
  const eff = d.effectiveness || {};
  const topSkills = Object.entries(eff).sort((a,b) => (b[1].success_rate||0)-(a[1].success_rate||0)).slice(0,8);
  card([
    mc('Total Events', d.total_events),
    mc('Overall Success', ((d.overall_success_rate||0)*100).toFixed(1)+'%'),
  ].join(''), 'skills-cards');

  if (charts.skills) charts.skills.destroy();
  charts.skills = new Chart(document.getElementById('chart-skills'), {
    type:'bar', data:{labels:topSkills.map(s=>s[0].slice(0,20)), datasets:[{label:'Success Rate',data:topSkills.map(s=>((s[1].success_rate||0)*100).toFixed(1)),backgroundColor:'#38bdf8'}]},
    options:{responsive:true,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{max:100}}}
  });

  const uh = d.usage_history || [];
  let html = '<table><tr><th>Skill</th><th>Success</th><th>Score</th></tr>';
  uh.slice(-10).forEach(u => {
    html += `<tr><td>${u.skill_name||u.skill||'-'}</td><td><span class="badge ${u.success?'badge-pass':'badge-fail'}">${u.success?'Pass':'Fail'}</span></td><td>${(u.quality_score||0).toFixed(1)}</td></tr>`;
  });
  html += '</table>';
  document.getElementById('skills-table').innerHTML = html;
}

async function loadAgents() {
  const [ap, act] = await Promise.all([api('agents'), api('recent-activity')]);
  const agents = ap.agent_metrics || {};
  const agentCount = Object.keys(agents).length;
  card([
    mc('Tracked Agents', agentCount),
    mc('Activity Records', act.total_records),
  ].join(''), 'agents-cards');

  const records = act.records || [];
  let html = '<table><tr><th>Time</th><th>Task</th><th>Quality</th><th>Status</th><th>Duration</th></tr>';
  records.slice(0,15).forEach(r => {
    const t = (r.timestamp||'').slice(0,16).replace('T',' ');
    html += `<tr><td>${t}</td><td>${r.task_type}</td><td>${r.quality_score}</td><td><span class="badge ${r.success?'badge-pass':'badge-fail'}">${r.success?'Pass':'Fail'}</span></td><td>${r.duration||'-'}s</td></tr>`;
  });
  html += '</table>';
  document.getElementById('activity-table').innerHTML = html;
}

function mc(label, value) {
  return `<div class="card"><div class="label">${label}</div><div class="value">${value}</div></div>`;
}

async function loadAll() {
  try {
    const model = await api('current-model');
    document.getElementById('model-info').textContent = model.model || 'Unknown';
    await Promise.all([loadOverview(), loadQuality(), loadSkills(), loadAgents()]);
    refreshTime();
  } catch(e) { console.error(e); }
}

loadAll();
setInterval(loadAll, 30000);
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Flask app factory
# ---------------------------------------------------------------------------


def create_app(patterns_dir: str = ".claude-patterns") -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return DASHBOARD_HTML.replace("{{PATTERNS_DIR}}", patterns_dir)

    @app.route("/api/overview")
    def api_overview():
        return jsonify(get_overview_metrics(patterns_dir))

    @app.route("/api/quality-trends")
    @app.route("/api/quality-trends/<int:days>")
    def api_quality_trends(days=30):
        return jsonify(get_quality_trends(patterns_dir, days))

    @app.route("/api/skills")
    def api_skills():
        return jsonify(get_skill_metrics(patterns_dir))

    @app.route("/api/agents")
    def api_agents():
        return jsonify(get_agent_performance(patterns_dir))

    @app.route("/api/recent-activity")
    @app.route("/api/recent-activity/<int:limit>")
    def api_recent_activity(limit=20):
        return jsonify(get_recent_activity(patterns_dir, limit))

    @app.route("/api/current-model")
    def api_current_model():
        return jsonify(get_current_model(patterns_dir))

    @app.route("/api/model-quality-scores")
    def api_model_quality_scores():
        return jsonify(get_model_quality_scores(patterns_dir))

    @app.route("/api/debugging-performance")
    def api_debugging_performance():
        return jsonify(get_debugging_performance(patterns_dir))

    @app.route("/api/tokens/overview")
    def api_tokens_overview():
        return jsonify(get_token_overview(patterns_dir))

    @app.route("/api/kpi/overview")
    def api_kpi_overview():
        return jsonify(get_kpi_overview(patterns_dir))

    return app


# ---------------------------------------------------------------------------
# Server utilities
# ---------------------------------------------------------------------------


def _find_port(start: int = 5000, host: str = "127.0.0.1", tries: int = 20) -> int:
    """Find an available port starting from *start*."""
    for port in range(start, start + tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((host, port)) != 0:
                    return port
        except OSError:
            return port
    return start


def run_dashboard(
    host: str = "127.0.0.1",
    port: int = 5000,
    patterns_dir: str = ".claude-patterns",
    debug: bool = False,
    open_browser: bool = True,
) -> None:
    """Start the dashboard server."""
    port = _find_port(port, host)
    url = f"http://{host}:{port}"

    print("[START] Autonomous Agent Dashboard")
    print(f"[URL]   {url}")
    print(f"[DATA]  {patterns_dir}")
    print("[STOP]  Press Ctrl+C to stop")
    print()

    if open_browser:
        webbrowser.open(url)

    app = create_app(patterns_dir)
    app.run(host=host, port=port, debug=debug)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Autonomous Agent Dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--patterns-dir", default=".claude-patterns")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    run_dashboard(
        host=args.host,
        port=args.port,
        patterns_dir=args.patterns_dir,
        debug=args.debug,
        open_browser=not args.no_browser,
    )


if __name__ == "__main__":
    main()
