import logging

logger = logging.getLogger("Input")


class Input:
    """Class for handling user input."""

    @staticmethod
    def ask_string(question: str, default=None, example=None) -> str:
        """Ask the user for a string input. If default is provided, it will be used if the user doesn't provide any
        input. If example is provided, it will be shown as an example to the user."""
        message = f"{question}"
        if default:
            message += f" [{default}]"
        if example:
            message += f" (e.g. {example})"
        message += ": "

        result = input(message)
        if not result:
            if default:
                return default
            logging.warning("Empty input, please try again")
            return Input.ask_string(question)

        return result

    @staticmethod
    def ask_int(question: str, default=None) -> int:
        """Ask the user for an integer input. If default is provided, it will be used if the user doesn't provide any"""
        try:
            return int(Input.ask_string(question))
        except ValueError:
            if default:
                return default
            logging.warning("Invalid input, please try again")
            return Input.ask_int(question)

    @staticmethod
    def wait_for_input():
        """Wait for the user to press any key."""
        input("Press enter to continue...")

    @staticmethod
    def ask_bool(question: str, default=False) -> bool:
        """Ask the user for a boolean input. If default is True and the user doesn't provide any input, it will be
        assumed as True. If default is False and the user doesn't provide any input, it will be assumed as False."""
        result = Input.ask_string(f"{question} (y/n)", default="y" if default else "n")
        return result.lower() == "y"
