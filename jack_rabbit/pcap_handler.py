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
                try:
                    src_ip = str(packet[IP].src)
                    dst_ip = str(packet[IP].dst)
                    
                    # Initialize node attributes if they don't exist
                    if src_ip not in G:
                        G.add_node(src_ip, ip=src_ip, packet_count=0)
                    if dst_ip not in G:
                        G.add_node(dst_ip, ip=dst_ip, packet_count=0)
                    
                    # Create edge if it doesn't exist
                    if not G.has_edge(src_ip, dst_ip):
                        G.add_edge(src_ip, dst_ip, packet_count=0)
                    
                    # Increment counts
                    G[src_ip][dst_ip]['packet_count'] += 1
                    G.nodes[src_ip]['packet_count'] += 1
                    G.nodes[dst_ip]['packet_count'] += 1
                    
                except Exception as e:
                    logging.error(f"Error processing packet: {e}")
        
        return G

    @staticmethod
    def relabel_nodes(G):
        """Relabel nodes in the graph with integer labels and store original IP addresses."""
        mapping = {node: i for i, node in enumerate(G.nodes())}
        G_relabeled = nx.relabel_nodes(G, mapping)
        for new_node, original_node in mapping.items():
            G_relabeled.nodes[new_node]['ip'] = original_node
        return G_relabeled

    @staticmethod
    def calculate_positions(G):
        """Calculate positions for the nodes in the graph."""
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        
        # Log positions for debugging
        for node, position in pos.items():
            logging.info(f"Node {node} position: {position}")
        
        # Ensure all nodes have positions
        for node in G.nodes():
            if node not in pos:
                logging.warning(f"Node {node} does not have a position. Assigning random position.")
                pos[node] = (np.random.uniform(-1, 1), np.random.uniform(-1, 1))
        
        return pos

    @staticmethod
    def validate_graph(G):
        """Validate the graph to ensure all nodes have consistent data structures."""
        for node in G.nodes():
            if 'ip' not in G.nodes[node] or 'packet_count' not in G.nodes[node]:
                raise ValueError(f"Node {node} does not have required attributes 'ip' and 'packet_count'.")
        logging.info(f"Total number of nodes in the graph: {len(G.nodes())}")

    @staticmethod
    def plot_graph(G, pos):
        """Plot the graph using matplotlib."""
        try:
            plt.figure(figsize=(12, 8))
            nx.draw_networkx(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray", arrows=True, arrowstyle='-|>', arrowsize=20)
            plt.title("Network Graph from PCAP")
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            logging.error(f"Failed to plot graph: {e}")
            raise