import tkinter as tk
import colorsys
import math
import random


# generate a random hex color
def generate_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


# Check guess
def check_guess(random_color, color_input, recent_guess_display, guesses_list, hue_canvas, combined_canvas, reset_game):
    guess = '#' + color_input.get()
    if len(guess) != 7 or not guess.startswith("#"):
        tk.messagebox.showerror("Invalid Format", "Please enter a valid hex color code in the format #RRGGBB.")
        return

    recent_guess_display.config(bg=guess)
    guesses_list.insert(tk.END, guess)

    try:
        r_guess = int(guess[1:3], 16)
        g_guess = int(guess[3:5], 16)
        b_guess = int(guess[5:7], 16)
        guess_hue, guess_saturation, guess_value = colorsys.rgb_to_hsv(r_guess / 255, g_guess / 255, b_guess / 255)
        redraw_previous_markers(guesses_list, hue_canvas, combined_canvas)
        draw_marker(hue_canvas, guess_hue, "green")
        draw_combined_marker(combined_canvas, guess_saturation, guess_value, "green")

        guess_value_int = int(guess[1:], 16)
        random_color_int = int(random_color[1:], 16)
        color_difference = abs(guess_value_int - random_color_int)

        if color_difference <= 1500:
            tk.messagebox.showinfo("Success!", "You guessed close enough to the correct color!")
            reset_game()
        else:
            tk.messagebox.showerror("Try Again", "Incorrect guess. Keep trying!")
    except (ValueError, IndexError):
        tk.messagebox.showerror("Invalid Format", "Please enter a valid hex color code in the format #RRGGBB.")


# Drawing functions
def draw_marker(canvas, value, color):
    angle = math.radians(value * 360)
    x = 150 + 120 * math.cos(angle)
    y = 150 - 120 * math.sin(angle)
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="black")


def draw_combined_marker(canvas, saturation, value, color):
    x = saturation * 240 + 30
    y = (1 - value) * 240 + 30
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="black")


def redraw_previous_markers(guesses_list, hue_canvas, combined_canvas):
    for guess in guesses_list.get(0, tk.END):
        r_guess = int(guess[1:3], 16)
        g_guess = int(guess[3:5], 16)
        b_guess = int(guess[5:7], 16)
        guess_hue, guess_saturation, guess_value = colorsys.rgb_to_hsv(r_guess / 255, g_guess / 255, b_guess / 255)
        draw_marker(hue_canvas, guess_hue, "yellow")
        draw_combined_marker(combined_canvas, guess_saturation, guess_value, "yellow")


def draw_hue_wheel(canvas):
    for i in range(360):
        start_angle = i
        extent = 1
        rgb = colorsys.hsv_to_rgb(i / 360, 1, 1)
        hex_color = f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"
        canvas.create_arc(
            30, 30, 270, 270,
            start=start_angle, extent=extent, fill=hex_color, outline=""
        )


def draw_combined_square(canvas, hue):
    for i in range(240):
        for j in range(240):
            saturation = i / 240
            value = 1 - j / 240
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"
            canvas.create_line(i + 30, j + 30, i + 31, j + 30, fill=hex_color)
