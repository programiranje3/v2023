#%%
"""
Task 1

Write a function that asks the user for a whole number, and prints
whether the number is even or odd.
"""

def odd_or_even():
    num_as_str = input("Please enter a whole number\n")
    num = int(num_as_str)
    res, reminder = divmod(num, 2)
    if reminder == 0:
        print("The number you've entered (" + num_as_str + ") is EVEN")
    else:
        print("The number you've entered (" + num_as_str + ") is ODD")

#%%
# Test the function
odd_or_even()

#%%
"""
Task 2

Write a function that calculates and prints the factorial of a number.
The function accepts the number (should be a positive integer) as its 
sole input argument. 
"""

def factorial(number):
    f = 1
    # x * (x-1) * ... * 1
    for i in range(number, 0, -1):
        f *= i
    print("Factorial of number " + str(number) + " is " + str(f))

#%%
# Test the function
factorial(5)


#%%
"""
Task 3

Write a function that receives 2 input parameters: 
1) an iterable (items), and 2) a non-negative integer (n).  
The function returns the lowest n-th value of the iterable. 
If n is non-positive or greater than the number of elements 
in the iterable, the function returns the lowest value in the 
iterable.
"""

def nth_lowest(items, n):
    if n < 0 or n > len(items):
        return min(items)
    return sorted(items)[n-1]

#%%
# Test the function with...
# ... a sequence of numbers:
a = [31, 72, 13, 41, 5, 16, 87, 98, 9]
print("3rd lowest in [31, 72, 13, 41, 5, 16, 87, 98, 9]:")
print(nth_lowest(a,3))

# ... a sequence of letters:
print("6th lowest in ['f', 'r', 't', 'a', 'b', 'y', 'j', 'd', 'c']:")
print(nth_lowest(['f', 'r', 't', 'a', 'b', 'y', 'j', 'd', 'c'], 6))

# ... a string:
print("2nd lowest in 'today':")
print(nth_lowest('today', 2))


#%%
"""
Task 4

Write a function that receives a list of numbers and returns
a tuple with the following elements:
- the list element with the smallest absolute value
- the list element with the largest absolute value
- the sum of all non-negative elements in the list
- the product of all negative elements in the list
"""

def list_stats(numbers):
    min_abs = max_abs = numbers[0]
    sum_non_neg = 0
    prod_neg = 1
    for num in numbers:
        if abs(num) < min_abs:
            min_abs = abs(num)
        elif abs(num) > max_abs:
            max_abs = abs(num)
        if num >= 0:
            sum_non_neg += num
        else:
            prod_neg *= num
    return min_abs, max_abs, sum_non_neg, prod_neg



#%%
# Test the function
print(list_stats([3.4, 5.6, -4.2, -5.6, 9, 1.2, 11.3, -23.45, 81]))

#%%
"""
Task 5

Write a function that receives a list of numbers and a threshold value. 
The function:
- creates a new list with unique elements from the input list
  that are below the threshold
- prints the number of elements in the new list
- sorts the elements in the new list in the descending order,
  and prints them, one element per line
"""
def list_operations(numbers, threshold):
    new_list = []
    for number in numbers:
        if number < threshold and number not in new_list:
            new_list.append(number)
    print("The new list has " + str(len(new_list)) + " elements")
    print("List elements in the descending order:")
    for number in sorted(new_list, reverse=True):
        print(number)


#%%
# Test the function
list_operations([1, 1, 2, 3, 5, 8, 13, 5, 21, 34, 55, 89], 20)


#%%
"""
Task 6

Write a function that receives two strings and checks if they
are anagrams. The function returns appropriate boolean value.

Note: An anagram is a word or phrase formed by rearranging the
letters of a different word or phrase, using all the original 
letters exactly once.

Additional instructions: 
- Comparison of letters should be case insensitive. Use the 'lower' 
method of class string to assure all letters are in lower case 
- Except for the use of the 'lower' string method, solve this task 
using list methods only 
- The space characters, if present, should be discarded.     
"""

def anagram(s1, s2):
    s1 = list(s1.lower())
    s2 = list(s2.lower())

    while " " in s1:
        s1.remove(" ")
    while " " in s2:
        s2.remove(" ")

    return sorted(s1) == sorted(s2)



