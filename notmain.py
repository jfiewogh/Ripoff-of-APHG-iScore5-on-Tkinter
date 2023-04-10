import random
import time

####
#UNIT = 1
#PART = 1
####

file = open('data.txt', 'r', encoding='utf-8')
lines = [x.strip() for x in file.readlines()]
file.close()

def get_unit_lines(unit_num):
	unit_name = f'U>{unit_num}'
	next_unit_name = f'U>{unit_num+1}'
	unit_index = lines.index(unit_name) if unit_name in lines else quit()
	next_unit_index = lines.index(next_unit_name) if next_unit_name in lines else len(lines)
	return lines[unit_index+1:next_unit_index]

def get_part_lines(unit_lines, part_num):
	part_name = f'P>{part_num}'
	next_part_name = f'P>{part_num+1}'
	part_index = unit_lines.index(part_name) if part_name in unit_lines else quit()
	next_part_index = unit_lines.index(next_part_name) if next_part_name in unit_lines else len(unit_lines)
	return unit_lines[part_index+1:next_part_index]

def get_questions(part_lines):
	questions_indexes = [i for i, x in enumerate(part_lines) if 'Q>' in x]
	questions = []
	for i, question_index in enumerate(questions_indexes):
		next_question_index = questions_indexes[i+1] if i != len(questions_indexes)-1 else len(part_lines) 
		question_lines = part_lines[question_index:next_question_index]
		questions.append(question_lines)
	random.shuffle(questions)
	return questions

#unit_lines = get_unit_lines(UNIT)
#part_lines = get_part_lines(unit_lines, PART)
#questions = get_questions(part_lines)

# line 147 of data.txt needs image
# 1.1.1 = 34 questions

def get_question(question_parts):
	question = question_parts[0].replace('Q>', '')
	correct_answers = [x.replace('Y>', '') for x in question_parts if 'Y>' in x]
	incorrect_answers = [x.replace('N>', '') for x in question_parts if 'N>' in x]
	image = [x.replace('I>', '') for x in question_parts if 'I>' in x]
	all_answers = correct_answers + incorrect_answers
	random.shuffle(all_answers)
	return question, image, correct_answers, incorrect_answers, all_answers

# correct, incorrect, total = 0, 0, 0

# start_time = time.time()

# for question_parts in questions:
# 	question, correct_answers, incorrect_answers, all_answers = get_question(question_parts)
	
# 	print('\n'.join([f'{i+1}. {x}' for i, x in enumerate(all_answers)]))
	
# 	asdf = int(input('Your answer (number): '))
# 	if all_answers[asdf-1] in correct_answers:
# 		print('Correct!')
# 		correct += 1
# 	else:
# 		print('Incorrect!')
# 		incorrect += 1
# 	total += 1

# 	print(f'{correct}/{total} ({round(correct/total*100, 2)}%)')
# 	total_time = time.time() - start_time
# 	print(f'{round(total_time, 3)} {round(total_time/total, 3)}\n')


#print('\n'.join([str(x) for x in questions]))