import tkinter as tk
from tkinter import messagebox
from transformers import pipeline
import mysql.connector

# Initialize summarization pipelines
abstractive_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
extractive_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Function to create or get the MySQL database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root",       
            password="tanzila@123",  
            database="summary"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        return None

# Function to store summary in MySQL database
def store_summary(input_text, summary_text):
    try:
        conn = get_db_connection()
        if not conn:
            return 

        cursor = conn.cursor()
        cursor.execute("INSERT INTO summaries (original_text, summary) VALUES (%s, %s)", (input_text, summary_text))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Summary stored in the database.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred while storing the summary: {err}")

# Function to fetch all stored summaries from the database
def fetch_history():
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT original_text, summary FROM summaries")
        history = cursor.fetchall()
        conn.close()
        return history

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred while fetching the history: {err}")
        return []

# Function to perform summarization
def summarize():
    input_text = text_input.get("1.0", "end-1c").strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text for summarization.")
        return

    summarization_type = method_var.get()

    try:
        if summarization_type == "Abstractive":
            summary = abstractive_summarizer(input_text, max_length=200, min_length=50, do_sample=False)
        elif summarization_type == "Extractive":
            summary = extractive_summarizer(input_text, max_length=200, min_length=50, do_sample=False)
        else:
            messagebox.showwarning("Method Error", "Please select a valid summarization method.")
            return

        summary_text = summary[0]['summary_text']
        store_summary(input_text, summary_text)

        summary_output.delete("1.0", "end")
        summary_output.insert(tk.END, summary_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to show history in the new window
def show_history():
    history = fetch_history()
    
    if not history:
        messagebox.showinfo("History", "No history available.")
        return
    
    history_window = tk.Toplevel(root)
    history_window.title("Summary History")
    history_window.geometry("600x400")
    
    # Create a text box to display the history
    history_text = tk.Text(history_window, height=15, width=70, font=("Arial", 12), bd=2, relief="solid", bg="#2C2F38", fg="#D1D3D4")
    history_text.pack(pady=10)
    
    # Display the history in the text box
    for entry in history:
        original_text, summary = entry
        history_text.insert(tk.END, f"Original Text:\n{original_text}\nSummary:\n{summary}\n\n{'-'*50}\n\n")
    
    history_text.config(state=tk.DISABLED)  # Make the text box read-only

# Create the main application window
root = tk.Tk()
root.title("AI-Powered Text Summarization")
root.geometry("800x600")

# Dark mode background color
root.configure(bg="#1A1A1A")  # Dark background color

# Create UI Frame with dark theme
frame = tk.Frame(root, bg="#2C2F38", padx=40, pady=40, relief="solid", bd=2, highlightbackground="#444", highlightthickness=1)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Title Label
title_label = tk.Label(frame, text="Text Summarization Tool", font=("Helvetica", 20, "bold"), bg="#2C2F38", fg="#D1D3D4")
title_label.pack(pady=20)

# Input Label
input_label = tk.Label(frame, text="Enter Text:", font=("Helvetica", 14), bg="#2C2F38", fg="#D1D3D4")
input_label.pack(anchor="w")

# Input Text Box
text_input = tk.Text(frame, height=8, width=60, font=("Arial", 12), bd=2, relief="solid", bg="#2C2F38", fg="#D1D3D4", highlightbackground="#444", highlightthickness=1)
text_input.pack(pady=10)

# Summarization Method Selection
method_var = tk.StringVar(value="Abstractive")
method_frame = tk.Frame(frame, bg="#2C2F38")
method_frame.pack(pady=15)

abstractive_button = tk.Radiobutton(method_frame, text="Abstractive", variable=method_var, value="Abstractive",
                                    font=("Arial", 14), bg="#2C2F38", fg="#FF5733", selectcolor="#FFDAB9", activebackground="#FF7F50")
extractive_button = tk.Radiobutton(method_frame, text="Extractive", variable=method_var, value="Extractive",
                                   font=("Arial", 14), bg="#2C2F38", fg="#3498DB", selectcolor="#FFDAB9", activebackground="#1E90FF")

abstractive_button.pack(side="left", padx=30)
extractive_button.pack(side="left", padx=30)

# Summarize Button
summarize_button = tk.Button(frame, text="Generate Summary", command=summarize, font=("Arial", 14, "bold"), 
                             bg="#28A745", fg="white", bd=3, relief="raised", padx=10, pady=10, activebackground="#218838")
summarize_button.pack(pady=20)

# Output Label
output_label = tk.Label(frame, text="Summary:", font=("Arial", 14, "bold"), bg="#2C2F38", fg="#D1D3D4")
output_label.pack(anchor="w")

# Output Text Box
summary_output = tk.Text(frame, height=8, width=60, font=("Arial", 12), bd=2, relief="solid", bg="#2C2F38", fg="#D1D3D4", highlightbackground="#444", highlightthickness=1)
summary_output.pack(pady=10)

# History Button
history_button = tk.Button(frame, text="View History", command=show_history, font=("Arial", 14, "bold"), 
                            bg="#FFD700", fg="black", bd=3, relief="raised", padx=10, pady=10, activebackground="#FFBF00")
history_button.pack(pady=20)

# Run Tkinter Main Loop
root.mainloop()
