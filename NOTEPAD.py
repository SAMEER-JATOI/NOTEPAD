import tkinter as tk 
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font


def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
            root.title(f"Notepad - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

 
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END)) 
            root.title(f"Notepad - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")


def quit_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()


def change_font():
    font_choice = simpledialog.askstring("Font", "Enter font name (e.g., Arial, Times New Roman):")
    if font_choice:
        try:
            text_area.config(font=(font_choice, 12))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid font: {e}")


def change_font_size():
    font_size = simpledialog.askinteger("Font Size", "Enter font size (e.g., 12, 14, 16):")
    if font_size:
        try:
            current_font = font.nametofont(text_area.cget("font"))
            current_font.actual()["size"] = font_size
            text_area.config(font=current_font)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid font size: {e}")


def bold_text():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
        text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))


def italic_text():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
        text_area.tag_configure("italic", font=("Helvetica", 12, "italic"))


def underline_text():
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
        text_area.tag_configure("underline", underline=True)


def find_text():
    find_word = simpledialog.askstring("Find", "Enter text to find:")
    if find_word:
        text_area.tag_remove("found", "1.0", tk.END)
        start_pos = "1.0"
        while True:
            start_pos = text_area.search(find_word, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(find_word)}c"
            text_area.tag_add("found", start_pos, end_pos)
            start_pos = end_pos
        text_area.tag_configure("found", background="yellow")


def replace_text():
    find_word = simpledialog.askstring("Find", "Enter text to find:")
    replace_word = simpledialog.askstring("Replace", "Enter text to replace with:")
    if find_word and replace_word:
        text = text_area.get(1.0, tk.END)
        new_text = text.replace(find_word, replace_word)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, new_text)


def update_status_bar(event=None):
    row, col = text_area.index(tk.INSERT).split(".")
    status_label.config(text=f"Line: {row} | Column: {col}")


root = tk.Tk()
root.title("Advanced Notepad")
root.geometry("800x600")


text_area = tk.Text(root, wrap=tk.WORD, undo=True)
text_area.pack(expand=True, fill=tk.BOTH)


menu_bar = tk.Menu(root)


file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_app)


edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Change Font", command=change_font)
edit_menu.add_command(label="Change Font Size", command=change_font_size)
edit_menu.add_separator()
edit_menu.add_command(label="Bold", command=bold_text)
edit_menu.add_command(label="Italic", command=italic_text)
edit_menu.add_command(label="Underline", command=underline_text)


find_menu = tk.Menu(menu_bar, tearoff=0)
find_menu.add_command(label="Find", command=find_text)
find_menu.add_command(label="Replace", command=replace_text)


menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Find", menu=find_menu)


root.config(menu=menu_bar)


status_bar = tk.Frame(root, height=20, bd=1, relief=tk.SUNKEN)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)

status_label = tk.Label(status_bar, text="Line: 1 | Column: 1", anchor="w")
status_label.pack(side=tk.LEFT)


text_area.bind("<KeyRelease>", update_status_bar)


root.mainloop()
