"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = list(list1)
    for index in range(len(list1) - 1):
        if list1[index] == list1[index +1]:
            new_list.remove(list1[index])
    return new_list

def intersect(lst1, lst2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = []
    index1 = 0
    index2 = 0
        
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] > lst2[index2]:
            index2 += 1
        elif lst1[index1] == lst2[index2]:
            intersection.append(lst1[index1])
            index1 += 1
            index2 += 1
        else:
            index1 += 1
            
    return intersection

# Functions to perform merge sort

def merge(lst1, lst2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    index1 = 0
    index2 = 0
    new_list = []
    while index1 <= len(lst1) and index2 <= len(lst2):
        if index1 == len(lst1):
            new_list.extend(lst2[index2:])
            index2 = len(lst2)
            index1 += 1
        elif index2 == len(lst2):
            new_list.extend(lst1[index1:])
            index1 = len(lst1)
            index2 += 1
        elif lst1[index1] < lst2[index2]:
            new_list.append(lst1[index1])
            index1 += 1
        else:
            new_list.append(lst2[index2])
            index2 += 1 
            
    return new_list

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return list1
    elif len(list1) == 1:
        return list1
    else:
        print
        return merge(merge_sort(list1[:len(list1) / 2]), merge_sort(list1[len(list1) / 2:])) 

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    
    if len(word) == 0:
        return [word]
    
    first = word[0]
    rest = word[1:]
    
    rest_strings = gen_all_strings(rest)
    all_strings = []
    
    for string in rest_strings:
        for index in range(len(string)) + [len(string)]:
            all_strings.append(string[:index] + first + string[index:])
        
    return rest_strings + all_strings


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    return [word[:-1] for word in netfile]
	
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
