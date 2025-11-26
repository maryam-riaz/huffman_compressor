import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from ..compression.huffman_decoder import decompress_file


class DecompressPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="File Decompression",
                     font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(self, text="Choose .huff File",
                      command=self.pick_file).pack(pady=10)

        self.file_label = ctk.CTkLabel(self, text="No file selected")
        self.file_label.pack(pady=10)

        ctk.CTkButton(self, text="Decompress",
                      command=self.decompress_file).pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def pick_file(self):
        file = filedialog.askopenfilename(title="Select Huffman File",
                                          filetypes=[("Huffman Files", "*.huff"), ("All files", "*.*")])
        if file:
            self.file_path = file
            self.file_label.configure(text=file)

    def decompress_file(self):
        if not hasattr(self, "file_path"):
            messagebox.showerror("Error", "Please select a file first!")
            return

        default_name = os.path.splitext(os.path.basename(self.file_path))[0] + "_decoded.txt"
        out = filedialog.asksaveasfilename(title="Save decompressed file as",
                                           defaultextension=".txt",
                                           initialfile=default_name,
                                           filetypes=[("Text files", "*.txt"), ("All files","*.*")])
        if not out:
            return

        t = threading.Thread(target=self._do_decompress, args=(self.file_path, out), daemon=True)
        t.start()
        self.status_label.configure(text="Decompressing...")

    def _do_decompress(self, input_path, out_path):
        try:
            success = decompress_file(input_path, out_path)
            if success:
                self.after(0, lambda: self._on_success(out_path))
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Decompression failed"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Decompression failed:\n{e}"))

    def _on_success(self, out_path):
        self.status_label.configure(text=f"Saved: {out_path}")
        messagebox.showinfo("Success", f"File decompressed successfully: {out_path}")
