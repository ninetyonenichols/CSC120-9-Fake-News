'''
File: fake-news.py
Author: Justin Nichols
Purpose: Finds the most frequent words in the headlines of articles.
         Organizes them by count (descending order).
Prints out the n-most-frequent, where n is determined by user input.
CSC120, Section 1, Fall 18
'''


import sys
import csv
import string


HEADLINE_INDEX = 4
TRIVIAL_WORD_LENGTH = 2


class LinkedList:
    def __init__(self):
        '''
        Purpose: creates a ll-object that will be used to store info about the
                 frequency of different words in article headlines
        Init'd Attributes: _head, the head of the ll. Init'd as 'None.' May
                           eventually become a Node-obj
        '''
        self._head = None
        
    
    def sort(self):
        '''
        Purpose: sort the nodes in the list by count (descending order)
        '''
        
        # if linked-list is empty, terminating immediately
        if self._head == None:
            return
        
        sorted_ll = LinkedList()
        curr = self._head

        # making sure still in original linked list
        while curr != None:
            removed_node = self.remove()
            removed_count = removed_node.count()

            # case removed node goes at head of sorted list
            if (sorted_ll._head == None) or \
               (removed_count >= sorted_ll._head.count()):
                sorted_ll.add(removed_node)

            # case when removed node goes somewhere besides the head of the
            #     sorted list
            else:
                curr_sorted = sorted_ll._head
                # iterating over sorted list to determine where to place
                #     current value
                while curr_sorted != None:

                # case when current element in sorted list is not the last
                    if curr_sorted.next() != None:

                        # aux vars
                        next_sorted = curr_sorted.next()
                        next_count_sorted = next_sorted.count()

                        # inserting new value
                        if removed_count >= next_count_sorted: 
                            sorted_ll.insert(curr_sorted, removed_node)
                            break
    
                            
                    # case when current element in sorted list is the last
                    else:
                        sorted_ll.insert(curr_sorted, removed_node)
                        break
                    
                    curr_sorted = curr_sorted.next()
                    
            curr = self._head
            
        self._head = sorted_ll._head
    
    # Note: this method was copied over from the short problem
    def add(self, node):
        '''
        Purpose: adds a Node-obj to the head of the ll
        Argument: node, the Node-obj to be added.
        '''
        node._next = self._head
        self._head = node
        
    # Note: this method was copied over from the short problem
    def remove(self):
        '''
        Purpose: removes the first node from the ll.
        Returns: the node that was removed ends up being the return-value
        '''
        assert self._head != None
        _node = self._head
        self._head = _node._next
        _node._next = None
        return _node
    
    # Note: this method was copied over from the short problem
    def insert(self, node1, node2):
        '''
        Purpose: inserts node2 after node1
        Arguments: node2, the Node-obj to be inserted
                   node1, the Node-obj that node2 gets inserted after.
        '''
        assert node1 != None
        node2._next = node1._next
        node1._next = node2


    def is_empty(self):
        '''
        Returns: 'True' if ll is empty, 'False' otherwise
        '''
        return self._head == None


    def update_count(self, word):
        '''
        Purpose: Creates Node-obj for word if it doesn't already exist.
                 Otherwise, updates count
        Arguments: word, a str. The word mentioned above
        '''
        if self.is_empty():
            word_node = Node(word)
            self.add(word_node)
            return

        curr = self._head
        while curr != None:
            # case when appropriate node already exists
            if curr.word() == word:
                curr.incr()
                return
            prev = curr
            curr = curr.next()
        # case when appropriate node does not already exist
        # at this point, 'prev' will be the last node in the linked list
        word_node = Node(word)
        self.insert(prev, word_node)


    def get_nth_highest_count(self, n):
        '''
        Purpose: returns the count of the nth word in the sorted ll
        Argument: n, an int.
        Pre-Conditions: ll must already be sorted by count(descending order).
                        The 'sort' method will take care of this
        '''
        assert n >= 0

        # handling the empty ll
        if self._head == None:
            return 0
        i = 1
        curr = self._head
        next_node = curr.next()

        # in this loop, current node is not the last in the ll
        while (i < n + 1) and (next_node != None):
            i += 1
            curr = curr.next()
            next_node = curr.next()
            
        # Invariant: either i == n or next_node == None

        # if i == n, then curr is the node with the nth hightest count
        if i == n + 1:
            return curr.count()
        
        # if i != n, then no such node exists. 0 is returned so that nothingis
        #     printed later
        return 0
        

    def print_upto_count(self, k):
        '''
        Purpose: prints all words with count >= k
        Argument: k, a positive int.
        Pre-Condition: 'self' must be sorted prior to calling this method.
                       The 'sort' method will take care of this.
        '''
        curr = self._head
        if curr == None:
            return

        # iterating up to appropriate node (if it exists) or end of ll (otherwise)
        while (curr.count() >= k) and (curr.next() != None):
            print("{} : {:d}".format(curr.word(), curr.count()))
            curr = curr.next()

        # Invariant: either curr.count() < k or curr.next() == None

        # if appropriate node exists, printing out appropriate word and count
        if (curr.next() == None) and (curr.count() >= k):
            print("{} : {:d}".format(curr.word(), curr.count()))

            
    # getters
    def head(self):
        return self._head


    # Note: this method was copied over from the short problem
    def __str__(self):
        string = 'List[ '
        curr_node = self._head
        while curr_node != None:
            string += str(curr_node)
            curr_node = curr_node.next()
        string += ']'
        return string


