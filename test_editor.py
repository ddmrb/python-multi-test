import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

# Global variables
questions = []
current_question = 0
image_label = None  # Store the image label globally
image_folder = os.path.join(os.path.dirname(__file__), 'images')
csv_file_path = ""  # To keep track of the CSV file path

# Function to load the CSV file
def load_test():
    global questions, current_question, csv_file_path
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_file_path = file_path  # Store the file path for saving later
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                questions.clear()
                questions.extend([row for row in reader])
            current_question = 0
            root.title(f"Test Editor - {file_path}")
            show_question(current_question)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")

# Function to save the CSV file immediately to the same file
def save_test():
    global csv_file_path
    if csv_file_path:
        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['question', 'answera', 'answerb', 'answerc', 'answerd', 'actual_answer', 'book', 'regulation_table', 'image']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

                writer.writeheader()
                for question in questions:
                    writer.writerow(question)

            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {str(e)}")
    else:
        messagebox.showerror("Error", "No CSV file loaded.")

# Function to show a question and make all fields editable
def show_question(index):
    global image_label, current_question
    current_question = index

    if index >= len(questions):
        return  # No more questions

    # Clear the current content
    for widget in frame.winfo_children():
        widget.destroy()

    question_data = questions[index]

    # Show the image if the "image" field is defined
    image_path = question_data.get('image', '').strip()
    if image_path:
        try:
            img = Image.open(image_path)
            original_width, original_height = img.size
            max_size = 350
            if original_width > max_size or original_height > max_size:
                scaling_factor = min(max_size / original_width, max_size / original_height)
                new_size = (int(original_width * scaling_factor), int(original_height * scaling_factor))
                img = img.resize(new_size, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(frame, image=img, bg='white')
            image_label.image = img  # Keep a reference to the image
            image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    # Editable fields for question and answers
    tk.Label(frame, text="Question", font=("Arial", 14)).pack(anchor='w')
    question_entry = tk.Entry(frame, width=150)
    question_entry.insert(0, question_data['question'])
    question_entry.pack(pady=5)

    tk.Label(frame, text="Answer A", font=("Arial", 12)).pack(anchor='w')
    answera_entry = tk.Entry(frame, width=150)
    answera_entry.insert(0, question_data['answera'])
    answera_entry.pack(pady=5)

    tk.Label(frame, text="Answer B", font=("Arial", 12)).pack(anchor='w')
    answerb_entry = tk.Entry(frame, width=150)
    answerb_entry.insert(0, question_data['answerb'])
    answerb_entry.pack(pady=5)

    tk.Label(frame, text="Answer C", font=("Arial", 12)).pack(anchor='w')
    answerc_entry = tk.Entry(frame, width=150)
    answerc_entry.insert(0, question_data['answerc'])
    answerc_entry.pack(pady=5)

    tk.Label(frame, text="Answer D", font=("Arial", 12)).pack(anchor='w')
    answerd_entry = tk.Entry(frame, width=150)
    answerd_entry.insert(0, question_data['answerd'])
    answerd_entry.pack(pady=5)

    # Create radio buttons for selecting actual answer and show actual_answer text field
    answer_var = tk.StringVar()
    actual_answer_entry = tk.Entry(frame, width=150)
    actual_answer_entry.insert(0, question_data['actual_answer'])

    def update_actual_answer():
        actual_answer_entry.delete(0, tk.END)
        actual_answer_entry.insert(0, answer_var.get())

    # Display and pre-select the radio button if actual_answer has a value
    tk.Label(frame, text="Select the correct answer:", font=("Arial", 12)).pack(anchor='w', pady=10)
    
    radio_a = tk.Radiobutton(frame, text="A", variable=answer_var, value=question_data['answera'], command=update_actual_answer)
    radio_b = tk.Radiobutton(frame, text="B", variable=answer_var, value=question_data['answerb'], command=update_actual_answer)
    radio_c = tk.Radiobutton(frame, text="C", variable=answer_var, value=question_data['answerc'], command=update_actual_answer)
    radio_d = tk.Radiobutton(frame, text="D", variable=answer_var, value=question_data['answerd'], command=update_actual_answer)

    radio_a.pack(anchor='w')
    radio_b.pack(anchor='w')
    radio_c.pack(anchor='w')
    radio_d.pack(anchor='w')

    # Set the radio button based on actual_answer
    if question_data['actual_answer']:
        if question_data['actual_answer'] == question_data['answera']:
            radio_a.select()
        elif question_data['actual_answer'] == question_data['answerb']:
            radio_b.select()
        elif question_data['actual_answer'] == question_data['answerc']:
            radio_c.select()
        elif question_data['actual_answer'] == question_data['answerd']:
            radio_d.select()

    tk.Label(frame, text="Actual Answer", font=("Arial", 12)).pack(anchor='w', pady=10)
    actual_answer_entry.pack(pady=5)

    # Editable fields for hidden fields: book, regulation_table, image
    tk.Label(frame, text="Book", font=("Arial", 12)).pack(anchor='w')
    book_entry = tk.Entry(frame, width=150)
    book_entry.insert(0, question_data['book'])
    book_entry.pack(pady=5)

    tk.Label(frame, text="Regulation Table", font=("Arial", 12)).pack(anchor='w')
    regulation_table_entry = tk.Entry(frame, width=150)
    regulation_table_entry.insert(0, question_data['regulation_table'])
    regulation_table_entry.pack(pady=5)

    tk.Label(frame, text="Image", font=("Arial", 12)).pack(anchor='w')
    image_entry = tk.Entry(frame, width=150)
    image_entry.insert(0, question_data['image'])
    image_entry.pack(pady=5)

    def open_image():
        img_file = filedialog.askopenfilename(initialdir=image_folder, title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.gif")])
        if img_file:
            image_entry.delete(0, tk.END)
            image_entry.insert(0, img_file)

    tk.Button(frame, text="Open Image", command=open_image).pack(pady=5)

    # Navigation buttons to save changes and move to the next question
    def save_changes():
        # Save changes for the current question
        question_data['question'] = question_entry.get()
        question_data['answera'] = answera_entry.get()
        question_data['answerb'] = answerb_entry.get()
        question_data['answerc'] = answerc_entry.get()
        question_data['answerd'] = answerd_entry.get()
        question_data['actual_answer'] = actual_answer_entry.get()
        question_data['book'] = book_entry.get()
        question_data['regulation_table'] = regulation_table_entry.get()
        question_data['image'] = image_entry.get()

    # Save Changes Button
    tk.Button(frame, text="Save Changes", command=lambda: (save_changes(), save_test())).pack(pady=20)

    # Navigation Buttons
    if index + 1 < len(questions):
        tk.Button(frame, text="Next Question", command=lambda: (save_changes(), show_question(index + 1))).pack()

    if index - 1 >= 0:
        tk.Button(frame, text="Previous Question", command=lambda: (save_changes(), show_question(index - 1))).pack()

    # Delete Question Button
    tk.Button(frame, text="Delete Question", command=lambda: delete_question(index)).pack(pady=10)

# Function to delete the current question
def delete_question(index):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?"):
        del questions[index]
        if len(questions) > 0:
            new_index = index - 1 if index > 0 else 0
            show_question(new_index)
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            messagebox.showinfo("Info", "No more questions left.")
        save_test()

# Function to add a new question at the end of the list
def add_new_question():
    new_question = {
        'question': '',
        'answera': '',
        'answerb': '',
        'answerc': '',
        'answerd': '',
        'actual_answer': '',
        'book': '',
        'regulation_table': '',
        'image': ''
    }
    questions.append(new_question)
    show_question(len(questions) - 1)  # Show the new empty question

# Function to set up the GUI
def setup_gui():
    global root, frame

    root = tk.Tk()
    root.title("Test Editor")
    root.geometry("1600x1200")  # Set form size to 1600x1200

    # Allow the window to expand if necessary
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Create a frame to hold the content and center it
    frame = tk.Frame(root, bg='white')
    frame.pack(expand=True, fill='both', padx=50, pady=20)

    # Load Test button
    load_button = ttk.Button(root, text="Load Test", command=load_test)
    load_button.pack(pady=10)

    # Add New Question button
    add_question_button = ttk.Button(root, text="Add New Question", command=add_new_question)
    add_question_button.pack(pady=10)

    # Save Test button
    save_button = ttk.Button(root, text="Save Test", command=save_test)
    save_button.pack(pady=10)

    root.mainloop()

# Start the GUI setup
setup_gui()
