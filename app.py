from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Global variables
questions = []
current_question_index = 0
correct_answers = 0
incorrect_questions = []
submitted_answer = None  # Track the submitted answer

# Path to the directory containing the CSV test files
TESTS_DIR = os.path.join('static', 'tests')

# Load the test from a selected CSV file
def load_test(file_name):
    global questions, correct_answers, incorrect_questions, current_question_index, submitted_answer
    file_path = os.path.join(TESTS_DIR, file_name)
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            questions = [row for row in reader]
        correct_answers = 0
        incorrect_questions.clear()
        current_question_index = 0
        submitted_answer = None
    except Exception as e:
        print(f"Error loading CSV file: {e}")

# Route to the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the selected file name from the form
        file_name = request.form['file_name']
        load_test(file_name)
        return redirect(url_for('question', index=0))
    
    # List all CSV files in the static/tests directory
    csv_files = [f for f in os.listdir(TESTS_DIR) if f.endswith('.csv')]
    return render_template('index.html', csv_files=csv_files)

# Route to display a question
@app.route('/question/<int:index>', methods=['GET', 'POST'])
def question(index):
    global current_question_index, correct_answers, incorrect_questions, submitted_answer
    if index >= len(questions):
        return redirect(url_for('summary'))

    current_question_index = index
    question_data = questions[index]

    if request.method == 'POST':
        submitted_answer = request.form.get('answer')
        actual_answer = question_data['actual_answer']

        # Check if the answer is correct
        if submitted_answer == actual_answer:
            correct_answers += 1
        else:
            incorrect_questions.append(index)

        # Render the same question page with the submitted answer and correct info
        return render_template('question.html', question=question_data, index=index, submitted=True, selected_answer=submitted_answer)

    # Render the question page without any submitted answer
    return render_template('question.html', question=question_data, index=index, submitted=False)

# Route to display the summary at the end of the test
@app.route('/summary')
def summary():
    total_questions = len(questions)
    incorrect_count = total_questions - correct_answers
    return render_template('summary.html', correct_answers=correct_answers, total_questions=total_questions, incorrect_count=incorrect_count)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
