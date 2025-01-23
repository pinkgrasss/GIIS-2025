import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import random
import tkinter as tk

def add_noise(image, noise_level):
    noisy_image = np.array(image)
    num_pixels = noisy_image.size
    num_noisy_pixels = int(noise_level * num_pixels)

    changed_pixels = set()
    while len(changed_pixels) < num_noisy_pixels:
        x = random.randint(0, noisy_image.shape[0] - 1)
        y = random.randint(0, noisy_image.shape[1] - 1)
        if (x, y) not in changed_pixels:
            changed_pixels.add((x, y))
            noisy_image[x, y] = 255 if random.random() > 0.5 else 0

    return Image.fromarray(noisy_image)

def threshold_filter(image, threshold):
    image_array = np.array(image)
    filtered_array = image_array.copy()

    rows, cols = image_array.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            window = image_array[i - 1:i + 2, j - 1:j + 2].flatten()
            median = np.median(window)
            if abs(image_array[i, j] - median) > threshold:
                filtered_array[i, j] = median

    return Image.fromarray(filtered_array)

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixFilter")

        self.image = None
        self.noisy_image = None
        self.filtered_image = None

        self.load_button = ttk.Button(root, text="Upload image", command=self.load_image, width=30, style="TButton")
        self.load_button.pack(pady=10, padx=20, fill=X)

        noise_frame = ttk.Frame(root)
        noise_frame.pack(fill=X, pady=5, padx=10)

        self.noise_label = ttk.Label(noise_frame, text="Noise level:      ", font=("Helvetica", 12))
        self.noise_label.pack(side=LEFT, padx=5)

        self.noise_slider = ttk.Scale(noise_frame, from_=0, to=100, orient=HORIZONTAL, value=0, bootstyle="info",
                                      command=self.update_noise_value, length=350)
        self.noise_slider.pack(side=LEFT, padx=5)

        self.noise_value_label = ttk.Label(noise_frame, text="0%", font=("Helvetica", 12))
        self.noise_value_label.pack(side=LEFT, padx=5)

        threshold_frame = ttk.Frame(root)
        threshold_frame.pack(fill=X, pady=5, padx=10)

        self.threshold_label = ttk.Label(threshold_frame, text="Threshold filter:", font=("Helvetica", 12))
        self.threshold_label.pack(side=LEFT, padx=5)

        self.threshold_slider = ttk.Scale(threshold_frame, from_=0, to=255, orient=HORIZONTAL, value=0,
                                          bootstyle="warning", command=self.update_threshold_value, length=350)
        self.threshold_slider.pack(side=LEFT, padx=5)

        self.threshold_value_label = ttk.Label(threshold_frame, text="0", font=("Helvetica", 12))
        self.threshold_value_label.pack(side=LEFT, padx=5)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10, padx=10, fill=X)

        self.add_noise_button = ttk.Button(button_frame, text="Add noise", command=self.apply_noise, style="TButton")
        self.add_noise_button.pack(side=LEFT, padx=10, fill=X, expand=True)

        self.filter_button = ttk.Button(button_frame, text="Apply filter", command=self.apply_filter, style="TButton")
        self.filter_button.pack(side=LEFT, padx=10, fill=X, expand=True)

        self.save_button = ttk.Button(button_frame, text="Save result", command=self.save_image, style="TButton")
        self.save_button.pack(side=LEFT, padx=10, fill=X, expand=True)

        self.image_label = ttk.Label(root)
        self.image_label.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=(10, 10))

        style = ttk.Style()
        style.configure("TButton",
                        background="#D3D3D3",
                        foreground="black",
                        borderwidth=2,
                        relief="solid",
                        bordercolor="#2F4F4F",
                        focusthickness=3,
                        focuscolor="none")

        style.map("TButton", background=[("active", "#A9A9A9")])

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path).convert("L")
            self.display_image(self.image)

    def apply_noise(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение")
            return
        noise_level = self.noise_slider.get() / 100
        self.noisy_image = add_noise(self.image, noise_level)
        self.display_image(self.noisy_image)

    def apply_filter(self):
        if self.noisy_image is None:
            messagebox.showerror("Ошибка", "Сначала добавьте шум к изображению")
            return
        threshold = self.threshold_slider.get()
        self.filtered_image = threshold_filter(self.noisy_image, threshold)
        self.display_image(self.filtered_image)

    def save_image(self):
        if self.filtered_image is None:
            messagebox.showerror("Ошибка", "Нет отфильтрованного изображения для сохранения")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.filtered_image.save(file_path)

    def display_image(self, img):
        img_resized = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def update_noise_value(self, value):
        int_value = int(round(float(value)))
        self.noise_value_label.config(text=f"{int_value}%")

    def update_threshold_value(self, value):
        self.threshold_value_label.config(text=f"{int(float(value))}")

if __name__ == "__main__":
        app = ttk.Window()
        app.title("PixFilter")

        icon_image = ImageTk.PhotoImage(file="../images/logo.jpg")
        app.iconphoto(False, icon_image)

        app_width = 600
        app_height = 600

        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)

        app.geometry(f"{app_width}x{app_height}+{x}+{y}")

        app.configure(background="#D3D3D3")

        style = ttk.Style()
        style.configure("TScale",
                        background="#D3D3D3",
                        troughcolor="#D3D3D3",
                        sliderlength=110,
                        sliderrelief="solid",
                        lightcolor="#D3D3D3",
                        darkcolor="#D3D3D3")

style.configure("TLabel",
                    background="#D3D3D3",
                    foreground="black",
                    font=("Arial", 10))

style.configure("TButton",
                    background="#B0B0B0",
                    foreground="black",
                    borderwidth=2,
                    relief="solid",
                    bordercolor="#2F4F4F",
                    focusthickness=3,
                    focuscolor="none")

style.configure("TFrame",
                    background="#D3D3D3")

ImageFilterApp(app)
app.mainloop()