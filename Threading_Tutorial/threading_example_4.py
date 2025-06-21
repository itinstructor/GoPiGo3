#!/usr/bin/env python3
"""
    Filename: threading_example_4.py
    Description: Example of threading in Python using queues.
"""

import threading        # https://docs.python.org/3/library/threading.html
import queue            # https://docs.python.org/3/library/queue.html
import time             # https://docs.python.org/3/library/time.html


class ThreadExample():
    def __init__(self):
        # Define a thread lock to prevent threads running into each other
        self.thread_lock = threading.Lock()

        # Create thread queue to keep track of the threads
        self.q = queue.Queue()

        # Define number of threads
        NUMBER_OF_THREADS = 5

        # Create/spawn multiple threads
        for r in range(NUMBER_OF_THREADS):

            # Set the thread target method
            thread = threading.Thread(target=self.worker)

            # All threads end when main program ends for cleaner shutdown
            thread.daemon = True

            # Start/spawn the thread
            thread.start()

        # Start timer before sending tasks to the queue
        start_time = time.time()

        print(f"Creating a task request for each item in the given range\n")

        # Put all task requests into the queue
        for item in range(10):
            self.q.put(item)

        # Block until all worker tasks are complete in the queue
        self.q.join()

        # Calculate elapsed time
        elapsed_time = round(time.time() - start_time, 2)
        print(
            f"All workers completed their tasks after {elapsed_time} seconds"
        )

# ------------------------ WORKER METHOD ----------------------------------- #
    def worker(self):
        """This method does all the work"""
        while True:
            # Get the next task in the queue
            item = self.q.get()

            # Actual work
            time.sleep(1)

            # Output of the task
            # thread_lock prevents the threads from running into each other
            with self.thread_lock:
                print(f"Working on {item}")
                print(f"Finished {item}")

            # Remove task from queue
            self.q.task_done()


thread_example = ThreadExample()
