#!/usr/bin/env python3
"""
Robust Dashboard Launcher for Autonomous Agent

Handles dashboard startup with automatic port detection,
health monitoring, and automatic restart capabilities.
Prevents dashboard connectivity issues through proactive monitoring.
"""

import subprocess
import sys
import time
import requests
import socket
import argparse
from pathlib import Path
import signal
import logging

# Ensure log directory exists
log_dir = Path('.claude/logs')
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'dashboard-launcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DashboardLauncher:
    """Robust dashboard launcher with health monitoring and auto-restart."""

    def __init__(self, host: str = '127.0.0.1', port: int = 5000,
                 patterns_dir: str = '.claude-patterns', auto_restart: bool = True):
        self.host = host
        self.port = port
        self.patterns_dir = patterns_dir
        self.auto_restart = auto_restart
        self.dashboard_process = None
        self.restart_count = 0
        self.max_restarts = 5

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down dashboard...")
        self.stop_dashboard()
        sys.exit(0)

    def is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((self.host, port))
                return result != 0
        except Exception as e:
            logger.warning(f"Port check failed for {port}: {e}")
            return False

    def find_available_port(self, start_port: int = 5000,
                           max_attempts: int = 10) -> int:
        """Find an available port starting from start_port."""
        for i in range(max_attempts):
            port = start_port + i
            if self.is_port_available(port):
                return port
        # Fallback to random port in 8000-9000 range
        import random
        for _ in range(10):
            port = random.randint(8000, 9000)
            if self.is_port_available(port):
                return port
        raise RuntimeError("No available ports found")

    def is_dashboard_responding(self, url: str, timeout: int = 5) -> bool:
        """Check if dashboard API is responding."""
        try:
            response = requests.get(f"{url}/api/overview", timeout=timeout)
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Dashboard health check failed: {e}")
            return False

    def start_dashboard(self) -> Tuple[bool, str, int]:
        """Start the dashboard with automatic port detection."""
        try:
            # Find available port
            original_port = self.port
            if not self.is_port_available(self.port):
                logger.info(f"Port {self.port} is occupied, finding alternative...")
                self.port = self.find_available_port(self.port)
                if self.port != original_port:
                    logger.info(f"Using alternative port: {self.port}")

            # Ensure patterns directory exists
            Path(self.patterns_dir).mkdir(parents=True, exist_ok=True)

            # Start dashboard process
            dashboard_script = Path(__file__).parent / 'dashboard.py'
            cmd = [
                sys.executable, str(dashboard_script),
                '--host', self.host,
                '--port', str(self.port),
                '--patterns-dir', self.patterns_dir,
                '--no-browser'  # We handle browser opening separately
            ]

            logger.info(f"Starting dashboard with command: {' '.join(cmd)}")

            # Start dashboard in background
            self.dashboard_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Wait for startup and validate
            dashboard_url = f"http://{self.host}:{self.port}"
            logger.info(f"Waiting for dashboard to start at {dashboard_url}...")

            # Wait up to 30 seconds for dashboard to start
            startup_timeout = 30
            start_time = time.time()

            while time.time() - start_time < startup_timeout:
                if self.dashboard_process.poll() is not None:
                    # Process terminated
                    stdout, _ = self.dashboard_process.communicate()
                    error_msg = f"Dashboard process terminated. Output: {stdout}"
                    logger.error(error_msg)
                    return False, error_msg, 0

                if self.is_dashboard_responding(dashboard_url):
                    logger.info(f"Dashboard is responding at {dashboard_url}")
                    return True, f"Dashboard started successfully at {dashboard_url}", self.port

                time.sleep(1)

            # Timeout reached
            error_msg = f"Dashboard failed to start within {startup_timeout} seconds"
            logger.error(error_msg)
            self.stop_dashboard()
            return False, error_msg, 0

        except Exception as e:
            error_msg = f"Failed to start dashboard: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, 0

    def stop_dashboard(self):
        """Stop the dashboard process."""
        if self.dashboard_process:
            try:
                self.dashboard_process.terminate()
                # Give it time to terminate gracefully
                time.sleep(2)
                if self.dashboard_process.poll() is None:
                    # Force kill if still running
                    self.dashboard_process.kill()
                logger.info("Dashboard stopped")
            except Exception as e:
                logger.error(f"Error stopping dashboard: {e}")

    def monitor_dashboard(self):
        """Monitor dashboard health and restart if needed."""
        if not self.auto_restart:
            return

        dashboard_url = f"http://{self.host}:{self.port}"

        while self.dashboard_process and self.dashboard_process.poll() is None:
            time.sleep(30)  # Check every 30 seconds

            # Check if process is still running
            if self.dashboard_process.poll() is not None:
                logger.warning("Dashboard process died, attempting restart...")
                break

            # Check if dashboard is responding
            if not self.is_dashboard_responding(dashboard_url):
                logger.warning("Dashboard not responding, attempting restart...")
                break

            logger.debug("Dashboard health check passed")

        # Attempt restart if enabled and under max restarts
        if self.auto_restart and self.restart_count < self.max_restarts:
            self.restart_count += 1
            logger.info(
    f"Restarting dashboard (attempt {self.restart_count}/{self.max_restarts})",
)

            self.stop_dashboard()
            time.sleep(2)  # Brief pause before restart

            success, message, port = self.start_dashboard()
            if success:
                logger.info("Dashboard restarted successfully")
                # Continue monitoring
                self.monitor_dashboard()
            else:
                logger.error(f"Failed to restart dashboard: {message}")
        else:
            if self.restart_count >= self.max_restarts:
                logger.error(f"Max restart attempts ({self.max_restarts}) reached")

    def run(self, open_browser: bool = True) -> Tuple[bool, str, int]:
        """Run the dashboard with monitoring."""
        try:
            # Start dashboard
            success, message, port = self.start_dashboard()
            if not success:
                return False, message, 0

            # Open browser if requested
            if open_browser:
                try:
                    import webbrowser
                    dashboard_url = f"http://{self.host}:{port}"
                    webbrowser.open(dashboard_url)
                    logger.info(f"Opened browser at {dashboard_url}")
                except Exception as e:
                    logger.warning(f"Failed to open browser: {e}")

            # Start monitoring in background if auto-restart enabled
            if self.auto_restart:
                import threading
                monitor_thread = threading.Thread(target=self.monitor_dashboard, daemon=True)
                monitor_thread.start()
                logger.info("Dashboard monitoring started")

            # Print success message
            dashboard_url = f"http://{self.host}:{port}"
            success_message = f"""
Dashboard Started Successfully!

URL: {dashboard_url}
Port: {port}
Auto-restart: {'Enabled' if self.auto_restart else 'Disabled'}

Commands:
- Press Ctrl+C to stop the dashboard
- The dashboard will auto-restart if it crashes (if enabled)
- Check logs at: .claude/logs/dashboard-launcher.log

API Access:
- Overview: {dashboard_url}/api/overview
- System Health: {dashboard_url}/api/system-health
- Quality Trends: {dashboard_url}/api/quality-trends
"""

            print(success_message)
            logger.info(f"Dashboard running at {dashboard_url}")

            # Keep main thread alive
            try:
                while self.dashboard_process and self.dashboard_process.poll() is None:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, stopping dashboard...")

            return True, message, port

        except KeyboardInterrupt:
            logger.info("Dashboard stopped by user")
            return True, "Dashboard stopped by user", self.port
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, 0
        finally:
            self.stop_dashboard()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Robust Dashboard Launcher')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument(
    '--patterns-dir',
    default='.claude-patterns',
    help='Pattern directory',
)
    parser.add_argument('--no-browser', action='store_true', help='Don\'t open browser')
    parser.add_argument(
    '--no-restart',
    action='store_true',
    help='Disable auto-restart',
)
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    launcher = DashboardLauncher(
        host=args.host,
        port=args.port,
        patterns_dir=args.patterns_dir,
        auto_restart=not args.no_restart
    )

    success, message, port = launcher.run(open_browser=not args.no_browser)

    if not success:
        print(f"ERROR: Failed to start dashboard: {message}")
        sys.exit(1)
    else:
        print(f"SUCCESS: {message}")

if __name__ == '__main__':
    main()
