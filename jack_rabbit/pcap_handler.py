import networkx as nx
from scapy.all import rdpcap, IP

class PCAPHandler:
    @staticmethod
    def load_pcap(file_path):
        try:
            return rdpcap(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read PCAP file: {e}")

    @staticmethod
    def extract_edges(pcap):
        G = nx.DiGraph()
        for packet in pcap:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                G.add_edge(src_ip, dst_ip)
        return G

    @staticmethod
    def relabel_nodes(G):
        mapping = {node: i for i, node in enumerate(G.nodes())}
        return nx.relabel_nodes(G, mapping)

    @staticmethod
    def calculate_positions(G):
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        return {mapping[node]: pos[node] for node, mapping in zip(G.nodes(), PCAPHandler.relabel_nodes(G).nodes())}