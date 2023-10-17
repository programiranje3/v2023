#%%
"""
LAB 2
"""

"""
TASK 1:

Write a function that receives two lists, as its input parameters, and 
returns a new list that contains only those elements (without duplicates) 
that appear in both input lists.
"""

def common_elements(l1, l2):
    # Option 1
    # new_list = []
    # for item in l1:
    #     if item in l2 and item not in new_list:
    #         new_list.append(item)
    # return new_list
    #
    # Option 2
    return [item for item in set(l1) if item in l2]


#%%
# Test the function:
a = [1, 1, 2, 3, 5, 8, 13, 21, 55, 89, 5, 10]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
print(common_elements(a,b))


#%%

"""
TASK 2:

Write a function that receives 2 lists of the same length and returns a new list 
obtained by concatenating the two input lists index-wise. Example:
Input lists:
list1 = ["M", "na", "i", "Ke"]
list2 = ["y", "me", "s", "lly"]
Output: ['My', 'name', 'is', 'Kelly']
"""

def concat_index_wise(l1, l2):
    # Option 1
    # new_list = []
    # for item1, item2 in zip(l1, l2):
    #     new_list.append(str(item1) + str(item2))
    # return new_list
    #
    # Option 2
    return [f"{item1}{item2}" for item1, item2 in zip(l1, l2)]

#%%
# Test the function:
list1 = ["M", "na", "i", "Ke", "!"]
list2 = ["y", "me", "s", "lly"]
print(concat_index_wise(list1, list2))
print()
list3 = [12, 34, 56, 78, 90]
list4 = [90, 78, 56, 34, 12]
print(concat_index_wise(list3, list4))


#%%
""" 
TASK 3:

Write a function that checks and returns whether a given string is a pangram or not.
Pangrams are sentences or phrases containing every letter of the alphabet at least once 
(for example: "The quick brown fox jumps over the lazy dog")

Hint: ascii_lowercase from the string module can be used to get all letters
"""

def pangram(s):
    from string import ascii_lowercase
    # print(ascii_lowercase)
    #
    # Option 1
    # for letter in ascii_lowercase:
    #     if letter not in s.lower():
    #         return False
    # return True
    #
    # Option 2
    # return all([letter in s.lower() for letter in ascii_lowercase])
    #
    # Option 3
    letters_only = [ch for ch in set(s.lower()) if ch.isalpha()]
    return "".join(sorted(letters_only)) == ascii_lowercase


#%%
# Test the function:
print("The quick brown fox jumps over the lazy dog")
print(pangram("The quick brown fox jumps over the lazy dog"))
print()
print("The quick brown fox jumps over the lazy cat")
print(pangram("The quick brown fox jumps over the lazy cat"))


#%%
"""
TASK 4:

Write a function that receives a string with a mix of lower and upper case letters.
The function arranges letters in such a way that all lowercase letters come first,
followed by all upper case letters. Non-letter characters (if any) are ignored, that is,
not included in the new 're-arranged' string.
The new,'re-arranged' string is the function's return value.
"""

def rearrange_string(s):
    # Option 1
    # lower_case = [ch for ch in s if ch.islower()]
    # upper_case = [ch for ch in s if ch.isupper()]
    # return "".join(lower_case + upper_case)
    #
    # Option 2
    lower_case = []
    upper_case = []
    for ch in s:
        if ch.islower():
            lower_case.append(ch)
        elif ch.isupper():
            upper_case.append(ch)
    return "".join(lower_case) + "".join(upper_case)


#%%
# Test the function:
print("Rearranging string: 'Programming 3, Lab 2'")
print(rearrange_string("Programming 3, Lab 2"))

#%%
"""
TASK 5:

Write a function that accepts a sequence of comma separated passwords and
checks their validity using the following criteria:
1. At least 1 letter between [a-z] => At least 1 lower case letter
2. At least 1 number between [0-9] => At least 1 digit
3. At least 1 letter between [A-Z] => At least 1 upper case letter
4. At least 1 of these characters: $,#,@
5. Length in the 6-12 range (including 6 and 12)
Passwords that match the criteria should be printed in one line separated by a comma.
"""

