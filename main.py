import tkinter as tk
from PIL import ImageTk, Image
import os
from pygame import mixer
import notmain

mixer.init()
correct_sound = 'sounds/correct.wav'
wrong_sound = 'sounds/wrong.wav'

###### SETUP ######

root = tk.Tk()
root.title('iScore5 AP Human Geography')
root.geometry('1000x800')

start_page = tk.Frame(root)
start_page.pack()

choose_questions = tk.Frame(start_page)
choose_questions.pack()

unit_select_buttons = [True]*7
chosen = {}

def click_unit(unit):
	for checkbutton in chosen[unit]:
		checkbutton.set(1 if unit_select_buttons[unit-1] else 0)
	unit_select_buttons[unit-1] = not unit_select_buttons[unit-1]

def create_unit_select(y):
	tk.Button(choose_questions, text=f'Unit {y+1}', command=lambda: click_unit(y+1)).grid(row=0, column=y)
	chosen[y+1] = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

	part_buttons = []
	for x in range(4):
		part_button = tk.Checkbutton(choose_questions, text=x+1, variable=chosen[y+1][x], onvalue=1, offvalue=0)
		part_button.grid(row=x+1, column=y)
		part_buttons.append(part_button)

## create unit select
for y in range(7):
	create_unit_select(y)

def get_unit_part_questions(unit, part):
	return notmain.questions(unit, part)


def get_the_questions():
	global questions
	questions = []
	for unit, parts in chosen.items():
		unit_lines = notmain.get_unit_lines(unit)
		for i, part in enumerate(parts):
			if part.get() == 1:
				part_lines = notmain.get_part_lines(unit_lines, i+1)
				questions += notmain.get_questions(part_lines)


quiz_page = tk.Frame(root)


def start_button():
	global total_correct, total_incorrect, total
	total_correct, total_incorrect, total = 0, 0, 0
	
	get_the_questions()

	start_page.pack_forget()
	quiz_page.pack()

	update_question(1)


tk.Button(start_page, text='Start', command=start_button).pack()

######

question_num_var = tk.IntVar()
tk.Label(quiz_page, textvariable=question_num_var, bg="#FF0000", fg='#FFFF00').pack()

results_var = tk.StringVar()
tk.Label(quiz_page, textvariable=results_var).pack()


def submit_question():
	if question_choice.get() != -1:
		global total, total_correct, total_incorrect
		total += 1

		if all[question_choice.get()] in correct:
			total_correct += 1
			mixer.music.load(correct_sound)
		else:
			total_incorrect += 1
			mixer.music.load(wrong_sound)
		mixer.music.play()

		update_question(question_num_var.get() + 1)


tk.Button(quiz_page, text='Submit', width=20, height=2, font=('Arial', 18), bg='#00FF00', command=submit_question).pack()

question_text_var = tk.StringVar()
tk.Label(quiz_page, textvariable=question_text_var, font=('Arial', 18, 'bold'), wraplength=1000).pack()


def get_image(name, height=300):
	image_a = Image.open(f'images/{name}')
	image_a_width, image_a_height = image_a.size
	image_ratio = image_a_width / image_a_height

	image_b_size = (int(height * image_ratio), int(height))
	return ImageTk.PhotoImage(image_a.resize(image_b_size))


images = {image: get_image(image) for image in os.listdir(path='images')}

choice_1_var = tk.StringVar()
choice_2_var = tk.StringVar()
choice_3_var = tk.StringVar()
choice_4_var = tk.StringVar()
choice_5_var = tk.StringVar()

question_choice = tk.IntVar()

tk.Radiobutton(quiz_page, textvariable=choice_1_var, variable=question_choice, value=0, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(quiz_page, textvariable=choice_2_var, variable=question_choice, value=1, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(quiz_page, textvariable=choice_3_var, variable=question_choice, value=2, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(quiz_page, textvariable=choice_4_var, variable=question_choice, value=3, font=('Arial', 18)).pack(anchor='w')
tk.Radiobutton(quiz_page, textvariable=choice_5_var, variable=question_choice, value=4, font=('Arial', 18)).pack(anchor='w')

image_label = tk.Label(quiz_page)
image_label.pack()


def update_question(question_num):
	if question_num == len(questions):
		quiz_page.pack_forget()
		start_page.pack()

	if question_num < len(questions) + 2:
		atotal = total if total != 0 else 1
		results_var.set(f'Correct: {total_correct}\tIncorrect: {total_incorrect}\tAnswered: {total}\tTotal Questions: {len(questions)}\tGrade: {round(total_correct/atotal*100, 2)}%')

	if question_num < len(questions) + 1:
		global correct, incorrect, all, image_label
		question, image, correct, incorrect, all = notmain.get_question(
		 questions[question_num - 1])

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


#update_question(1)

root.mainloop()
