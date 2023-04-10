import tkinter as tk
from PIL import ImageTk, Image
import os

import main

UNIT = 1
PART = 2

unit_lines = main.get_unit_lines(UNIT)
part_lines = main.get_part_lines(unit_lines, PART)
questions = main.get_questions(part_lines)

#a = [x for x in questions if 'Which ethnicity is displayed using the county-level scale map ' in x[0]]
#questions = [questions[0]]*2 + a + [questions[0]] + a + [questions[0]]*5 + a

root = tk.Tk()
root.title('iScore5 AP Human Geography')
root.geometry('1000x800')

######

total_correct = 0 
total_incorrect = 0
total = 0

question_num_var = tk.IntVar()
tk.Label(root, textvariable=question_num_var, bg="#FF0000", fg='#FFFF00').pack()

results_var = tk.StringVar()
tk.Label(root, textvariable=results_var).pack()

def submit_question():
    if question_choice.get() != -1:
        global total, total_correct, total_incorrect
        total += 1
        
        if all[question_choice.get()] in correct:
            total_correct += 1
        else:
            total_incorrect += 1
        
        update_question(question_num_var.get() + 1)

tk.Button(root, text='Submit', width=20, height=2, font=('Arial', 18), bg='#00FF00', command=submit_question).pack()

question_text_var = tk.StringVar()
tk.Label(root, textvariable=question_text_var, font=('Arial', 18, 'bold'), wraplength=1000).pack()


def get_image(name):
    image_a = Image.open(f'images/{name}')
    image_a_width, image_a_height = image_a.size
    image_ratio = image_a_width/image_a_height

    image_b_height = 200
    image_b_size = (int(image_b_height*image_ratio), int(image_b_height))
    return ImageTk.PhotoImage(image_a.resize(image_b_size))

images = {image: get_image(image) for image in os.listdir(path='images')}

choice_1_var = tk.StringVar()
choice_2_var = tk.StringVar()
choice_3_var = tk.StringVar()
choice_4_var = tk.StringVar()
choice_5_var = tk.StringVar()

question_choice = tk.IntVar()

tk.Radiobutton(root, textvariable=choice_1_var, variable=question_choice, value=0, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(root, textvariable=choice_2_var, variable=question_choice, value=1, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(root, textvariable=choice_3_var, variable=question_choice, value=2, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(root, textvariable=choice_4_var, variable=question_choice, value=3, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(root, textvariable=choice_5_var, variable=question_choice, value=4, font=('Arial', 18)).pack(anchor='w')

image_label = tk.Label(root); image_label.pack()

def update_question(question_num):
    if question_num < len(questions)+2:
        atotal = total if total != 0 else 1
        results_var.set(f'Correct: {total_correct}\tIncorrect: {total_incorrect}\tAnswered: {total}\tTotal Questions: {len(questions)}\tGrade: {round(total_correct/atotal*100, 2)}%')

    if question_num < len(questions)+1:
        global correct, incorrect, all, image_label
        question, image, correct, incorrect, all = main.get_question(questions[question_num-1])

        if len(image) != 0:
            image_label.pack()
            image_label.config(image=images[image[0]])
        else:
            image_label.pack_forget()

        question_num_var.set(question_num)

        question_text_var.set(question)

        question_choice.set(-1)

        choice_1_var.set(all[0])
        choice_2_var.set(all[1])
        choice_3_var.set(all[2])
        choice_4_var.set(all[3])
        choice_5_var.set(all[4])

update_question(1)

root.mainloop()