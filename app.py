from bs4 import BeautifulSoup

# Path to the HTML file
html_file_path = 'quiz.html'

# Read the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'lxml')

# Find all questions
questions = soup.find_all('div', class_='qt-mc-question')

# Loop through each question and extract the text and answers
i=0
for question in questions:
    question_text = question.find('div', class_='qt-question').get_text(strip=True)
    
    # Find all choices for the current question
    choices = question.find_all('div', class_='gcb-mcq-choice')
    answers = [choice.find('label').get_text(strip=True) for choice in choices]

    # Output the question and answers
    print("Question",i+1,": ", question_text)
    i=i+1
    print("Answers:")
    for answer in answers:
        print(answer)
    print()  # Add an empty line for better separation between questions

