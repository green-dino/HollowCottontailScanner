import networkx as nx
from scapy.all import rdpcap, IP
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class PCAPHandler:
    @staticmethod
    def load_pcap(file_path):
        """Load a PCAP file and return the packets."""
        try:
            return rdpcap(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read PCAP file: {e}")

    @staticmethod
    def extract_edges(pcap):
        """Extract edges from the PCAP file and create a directed graph with attributes."""
        G = nx.DiGraph()
        for packet in pcap:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                if G.has_edge(src_ip, dst_ip):
                    G[src_ip][dst_ip]['packet_count'] += 1
                else:
                    G.add_edge(src_ip, dst_ip, packet_count=1)
                if 'packet_count' in G.nodes[src_ip]:
                    G.nodes[src_ip]['packet_count'] += 1
                else:
                    G.nodes[src_ip]['packet_count'] = 1
                if 'packet_count' in G.nodes[dst_ip]:
                    G.nodes[dst_ip]['packet_count'] += 1
                else:
                    G.nodes[dst_ip]['packet_count'] = 1
        return G

    @staticmethod
    def relabel_nodes(G):
        """Relabel nodes in the graph with integer labels and store original IP addresses."""
        mapping = {node: i for i, node in enumerate(G.nodes())}
        G_relabeled = nx.relabel_nodes(G, mapping)
        for node, original_node in mapping.items():
            G_relabeled.nodes[node]['ip'] = original_node
        return G_relabeled

    @staticmethod
    def calculate_positions(G):
        """Calculate positions for the nodes in the graph."""
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        return PCAPHandler._validate_and_convert_positions(pos)

    @staticmethod
    def _validate_and_convert_positions(pos):
        """Validate and convert positions to ensure they are tuples of length 2."""
        if not isinstance(pos, dict):
            raise TypeError("Position data is not a dictionary.")

        for node, position in pos.items():
            pos[node] = PCAPHandler._convert_position(position, node)

        return pos

    @staticmethod
    def _convert_position(position, node):
        """Convert position to a tuple of length 2."""
        if isinstance(position, (list, tuple)) and len(position) == 2:
            return tuple(position)
        elif isinstance(position, np.ndarray) and position.shape == (2,):
            return tuple(position)
        else:
            raise ValueError(f"Position for node {node} is not a valid tuple of length 2: {position}")

    @staticmethod
    def validate_graph(G):
        """Validate the graph to ensure all nodes have consistent data structures."""
        for node in G.nodes():
            if 'ip' not in G.nodes[node] or 'packet_count' not in G.nodes[node]:
                raise ValueError(f"Node {node} does not have required attributes 'ip' and 'packet_count'.")

        logging.info(f"Total number of nodes in the graph: {len(G.nodes())}")

# Example usage
if __name__ == "__main__":
    file_path = "example.pcap"
    try:
        pcap = PCAPHandler.load_pcap(file_path)
        G = PCAPHandler.extract_edges(pcap)
        PCAPHandler.validate_graph(G)
        G_relabeled = PCAPHandler.relabel_nodes(G)
        pos = PCAPHandler.calculate_positions(G_relabeled)
        logging.info("Graph and positions successfully calculated.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")