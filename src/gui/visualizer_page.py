import customtkinter as ctk
from PIL import Image
import os
import webbrowser


class VisualizerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ctk.CTkLabel(
            self,
            text="Huffman Tree Visualization",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        # Info label
        self.image_label = ctk.CTkLabel(
            self,
            text="No tree visualized yet.",
            font=("Arial", 14)
        )
        self.image_label.pack(pady=5)

        # Scrollable frame to hold the image
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, width=950, height=520
        )
        self.scroll_frame.pack(pady=10, fill="both", expand=True)

        self.img_widget = None
        self.current_img_path = None

        # Button to open external viewer
        self.open_button = ctk.CTkButton(
            self,
            text="Open Image in Viewer",
            command=self.open_image,
            state="disabled"
        )
        self.open_button.pack(pady=10)

    # -------------------------------------------------------
    # LOAD IMAGE FROM COMPRESS PAGE
    # -------------------------------------------------------
    def load_image(self, image_path):
        if not image_path or not os.path.exists(image_path):
            self.image_label.configure(text="Image not found.")
            self.open_button.configure(state="disabled")
            return

        self.current_img_path = image_path
        self.image_label.configure(text=os.path.basename(image_path))

        # Load image using PIL
        img = Image.open(image_path)

        # Resize to fit scroll area width but keep aspect ratio
        max_w = 900
        ratio = max_w / img.width
        new_h = int(img.height * ratio)
        img = img.resize((max_w, new_h))

        # Convert to CTkImage
        ctk_img = ctk.CTkImage(img, size=(max_w, new_h))

        # If widget exists, update it — else create it
        if self.img_widget:
            self.img_widget.configure(image=ctk_img)
            self.img_widget.image = ctk_img
        else:
            self.img_widget = ctk.CTkLabel(
                self.scroll_frame,
                text="",
                image=ctk_img
            )
            self.img_widget.image = ctk_img
            self.img_widget.pack(pady=5)

        self.open_button.configure(state="normal")

    # -------------------------------------------------------
    # OPEN IMAGE IN DEFAULT WINDOWS VIEWER
    # -------------------------------------------------------
    def open_image(self):
        if self.current_img_path and os.path.exists(self.current_img_path):
            webbrowser.open(self.current_img_path)