class Node:
    def __init__(self, word):
        '''
        Purpose: creates a Node-obj that will store info about a word
        Arguments: word, a str that represents the word in question.
        Init'd Attributes: _word, the str mentioned above.
                           _count, the number of times that 'word' has occurred
                               so far in the headlines
                           _next, the next node in the ll. Init'd to 'None'
        '''
        self._word = word
        self._count = 1
        self._next = None


    # getters
    def word(self):
        return self._word

    def count(self):
        return self._count
    
    def next(self):
        return self._next
    

    # setters
    def set_next(self, target):
        self._next = target

    def incr(self):
        self._count += 1


    def __str__(self):
        return "{} : {:d} -> ".format(self.word(), self.count())


def parse_csv_file():
    '''
    Purpose: accepts (as input) the name of a csv-file.
             If possible, opens the file and uses csv.reader to return an
                 iterable-object containing lists (where each list contains
                 info about one headline)
             The first list contains no info about any headline and will be
                 deleted (later, in a different function)Since this code is so
                 short and not actually parsing the csv, you can just do it in main.
             Input statements in main are fine
    Returns: the iterable-object described above
    '''
    infile_name = input('File: ')
    try:
        infile_it_obj = open(infile_name)
    except FileNotFoundError:
        print("ERROR: Could not open file " + infile_name)
        sys.exit(1)
    
    return csv.reader(infile_it_obj)


def clean_headlines_update_counts(infile_it_obj, counts_ll):
    '''
    Purpose: removes all punctuation from every word in the collection of
             headlines being considered and updates their counts in the ll
             (there is a method 'update_counts' specifically for this
             latter part. See its documentation for more info)
    Arguments: infile_it_object. This is the file that was provided (by the
                   user-input), except now in iterable-object form
                   counts_ll, a linked-list. Keeps track of the counts of different
                   words that appeared in the collection of headlines
    Post-Condition: counts_ll now has a node for each word that appeared in any
                    headline, along with a count of the number of times that the
                    word occured (running total of appearances across all
                    headlines)
    '''
    headlines_list = []

    # getting rid of first line in file, which contains no information about
    #     any article
    infile_list_form = list(infile_it_obj)
    del infile_list_form[0]

    
    # iterating over the headlines of each article
    for article_info_list in infile_list_form:
        headline = article_info_list[HEADLINE_INDEX]
        # replacing punctuation in current headline with whitespace
        headline_no_punc = ''
        for character in headline:
            if character not in string.punctuation:
                headline_no_punc += character
            else:
                headline_no_punc += ' '
        headline_words = headline_no_punc.lower().split()
        for word in headline_words:
            if len(word) > TRIVIAL_WORD_LENGTH:
                counts_ll.update_count(word)


def get_n():
    '''
    Purpose: prompts the user for an input.
             If possible, converts it to an int and returns that int
    '''
    n_name = input('N: ')You can also do int(input("N: ")).
    try:
        return int(n_name)
    except ValueError:
        print('ERROR: Could not read N')
        sys.exit(1)


def main():
    # parsing the csv file. Creating and organizing the ll
    infile_it_obj = parse_csv_file()
    counts_ll = LinkedList()
    clean_headlines_update_counts(infile_it_obj, counts_ll)
    counts_ll.sort()

    # getting value 'n' from user and printing out the n most-frequent words
    n = get_n()
    k = counts_ll.get_nth_highest_count(n)
    counts_ll.print_upto_count(k)
    

main()