# Option 1
# def password_check(passwords):
#     passwords = passwords.split(",")
#     valid_passwords = []
#     for password in passwords:
#         password = password.lstrip()
#         conditions = [False]*5
#         for ch in password:
#             if ch.islower():
#                 conditions[0] = True
#             elif ch.isdigit():
#                 conditions[1] = True
#             elif ch.isupper():
#                 conditions[2] = True
#             elif ch in '$#@':
#                 conditions[3] = True
#             if 6 <= len(password) <= 12:
#                 conditions[4] = True
#         if all(conditions):
#             valid_passwords.append(password)
#     print("Valid passwords: " + ", ".join(valid_passwords))

# Option 2:
def password_check(passwords):
    pass_to_check = [p.lstrip() for p in passwords.split(",")]
    valid_passwords = []
    for p in pass_to_check:
        valid = True
        if len(p) < 6 or len(p) > 12:
            valid = False
        elif not any([ch.islower() for ch in p]):
            valid = False
        elif not any([ch.isdigit() for ch in p]):
            valid = False
        elif not any([ch.isupper() for ch in p]):
            valid = False
        elif not any([ch in '$#@' for ch in p]):
            valid = False
        if valid:
            valid_passwords.append(p)
    print("Valid passwords:", ", ".join(valid_passwords))


#%%
# Test the function:
print("Passwords to check: ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR")
password_check("ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR")

#%%
"""
TASK 6:

Write a function that receives a report (as a string) on the state (up / down) of several servers.
Each line of the report refers to one server, and has the following format:
"Server <server_name> is <up/down>"
Note that some lines may be empty.
Note also that some servers might be mentioned multiple times, in which case, the latest status
should be considered the valid one.
The function should process the report and print:
- the total number of servers mentioned in the report
- the proportion of servers that are down
- names of servers that are down (if any)
"""

def server_status(report):
    all_servers = []
    down_servers = []
    lines = [line.lstrip() for line in report.split("\n") if line.strip() != ""]
    lines.reverse()
    for line in lines:
        _, server, _, status = line.split()
        if server not in all_servers:
            all_servers.append(server)
            if status == "down":
                down_servers.append(server)
    print(f"Number of all servers: {len(all_servers)}")
    print(f"Proportion of servers that are down: {len(down_servers)/len(all_servers)}")
    print("Servers currently down: " + ",".join(down_servers))



#%%
# Test the function:
sample_input = '''
        Server abc01 is up
        Server abc02 is down
        Server xyz01 is down
        Server xyz02 is up
        Server abc01 is down
        Server xyz01 is up
        '''
server_status(sample_input)


#%%
"""
TASK 7:

Write a function that finds numbers between 100 and 400 (both included)
where each digit of a number is even. The numbers that match this criterion
should be printed as a comma-separated sequence.
"""

def all_even_digits(number):
    while number > 0:
        number, reminder = divmod(number, 10)
        if reminder % 2 != 0:
            return False
    return True

def numbers_with_all_even_digits():
    # Option 1
    # all_even = []
    # for number in range(100, 401):
    #     if all([ch in '24680' for ch in str(number)]):
    #         all_even.append(number)
    # print(", ".join([str(item) for item in all_even]))
    #
    # Option 2
    all_even = []
    for number in range(100, 401):
        if all_even_digits(number):
            all_even.append(number)
    print(", ".join([str(item) for item in all_even]))



#%%
# Test the function:
numbers_with_all_even_digits()

#%%

if __name__ == '__main__':
    pass

    # # Task 1:
    # a = [1, 1, 2, 3, 5, 8, 13, 21, 55, 89, 5, 10]
    # b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # print(common_elements(a,b))
    #
    # # Task 2:
    # list1 = ["M", "na", "i", "Ke"]
    # list2 = ["y", "me", "s", "lly"]
    # print(concat_index_wise(list1, list2))
    #
    # # Task 3:
    # print("The quick brown fox jumps over the lazy dog")
    # print(pangram("The quick brown fox jumps over the lazy dog"))
    # print("The quick brown fox jumps over the lazy cat")
    # print(pangram("The quick brown fox jumps over the lazy cat"))
    #
    # # Task 4:
    # print(("Rearranging string: 'PyNaTive_2021'"))
    # print(rearrange_string("PyNaTive_2021"))
    #
    # # Task 5:
    # print("Passwords to check: ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR")
    # password_check("ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456WR")
    #
    # # Task 6:
    # sample_input = '''
    #     Server abc01 is up
    #     Server abc02 is down
    #     Server xyz01 is down
    #     Server xyz02 is up
    #     '''
    # server_status(sample_input)
    #
    # # Task 7:
    # numbers_with_all_even_digits()
