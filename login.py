import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from PIL import Image, ImageTk  # Import PIL for image handling

# Function to verify login
def verify_login():
    username = entry_username.get()
    password = entry_password.get()

    # Check credentials
    if username == "tasneem" and password == "tasneem123":
        messagebox.showinfo("Login", "Login Successful")
        messagebox.showinfo("Flask Server", "Flask server started successfully!")  # New message box
        start_flask_server()  # Start Flask server after successful login
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

# Function to start the Flask server (sum.py)
def start_flask_server():
    try:
        # Running the Flask server (sum.py) in a new terminal window
        if os.name == 'nt':  # For Windows
            subprocess.Popen(["start", "cmd", "/K", "python", "sum.py"], shell=True)
        else:  # For macOS/Linux
            subprocess.Popen(["gnome-terminal", "--", "python3", "sum.py"], shell=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Flask server: {str(e)}")

# Creating the main window (login window)
window = tk.Tk()
window.title("Login Page")
window.geometry("800x600")  # Set the window size to 800x600
window.config(bg="#f0f0f0")

# Load and set background image to cover the full window
bg_image = Image.open("back1.jpg")  # Replace with your actual image path
bg_image = bg_image.resize((1500, 1000), Image.Resampling.LANCZOS)  # Resize to fit the full window size
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Make the background cover the whole window

# Create a frame for the login page with better fitting dimensions
login_frame = tk.Frame(window, bg="white", bd=10, relief="solid", padx=20, pady=20)
login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)  # Center the frame with adjusted size

# Add the title label
label_title = tk.Label(login_frame, text="Login", font=("Helvetica", 28, "bold"), bg="white", fg="#333")
label_title.pack(pady=20)

# Username label and entry with padding and border
label_username = tk.Label(login_frame, text="Username", font=("Helvetica", 14), bg="white", fg="#333")
label_username.pack(pady=5)
entry_username = tk.Entry(login_frame, font=("Helvetica", 14), width=20, bd=2, relief="solid", highlightbackground="#ccc", highlightcolor="#4CAF50")
entry_username.pack(pady=5)

# Password label and entry with padding and border
label_password = tk.Label(login_frame, text="Password", font=("Helvetica", 14), bg="white", fg="#333")
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, font=("Helvetica", 14), show="*", width=20, bd=2, relief="solid", highlightbackground="#ccc", highlightcolor="#4CAF50")
entry_password.pack(pady=5)

# Login button with rounded corners and hover effect simulation
login_button = tk.Button(
    login_frame, text="Login", font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="raised", bd=3,
    command=verify_login
)
login_button.pack(pady=20)

# Simulating hover effect using event binding
def on_enter(event):
    login_button.config(bg="#45a049")  # Darken button on hover

def on_leave(event):
    login_button.config(bg="#4CAF50")  # Reset button color on leave

login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

# Start the main loop
window.mainloop()
