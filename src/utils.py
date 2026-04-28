"""
Utility functions for the Network Traffic Visualizer
"""

import logging
import sys
from datetime import datetime


def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration

    Args:
        log_level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"traffic_visualizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def format_bytes(bytes_count):
    """
    Format bytes into human-readable format

    Args:
        bytes_count: Number of bytes

    Returns:
        Formatted string
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} TB"


def format_packet_count(count):
    """
    Format packet count

    Args:
        count: Number of packets

    Returns:
        Formatted string
    """
    if count >= 1_000_000:
        return f"{count / 1_000_000:.2f}M"
    elif count >= 1000:
        return f"{count / 1000:.2f}K"
    return str(count)
