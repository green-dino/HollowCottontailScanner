import tkinter as tk
from tkinter import filedialog, messagebox
from pcap_handler import PCAPHandler
from network_visualizer import NetworkVisualizer
from bokeh.io import output_file, show

class PCAPAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("PCAP Network Map Generator")
        master.geometry("800x800")

        self.open_button = tk.Button(master, text="Open PCAP", command=self.open_pcap)
        self.open_button.pack(pady=20)

        self.generate_button = tk.Button(master, text="Generate Network Map", command=self.generate_map, state=tk.DISABLED)
        self.generate_button.pack(pady=20)
        
        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(pady=20)

    def open_pcap(self):
        try:
            self.pcap_path = filedialog.askopenfilename(
                title="Select PCAP File",
                filetypes=[("PCAP Files", "*.pcap"), ("PCAPNG Files", "*.pcapng")]
            )
            if self.pcap_path:
                self.generate_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file dialog: {e}")

    def generate_map(self):
        try:
            pcap = PCAPHandler.load_pcap(self.pcap_path)
            G = PCAPHandler.extract_edges(pcap)
            G_relabeled = PCAPHandler.relabel_nodes(G)
            pos = PCAPHandler.calculate_positions(G_relabeled)
            
            plot = NetworkVisualizer.visualize_graph(G_relabeled, pos)
            
            output_file("network.html")
            show(plot)
            
            self.save_button = tk.Button(self.master, text="Save Network Map", command=lambda: self.save_map(plot))
            self.save_button.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate network map: {e}")

    def save_map(self, plot):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if file_path:
            try:
                output_file(file_path)
                show(plot)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save network map: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.update_idletasks()
    app = PCAPAnalyzerGUI(root)
    root.mainloop()