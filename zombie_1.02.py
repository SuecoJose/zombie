# Zombie Project Thomas Lindholm
import math
from random import randint


def reset_game():
    """
    Resets the main game state variables to their initial state. Unsure if this is good or not
    """
    score = 0
    used_combination = []
    game_over = False
    game = True
    return score, used_combination, game_over, game


def print_debug(debug_msg):
    print(f"\033[31m{debug_msg}\033[0m")


def input_valid_str(question_txt, error_txt, possible_answers):
    answer = input(question_txt)
    while answer not in possible_answers or len(answer) < 1:
        answer = input(f'{error_txt}\n{question_txt}')
    return answer


def input_valid_int(question_txt, error_txt, min=0, max=math.inf):
    while True:
        try:
            value = int(input(question_txt))
            if min <= value <= max:
                return value
            else:
                print(error_txt)
        except (ValueError):
            print(error_txt)


def generate_question(operator, operand=0, max_repeats=0, used_values=''):
    """
    Generates a question and returns both operands and result
    """
    generate = True
    while generate:
        number_1 = randint(0, 12)
        print_debug(f'Used numbers: {used_values}, Generating number: {number_1}')
        if max_repeats == 0 and used_values.count(number_1) == 0:
            generate = False
        elif used_values.count(number_1) < max_repeats:
            generate = False

    if operator == '*':
        correct_answer = number_1 * operand
    elif operator == '//':
        correct_answer = number_1 // operand
    elif operator == '%':
        correct_answer = number_1 % operand

    return [number_1, operand, correct_answer]


def main():
    # Init variables
    score, used_combination, game_over, game = reset_game()
    new_game = True
    DEBUG = False  # Debug off by default
    #DEBUG = True
    zombie_door = 0


    # Debugging for generate question
    # questions=27
    # used_combination = [0,1,2,3,4,5,6,7,8,9,10,11,12,0,1,2,3,4,5,6,7,8,9,10,11]
    # used_combination = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # valid_repeats = 3 if questions > 26 else 2 if questions > 13 else 0
    # print(valid_repeats)
    # operand_1, operand_2, correct_answer = generate_question('*', 12. , valid_repeats, used_combination)
    # print(valid_repeats)
    # exit()

    while game:
        if new_game:
            input_error_message = 'Please input a valid answer'
            questions = input_valid_int('How many questions (12-39): ', input_error_message, 12, 39)

            # Sets max numbers of allowance for repeting questions
            valid_repeats = 3 if questions > 26 else 2 if questions > 13 else 0

            choosen_method = input_valid_str('Please choose method (*, //, %):', input_error_message, ['*', '//', '%'])

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
            zombie_door = randint(1, questions-score)

            # Need to send used combinations to avoid to ask same question to many times.
            operand_1, operand_2, correct_answer = generate_question(choosen_method, table_divisor, valid_repeats, used_combination)
            used_combination.append(operand_1)
            if DEBUG:
                print_debug(f'Zombie behind door {zombie_door}')
                print_debug(f'Answer is: {correct_answer}')
            answer = input_valid_int(f'What is {operand_1} {choosen_method} {operand_2} : ', input_error_message, -100)
            if answer == correct_answer:
                score += 1
                if questions == score:
                    print(f'Congrats you won the game')
                    game_over = True
                    new_game = True
                else:
                    print(f'Correct you have {score} point(s) and {questions-score} doors left to open')
                    choosen_door = input_valid_int(f'Choose a door between 1 and {questions-score+1} ,and hope there is no zombie behind: ', input_error_message, 1, questions-score+1)
                    if choosen_door != zombie_door:
                        print(f'Congrats no zombie behind door, zombie was behind door {zombie_door}')
                    else:
                        print('Sorry, the Zombie killed ya, Game over')
                        game_over = True
                        new_game = False
            else:
                print(f'Sorry that was not the correct answer, correct answer was {correct_answer}. Game over!')
                game_over = True
                new_game = False

        question = ""
        play_again = input_valid_str('Do you want to play again? (j/J/n/N):', input_error_message, ['j', 'J', 'n', 'N'])
        if play_again in 'jJ':
            score, used_combination, game_over, game = reset_game()
            # Check if user won or loose, reset params if won and let user choose again
        else:
            game = False

    print('Program terminates!')


main()
