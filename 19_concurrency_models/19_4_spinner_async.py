import asyncio
import itertools

# import time


async def spin(msg: str) -> None:  # <1>

    # We don’t need the Event argument that was used
    # to signal that slow had completed its job in spinner_thread.py

    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, flush=True, end="")

        try:
            # Use await asyncio.sleep(.1) instead of time.sleep(.1),
            # to pause without blocking other coroutines
            await asyncio.sleep(0.1)  # <2>

        except asyncio.CancelledError:  # <3>
            # asyncio.CancelledError is raised when the cancel method is called on the
            # Task controlling this coroutine. Time to exit the loop
            break

    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


async def slow() -> int:

    # The slow coroutine also uses await asyncio.sleep instead of time.sleep
    await asyncio.sleep(3)  # <4>
    # time.sleep(3)
    return 42


def main() -> None:  # <1>
    """
    main is the only regular function defined in this program—the others are coroutines

    The asyncio.run function starts the event loop to drive the coroutine that will
    eventually set the other coroutines in motion. The main function will stay
    blocked until supervisor returns. The return value of supervisor will be the
    return value of asyncio.run.
    """
    result = asyncio.run(supervisor())  # <2>
    print(f"Answer: {result}")


async def supervisor() -> int:  # <3> Native coroutines are defined with async def

    # asyncio.create_task schedules the eventual execution of spin,
    # immediately returning an instance of asyncio.Task
    spinner = asyncio.create_task(spin("thinking!"))  # <4>

    # The repr of the spinner object looks like
    # <Task pending name='Task-2'coro=<spin() running at /path/to/spinner_async.py:11>>.
    print(f"spinner object: {spinner}")  # <5>

    # The await keyword calls slow, blocking supervisor until slow returns.
    # The return value of slow will be assigned to result.
    result = await slow()  # <6>

    # The Task.cancel method raises a CancelledError exception inside the spin coroutine
    spinner.cancel()  # <7>

    return result


if __name__ == "__main__":
    # Example demonstrates the three main ways of running a coroutine:
    # asyncio.run(coro())
    # asyncio.create_task(coro())
    # await coro()
    main()