#%%
# Test the function
print("anagram('School master', 'The classroom'):")
print(anagram('School master', 'The classroom'))
print()
print("anagram('Dormitory', 'Dirty room'):")
print(anagram('Dormitory', 'Dirty room'))
print()
print("anagram('Conversation', 'Voices rant on'):")
print(anagram('Conversation', 'Voices rant on'))
print()
print("anagram('Bob', 'Bill'):")
print(anagram('Bob', 'Bill'))


#%%
"""
Task 7

Write a function that receives a string and checks if the string is palindrome. 
The function returns appropriate boolean value.

Note: a palindrome is a word, phrase, or sequence that reads the same
backwards as forwards, e.g. "madam" or "nurses run".

The set of additional instructions given for the previous task, applies to
this task, as well 
"""

def palindrome(s):
    s = list(s.lower())
    while " " in s:
        s.remove(" ")
    s1 = s.copy()
    s1.reverse()
    return s == s1


#%%
# Test the function
print("palindrome('Madam'):")
print(palindrome("Madam"))
print()
print("palindrome('nurses run'):")
print(palindrome("nurses run"))
print()
print("palindrome('nurse run'):")
print(palindrome("nurse run"))


#%%
"""
Task 8

Write a function to play a guessing game: to guess a number between 1 and 9.
Scenario: 
- User is prompted to guess a number. 
- If the user guesses wrongly, the prompt reappears
- The user can try to guess max 3 times
- On a successful guess, user should get a "Well guessed!" message, and 
the function terminates. 
- If when guessing, the user enters a number that is out of the bounds 
(less than 1 or greater than 9), or a character that is not a number, 
they should be informed that only single digit values are allowed.

Hints: 
- you can use function 'randint' from 'random' package to generate a number to
be guessed in the game
- the 'isdigit' string function can be used to check if the user's input is a number 
"""

def guessing_game():
    from random import randint

    number_to_guess = randint(1,9)
    guess_counts = 0
    print("Welcome to the guessing game!")
    print("You will be prompted to guess a (single digit) number and will have 3 chances to make a correct guess")
    while guess_counts < 3:
        guess = input("Make your guess")
        if not guess.isdigit():
            print("Wrong input - note that only digits are allowed. You can try again")
            continue
        guess = int(guess)
        if guess < 1 or guess > 9:
            print("Wrong input - note that only digits in the [1,9] range are allowed. You can try again")
            continue
        if guess == number_to_guess:
            print("Correct! You won the game! Congratulations! ")
            return
        guess_counts += 1
        if guess_counts < 3:
            print("Incorrect! You can try again - you have " + str(3 - guess_counts) + " attempts")
        else:
            print("Incorrect! Sorry, no more attempts left! More luck next time!")


#%%
# Test the function
guessing_game()


#%%
if __name__ == '__main__':
    pass

    # odd_or_even()
    #
    # factorial(7)
    #
    # a = [31, 72, 13, 41, 5, 16, 87, 98, 9]
    # print("3rd lowest in [31, 72, 13, 41, 5, 16, 87, 98, 9]:")
    # print(nth_lowest(a, 3))
    # print("6th lowest in ['f', 'r', 't', 'a', 'b', 'y', 'j', 'd', 'c']:")
    # print(nth_lowest(['f', 'r', 't', 'a', 'b', 'y', 'j', 'd', 'c'], 6))
    # print("2nd lowest in 'today':")
    # print(nth_lowest('today', 2))
    #
    # print(list_stats([3.4, 5.6, -4.2, -5.6, 9, 1.2, 11.3, -23.45, 81]))
    #
    # list_operations([1, 1, 2, 3, 5, 8, 13, 5, 21, 34, 55, 89], 20)
    #
    # print("anagram('School master', 'The classroom'):")
    # print(anagram('School master', 'The classroom'))
    # print("anagram('Dormitory', 'Dirty room'):")
    # print(anagram('Dormitory', 'Dirty room'))
    # print("anagram('Conversation', 'Voices rant on'):")
    # print(anagram('Conversation', 'Voices rant on'))
    # print("anagram('Bob', 'Bill'):")
    # print(anagram('Bob', 'Bill'))
    #
    # print("palindrome('madam'):")
    # print(palindrome("madam"))
    # print("palindrome('nurses run'):")
    # print(palindrome("nurses run"))
    # print("palindrome('nurse run'):")
    # print(palindrome("nurse run"))
    #
    # guessing_game()
