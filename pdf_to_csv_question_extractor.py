import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfReader

# Function to load and scrape PDF content
def load_pdf():
    file_path = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            # Read the PDF
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Process the text to extract questions and answers using the selected format
            questions_data = extract_questions_format1(text) if format_var.get() == 1 else extract_questions_format2(text)

            if questions_data:
                offer_save(questions_data)
            else:
                messagebox.showerror("Error", "No questions found in the PDF.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF file: {str(e)}")

# Updated approach for extracting questions for format 1 ("Question X" format with multi-line questions)
def extract_questions_format1(text):
    # Split the text into blocks, where each block starts with "Question X"
    question_blocks = re.split(r'(Question\s+\d+)', text)
    
    questions = []
    
    # Iterate through every other element (skipping "Question X" label)
    for i in range(1, len(question_blocks), 2):
        question_number = question_blocks[i].strip()  # This is "Question X"
        question_block = question_blocks[i + 1].strip()  # The question text and answers

        # Split the question_block into individual lines
        lines = question_block.split("\n")
        
        # Initialize variables for question and answers
        question_lines = []
        answera = answerb = answerc = answerd = None

        # Process each line
        for line in lines:
            line = line.strip()  # Clean up the line

            # Check if the line starts with an answer option (a), b), etc.)
            if line.startswith('a)'):
                answera = clean_text(line.lstrip('a)'))
            elif line.startswith('b)'):
                answerb = clean_text(line.lstrip('b)'))
            elif line.startswith('c)'):
                answerc = clean_text(line.lstrip('c)'))
            elif line.startswith('d)'):
                answerd = clean_text(line.lstrip('d)'))
            else:
                # Otherwise, it's part of the question
                question_lines.append(line)

        # Join the question lines to form the full question text
        question_text = clean_text(' '.join(question_lines))

        # Store the extracted question and answers in a dictionary
        if question_text and answera and answerb and answerc and answerd:
            question = {
                'question': question_text,
                'answera': answera,
                'answerb': answerb,
                'answerc': answerc,
                'answerd': answerd,
                'actual_answer': '',  # Leave blank for now
                'book': '',           # Leave blank for now
                'regulation_table': '',  # Leave blank for now
                'image': ''  # Leave blank for now, to be added manually
            }
            questions.append(question)

    return questions

# Extract questions for format 2 (e.g., "1. <question>" format)
def extract_questions_format2(text):
    pattern = re.compile(
        r'\d+\.\s+(.+?)\s+a\)\s+(.+?)\s+b\)\s+(.+?)\s+c\)\s+(.+?)\s+d\)\s+(.+?)(?=\n\d+\.|\Z)', 
        re.DOTALL
    )

    matches = pattern.findall(text)

    questions = []
    for match in matches:
        question_text = clean_text(match[0])
        answera = clean_text(match[1])
        answerb = clean_text(match[2])
        answerc = clean_text(match[3])
        answerd = clean_text(match[4])

        question = {
            'question': question_text,
            'answera': answera,
            'answerb': answerb,
            'answerc': answerc,
            'answerd': answerd,
            'actual_answer': '',  # Leave blank for now
            'book': '',           # Leave blank for now
            'regulation_table': '',  # Leave blank for now
            'image': ''  # Leave blank for now, to be added manually
        }
        questions.append(question)
    
    return questions

# Function to clean up extracted text (remove excess whitespace and newlines)
def clean_text(text):
    return text.replace('\n', ' ').strip()

# Function to offer saving the questions in CSV format
def offer_save(questions_data):
    save_prompt = messagebox.askyesno("Save Questions", "Do you want to save the extracted questions as CSV?")
    
    if save_prompt:
        save_csv(questions_data)

# Function to save the questions to a CSV file, ensuring elements are in quotes
def save_csv(questions_data):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if save_path:
        try:
            # Writing questions to the CSV file
            with open(save_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['question', 'answera', 'answerb', 'answerc', 'answerd', 'actual_answer', 'book', 'regulation_table', 'image']
                writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

                writer.writeheader()
                for question in questions_data:
                    # Write each question and answers as a separate row
                    writer.writerow({
                        'question': question['question'],
                        'answera': question['answera'],
                        'answerb': question['answerb'],
                        'answerc': question['answerc'],
                        'answerd': question['answerd'],
                        'actual_answer': question['actual_answer'],
                        'book': question['book'],
                        'regulation_table': question['regulation_table'],
                        'image': question['image']  # Add the image path
                    })

            messagebox.showinfo("Success", "Questions saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {str(e)}")

# Set up the main window
root = tk.Tk()
root.title("PDF to CSV Question Extractor")

# Create a variable to store the selected format
format_var = tk.IntVar(value=1)

# Create the UI components
ttk.Label(root, text="Select Question Format:").pack(pady=10)
ttk.Radiobutton(root, text="Format 1 (Question X)", variable=format_var, value=1).pack(anchor='w', padx=20)
ttk.Radiobutton(root, text="Format 2 (Numbered Questions)", variable=format_var, value=2).pack(anchor='w', padx=20)

load_button = ttk.Button(root, text="Load PDF", command=load_pdf)
load_button.pack(pady=20)

# Start the main event loop
root.mainloop()
