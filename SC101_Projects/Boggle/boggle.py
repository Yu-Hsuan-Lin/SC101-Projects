"""
File: boggle.py
Name:
----------------------------------------
TODO:
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
python_dict = {}
boggle_lst = []
boggle_ch_lst = []
head_lst = []
ans_lst = []  # For some time different chs comprise the same word.

import time


def main():
	"""
	TODO: Find all the words in the boggle.
	"""
	word_count = [0]
	# Read input
	for i in range(4):
		row = input(f'{i+1} row of letters: ')
		if not legal_input(row):
			print('Illegal input')
			break
		create_boggle_lst(row)
	t1 = time.time()
	# Start to run boggle
	# Choose the first character
	read_dictionary(boggle_ch_lst)
	for y in range(len(boggle_lst)):
		for x in range(len(boggle_lst[0])):
			word = ''
			cor_run = []  # Store tuple of cor already run
			check = [0]
			find_boggle(x, y, word, cor_run, check, word_count, ans_lst)
	print(f'There are {word_count[0]} words in total.')
	t2 = time.time()
	print(t2-t1)


def find_boggle(x, y, word, cor_run, one_means_not_1st, word_count, ans_lst):
	"""
	Start from one word, then re-run.
	:param cor_run:
	:return:
	"""
	# If all the next word has been choose
	if word == '' and one_means_not_1st[0] == 1:
		return
	else:
		# Choose the next character
		for y_co in range(y - 1, y + 2):
			# Check if the cor is legal: within 0-4
			if 0 <= y_co < len(boggle_lst[0]):
				for x_co in range(x - 1, x + 2):
					# Check if the cor is legal: within 0-4
					if 0 <= x_co < len(boggle_lst):
						cor_set = (x_co, y_co)
						if not head_has_been_run(word, head_lst, cor_set):
							if word == '':
								head_lst.append((x_co, y_co))
							# Choose the one hasn't be run yet
							if cor_set not in cor_run:
								# Choose
								ch = boggle_lst[y_co][x_co]
								if has_prefix(word + ch):  # make sure word = '' or one word
									if len(word+ch) >= 4:
										if is_dict_word(word+ch):
											if word+ch not in ans_lst:
												ans_lst.append(word+ch)
												print(f'Found "{word+ch}"')
												word_count[0] += 1
									cor_run.append(cor_set)
									# Explore
									find_boggle(x_co, y_co, word+ch, cor_run, one_means_not_1st, word_count, ans_lst)
									# Un-choose
									cor_run.pop()
	one_means_not_1st[0] += 1


def is_dict_word(word):
	for dict_word in python_dict[word[:2]]:
		if word == dict_word:
			return True


def head_has_been_run(word, run_head_lst, cor_tuple):
	if (word == '') and (cor_tuple in run_head_lst):
		return True
	return False


def create_boggle_lst(row):
	"""
	Create boggle lst and boggle ch lst.
	:param row: str, a row in the boggle.
	:return: lst, boggle_lst and boggle_ch_lst.
	"""
	# Read row to lst
	row_lst = row.split(' ')
	row_lst = case_insensitive(row_lst)
	# Create boggle list
	boggle_lst.append(row_lst)
	# Create boggle_ch_lst
	for ch in row_lst:
		boggle_ch_lst.append(ch)


def legal_input(input_w):
	"""
	:param input_w: string, row.
	:return: True, if all are legal format.
	"""
	if len(input_w) != 7:
		return False
	for i in range(len(input_w)):
		if i % 2 == 0:
			if not input_w[i].isalpha():
				return False
		elif i % 2 != 0:
			if input_w[i] != ' ':
				return False
		if i == len(input_w)-1:
			return True


def read_dictionary(target):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python dict
	"""
	count_dic_lst = [0]
	with open(FILE, 'r') as f:
		for line in f:
			word = line.strip()
			# All character within are in boggle
			if check_dict_word(word, target):
				# Create key for dict
				if len(word) == 1:  # One character
					dict_key = word
				else:
					dict_key = word[0:2]  # The first two word
				# Add word to python_dict
				if dict_key in python_dict:
					python_dict[dict_key].append(word)
				else:
					python_dict[dict_key] = [word]
	return python_dict


def check_dict_word(word, target_lst):
	"""
	Check dict word. If one character not in searching word, then not add the word to python_dict.
	:param word: str, word in dictionary.txt.
	:param target: str, the searching word
	:return: True, all character within are in searching word.
	"""
	# Level one: check len
	if 4 <= len(word) <= len(target_lst):
		# Check all the word: contains -> contains, contais
		for ch in word:
			if ch not in target_lst:
				return False
			else:
				if ch == word[len(word)-1]:
					return True


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	# find everytime version
	if len(sub_s) == 1:
		return True
	elif len(sub_s) == 2:
		return sub_s in python_dict
	# Already confirm key in python_dict
	elif len(sub_s) > 2:
		checking_lst = python_dict[sub_s[:2]]
		for dict_word in checking_lst:
			if dict_word.startswith(sub_s):
				return True


def case_insensitive(ch_lst):
	"""
	:param ch_lst: lst, a character.
	:return: lst, a lower character lst.
	"""
	new_lst = []
	for ch in ch_lst:
		if ch.islower():
			new_lst.append(ch)
		else:
			new_lst.append(ch.lower())
	return new_lst


if __name__ == '__main__':
	main()
