"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""
import time
# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

# Global variable
python_dict = {}


def main():
    print(f'Welcome to stanCode "Anagram Generator" (or {EXIT} to quit)')
    count = 0
    while True:
        searching = case_insensitive(input('Find anagrams for: '))

        # Timer
        t1 = time.time()

        # read_dictionary
        read_dictionary(searching)

        # If -1, quit
        if searching == EXIT:
            break

        # Print
        print('Searching...')
        ans_lst = find_anagrams(searching)[0]
        for anagram in ans_lst:
            print('Found: ', anagram)
            print('Searching...')
        print(f'{len(ans_lst)} anagrams:', ans_lst)
        print(find_anagrams(searching)[1])
        # Timer
        t2 = time.time()
        print(t2-t1)


def check_dict_word(word, target):
    """
    Check dict word. If one character not in searching word, then not add the word to python_dict.
    :param word: str, word in dictionary.txt.
    :param target: str, the searching word
    :return: True, all character within are in searching word.
    """
    # Level one: check len
    if len(word) == len(target):
        # Check all the word: contains -> contains, contais
        for ch in word:
            if ch not in target:
                return False
            else:
                if ch == word[len(word)-1]:
                    return True


def read_dictionary(target):
    """
    Read the dictionary.txt and turn it into a list.
    :return: list, a python list.
    """
    count_dic_lst = [0]
    with open(FILE, 'r') as f:
        for line in f:
            word = line.strip()
            # All character within are in searching word
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


def find_anagrams(s):
    """
    :param s: str, searching word.
    :return: list, find all the anagram.
    """
    ans_lst = []
    count_lst = [0]
    duplicate_lst = []
    # Make the string become a list
    s_lst = []
    for i in s:
        s_lst.append(i)
    ans_len = len(s)
    # Sort the lst
    # s_lst.sort()
    # Helper
    helper(s_lst, '', ans_lst, ans_len, count_lst, duplicate_lst)
    return ans_lst, count_lst


def helper(word, anagram_word, ans_lst, ans_len, count_lst, duplicate_lst):
    """
    :param word: str, the searching word.
    :param anagram_word: str, anagram.
    :param ans_lst: list, all the anagrams.
    :param ans_len: int, the length of the original word.
    :param count_lst: list, count how many time helper has been called.
    :param duplicate_lst
    :return: list, all anagram.
    """
    count_lst[0] += 1

    if len(anagram_word) == ans_len:
        if len(anagram_word) > 2:
            if anagram_word in python_dict[anagram_word[:2]]:
                ans_lst.append(anagram_word)
    else:
        # Pruning
        if has_prefix(anagram_word):
            # Choose
            for i in range(len(word)):
                ch = word[i]
                # Pruning
                if duplicate(duplicate_lst, ch, anagram_word):
                    break
                word.pop(i)
                # Explore
                helper(word, anagram_word+ch, ans_lst, ans_len, count_lst, duplicate_lst)
                # Un-choose
                word.insert(i, ch)
                # Sort is to make append back to the original place to make it self-similar


            # for ch in word:
            #     anagram_word.append()


def has_prefix(sub_s):
    """
    Everytime add a ch to the str, check if the current str in dictionary.
    :param sub_s: The first few words from all the possible two-words from searching word.
    :return: True or False, No word in the dictionary starts with sub_s, vice versa.
    """
    # find everytime version
    if len(sub_s) <= 1:
        return True
    if len(sub_s) == 2:
        return sub_s in python_dict
    # Already confirm key in python_dict
    elif len(sub_s) > 2:
        checking_lst = python_dict[sub_s[:2]]
        for dict_word in checking_lst:
            if dict_word.startswith(sub_s):
                return True


def duplicate(duplicate_lst, ch, sub_s):
    """
    True means sub_s+ch is already run.
    :param duplicate_lst: list, the sub_s may be duplicated.
    :param ch: str, ch about to add into sub_s.
    :param sub_s: str, current_s.
    :return: True.
    """
    new_sub_s = sub_s+ch
    if new_sub_s in duplicate_lst:
        return True
    # If the word has the same element, add it to duplicate_lst
    elif ch in sub_s:
        duplicate_lst.append(new_sub_s)
        return False


def case_insensitive(string):
    """
    :param string: str, a character.
    :return: lst, a lower character lst.
    """
    new_string = ''
    for ch in string:
        if ch.islower():
            new_string += ch
        else:
            new_string += ch.lower()
    return new_string




if __name__ == '__main__':
    main()
