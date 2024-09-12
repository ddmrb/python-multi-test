install python

1. https://www.python.org/downloads/windows/
2. Click on the link to --- Latest Python 3 Release - Python ......
3. Scroll to the bottom of the page and click on the link --- Windows installer (64-bit)
4. After it downloads open the downloads folder and right click the file python.....exe and choose run as administrator.
5. Select add python.exe to Path and click customize installation
6. When you get to advanced options select Install python 3.12 for all users
7. Once complete close any cmd or powershell windows
8. Copy all pdf tests that you want to convert to compatible tests into the python-elect-test folder.
8. run the following in a new admin cmd windows --   pip install pillow PyPDF2


Importing new pdfs
-------------------
To import a new pdf to convert to a compatible test double click file "pdf_to_csv_question_extractor.bat".
When the window opens you need to choose either format 1 or format 2.
To determine the format , open the pdf you want to import and check the first question.
If it looks like this then choose format 1:

Question 1 
To which of the following situations does BS 7671 apply? 
a) manufacture of Electrical Equipment
b) inspection and testing of the electrical installation on oil rigs
c) design of an electrical installation for a floor heating system
d) public electricity supply system

IF it looks like this then choose format 2:

1. To which of the following situations does BS 7671 apply? 
a) manufacture of Electrical Equipment
b) inspection and testing of the electrical installation on oil rigs
c) design of an electrical installation for a floor heating system 
d) public electricity supply system

CLick load pdf to open another explorer windows and select the relevant pdf and click open.
Click Yes to Save the extracted questions as a CSV
Provide a relevant name for your test and click save.
You should see a final dialog that states success - questions saved successfully.
Click OK and repeat for all other pdfs you wish to import.
To close the import tool click the x.

Adding answers to the imported tests
------------------------------------

DO NOT edit files manually as this will corrupt the file format.

1. Double click "test_editor.bat".
2. Click load test button and select/open the test file you want to edit. All questions answers are editable.
3. If the actual answer is empty then select the corect answer as inicated to fill the empty text box with the correct value.
4. Click save changes to save the change to the file. You may also wait until you have edited all questions before clicking save text button at the very bottom of the form.
5. You can move through the questions by using the next question and previous question buttons.
6. To delete a question, find the relevant question and click delete. The change will be auto saved if you select yes to the prompt to delete.

Running a test
--------------
1. Double click TESTME.bat
2. Click the "Load Test" button.
3. Select any of the test files (csv file extension), select and click "Open" to start the test.

By default each question will have the first answer selected.
Whether you answer correctly or incorrectly a dialog will popup and display the correct answer along with any relevant info e.g. the relevant book, the regulation, page and/or table etc


