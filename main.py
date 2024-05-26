import webbrowser
import tkinter as tk
from tkinter import ttk

# Centers window
def CenterWindowToDisplay(Screen: tk, width: int, height: int):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 1.5))
    return f"{width}x{height}+{x}+{y}"

def ok_button_click(event=None):
    region = combo_box.get()
    champion = champion_entry.get()
    url = "https://www.op.gg/leaderboards/champions/" + champion.lower() + "?region=" + region.lower()
    webbrowser.open(url, new=2, autoraise=False)
    root.destroy()

root = tk.Tk()
root.geometry(CenterWindowToDisplay(root, 570, 130))
root.title("OP.GG Build Finder")

# Change font of Combobox dropdown list
root.option_add("*TCombobox*Listbox.font", "Arial 25")

# Region
label = tk.Label(root, text="Region: ", font=("Arial", 25))
label.grid(row=0, column=0, sticky="w", pady=10)
# Dropdown list
combo_box = ttk.Combobox(root, values=["NA", "EUW", "EUNE", "OCE", "KR", "JP", "BR", "LAS", "LAN", "RU", "TR",
                                       "SG", "PH", "TR", "TW", "VN", "TH"], font=("Arial", 25))
combo_box.grid(row=0, column=1, sticky="w", pady=10, padx=5)
# Set default value
combo_box.set("KR")

# Champion name
label = tk.Label(root, text="Champion: ", font=("Arial", 25))
label.grid(row=1, column=0, sticky="w", pady=10)
champion_entry = tk.Entry(root, font=("Arial", 25))
champion_entry.grid(row=1, column=1, sticky="w", pady=10, padx=5)
champion_entry.focus()

# OK Button
ok_button = tk.Button(root, text="OK", font=("Arial", 18), command=ok_button_click)
ok_button.grid(row=1, column=1, sticky="e")

# Enter key
root.bind('<Return>', ok_button_click)

root.mainloop()
