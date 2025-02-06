from inspect import trace

import PySimpleGUI as sg
import ast  # To safely evaluate the list input

def arithmetic_arranger(problems, show_answers=False):
    # Step 1: input the problems and Check the number of problems
        #validation
    if len(problems) > 5:
        return 'Error: Too many problems.'

    # Initialize lists for each row of result
    first_value = []
    second_value = []
    lines = []
    results = []
    # Validate by iterating over each problem

    for problem in problems:
        # Split the problem into components
        left_value, operator, right_value = problem.split()

        # Step 2: Check if the operator is either '+' or '-'
        if operator not in ['+', '-']:
            return "Error: Operator must be '+' or '-'."

        # Step 3: Check if both values are digits
        if not (left_value.isdigit() and right_value.isdigit()):
            return 'Error: Numbers must only contain digits.'

        # Step 4: Check if each value is less than 4 digits long
        if len(left_value) > 4 or len(right_value) > 4:
            return 'Error: Numbers cannot be more than four digits.'

        # Find the width for alignment
        width = max(len(left_value), len(right_value)) + 2  # 2 extra spaces for operator

        # Format each component with right alignment
        first_value.append(left_value.rjust(width))
        second_value.append(operator + " " + right_value.rjust(width - 2))
        lines.append('-' * width)

        # Calculate the result if show_answers is True
        if show_answers:
            if operator == '+':
                result = str(int(left_value) + int(right_value))
            else:
                result = str(int(left_value) - int(right_value))
            results.append(result.rjust(width))

    # Combine each row with 4 spaces between problems
    arranged_problems = '    '.join(first_value) + '\n' + '    '.join(second_value) + '\n' + '    '.join(lines)

    # Add answers if requested
    if show_answers:
        arranged_problems += '\n' + '    '.join(results)


    return arranged_problems

#GUI setup
def get_list_input():
    # Define the layout
    layout = [
        [sg.Text("Enter your list of problems (e.g., '24 + 8515', '3801 - 2', '45 + 43')")],
        [sg.Multiline(size=(50, 10), key='-INPUT-', enter_submits=True)],
        [sg.Text("Show Answers?")],
        [
            sg.Radio("No", "R1", default=False, key='-SHOW-NO-'),
            sg.Radio("Yes", "R2", default=True, key='-SHOW-YES-'),
        ],

        [sg.Button("Submit"), sg.Button("Cancel"), sg.Button("Reset")]
    ]

    # Create the window
    window = sg.Window("Input List of Problems", layout)

    # Event loop to process events
    while True:
        event, values = window.read()
        if event == "Submit":
            input_text = values['-INPUT-'].strip()
            show_answers = values['-SHOW-YES-']  # Determine if "Yes" is selected
            try:
                # Safely parse the input as a Python list
                user_list = [problem.strip() for problem in input_text.split(',')]
                if isinstance(user_list, list):
                    #print(f"List entered: {user_list}")
                    break
                else:
                    sg.popup("Error: Please enter a valid list format.")
            except:
                sg.popup("Error: Please enter a valid list format.")

        if event == "Reset":
            window['-INPUT-'].update("")
            window['-SHOW-YES-'].update(value=True)
            window['-SHOW-NO-'].update(value=False)

        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break

    # Close the window
    return user_list, show_answers


# Call the function to get list input
def result_window(problems, show_answers):
    arranged_result = arithmetic_arranger(problems, show_answers)
    if "Error:" in arranged_result:
        sg.popup(arranged_result)
        return
    layout =[
        [sg.Text("Arranged Results:")],
        [sg.Multiline(arranged_result,size=(70,15), disabled=True, key = '-OUTPUT-' )],
        [sg.Button("Reset"), sg.Button("Exit")]
    ]
    window =sg.Window("Arithemetic Arranger Results", layout)

    while True:
        event, _ = window.read()
        if event == "Reset":
            window.close()
            main()
            break
        elif event in (sg.WINDOW_CLOSED, "Exit"):
            break
    window.close()

def main():
    problems, show_answers = get_list_input()
    if problems:
            result_window(problems, show_answers)


if __name__ == "__main__":
    main()
