'''
Modifications:
1) Handling errors with reading a file. If found a mistake or a bug, please pull a request on github: @alekkras
2) Generates up to a random number of words from the model "markov" in method generateWordChain
3) - Works with randomly generated file as well using trigrams with the base condition [None, None, None]
   - Problem: used a library random_words to create nouns but they are unique so I implemented repeating them in
   txt file by using random function, so each word was written with repeated number of times. The algorithm works if
   there are more than 1000 words being created. You can open random_file.txt and the output to see that they are
   different. Possible improvement: random words are not only nouns but verbs, adjectives to make the output more human

'''
from new_file_Markov import Markov
from random_words import RandomWords
import random

def makeWordModel(filename):
    '''creates a Morkov model from the words in the file with filename.
    pre: The file with name filename exists.
    post: A Markov chain from the text in the file is returned. '''
    # creates a Markov model from words in filename
    infile = open(filename)
    tmpmodel = Markov()
    for line in infile:
        words = line.split()
        for w in words:
            tmpmodel.add(w)
    infile.close()
    # Add a sentinel at the end of the text
    tmpmodel.add(None)
    tmpmodel.reset()
    return tmpmodel

def generateWordChain(markov, n):
    ''' generates up to n words on output from the model "markov"
    pre: markov is a valid Markov chain where the length is longer than "n"
    post: a string of n words will be returned using the Markov chain.'''
    # generates up to n words of output from a model
    words = []
    for i in range(n):
        next = markov.randomNext()
        if next is None:
            break  # got to a final state
        words.append(next)
    return " ".join(words)


def main():
    '''
    generate the function redo which will ask a user to retype the name of the file if
    there are any errors. We use it as we identify the following errors:
    1) FileNotFoundError
    2) IOError
    3) ValueError
    4) ImportError
    5) EOFError
    6) KeyboardInterrupt
    That is more efficient to create a function within a main function and use it only within
    that specific function not to make it hardcoding. In case you found any mistakes, please
    pull requests on github: @alekkras
    '''

    def redo():
        '''
        Used for processing user's answer. If the user answers yes, we run the main function again.
        If the user says something different, then the program stops executing using exit() method
        '''
        redo = input("Would you like to try again?\n")
        if redo.lower().startswith("y"):
            main()
        else:
            exit()


    '''
    Analysis of code for reflection of Big O 
    starts here
    '''
    try:
        choice = input("Would you like to work on existing file or create a totally random one?\n")

        #If a user choses to work with an existing file

        if choice.lower().startswith("e"):
            fname = input('enter filename: ')
            m = makeWordModel(fname)
            print(generateWordChain(m, random.randrange(10,1000,10)))

        #If a user choses to create and work with a new file

        elif choice.lower().startswith("r"):
            new = open("random_file.txt", "w")
            number_of_words = int(input("How many words would you like?"))
            n = 0 #iterator
            while n < number_of_words:
                rw = RandomWords() #generate random words method
                word = rw.random_word()
                new.write((word + " ")*random.randrange(1,5))
                #print(word) - uncomment in case of debugging
                n += 1
            m = makeWordModel("random_file.txt")
            print(generateWordChain(m, random.randrange(100, 1000000, 100)))
            new.close()

        else:
            print("We are so sorry that you are a party pooper\n")


        '''
        Analysis of code for reflection of Big O 
        ends here
        '''
    except FileNotFoundError:
        print("There is no file")
        redo()
        '''
        except IOError:
            print('An error occured trying to read the file.')
            redo()
    
        except ValueError:
            print('Non-numeric data found in the file.')
            redo()
    
        except ImportError:
            print("NO module found")
            redo()
    
        except EOFError:
            print('EOF file happened, come back later')
            redo()
    
        except KeyboardInterrupt:
            print('You cancelled the operation.')
            redo()
        '''

        '''
            above except statements were given for most common errors, 
            the below statement is for any unexpected errors.
        '''

    except Exception as e:
        print('An error', e, 'happened, lol')
        redo()

if __name__ == "__main__":
    main()