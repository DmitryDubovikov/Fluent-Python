import itertools
import time
from threading import Thread, Event


def spin(msg: str, done: Event) -> None:  # <1>
    """
    This function will run in a separate thread. The done argument is an instance of
    threading.Event, a simple object to synchronize threads.
    """
    for char in itertools.cycle(r"\|/-"):  # <2> This is an infinite loop

        status = f"\r{char} {msg}"  # <3>
        print(status, end="", flush=True)

        # The Event.wait(timeout=None) method returns True when the event is set by
        # another thread; if the timeout elapses, it returns False.
        if done.wait(0.1):  # <4>
            break  # <5> Exit the infinite loop.

    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")  # <6>


def slow() -> int:
    """
    slow() will be called by the main thread. Imagine this is a slow API call over the
    network. Calling sleep blocks the main thread, but the GIL is released so the
    spinner thread can proceed.

    The first important insight of this example is that time.sleep()
    blocks the calling thread but releases the GIL, allowing other
    Python threads to run.
    """
    time.sleep(3)  # <7>
    return 42


def supervisor() -> int:  # <1>
    """supervisor will return the result of slow."""

    # The threading.Event instance is the key to coordinate
    # the activities of the main thread and the spinner thread
    done = Event()  # <2>

    # create a new Thread
    spinner = Thread(target=spin, args=("thinking!", done))  # <3>

    # Display the spinner object. The output is <Thread(Thread-1, initial)>,
    # where initial is the state of the thread—meaning it has not started.
    print(f"spinner object: {spinner}")  # <4>

    # Start the spinner thread
    spinner.start()  # <5>

    # Call slow, which blocks the main thread.
    # Meanwhile, the secondary thread is running the spinner animation
    result = slow()  # <6>

    # Set the Event flag to True;
    # this will terminate the for loop inside the spin function.
    done.set()  # <7>

    # Wait until the spinner thread finishes
    spinner.join()  # <8>

    return result


def main() -> None:
    result = supervisor()  # <9>
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
