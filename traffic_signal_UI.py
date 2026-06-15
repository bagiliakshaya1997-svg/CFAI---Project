import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Traffic Logic
# -----------------------------
def get_signal_time(count):
    if count > 20:
        return "High", 60
    elif count > 10:
        return "Medium", 40
    else:
        return "Low", 20


# -----------------------------
# Global Variables
# -----------------------------
roads = ["Road 1", "Road 2", "Road 3", "Road 4"]
roads_order = []
time_values = {}
current_index = 0
current_time_left = 0
timer_running = False
right_box_text_id = None


# -----------------------------
# UI Helpers
# -----------------------------
def update_lights(priority_index):
    for light in green_lights:
        canvas.itemconfig(light, fill="gray")
    for light in red_lights:
        canvas.itemconfig(light, fill="red")

    canvas.itemconfig(red_lights[priority_index], fill="gray")
    canvas.itemconfig(green_lights[priority_index], fill="green")


def update_result_box(priority_road, priority_count, level, time_allocated):
    result_text.set(
        f"Priority Road : {priority_road}\n"
        f"Vehicle Count : {priority_count}\n"
        f"Traffic Level : {level}\n"
        f"Green Signal Time : {time_allocated} sec"
    )


def draw_right_box():
    canvas_sequence.delete("all")
    canvas_sequence.create_rectangle(20, 20, 820, 240, outline="#999", width=2, fill="white")

    display_text = (
        "Next Road Sequence\n\n"
        f"1. {roads_order[0]}  -  {time_values[roads_order[0]]} sec\n"
        f"2. {roads_order[1]}  -  {time_values[roads_order[1]]} sec\n"
        f"3. {roads_order[2]}  -  {time_values[roads_order[2]]} sec\n"
        f"4. {roads_order[3]}  -  {time_values[roads_order[3]]} sec\n\n"
        "After the current priority road finishes, the next road in the list gets green signal."
    )

    canvas_sequence.create_text(
        40, 40,
        anchor="nw",
        text=display_text,
        font=("Arial", 12),
        fill="black",
        justify="left"
    )


def refresh_right_box():
    draw_right_box()


def start_sequence_timer(index=0):
    global current_index, current_time_left, timer_running

    if index >= len(roads_order):
        timer_status.set("Done")
        draw_right_box()
        timer_running = False
        return

    timer_running = True
    current_index = index
    road = roads_order[current_index]
    current_time_left = time_values[road]
    countdown_tick()


def countdown_tick():
    global current_time_left, current_index

    if not timer_running:
        return

    road = roads_order[current_index]
    timer_status.set(f"{road} : {current_time_left} sec")
    priority_idx = roads.index(road)
    update_lights(priority_idx)
    draw_right_box()

    if current_time_left > 0:
        current_time_left -= 1
        root.after(1000, countdown_tick)
    else:
        root.after(1000, start_sequence_timer, current_index + 1)


# -----------------------------
# Optimize Traffic
# -----------------------------
def optimize_traffic():
    try:
        counts = [
            int(road1.get()),
            int(road2.get()),
            int(road3.get()),
            int(road4.get())
        ]

        global roads_order, time_values, timer_running

        paired = sorted(zip(counts, roads), reverse=True)
        roads_order = [road for count, road in paired]
        time_values = {}

        for count, road in paired:
            level, t = get_signal_time(count)
            time_values[road] = t

        priority_count, priority_road = paired[0]
        level, time_allocated = get_signal_time(priority_count)
        priority_index = roads.index(priority_road)

        update_lights(priority_index)
        update_result_box(priority_road, priority_count, level, time_allocated)

        timer_running = False
        root.after(100, start_sequence_timer, 0)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid vehicle counts.")


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Traffic Signal Optimization System")
root.geometry("1400x720")
root.configure(bg="#f2f6fc")

timer_status = tk.StringVar(value="00 sec")

