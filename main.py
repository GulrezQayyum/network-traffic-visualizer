"""
Network Traffic Visualizer - Main entry point
"""

import argparse
import sys
from src.packet_capture import PacketCapture
from src.data_processor import DataProcessor
from src.visualizer import TrafficVisualizer
from src.utils import setup_logging, format_bytes


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Network Traffic Visualizer")
    parser.add_argument(
        "-i",
        "--interface",
        help="Network interface to capture from",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="Number of packets to capture",
        default=100,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="Capture timeout in seconds",
        default=10,
    )
    parser.add_argument(
        "-f",
        "--filter",
        help="BPF filter string",
        default="",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Display visualizations",
    )

    args = parser.parse_args()

    setup_logging()

    print("=" * 60)
    print("   Network Traffic Visualizer")
    print("=" * 60)
    print(f"\nCapturing {args.count} packets...")
    print(f"Interface: {args.interface or 'default'}")
    print(f"Filter: {args.filter or 'none'}")
    print(f"Timeout: {args.timeout}s\n")

    # Capture packets
    capturer = PacketCapture(interface=args.interface, packet_count=args.count)
    capturer.start_capture(filter_str=args.filter, timeout=args.timeout)

    packets = capturer.get_packets()
    if not packets:
        print("No packets captured. Exiting.")
        sys.exit(1)

    print(f"\n✓ Captured {len(packets)} packets\n")

    # Process data
    processor = DataProcessor(packets)

    # Display statistics
    bandwidth_stats = processor.get_bandwidth_stats()
    print(f"Total bytes: {format_bytes(bandwidth_stats['total_bytes'])}")
    print(f"Total packets: {bandwidth_stats['packet_count']}")

    protocol_dist = processor.get_protocol_distribution()
    print(f"\nProtocol Distribution:")
    for protocol, count in protocol_dist.items():
        print(f"  {protocol}: {count} ({100 * count / len(packets):.1f}%)")

    print(f"\nTop 5 Source IPs:")
    for ip, count in processor.get_top_ips(5):
        print(f"  {ip}: {count} packets")

    # Create visualizations if requested
    if args.visualize:
        print("\nGenerating visualizations...")
        visualizer = TrafficVisualizer(processor)
        visualizer.plot_protocol_distribution("protocol_distribution.png")
        visualizer.plot_top_ips(10, "top_ips.png")
        visualizer.plot_bandwidth_stats("bandwidth_stats.png")
        visualizer.plot_connections_network(20, "connections.html")
        print("✓ Visualizations saved")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
