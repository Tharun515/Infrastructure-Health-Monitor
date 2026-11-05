# Cross-Platform Infrastructure Health Monitor

A lightweight Python automation project that checks core workstation/server health signals and creates a timestamped JSON report. It is designed as a practical demonstration of infrastructure monitoring, troubleshooting, network checks, logging, and repeatable operational automation.

## What it checks

- **CPU utilization** — flags usage at or above a configurable threshold.
- **Memory utilization** — reports used/total memory and flags high usage.
- **Disk capacity** — reports used/total disk space and flags low-capacity conditions.
- **Network reachability** — tests a TCP connection to a configurable host and port.
- **Operational records** — writes a persistent log and a machine-readable JSON report.

## Technology

Python 3, `psutil`, operating-system utilities, TCP sockets, JSON, and Python logging.

## Run locally

### 1. Clone or download the repository

```bash
git clone <your-github-repository-url>
cd Infrastructure-health-monitor
```

### 2. Create a virtual environment (recommended)

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies and run

```bash
pip install -r requirements.txt
python monitor.py
```

The script creates `logs/health_monitor.log` and `reports/latest_report.json`.

## Customize checks

```bash
python monitor.py --host example.com --port 443 --cpu-warn 75 --memory-warn 80 --disk-warn 85
```

On Linux, you can select a mounted disk path:
```bash
python monitor.py --disk /
```

On Windows, the default disk path is `C:\`.

## Example output (illustrative)

```json
{
  "hostname": "sample-host",
  "operating_system": "Windows 11",
  "cpu_percent": 18.4,
  "memory_percent": 62.1,
  "disk_percent": 71.8,
  "network_check": {
    "host": "example.com",
    "port": 443,
    "status": "UP",
    "latency_ms": 24.6
  },
  "status": "HEALTHY",
  "alerts": []
}
```

Values above are sample data, not a result from your machine.

## Operational considerations

- Thresholds are configurable to suit different workloads.
- A failed TCP check can indicate a network issue, unavailable service, firewall rule, or incorrect host/port; it does not by itself identify the root cause.
- Run with suitable permissions when monitoring protected disks or system resources.
- For production use, add centralized metrics, alert delivery, secure configuration, service-specific checks, and retention controls.

## Possible next enhancements

1. Schedule recurring checks with Windows Task Scheduler or Linux cron.
2. Export metrics to a dashboard.
3. Add AWS EC2 status and CloudWatch metrics using appropriately scoped AWS credentials.
4. Add unit tests and a CI workflow.

## Scope and limitations

This is a local monitoring and automation demonstration. It does not connect to AWS, manage enterprise infrastructure, or automatically remediate incidents. Those integrations can be added as a separate, tested enhancement.
