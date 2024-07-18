import keyboard
import time
import tkinter as tk
from PIL import Image, ImageTk

def load_key_bindings():
    key_bindings = {}
    with open('bind.txt', 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(', ')
                if len(parts) == 3:
                    key, sequence, photo = parts
                    key_bindings[key] = {'sequence': sequence, 'photo': photo}
                else:
                    print(f"Warning: Skipping invalid line in bind.txt: {line}")
    return key_bindings

key_bindings = load_key_bindings()

def simulate_key_presses(sequence):
    for key in sequence:
        keyboard.press_and_release(key)
        time.sleep(0.05)

root = tk.Tk()
root.title("Key Binder Invoker")

root.attributes('-alpha', 0.8)

root.attributes('-topmost', True)

root.overrideredirect(True)

win_x = 0
win_y = 0
start_x = 0
start_y = 0
moving = False

def start_move(event):
    global moving, start_x, start_y
    moving = True
    start_x = event.x
    start_y = event.y

def move_window(event):
    global win_x, win_y
    if moving:
        deltax = event.x - start_x
        deltay = event.y - start_y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

def stop_move(event):
    global moving
    moving = False

root.bind('<ButtonPress-1>', start_move)
root.bind('<B1-Motion>', move_window)
root.bind('<ButtonRelease-1>', stop_move)

left_frame = tk.Frame(root, bg='white')
left_frame.grid(row=0, column=0, sticky='n', padx=10, pady=10)

right_frame = tk.Frame(root, bg='white')
right_frame.grid(row=0, column=1, sticky='n', padx=10, pady=10)

image_labels = []
for i, (key, value) in enumerate(key_bindings.items()):
    if i < 5:
        image_path = f"{value['photo']}.webp"
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(left_frame, image=photo)
        label.photo = photo
        label.pack()

        key_label = tk.Label(left_frame, text=f"{key}", bg='white')
        key_label.pack()

        image_labels.append((label, key_label))
    else:
        image_path = f"{value['photo']}.webp"
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(right_frame, image=photo)
        label.photo = photo
        label.pack()

        key_label = tk.Label(right_frame, text=f"{key}", bg='white')
        key_label.pack()

        image_labels.append((label, key_label))

def on_esc(event):
    root.destroy()

root.bind('<Escape>', on_esc)

for key, value in key_bindings.items():
    sequence = value['sequence']
    keyboard.add_hotkey(key, simulate_key_presses, args=(sequence,))

print("Binder is running. Press ESC to stop.")
root.mainloop()
