import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Welcome to Huffman Compression Tool",
                     font=("Arial", 24, "bold")).pack(pady=40)

        ctk.CTkLabel(self, text="Compress and decompress files using Huffman Coding.\n"
                                "Use the sidebar to get started.",
                     font=("Arial", 16)).pack(pady=10)
