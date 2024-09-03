import tkinter as tk
from tkinter import filedialog, messagebox
from pcap_handler import PCAPHandler
from network_visualizer import NetworkVisualizer
from bokeh.io import output_file, show
import logging

class PCAPAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("PCAP Network Map Generator")
        self.master.geometry("800x800")

        self.pcap_path = None
        self.create_widgets()

    def create_widgets(self):
        self.open_button = tk.Button(self.master, text="Open PCAP", command=self.open_pcap)
        self.open_button.pack(pady=20)

        self.generate_button = tk.Button(self.master, text="Generate Network Map", command=self.generate_map, state=tk.DISABLED)
        self.generate_button.pack(pady=20)
        
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack(pady=20)

    def open_pcap(self):
        self.pcap_path = filedialog.askopenfilename(
            title="Select PCAP File",
            filetypes=[("PCAP Files", "*.pcap"), ("PCAPNG Files", "*.pcapng")]
        )
        if self.pcap_path:
            self.generate_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Warning", "No file selected.")

    def generate_map(self):
        if not self.pcap_path:
            messagebox.showwarning("Warning", "Please open a PCAP file first.")
            return

        try:
            pcap = PCAPHandler.load_pcap(self.pcap_path)
            G = PCAPHandler.extract_edges(pcap)
            PCAPHandler.validate_graph(G)  # Validation step before relabeling
            G_relabeled = PCAPHandler.relabel_nodes(G)
            pos = PCAPHandler.calculate_positions(G_relabeled)

            self.validate_positions(pos)

            plot = NetworkVisualizer.visualize_graph(G_relabeled, pos)
            output_file("network.html")
            show(plot)
            self.create_save_button(plot)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate network map: {e}")
            logging.error(f"Failed to generate network map: {e}")

    def validate_positions(self, pos):
        if not isinstance(pos, dict):
            raise TypeError("Position data is not a dictionary.")
        
        for node, position in pos.items():
            if not isinstance(position, tuple) or len(position) != 2:
                raise ValueError(f"Position for node {node} is not a valid tuple of length 2: {position}")

    def create_save_button(self, plot):
        self.save_button = tk.Button(self.master, text="Save Network Map", command=lambda: self.save_map(plot))
        self.save_button.pack(pady=20)

    def save_map(self, plot):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if file_path:
            try:
                output_file(file_path)
                show(plot)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save network map: {e}")
        else:
            messagebox.showwarning("Warning", "No save location selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCAPAnalyzerGUI(root)
    root.mainloop()