# -----------------------------
# Header
# -----------------------------
title = tk.Label(
    root,
    text="TRAFFIC SIGNAL OPTIMIZATION SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#1f4e79",
    fg="white",
    pady=15
)
title.pack(fill="x")

# -----------------------------
# Input Frame
# -----------------------------
input_frame = tk.Frame(root, bg="#f2f6fc")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Road 1", font=("Arial", 11, "bold"), bg="#f2f6fc").grid(row=0, column=0, padx=20)
road1 = tk.Entry(input_frame, width=10)
road1.grid(row=1, column=0)

tk.Label(input_frame, text="Road 2", font=("Arial", 11, "bold"), bg="#f2f6fc").grid(row=0, column=1, padx=20)
road2 = tk.Entry(input_frame, width=10)
road2.grid(row=1, column=1)

tk.Label(input_frame, text="Road 3", font=("Arial", 11, "bold"), bg="#f2f6fc").grid(row=0, column=2, padx=20)
road3 = tk.Entry(input_frame, width=10)
road3.grid(row=1, column=2)

tk.Label(input_frame, text="Road 4", font=("Arial", 11, "bold"), bg="#f2f6fc").grid(row=0, column=3, padx=20)
road4 = tk.Entry(input_frame, width=10)
road4.grid(row=1, column=3)

# -----------------------------
# Button
# -----------------------------
opt_btn = tk.Button(
    root,
    text="Optimize Traffic",
    font=("Arial", 12, "bold"),
    bg="#28a745",
    fg="white",
    padx=15,
    pady=5,
    command=optimize_traffic
)
opt_btn.pack(pady=10)

# -----------------------------
# Traffic Lights
# -----------------------------
lights_frame = tk.Frame(root, bg="#f2f6fc")
lights_frame.pack(pady=10)

canvas = tk.Canvas(
    lights_frame,
    width=900,
    height=200,
    bg="#f2f6fc",
    highlightthickness=0
)
canvas.pack()

red_lights = []
green_lights = []
x_positions = [100, 300, 500, 700]

for i, x in enumerate(x_positions):
    canvas.create_text(x, 20, text=f"Road {i+1}", font=("Arial", 12, "bold"))
    red = canvas.create_oval(x-20, 40, x+20, 80, fill="red")
    green = canvas.create_oval(x-20, 100, x+20, 140, fill="gray")
    red_lights.append(red)
    green_lights.append(green)

# -----------------------------
# Bottom Section
# -----------------------------
bottom_frame = tk.Frame(root, bg="#f2f6fc")
bottom_frame.pack(fill="both", expand=True, pady=10)

# Left Box
left_frame = tk.Frame(bottom_frame, bg="#f2f6fc")
left_frame.pack(side="left", padx=25, pady=10, anchor="n")

tk.Label(
    left_frame,
    text="Current Priority",
    font=("Arial", 13, "bold"),
    bg="#f2f6fc"
).pack(anchor="w", pady=(0, 5))

result_text = tk.StringVar(value="")
result_label = tk.Label(
    left_frame,
    textvariable=result_text,
    font=("Arial", 13),
    bg="white",
    width=35,
    height=6,
    relief="ridge",
    bd=2,
    justify="left"
)
result_label.pack()

# Right Box
right_frame = tk.Frame(bottom_frame, bg="#f2f6fc")
right_frame.pack(side="right", padx=25, pady=10, anchor="n", fill="both", expand=True)

tk.Label(
    right_frame,
    text="Next Order of Priority",
    font=("Arial", 13, "bold"),
    bg="#f2f6fc"
).pack(anchor="w", pady=(0, 5))

canvas_sequence = tk.Canvas(
    right_frame,
    width=900,
    height=260,
    bg="#f2f6fc",
    highlightthickness=0
)
canvas_sequence.pack(fill="both", expand=True)

roads_order = ["Road 1", "Road 2", "Road 3", "Road 4"]
time_values = {
    "Road 1": 20,
    "Road 2": 20,
    "Road 3": 20,
    "Road 4": 20
}

draw_right_box()
root.mainloop()