import customtkinter as ctk
from src.gui.home_page import HomePage
from src.gui.compress_page import CompressPage
from src.gui.decompress_page import DecompressPage
from src.gui.visualizer_page import VisualizerPage



class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Huffman Compression Tool")
        self.geometry("1100x650")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)

        ctk.CTkLabel(self.sidebar, text="Huffman Compressor",
                     font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(self.sidebar, text="Home", command=lambda: self.show_frame("home")).pack(pady=10, fill='x')
        ctk.CTkButton(self.sidebar, text="Compress", command=lambda: self.show_frame("compress")).pack(pady=10, fill='x')
        ctk.CTkButton(self.sidebar, text="Decompress", command=lambda: self.show_frame("decompress")).pack(pady=10, fill='x')
        ctk.CTkButton(self.sidebar, text="Visualization", command=lambda: self.show_frame("visualizer")).pack(pady=10, fill='x')

        # Container for main pages
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frames = {}
        self.init_pages()

        self.show_frame("home")

    def init_pages(self):
        pages = {
            "home": HomePage,
            "compress": CompressPage,
            "decompress": DecompressPage,
            "visualizer": VisualizerPage
        }

        for name, PageClass in pages.items():
            frame = PageClass(self.container)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
