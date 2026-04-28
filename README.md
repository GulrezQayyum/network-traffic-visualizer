# Network Traffic Visualizer

A comprehensive real-time network traffic analysis and visualization tool built with Python. This application captures, analyzes, and visualizes network packets to provide insights into network behavior, protocol distribution, bandwidth usage, and IP communication patterns.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Options](#command-line-options)
- [Output & Visualizations](#output--visualizations)
- [Project Architecture](#project-architecture)
- [Troubleshooting](#troubleshooting)
- [Technologies](#technologies)
- [Contributing](#contributing)

## Features

- 🔍 **Real-time Packet Capture** - Capture network packets with customizable filters and interfaces
- 📊 **Protocol Distribution Analysis** - Visualize the distribution of TCP, UDP, ICMP, and other protocols
- 📈 **Bandwidth Statistics** - Analyze total bytes, average packet size, and traffic patterns
- 🌐 **IP Connection Mapping** - Network graph visualization of connections between IP addresses
- 📉 **Top IPs Analysis** - Identify the most active source and destination IP addresses
- 💾 **Data Export** - Generate multiple visualization formats (PNG, HTML)
- 🎨 **Interactive Visualizations** - Interactive HTML-based network graphs using Plotly
- 🖥️ **Detailed Statistics** - Comprehensive packet-level analysis with protocol breakdown

## Requirements

### System Requirements

- **Linux, macOS, or Windows** with Python 3.8 or higher
- **Administrator/Root privileges** for packet capture (required for network sniffing)
- **Network interface access** to capture packets from

### Python Dependencies

See [requirements.txt](requirements.txt) for the complete list:
- **scapy** (≥2.5.0) - Packet manipulation and capture
- **matplotlib** (≥3.8.0) - Static visualizations
- **plotly** (≥5.18.0) - Interactive visualizations
- **pandas** (≥2.1.0) - Data analysis and manipulation
- **psutil** (≥5.9.0) - System and process utilities
- **numpy** (≥1.26.0) - Numerical computing

## Installation

### Step 1: Clone or Download the Project

```bash
cd /path/to/Networking
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (Requires Root/Admin Privileges)

The application requires elevated privileges to capture network packets. Run with `sudo`:

```bash
# Linux/macOS - Activate venv first
source venv/bin/activate
sudo venv/bin/python main.py
```

**On Windows (Run Command Prompt as Administrator):**
```bash
venv\Scripts\activate
python main.py
```

### Default Behavior

When run without arguments, the program will:
1. Capture 100 packets from the default network interface
2. Apply no protocol filter (captures all packets)
3. Wait up to 10 seconds for packets
4. Display statistical analysis only (no visualizations)

## Command-Line Options

The application supports the following command-line arguments:

```bash
python main.py [OPTIONS]
```

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--interface` | `-i` | string | default | Network interface to capture from (e.g., `eth0`, `en0`) |
| `--count` | `-c` | integer | 100 | Number of packets to capture |
| `--timeout` | `-t` | integer | 10 | Capture timeout in seconds |
| `--filter` | `-f` | string | "" | BPF filter string (e.g., `tcp port 80`, `udp`, `icmp`) |
| `--visualize` | `-v` | flag | false | Generate and save visualization files |
| `--help` | `-h` | flag | - | Show help message |

### Usage Examples

**Capture 500 TCP packets with visualizations:**
```bash
sudo venv/bin/python main.py -c 500 -f "tcp" -v
```

**Capture packets from specific interface (eth0) for 20 seconds:**
```bash
sudo venv/bin/python main.py -i eth0 -t 20 -v
```

**Capture HTTP traffic (port 80) only:**
```bash
sudo venv/bin/python main.py -c 200 -f "tcp port 80" -v
```

**Capture DNS traffic (UDP port 53):**
```bash
sudo venv/bin/python main.py -f "udp port 53" -c 100 -v
```

**Capture ICMP packets (ping):***
```bash
sudo venv/bin/python main.py -f "icmp" -v
```

## BPF Filter Examples

The `--filter` option uses Berkeley Packet Filter syntax:

- `tcp` - All TCP packets
- `udp` - All UDP packets
- `icmp` - All ICMP packets
- `tcp port 80` - TCP traffic on port 80 (HTTP)
- `tcp port 443` - TCP traffic on port 443 (HTTPS)
- `udp port 53` - UDP traffic on port 53 (DNS)
- `src 192.168.1.100` - Packets from specific source IP
- `dst 10.0.0.5` - Packets to specific destination IP
- `tcp and dst port 22` - SSH traffic

## Output & Visualizations

### Console Output

The program displays the following statistics:

```
============================================================
   Network Traffic Visualizer
============================================================

✓ Captured 150 packets

Total bytes: 45.2 KB
Total packets: 150

Protocol Distribution:
  TCP: 95 (63.3%)
  UDP: 32 (21.3%)
  ICMP: 23 (15.3%)

Top 5 Source IPs:
  192.168.1.100: 45 packets
  10.0.0.5: 32 packets
  172.16.0.1: 20 packets
  ...
============================================================
```

### Generated Visualization Files (with `-v` flag)

When the `--visualize` flag is used, the program generates:

1. **protocol_distribution.png** - Pie chart showing protocol breakdown
2. **top_ips.png** - Bar chart of top 10 source IPs
3. **bandwidth_stats.png** - Bandwidth and packet statistics
4. **connections.html** - Interactive network graph (open in browser)

All files are saved in the project root directory.

## Project Architecture

### Directory Structure

```
Networking/
├── src/                           # Source code modules
│   ├── __init__.py               # Package initialization
│   ├── packet_capture.py         # PacketCapture class - handles sniffing
│   ├── data_processor.py         # DataProcessor class - analyzes packets
│   ├── visualizer.py             # TrafficVisualizer class - creates charts
│   └── utils.py                  # Utility functions (logging, formatting)
├── tests/                         # Test files (for future expansion)
│   └── __init__.py
├── data/                          # Data storage directory
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── connections.html               # Generated network graph
├── protocol_distribution.png      # Generated pie chart
├── top_ips.png                   # Generated bar chart
├── bandwidth_stats.png           # Generated statistics chart
└── README.md                      # This file
```

### Module Descriptions

#### `packet_capture.py`
- **Class:** `PacketCapture`
- **Purpose:** Captures network packets using Scapy
- **Key Methods:**
  - `start_capture()` - Begin packet sniffing
  - `get_packets()` - Retrieve captured packets
  - `packet_callback()` - Process each captured packet

#### `data_processor.py`
- **Class:** `DataProcessor`
- **Purpose:** Analyzes captured packet data
- **Key Methods:**
  - `extract_packet_info()` - Extract packet details into a DataFrame
  - `get_bandwidth_stats()` - Calculate total bytes and packet counts
  - `get_protocol_distribution()` - Count packets by protocol type
  - `get_top_ips()` - Identify most active source IPs

#### `visualizer.py`
- **Class:** `TrafficVisualizer`
- **Purpose:** Creates visualizations from analyzed data
- **Key Methods:**
  - `plot_protocol_distribution()` - Generate pie chart
  - `plot_top_ips()` - Generate bar chart of active IPs
  - `plot_bandwidth_stats()` - Generate statistics chart
  - `plot_connections_network()` - Generate interactive network graph

#### `utils.py`
- **Purpose:** Utility functions
- **Key Functions:**
  - `setup_logging()` - Configure logging
  - `format_bytes()` - Human-readable byte formatting

#### `main.py`
- **Purpose:** Application entry point
- **Functionality:**
  - Argument parsing
  - Workflow orchestration
  - Output formatting

## Troubleshooting

### "Operation not permitted" Error

**Problem:** `[Errno 1] Operation not permitted`

**Cause:** Packet capture requires root/administrator privileges.

**Solution:**
- **Linux/macOS:** Run with `sudo`
  ```bash
  sudo venv/bin/python main.py
  ```
- **Windows:** Run Command Prompt as Administrator
  ```cmd
  python main.py
  ```

### "No packets captured" Error

**Cause:** Network timeout or no traffic on the specified interface.

**Solutions:**
1. Increase the timeout value:
   ```bash
   sudo venv/bin/python main.py -t 30
   ```

2. Generate network traffic during capture:
   ```bash
   # In another terminal
   ping 8.8.8.8
   ```

3. Specify the correct network interface:
   ```bash
   sudo venv/bin/python main.py -i eth0
   ```

### ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'scapy'`

**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt
```

### Python Version Issues

**Problem:** Application requires Python 3.8+

**Solution:** Check your Python version
```bash
python3 --version
```

Update to Python 3.8 or higher if needed.

## Technologies

### Core Technologies

- **Python 3.8+** - Programming language
- **Scapy 2.5+** - Packet capture and manipulation library
- **Matplotlib 3.8+** - Static data visualization
- **Plotly 5.18+** - Interactive data visualization
- **Pandas 2.1+** - Data analysis and manipulation
- **NumPy 1.26+** - Numerical computing
- **Psutil 5.9+** - System utilities

### Network Protocols Supported

- TCP (Transmission Control Protocol)
- UDP (User Datagram Protocol)
- ICMP (Internet Control Message Protocol)
- IP (Internet Protocol)

## Use Cases

This tool is useful for:

- **Network Troubleshooting** - Identify traffic patterns and anomalies
- **Security Analysis** - Monitor suspicious network activity
- **Performance Monitoring** - Track bandwidth usage and protocol distribution
- **Educational Purposes** - Learn about network protocols and packet structure
- **Network Optimization** - Identify bandwidth hogs and optimize routing
- **Compliance Monitoring** - Audit network traffic for policy compliance

## Contributing

Contributions are welcome! You can:

1. Report bugs and issues
2. Suggest features and improvements
3. Submit pull requests with enhancements
4. Improve documentation

### Areas for Enhancement

- [ ] Add support for more protocols (DNS, HTTP, SSL/TLS analysis)
- [ ] Implement real-time streaming dashboard
- [ ] Add packet replay functionality
- [ ] Include geographic IP mapping
- [ ] Support for remote packet capture
- [ ] Advanced filtering UI
- [ ] Packet export formats (PCAP, CSV)
- [ ] Unit and integration tests

## Notes

- **Packet Capture Privileges:** Network packet sniffing requires elevated privileges on all operating systems for security reasons
- **Performance:** Large packet captures (>10,000 packets) may take longer to visualize
- **Linux Permissions:** On Linux, you can alternatively grant capabilities to Python:
  ```bash
  sudo setcap cap_net_raw=ep venv/bin/python
  ```

## License

[Add license information if applicable]

---

**Last Updated:** April 2026
**Python Version:** 3.8+
**Status:** Active Development
- **Matplotlib/Plotly** - Visualization
- **Pandas** - Data manipulation
- **Psutil** - System metrics

## Requirements

- Root/Administrator privileges (for packet capture)
- Linux, macOS, or Windows

## License

MIT
