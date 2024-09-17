import re
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PyPDF2 import PdfReader

# Function to load and scrape input content
def load_input():
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")])
    if file_path:
        try:
            # Read the content based on selected file type
            if file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

            # Process the text to extract questions and answers using the selected format
            if format_var.get() == 1:
                questions_data = extract_questions_format1(text)
            elif format_var.get() == 2:
                questions_data = extract_questions_format2(text)
            elif format_var.get() == 3:
                questions_data = extract_questions_format3(text)

            if questions_data:
                offer_save(questions_data)
            else:
                messagebox.showerror("Error", "No questions found in the input file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load input file: {str(e)}")

# Extract questions for format 1 ("Question X" format with multi-line questions)
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

# Extract questions for format 2 ("1. <question>" format)
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
            'actual_answer': '',
            'book': book_entry.get(),  # Get book value from input
            'regulation_table': '',
            'image': ''
        }
        questions.append(question)

    return questions

# Extract questions for format 3 (text file with "Q2)" format)
def extract_questions_format3(text):
    # Split the text into blocks using the question numbering format "Q<number>)"
    question_blocks = re.split(r'(Q\d+\))', text)
    questions = []

    # Iterate through every other element (skipping "Q<number>)" label)
    for i in range(1, len(question_blocks), 2):
        question_number = question_blocks[i].strip()
        question_block = question_blocks[i + 1].strip()

        answera = answerb = answerc = answerd = regulation_table = question_text = question_match = None

      # Use regular expression to extract the question text (from start to first "a)")
        question_match = re.search(r'(.+?)\s+a\)', question_block, re.DOTALL)
        if question_match:
            question_text = clean_text(question_match.group(1))
        else:
            question_text = ""



        # Use regular expression to extract the regulation table (from after "d)" to the end)
        regulation_table_match = re.search(r'd\)\s*.+?\n\s*rt\)\s*(.+)', question_block, re.DOTALL)
        regulation_table = clean_text(regulation_table_match.group(1)) if regulation_table_match else ""

        # Split the question_block into individual lines
        lines = question_block.split("\n")


        # Process each line
        for line in lines:
            line = line.strip()
            if line.startswith('a)'):
                answera = clean_text(line.lstrip('a)'))
            elif line.startswith('b)'):
                answerb = clean_text(line.lstrip('b)'))
            elif line.startswith('c)'):
                answerc = clean_text(line.lstrip('c)'))
            elif line.startswith('d)'):
                answerd = clean_text(line.lstrip('d)'))

        if question_text and answera and answerb and answerc and answerd:
            question = {
                'question': question_text,
                'answera': answera,
                'answerb': answerb,
                'answerc': answerc,
                'answerd': answerd,
                'actual_answer': '',
                'book': book_entry.get(),  # Get book value from input
                'regulation_table': regulation_table if regulation_table else '',
                'image': ''
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
            with open(save_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['question', 'answera', 'answerb', 'answerc', 'answerd', 'actual_answer', 'book', 'regulation_table', 'image']
                writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                for question in questions_data:
                    writer.writerow({
                        'question': question['question'],
                        'answera': question['answera'],
                        'answerb': question['answerb'],
                        'answerc': question['answerc'],
                        'answerd': question['answerd'],
                        'actual_answer': question['actual_answer'],
                        'book': question['book'],
                        'regulation_table': question['regulation_table'],
                        'image': question['image']
                    })
            messagebox.showinfo("Success", "Questions saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {str(e)}")

# Set up the main window
root = tk.Tk()
root.title("PDF/Text to CSV Question Extractor")

# Create a variable to store the selected format
format_var = tk.IntVar(value=1)

# Create the UI components
ttk.Label(root, text="Select Question Format:").pack(pady=10)
ttk.Radiobutton(root, text="Format 1 (Question X)", variable=format_var, value=1).pack(anchor='w', padx=20)
ttk.Radiobutton(root, text="Format 2 (Numbered Questions)", variable=format_var, value=2).pack(anchor='w', padx=20)
ttk.Radiobutton(root, text="Format 3 (Q<number>) Text File)", variable=format_var, value=3).pack(anchor='w', padx=20)

# Add a text input field for the "book" value
ttk.Label(root, text="Enter Book Value:").pack(pady=5)
book_entry = ttk.Entry(root, width=50)
book_entry.pack(pady=5)

load_button = ttk.Button(root, text="Load Input", command=load_input)
load_button.pack(pady=20)

# Start the main event loop
root.mainloop()
