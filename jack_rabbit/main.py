from pcap_analyzer_gui import PCAPAnalyzerGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.update_idletasks() 
    app = PCAPAnalyzerGUI(root)
    root.mainloop()