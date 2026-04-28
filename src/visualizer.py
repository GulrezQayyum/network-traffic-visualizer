"""
Module for visualizing network traffic data
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrafficVisualizer:
    """Create visualizations for network traffic data"""

    def __init__(self, data_processor):
        """
        Initialize visualizer

        Args:
            data_processor: DataProcessor object with analyzed data
        """
        self.processor = data_processor

    def plot_protocol_distribution(self, save_path=None):
        """
        Create pie chart of protocol distribution

        Args:
            save_path: Optional path to save the figure
        """
        protocols = self.processor.get_protocol_distribution()

        if not protocols:
            logger.warning("No protocol data available")
            return

        labels = list(protocols.keys())
        values = list(protocols.values())

        fig, ax = plt.subplots(figsize=(10, 7))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Protocol Distribution")

        if save_path:
            plt.savefig(save_path)
            logger.info(f"Protocol distribution chart saved to {save_path}")
        else:
            plt.show()

    def plot_top_ips(self, top_n=10, save_path=None):
        """
        Create bar chart of top source IPs

        Args:
            top_n: Number of top IPs to display
            save_path: Optional path to save the figure
        """
        top_ips = self.processor.get_top_ips(top_n)

        if not top_ips:
            logger.warning("No IP data available")
            return

        ips, counts = zip(*top_ips)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(ips, counts)
        ax.set_xlabel("Packet Count")
        ax.set_title(f"Top {top_n} Source IPs")
        ax.invert_yaxis()

        if save_path:
            plt.savefig(save_path)
            logger.info(f"Top IPs chart saved to {save_path}")
        else:
            plt.show()

    def plot_bandwidth_stats(self, save_path=None):
        """
        Create visualization of bandwidth statistics

        Args:
            save_path: Optional path to save the figure
        """
        stats = self.processor.get_bandwidth_stats()

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(["Total Bytes", "Packet Count"], [stats["total_bytes"], stats["packet_count"]])
        ax.set_ylabel("Count")
        ax.set_title("Bandwidth Statistics")

        if save_path:
            plt.savefig(save_path)
            logger.info(f"Bandwidth statistics chart saved to {save_path}")
        else:
            plt.show()

    def plot_connections_network(self, top_n=20, save_path=None):
        """
        Create network graph of IP connections using Plotly

        Args:
            top_n: Number of top connections to display
            save_path: Optional path to save the figure
        """
        connections = self.processor.get_connection_pairs()[:top_n]

        if not connections:
            logger.warning("No connection data available")
            return

        sources = [conn[0] for conn in connections]
        targets = [conn[1] for conn in connections]
        values = [conn[2] for conn in connections]

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=list(set(sources + targets)),
                    ),
                    link=dict(
                        source=[list(set(sources + targets)).index(s) for s in sources],
                        target=[list(set(sources + targets)).index(t) for t in targets],
                        value=values,
                    ),
                )
            ]
        )

        fig.update_layout(title="IP Connection Flow", font=dict(size=10))

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Connection network chart saved to {save_path}")
        else:
            fig.show()
