"""
Cross-platform Infrastructure Health Monitor
Checks CPU, memory, disk, and network reachability.
Works on Windows and Linux. Uses configurable warning thresholds.
"""
import argparse
import json
import logging
import platform
import shutil
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil

LOG_DIR = Path("logs")
REPORT_DIR = Path("reports")
LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "health_monitor.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def check_network(host: str, port: int, timeout: float = 2.0) -> dict:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
        return {"host": host, "port": port, "status": "UP", "latency_ms": latency_ms}
    except OSError as exc:
        return {"host": host, "port": port, "status": "DOWN", "error": str(exc)}

def collect_metrics(disk_path: str, cpu_warn: float, memory_warn: float,
                    disk_warn: float, host: str, port: int) -> dict:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage(disk_path)

    metrics = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "operating_system": f"{platform.system()} {platform.release()}",
        "cpu_percent": cpu,
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024 ** 3), 2),
        "memory_total_gb": round(memory.total / (1024 ** 3), 2),
        "disk_percent": round(disk.used / disk.total * 100, 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "network_check": check_network(host, port),
    }

    alerts = []
    if cpu >= cpu_warn:
        alerts.append(f"High CPU usage: {cpu}% (threshold {cpu_warn}%)")
    if memory.percent >= memory_warn:
        alerts.append(f"High memory usage: {memory.percent}% (threshold {memory_warn}%)")
    disk_percent = metrics["disk_percent"]
    if disk_percent >= disk_warn:
        alerts.append(f"High disk usage: {disk_percent}% (threshold {disk_warn}%)")
    if metrics["network_check"]["status"] == "DOWN":
        alerts.append(f"Network endpoint unavailable: {host}:{port}")

    metrics["status"] = "WARNING" if alerts else "HEALTHY"
    metrics["alerts"] = alerts
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Cross-platform infrastructure health monitor")
    parser.add_argument("--disk", default="C:\\" if platform.system() == "Windows" else "/",
                        help="Disk path to inspect")
    parser.add_argument("--host", default="8.8.8.8", help="Host for TCP reachability check")
    parser.add_argument("--port", type=int, default=53, help="TCP port to test")
    parser.add_argument("--cpu-warn", type=float, default=80)
    parser.add_argument("--memory-warn", type=float, default=85)
    parser.add_argument("--disk-warn", type=float, default=90)
    args = parser.parse_args()

    result = collect_metrics(args.disk, args.cpu_warn, args.memory_warn,
                             args.disk_warn, args.host, args.port)
    report_path = REPORT_DIR / "latest_report.json"
    report_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    logging.info("System status=%s alerts=%s", result["status"], len(result["alerts"]))
    print(json.dumps(result, indent=2))
    print(f"\nReport saved to: {report_path}")
    print(f"Log saved to: {LOG_DIR / 'health_monitor.log'}")

if __name__ == "__main__":
    main()
