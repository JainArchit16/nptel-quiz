import pdfplumber
import re
import os

def extract_questions_answers(pdf_path):
    quiz_data = []
    multi_line_question = ""  # To handle multi-line questions

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            question_pattern = re.compile(r'^\d+\)')  # Pattern for question number
            option_pattern = re.compile(r'^[A-D]\.')  # Pattern for options
            correct_pattern = re.compile(r'^Ans\.\s([A-D])=')  # Pattern for correct answer

            question, options, correct_answer = None, [], None

            for line in lines:
                line = line.strip()

                if question_pattern.match(line):  # New question detected
                    # Append the previous question to quiz_data if it is complete
                    if question and options and correct_answer:
                        quiz_data.append({
                            'question': question.strip(),
                            'options': options,
                            'correct_answer': correct_answer
                        })
                    # Reset and initialize for the new question
                    multi_line_question = line.strip()
                    question, options, correct_answer = None, [], None

                elif option_pattern.match(line):  # Options (A., B., C., D.)
                    if multi_line_question:
                        question = multi_line_question
                        multi_line_question = ""  # Reset the multi-line question buffer
                    options.append(line.strip())

                elif correct_pattern.match(line):  # Correct answer detected
                    correct_answer = correct_pattern.match(line).group(1)

                else:
                    # Continue concatenating multi-line questions
                    if multi_line_question and not option_pattern.match(line) and line:
                        multi_line_question += ' ' + line

            # Append the last question if it is complete
            if question and options and correct_answer:
                quiz_data.append({
                    'question': question.strip(),
                    'options': options,
                    'correct_answer': correct_answer
                })

    return quiz_data

def extract_from_multiple_pdfs(directory):
    all_quiz_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            all_quiz_data.extend(extract_questions_answers(pdf_path))
    return all_quiz_data

def run_quiz(quiz_data):
    score = 0
    for idx, entry in enumerate(quiz_data, 1):
        print(f"Question {idx}: {entry['question']}")
        for option in entry['options']:
            print(option)
        
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        
        if user_answer == entry['correct_answer']:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {entry['correct_answer']}\n")
    
    print(f"Quiz finished! Your score: {score}/{len(quiz_data)}")

# Example usage
directory_path = './questions' 
quiz_data = extract_from_multiple_pdfs(directory_path)
run_quiz(quiz_data)
