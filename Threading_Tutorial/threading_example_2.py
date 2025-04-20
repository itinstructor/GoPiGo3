#!/usr/bin/env python3
"""
    Filename: threading_example_2.py
"""
import threading


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
    # ----------------- NORMAL SEQUENTIAL FUNCTIONS ------------------------ #
    # If we call these functions, the first function call
    # MUST complete before the next, they are executed linearly
    # function1()
    # function2()
    # function3()

    # ---------------------- THREADED FUNCTIONS ---------------------------- #
    # We can execute these functions concurrently using threads.
    # We must have a target function for a thread.
    t1 = threading.Thread(target=function1)
    t2 = threading.Thread(target=function2)
    t3 = threading.Thread(target=function3)

    t1.start()
    t2.start()
    t3.start()


# If a standalone program, call the main function
# Else, use as a module
if __name__ == "__main__":
    main()
