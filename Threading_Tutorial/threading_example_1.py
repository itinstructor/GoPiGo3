#!/usr/bin/env python3
"""
    Filename: threading_example_1.py
"""


# ------------------------ TEST FUNCTIONS ---------------------------------- #
def function1():
    for i in range(5):
        print("ONE ")


def function2():
    for i in range(5):
        print("TWO ")


def function3():
    for i in range(5):
        print("THREE ")


def main():
    # --------------- NORMAL SEQUENTIAL FUNCTIONS -------------------------- #
    # When we call these functions, the first function call
    # MUST complete before the next, they are executed in sequence
    function1()
    function2()
    function3()


# If a standalone program, call the main function
# Else, use as a module
if __name__ == "__main__":
    main()
