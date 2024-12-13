import tkinter as tk
from tkinter import messagebox
import colorsys
from logic import generate_random_color, check_guess, draw_hue_wheel, draw_combined_square, draw_marker, draw_combined_marker

'''
References
https://docs.python.org/3/library/colorsys.html
https://docs.python.org/3/library/tkinter.html
https://tkdocs.com
'''



# Initialize global variables
random_color = generate_random_color()
bg_hue, bg_saturation, bg_value = None, None, None

# Create the main Tkinter window
window = tk.Tk()
window.title("Guess the Hex Color")
window.geometry("800x600")

def reset_game():
    global random_color, bg_hue, bg_saturation, bg_value
    random_color = generate_random_color()
    window.config(bg=random_color)
    r_bg = int(random_color[1:3], 16)
    g_bg = int(random_color[3:5], 16)
    b_bg = int(random_color[5:7], 16)
    bg_hue, bg_saturation, bg_value = colorsys.rgb_to_hsv(r_bg / 255, g_bg / 255, b_bg / 255)
    guesses_list.delete(0, tk.END)
    hue_canvas.delete("all")
    combined_canvas.delete("all")
    draw_hue_wheel(hue_canvas)
    draw_marker(hue_canvas, bg_hue, "red")
    draw_combined_square(combined_canvas, bg_hue)
    draw_combined_marker(combined_canvas, bg_saturation, bg_value, "red")
    recent_guess_display.config(bg="white")
    instruction_label.config(bg=random_color)

def submit_guess():
    check_guess(
        random_color=random_color,
        color_input=color_input,
        recent_guess_display=recent_guess_display,
        guesses_list=guesses_list,
        hue_canvas=hue_canvas,
        combined_canvas=combined_canvas,
        reset_game=reset_game
    )

# Parse initial random color values
r_bg = int(random_color[1:3], 16)
g_bg = int(random_color[3:5], 16)
b_bg = int(random_color[5:7], 16)
bg_hue, bg_saturation, bg_value = colorsys.rgb_to_hsv(r_bg / 255, g_bg / 255, b_bg / 255)
window.config(bg=random_color)

# Frame for wheels
wheels_frame = tk.Frame(window)
wheels_frame.pack(side=tk.LEFT, padx=10)

# Hue wheel
hue_canvas = tk.Canvas(wheels_frame, width=300, height=300, bg="white", highlightthickness=0)
hue_canvas.pack(pady=10)
tk.Label(wheels_frame, text="Hue", font=("Arial", 12)).pack()
draw_hue_wheel(hue_canvas)
draw_marker(hue_canvas, bg_hue, "red")

# Combined Saturation-Value square
combined_canvas = tk.Canvas(wheels_frame, width=300, height=300, bg="white", highlightthickness=0)
combined_canvas.pack(pady=10)
tk.Label(wheels_frame, text="Saturation-Brightness", font=("Arial", 12)).pack()
draw_combined_square(combined_canvas, bg_hue)
draw_combined_marker(combined_canvas, bg_saturation, bg_value, "red")

# Right frame for input and guesses
right_frame = tk.Frame(window)
right_frame.pack(side=tk.LEFT, padx=10)

#label and entry for the hex color input
tk.Label(right_frame, text="Guess the Hex Color Code:", font=("Arial", 12)).pack(pady=5)
color_input = tk.Entry(right_frame, font=("Arial", 12))
color_input.pack(pady=5)

# Add a square to display the most recent guess
recent_guess_display = tk.Label(right_frame, text="", bg="white", width=20, height=10, relief="solid")
recent_guess_display.pack(pady=10)

# Create a Submit button
submit_button = tk.Button(
    right_frame,
    text="Submit Guess",
    font=("Arial", 12),
    command=lambda: submit_guess())
submit_button.pack(pady=10)

#display previous guesses
tk.Label(right_frame, text="Previous Guesses:", font=("Arial", 12)).pack(pady=5)
guesses_list = tk.Listbox(right_frame, font=("Arial", 12), height=10, width=15)
guesses_list.pack(pady=5)

# abel
instruction_label = tk.Label(
    right_frame,
    text="Red marker = Background color\\nYellow marker = Previous guesses\\nGreen marker = Most recent guess",
    font=("Arial", 10),
    bg=random_color,
    fg="white")
instruction_label.pack()

# Run the Tkinter main loop
window.mainloop()
