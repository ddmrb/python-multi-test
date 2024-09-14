import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# Global variables
questions = []
current_question = 0
correct_answers = 0
incorrect_questions = []
user_answers = []
image_label = None  # Store the image label globally

# Function to load the CSV file
def load_test():
    global questions, current_question, correct_answers, incorrect_questions, user_answers
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                questions = [row for row in reader]
                correct_answers = 0
                incorrect_questions.clear()
                user_answers.clear()
                current_question = 0
                root.title(f"Test Loader - {file_path}")
                show_question(current_question)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")

# Function to show a question
def show_question(index):
    global image_label

    if index >= len(questions):
        show_summary()  # Show the summary at the end of the test
        return

    # Clear the current content
    for widget in frame.winfo_children():
        widget.destroy()

    question_data = questions[index]

    # Add the question number and letter prefix to the question text
    question_number = f"Q{index + 1}. {question_data['question']}"

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

    # Show the question
    question_label = tk.Label(frame, text=question_number, wraplength=700, bg='white', font=("Arial", 14))
    question_label.pack(pady=10)

    # Create radio buttons for answers
    answer_var = tk.StringVar()
    answer_var.set(question_data['answera'])  # Set the first answer as the default

    for i, option in enumerate(['answera', 'answerb', 'answerc', 'answerd']):
        if question_data[option]:
            letter = chr(65 + i)  # Get 'A', 'B', 'C', 'D' based on index
            tk.Radiobutton(frame, text=f"{letter}. {question_data[option]}", variable=answer_var, value=question_data[option],
                           wraplength=700, font=("Arial", 12), bg='white').pack(anchor='w', padx=20, pady=5)

    # Create an OK button to move to the next question
    ok_button = ttk.Button(frame, text="OK", command=lambda: check_answer(index, answer_var.get()))
    ok_button.pack(pady=20)


# Function to check the answer
def check_answer(index, selected_answer):
    global correct_answers, incorrect_questions
    question_data = questions[index]
    actual_answer = question_data['actual_answer']
    book = question_data.get('book', 'N/A')  # Get 'book' or 'N/A' if not present
    regulation_table = question_data.get('regulation_table', 'N/A')  # Get 'regulation_table' or 'N/A'

    if selected_answer == actual_answer:
        messagebox.showinfo("Result", f"Correct!\n\nCorrect Answer: {actual_answer}\nBook: {book}\nRegulation Table: {regulation_table}")
        correct_answers += 1
        user_answers.append((index + 1, True))  # Mark question as correct
    else:
        messagebox.showinfo("Result", f"Incorrect.\n\nCorrect Answer: {actual_answer}\nBook: {book}\nRegulation Table: {regulation_table}")
        incorrect_questions.append(index)
        user_answers.append((index + 1, False))  # Mark question as incorrect

    # Move to the next question
    show_question(index + 1)


# Function to show the summary after the last question
def show_summary():
    global correct_answers, incorrect_questions

    total_questions = len(questions)
    incorrect_count = total_questions - correct_answers
    summary_message = f"Test Complete!\n\nCorrect Answers: {correct_answers}/{total_questions}\nIncorrect Answers: {incorrect_count}"

    # Ask if the user wants to review incorrect answers
    if incorrect_count > 0:
        retry = messagebox.askyesno("Review Incorrect Questions", f"{summary_message}\n\nWould you like to review the incorrect questions?")
        if retry:
            review_incorrect_questions()
        else:
            messagebox.showinfo("Test Completed", "Thank you for completing the test!")
    else:
        messagebox.showinfo("Test Completed", summary_message)

# Function to review the incorrectly answered questions
def review_incorrect_questions():
    if incorrect_questions:
        show_question(incorrect_questions.pop(0))  # Show the first incorrect question
    else:
        messagebox.showinfo("Review Completed", "You have reviewed all incorrect questions.")

# Function to set up the GUI
def setup_gui():
    global root, frame

    root = tk.Tk()
    root.title("Test Loader")
    root.geometry("1024x768")  # Set form size to 1024x768

    # Allow the window to expand if necessary
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Create a frame to hold the content and center it
    frame = tk.Frame(root, bg='white')
    frame.pack(expand=True, fill='both', padx=50, pady=20)

    # Load Test button
    load_button = ttk.Button(root, text="Load Test", command=load_test)
    load_button.pack(pady=10)

    root.mainloop()

# Start the GUI setup
setup_gui()
