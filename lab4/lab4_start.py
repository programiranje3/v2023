#%%
"""
LAB 4
"""


#%%
"""
TASK 1

Write the 'compute_product' function that receives an arbitrary number of numeric values and computes their product. 
The function also receives a named argument "squared" with the default value False, which determines if the numeric 
values should be used as given or their squared value should be used instead. 
The computed product is the function's return value.

Implement the function in two different ways:
1) using a for loop
2) using the reduce() f. from the functools module together with an appropriate lambda f.
For an example and explanation of reduce() f. check, for example, these articles:
- https://realpython.com/python-reduce-function/
- https://www.python-course.eu/python3_lambda.php

Note: reduce is one of three functions often used together in data analysis: map, filter, reduce
For a funny illustration of these functions, check this page: 
https://www.globalnerdy.com/2016/06/23/map-filter-and-reduce-explained-using-emoji/
"""



#%%
# Test the function

# print(compute_product(1,-4,13,2))
# print(compute_product(1, -4, 13, 2, squared=True))
# print()

# # Calling the compute_product function with a list
# num_list = [2, 7, -11, 9, 24, -3]
# # This is NOT a way to make the call:
# print("Calling the function by passing a list as the argument")
# print(compute_product(num_list))
# print()
# # instead, this is how it should be done (the * operator is 'unpacking' the list):
# print("Calling the function by passing an UNPACKED list as the argument")
# print(compute_product(*num_list))


#%%
"""
TASK 2

Write the 'select_strings' function that receives an arbitrary number of strings and returns a list 
of those strings where the first and the last character are the same (case-insensitive) and the total 
number of unique characters is above the given threshold. The threshold is the function's named argument 
with the default value of 3.

Implement the function in three different ways:
1) using the for loop
2) using list comprehension
3) using the filter() f. together with an appropriate lambda f.
"""


#%%
# Test the function:
# str_list = ['yellowy', 'Bob', 'lovely', 'Yesterday', 'too']
# print(select_strings(*str_list))


#%%
"""
TASK 3

Write the 'process_product_orders' function that receives a list of product orders, 
where each order is a 4-tuple of the form (order_id, product_name, quantity, price_per_item). 
The function returns a list of 2-tuples of the form (order_id, total_price) where total price 
for an order is the product of the quantity and the price per item.
The function also receives two named arguments that may affect the computed total price:
- 'discount' - the discount, expressed in percentages, to be applied to the total price;
  the default value of this argument is None
- 'shipping' - the shipping cost to be added to orders with total price less than 100; 
  the default value of this argument is 10.

Implement the function in three different ways:
1) using for loop
2) using list comprehension
3) using the map() f. together with an appropriate auxiliary function
"""


#%%
# Test the function:
# orders = [("34587", "Learning Python, Mark Lutz", 4, 40.95),
#           ("98762", "Programming Python, Mark Lutz", 5, 56.80),
#           ("77226", "Head First Python, Paul Barry", 3, 32.95),
#           ("88112", "Einführung in Python3, Bernd Klein", 3, 24.99)]
#
# print(process_product_orders(orders))
# print()
# print("The same orders with discount of 10%")
# print(process_product_orders(orders, discount=10))

#%%
"""
TASK 4

Create a decorator ('timer') that measures the time a function takes to execute and 
prints the function's name and its duration to the console.

Hint 1: use the decorator-writing pattern:
import functools
def decorator(func):
     @functools.wraps(func)	 # preserves func's identity after it's decorated
     def wrapper_decorator(*args, **kwargs):
         # Do something before
         value = func(*args, **kwargs)
         # Do something after
         return value
     return wrapper_decorator

Hint 2: to measure the time of function execution, use the perf_counter() f.
from the time module (it returns a float value representing time in seconds).
"""

#%%
"""
TASK 4.1

Write the 'compute_sum' function that for each number x in the range 1..n (n is the input parameter)
computes the sum: S(x) = 1 + 2 + ... + x-1 + x, and returns the sum of all S(x).
Decorate the function with the timer decorator, to measure its execution time.

Write the function in a few different ways - (1) using a loop; (2) using list comprehension;
(3) using a combination of the map and reduce functions - and decorate each one with the timer 
to compare their performance
"""


#%%
# Test the function:
# print(compute_sum_loop(10000))
# print()
# print(compute_sum_lc(10000))
# print()
# print(compute_sum_mr(10000))

#%%
"""
TASK 4.2

Write the 'mean_median_diff' function that generates n random numbers (integers) between 1 and k, where 
n and k are the function's input (positional) parameters. It does so in several iterations, the exact number of 
iterations determined by the named input parameter 'iterations', with the default value of 10. 
In each iteration, the function computes the difference between mean and median of the generated numbers and stores 
it in a list. After completing all the iterations, the function prints the mean - median differences from all the 
iterations as well as the average difference.
  
Decorate the function with the timer decorator.
"""


#%%
# Test the function:
# mean_median_diff(100, 250, iterations=20)


#%%
"""
TASK 5

Create a decorator ('standardiser') that first checks if the function's positional arguments are numbers,
and if so, standardizes (= z-transforms) them before passing them to the decorated function for 
further computations. If not all positional arguments are numbers, the decorator reports that and passes
the arguments to the decorated function unchanged. 
The decorator also rounds the computation result to 4 digits before returning it (as its return value).

Bonus: before calling the decorated function, print, to the console, its name with the list of input 
parameters
"""

#%%
"""
TASK 5.1

Write the 'sum_of_sums' function that receives an arbitrary number of int values and 
for each value (x) computes the following sum:
S(x) = 1 + x + x**2 + x**3 + ... + x**n
where n is a named argument with default value 10.
The function returns the sum of S(x) of all received int values.
Decorate the function with the standardise decorator.
"""



#%%
# Test the function:
# print(sum_of_sums(1,3,5,7,9,11,13, n=7))


#%%

if __name__ == '__main__':

    pass

    # Task 1
    # print(compute_product(1,-4,13,2))
    # print(compute_product(1, -4, 13, 2, squared=True))
    # print()
    # # Calling the compute_product function with a list
    # num_list = [2, 7, -11, 9, 24, -3]
    # # This is NOT a way to make the call:
    # print("Calling the function by passing a list as the argument")
    # print(compute_product(num_list))
    # print()
    # # instead, this is how it should be done (the * operator is 'unpacking' the list):
    # print("Calling the function by passing an UNPACKED list as the argument")
    # print(compute_product(*num_list))
    # print()

    # Task 2
    # str_list = ['yellowy', 'Bob', 'lovely', 'Yesterday', 'too']
    # print(select_strings(*str_list))
    # print()

    # Task 3
    # orders = [("34587", "Learning Python, Mark Lutz", 4, 40.95),
    #           ("98762", "Programming Python, Mark Lutz", 5, 56.80),
    #           ("77226", "Head First Python, Paul Barry", 3, 32.95),
    #           ("88112", "Einführung in Python3, Bernd Klein", 3, 24.99)]
    #
    # print(process_product_orders(orders))
    # print()
    # print("The same orders with discount of 10%")
    # print(process_product_orders(orders, discount=10))
    # print()

    # Task 4.1
    # print(compute_sum_loop(10000))
    # print()
    # print(compute_sum_lc(10000))
    # print()
    # print(compute_sum_mr(10000))

    # Task 4.2
    # mean_median_diff(100, 250, iterations=20)
    # print()

    # Task 5.1
    # print(sum_of_sums(1,3,5,7,9,11,13, n=7))


