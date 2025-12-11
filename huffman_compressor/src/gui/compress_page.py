import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

from src.compression.huffman_encoder import compress_file
from src.visualization.tree_visualizer import visualize_tree


class CompressPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="File Compression",
                     font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(self, text="Choose File to Compress",
                      command=self.pick_file).pack(pady=10)

        self.file_label = ctk.CTkLabel(self, text="No file selected")
        self.file_label.pack(pady=10)

        ctk.CTkButton(self, text="Compress Now",
                      command=self.compress_file).pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)

        self.visualize_button = ctk.CTkButton(
            self,
            text="Show Tree (in Visualizer)",
            command=self.open_visualizer,
            state="disabled"
        )
        self.visualize_button.pack(pady=10)

        self.last_tree_path = None
        self.file_path = None

    # ---------------- FILE PICKER ----------------
    def pick_file(self):
        file = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[
                ("Text files", "*.txt;*.md;*.py;*.cpp;*.csv"),
                ("All files", "*.*")
            ]
        )
        if file:
            self.file_path = file
            self.file_label.configure(text=file)

    # ---------------- COMPRESS START ----------------
    def compress_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return

        default_name = os.path.splitext(os.path.basename(self.file_path))[0] + ".huff"

        out = filedialog.asksaveasfilename(
            title="Save compressed file as",
            defaultextension=".huff",
            initialfile=default_name,
            filetypes=[("Huffman files", "*.huff")]
        )
        if not out:
            return

        # Threading for responsiveness
        t = threading.Thread(target=self._do_compress, args=(self.file_path, out), daemon=True)
        t.start()
        self.status_label.configure(text="Compressing...")

    # ---------------- COMPRESS WORKER ----------------
    def _do_compress(self, input_path, out_path):
        try:
            stats, root = compress_file(input_path, out_path)

            # Correct path for tree image
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            img_dir = os.path.join(project_root, "assets", "images")
            os.makedirs(img_dir, exist_ok=True)

            tree_img_path = os.path.join(
                img_dir,
                os.path.splitext(os.path.basename(out_path))[0] + "_tree.png"
            )

            visualize_tree(root, tree_img_path)

            self.last_tree_path = tree_img_path

            self.after(0, lambda: self._on_success(stats, out_path))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Compression failed:\n{e}"))

    # ---------------- SUCCESS CALLBACK ----------------
    def _on_success(self, stats, out_path):
        self.status_label.configure(text=f"Saved: {out_path}")
        self.result_label.configure(
            text=f"Original: {stats['original_size']} bytes  •  "
                 f"Compressed: {stats['compressed_size']} bytes  •  "
                 f"Ratio: {stats['compression_ratio']}"
        )

        self.visualize_button.configure(state="normal")
        messagebox.showinfo("Success", f"File compressed successfully: {out_path}")

    # ---------------- OPEN VISUALIZER ----------------
    def open_visualizer(self):
        if not self.last_tree_path:
            messagebox.showerror("Error", "No tree image found!")
            return

        parent_app = self.master.master  # MainApp
        parent_app.show_frame("visualizer")

        viz_page = parent_app.frames.get("visualizer")
        if viz_page:
            viz_page.load_image(self.last_tree_path)
