import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import time
import threading
import webbrowser
import random
import pyttsx3
import pandas as pd

# ============== Voice Assistant ==============
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ============== Load CSV Data ==============
reminder_path = r"C:\Users\Bhargavi\Desktop\C Language\harry code\harry c\daily_reminder.csv"
safety_path = r"C:\Users\Bhargavi\Desktop\C Language\harry code\harry c\safety_monitoring.csv"
health_path = r"C:\Users\Bhargavi\Desktop\C Language\harry code\harry c\health_monitoring.csv"

df = pd.read_csv(reminder_path)
safety_df = pd.read_csv(safety_path)
health_df = pd.read_csv(health_path)

df['Day'] = ["D" + str(i // 10 + 1) for i in range(len(df))]
health_df['Day'] = ["D" + str(i // 10 + 1) for i in range(len(health_df))]

# ============== Medicine Reminder Thread ==============
def medicine_reminder():
    last_alerts = set()
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        matches = df[
            (df['Scheduled Time'].str[:5] == now) &
            (df['Reminder Type'].str.lower() == "medication")
        ]
        for _, row in matches.iterrows():
            key = f"{row['Scheduled Time']}_{row['Reminder Type']}"
            if key not in last_alerts:
                last_alerts.add(key)
                app.after(0, lambda msg=row['Reminder Type']: [
                    speak("It's time for your " + msg),
                    messagebox.showinfo("Reminder", f"Reminder: {msg} at {row['Scheduled Time']}")
                ])
        time.sleep(60)

# ============== Fullscreen Helper ==============
def fullscreen_window(title, bg="#5BA4A7"):
    win = tk.Toplevel(app)
    win.title(title)
    win.state("zoomed")
    win.configure(bg=bg)
    return win

# ============== Daily Reminders ==============
def open_reminder_window():
    speak("Opening your daily schedule.")
    window = fullscreen_window("Daily Reminders & Schedule", "#fef9e7")
    tk.Label(window, text="📋 View Schedule by Day", font=("Helvetica", 20, "bold"), bg="#fef9e7").pack(pady=20)

    day_var = tk.StringVar()
    days = sorted(df['Day'].unique())
    day_var.set(days[0])
    dropdown = ttk.Combobox(window, textvariable=day_var, values=days, state="readonly", font=("Helvetica", 14))
    dropdown.pack(pady=10)

    tree = ttk.Treeview(window, columns=("Time", "Reminder", "Status"), show="headings", height=20)
    for col in ["Time", "Reminder", "Status"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=200)
    tree.pack(fill="both", expand=True, padx=40, pady=20)

    def update_table(*args):
        tree.delete(*tree.get_children())
        selected_day = day_var.get()
        filtered = df[df['Day'] == selected_day]
        for idx, row in filtered.iterrows():
            tree.insert("", "end", iid=idx, values=(row["Scheduled Time"], row["Reminder Type"], row["Acknowledged (Yes/No)"]))

    def mark_as_done():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Reminder", "Please select a reminder.")
            return
        index = int(selected[0])
        df.at[index, "Acknowledged (Yes/No)"] = "Yes"
        update_table()
        speak("Marked as done.")
        df.to_csv(reminder_path, index=False)

    dropdown.bind("<<ComboboxSelected>>", update_table)
    update_table()

    tk.Button(window, text="Mark as Done", font=("Helvetica", 14), command=mark_as_done).pack(pady=10)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)

# ============== Safety Monitoring ==============
def open_safety_monitoring():
    speak("Opening safety monitoring.")
    window = fullscreen_window("Safety Monitoring", "#e8f4fc")
    tk.Label(window, text="🛡 Safety Monitoring", font=("Helvetica", 20, "bold"), bg="#e8f4fc").pack(pady=20)

    tree = ttk.Treeview(window, columns=safety_df.columns.tolist(), show="headings", height=20)
    for col in safety_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.pack(fill="both", expand=True, padx=20)

    for idx, row in safety_df.iterrows():
        tree.insert("", "end", iid=idx, values=tuple(row))

    def mark_resolved():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an alert.")
            return
        index = int(selected[0])
        safety_df.at[index, "Alert Triggered (Yes/No)"] = "No"
        safety_df.at[index, "Caregiver Notified (Yes/No)"] = "Yes"
        tree.item(index, values=tuple(safety_df.loc[index]))
        safety_df.to_csv(safety_path, index=False)
        speak("Alert marked as resolved.")

    tk.Button(window, text="Mark as Resolved", command=mark_resolved).pack(pady=10)

# ============== Health Monitoring ==============
def open_health_monitoring():
    speak("Opening health monitoring.")
    window = fullscreen_window("Health Monitoring", "#e9f7ef")
    tk.Label(window, text="🩺 Health Monitoring", font=("Helvetica", 20, "bold"), bg="#e9f7ef").pack(pady=20)

    frame = tk.Frame(window, bg="#e9f7ef")
    frame.pack(fill="both", expand=True, padx=20)

    tree = ttk.Treeview(frame, columns=health_df.columns.tolist(), show="headings", height=20)
    for col in health_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    for idx, row in health_df.iterrows():
        tree.insert("", "end", iid=idx, values=tuple(row))

# ============== Daily Motivation ==============
def show_motivation():
    motivation_win = tk.Toplevel(app)
    motivation_win.title("💖 Daily Motivation")
    motivation_win.geometry("1920x1100")
    motivation_win.configure(bg="#ffeef5")  # soft pink background

    tk.Label(motivation_win, text="💖 Daily Motivation", font=("Helvetica", 28, "bold"), bg="#ffeef5", fg="#c2185b").pack(pady=30)

    quotes = {
        "Positivity": [
            "Every day is a new beginning!",
            "Stay positive and strong.",
            "Let your smile change the world."
        ],
        "Wisdom": [
            "You are never too old to learn.",
            "A calm mind brings inner strength.",
            "Experience is the best teacher."
        ],
        "Health": [
            "Take care of your body. It’s the only place you have to live.",
            "Eat well, move more, sleep better.",
            "A healthy mind resides in a healthy body."
        ]
    }

    category_var = tk.StringVar(value="Positivity")
    quote_var = tk.StringVar()

    def get_quote():
        category = category_var.get()
        quote = random.choice(quotes[category])
        quote_var.set(f"“{quote}”")
        speak(quote)

    frame = tk.Frame(motivation_win, bg="#ffeef5")
    frame.pack(pady=20)

    tk.Label(frame, text="Select a category:", bg="#ffeef5", font=("Helvetica", 18)).grid(row=0, column=0, padx=10, pady=10)
    ttk.Combobox(frame, textvariable=category_var, values=list(quotes.keys()), font=("Helvetica", 14), state="readonly", width=20).grid(row=0, column=1, pady=10)

    quote_display = tk.Label(motivation_win, textvariable=quote_var, wraplength=1000, justify="center", bg="#ffeef5", font=("Helvetica", 22, "italic"), fg="#333")
    quote_display.pack(pady=40)

    tk.Button(motivation_win, text="Next Quote", font=("Helvetica", 16), bg="#c2185b", fg="white", width=20, command=get_quote).pack(pady=10)
    tk.Button(motivation_win, text="Close", font=("Helvetica", 14), command=motivation_win.destroy).pack(pady=10)

    get_quote()



# ============== Exercise Suggestion ==============
def suggest_exercise():
    window = tk.Toplevel(app)
    window.title("🧘 Suggest an Exercise")
    window.geometry("1920x1100")
    window.configure(bg="#e3f2fd")  # soft blue background

    tk.Label(window, text="🧘 Personalized Exercise Suggestion", font=("Helvetica", 28, "bold"), bg="#e3f2fd", fg="#1565c0").pack(pady=30)

    now = datetime.datetime.now().hour
    if now < 12:
        time_of_day = "Morning"
    elif 12 <= now < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"

    tk.Label(window, text=f"Time of Day: {time_of_day}", font=("Helvetica", 18), bg="#e3f2fd").pack(pady=10)
    tk.Label(window, text="How are you feeling today?", font=("Helvetica", 18), bg="#e3f2fd").pack(pady=10)

    energy_var = tk.StringVar(value="Normal")
    tk.Frame(window, bg="#e3f2fd", height=20).pack()

    tk.Radiobutton(window, text="Low Energy", variable=energy_var, value="Low", font=("Helvetica", 16), bg="#e3f2fd").pack()
    tk.Radiobutton(window, text="Normal", variable=energy_var, value="Normal", font=("Helvetica", 16), bg="#e3f2fd").pack()
    tk.Radiobutton(window, text="Energetic", variable=energy_var, value="High", font=("Helvetica", 16), bg="#e3f2fd").pack()

    exercises = {
        "Morning": {
            "Low": ["Gentle neck rolls", "Light stretching", "Toe taps"],
            "Normal": ["10-min walk", "Shoulder rolls", "Leg curls"],
            "High": ["Brisk walk", "Chair squats", "Stair stepping"]
        },
        "Afternoon": {
            "Low": ["Arm stretches", "Ankle circles", "Palm presses"],
            "Normal": ["Sit-to-stand", "Wall push-ups", "March in place"],
            "High": ["5-min dance", "Light weights", "Chair jacks"]
        },
        "Evening": {
            "Low": ["Breathing with music", "Wrist rolls", "Seated leg raises"],
            "Normal": ["House walk", "Seated yoga", "Forward bends"],
            "High": ["Short yoga", "Tai chi", "Wall sits"]
        }
    }

    def get_exercise():
        level = energy_var.get()
        selected = random.choice(exercises[time_of_day][level])
        speak(f"Here's your exercise: {selected}")
        messagebox.showinfo("Exercise Suggestion", selected)

    tk.Button(window, text="Get Suggestion", font=("Helvetica", 16), bg="#1565c0", fg="white", width=25, command=get_exercise).pack(pady=30)
    tk.Button(window, text="Close", font=("Helvetica", 14), command=window.destroy).pack(pady=10)




# ============== SOS & Contact ==============
def contact_family():
    webbrowser.open("https://wa.me/")
    speak("Opening WhatsApp.")

def send_sos():
    webbrowser.open("https://www.google.com/maps")
    speak("Emergency alert has been triggered.")
    messagebox.showwarning("SOS", "Emergency Alert Sent!")

# ============== Main App ==============
app = tk.Tk()
app.title("CAREMATE")
app.state("zoomed")
app.configure(bg="#5BA4A7")

tk.Label(app, text="🫂 CAREMATE", font=("Times New Roman", 28, "bold"), bg="#FFF").pack(pady=20)

features = [
    ("📋 Daily Reminders & Schedule", open_reminder_window),
    ("🛡 Safety Monitoring", open_safety_monitoring),
    ("❤ Health Monitoring", open_health_monitoring),
    ("💖 Daily Motivation", show_motivation),
    ("🧘 Suggest an Exercise", suggest_exercise),
    ("📞 Contact Family", contact_family),
    ("🆘 Emergency SOS", send_sos),
]

for text, command in features:
    tk.Button(app, text=text, font=("Times New Roman", 20), width=40, height=2, command=command).pack(pady=10)

tk.Label(app, text="Version 1.0 | Python Powered", font=("Helvetica", 10), bg="#fdf5e6").pack(side="bottom", pady=10)

# Start background thread
reminder_thread = threading.Thread(target=medicine_reminder, daemon=True)
reminder_thread.start()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to exit the app?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)


# Launch the app
app.mainloop()