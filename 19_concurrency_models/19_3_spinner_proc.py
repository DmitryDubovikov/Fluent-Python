import itertools
import time
from multiprocessing import Process, Event  # <1>
from multiprocessing import synchronize  # <2>


def spin(msg: str, done: synchronize.Event) -> None:  # <3>

    # [snip] the rest of spin and slow functions are unchanged from spinner_thread.py

    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow() -> int:
    time.sleep(3)
    return 42


def supervisor() -> int:
    done = Event()

    # Basic usage of the Process class is similar to Thread.
    spinner = Process(target=spin, args=("thinking!", done))  # <4>

    # The spinner object is displayed as <Process name='Process-1' parent=14868 initial>,
    # where 14868 is the process ID of the Python instance running spinner_proc.py.
    print(f"spinner object: {spinner}")  # <5>

    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
