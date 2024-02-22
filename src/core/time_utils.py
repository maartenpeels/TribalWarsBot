import sys
import time


class TimeUtils:
    @staticmethod
    def sleep(seconds: int):
        """Sleep for a given amount of seconds. This method will print a countdown to the console."""

        # Hacky? Yes. Does it work? Also yes.
        # Wait for the logger to finish writing
        time.sleep(0.1)

        for i in range(seconds, 0, -1):
            # For some stupid reason we cannot flush the output in the logger
            sys.stdout.write(f"\rSleeping for {i} seconds")
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\r\033[K")  # Erase to end of line
        sys.stdout.flush()
