# Zombie Project Thomas Lindholm
import math
from random import randint

def input_valid_str(question_txt, error_txt, possible_answers):
    answer = input(question_txt)
    while answer not in possible_answers or len(answer) < 1:
        answer = input(f'{error_txt}\n{question_txt}')
    return answer


def input_valid_int(question_txt, error_txt, min=0, max=math.inf):
    while True:  # Loopa tills korrekt värde skrivs in
        str = input(question_txt)
        if str.isdigit() and min <= int(str) <= max:
            return int(str)  # Korrekt tal, returnera värdet
        print(error_txt)


def play_again(question_txt, error_txt, possible_positive_answers):
    answer = input(question_txt)
    if answer in possible_positive_answers:
        return True
    else:
        return False


def place_zombie(lowest, highest, opened_doors=''):
    # Use Opened Doors to know which doors that cannot be used again
    # To be implemented in a later stage
    zombie = randint(lowest, highest)
    return zombie


def generate_question(operator, operand=0, max_repeats=0, used_values=''):
    """
    Generates a question and returns both operands and result
    """
    generate = True
    while generate:
        number_1 = randint(1, 99)
        if used_values.count(number_1) < max_repeats+1:
            generate = False

    if operator == '*':
        correct_answer = number_1 * operand
    elif operator == '//':
        correct_answer = number_1 // operand
    elif operator == '%':
        correct_answer = number_1 % operand

    return [number_1, operand, correct_answer]


def main():
    game = True
    opened_doors, used_combination = [], []
    zombie_door = 0
    score = 0
    game_over = False
    new_game = True

    DEBUG = False

    while game:
        if new_game:
            input_error_message = 'Please input a valid answer'
            questions = input_valid_int('How many questions (12-39): ',input_error_message, 12, 39)

            # Sets max numbers of allowance for repeting questions
            valid_repeats = 3 if questions > 27 else 2 if questions > 14 else 0

            choosen_method = input_valid_str('Please choose method (*, //, %):', input_error_message, '*, //, %')

            if choosen_method == '*':
                table_divisor = input_valid_int(f'Choose table (2-12): ', input_error_message, 2, 12)
            else:
                table_divisor = input_valid_int(f'Choose divisor (2-5): ', input_error_message, 2, 5)
        else:
            print('Okay, let\'s give it a new try')
        game = False

        print(f'Starting new game with {questions}, method: {choosen_method} and table/divisor {table_divisor}')
        if valid_repeats > 0:
            print(f'Questions are not allowed to be repeated more than {valid_repeats} times')
        else:
            print(f'Questions should not be repeated at all')
        print(f'Theres a zombie between one of the {questions} doors, do your best to avoid it')
        while not game_over:
            print('')
            zombie_door = place_zombie(1, questions-score)

            # Need to send used combinations to avoid to ask same question to many times.
            operand_1, operand_2, correct_answer = generate_question(choosen_method, table_divisor, valid_repeats, used_combination)
            used_combination.append(operand_1)
            answer = input_valid_int(f'What is {operand_1} {choosen_method} {operand_2} : ',input_error_message,1)
            if answer == correct_answer:
                score += 1
                if questions == score:
                    print(f'Congrats you won the game')
                    game_over = True
                    new_game = True
                else:
                    print(f'Correct you have {score} point(s) and {questions-score} doors left to open')
                    choosen_door = input_valid_int(f'Choose a door between 1 and {questions-score+1} ,and hope there is no zombie behind ', input_error_message, 1, questions-score+1)
                    if choosen_door != zombie_door:
                        print(f'Congrats no zombie behind door, zmbie was behind door {zombie_door}')
                    else:
                        print('Sorry, the Zombie killed ya, Game over')
                        game_over = True
                        new_game = False
            else:
                print(f'Sorry that was not the correct answer, correct answer was {correct_answer}. Game over!')
                game_over = True
                new_game = False

        question = ""
        if play_again('Do you want to play again? (j/n)', input_error_message, 'j, J'):
            game_over = False
            game = True
            score = 0
            opened_doors, used_combination = [], []
            # Check if user won or loose, reset params if won and let user choose again

    print('Program terminates!')


main()
