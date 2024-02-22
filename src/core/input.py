import logging

logger = logging.getLogger("Input")


class Input:
    @staticmethod
    def ask_string(question: str, default=None, example=None) -> str:
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
        try:
            return int(Input.ask_string(question))
        except ValueError:
            if default:
                return default
            logging.warning("Invalid input, please try again")
            return Input.ask_int(question)

    @staticmethod
    def wait_for_input():
        input("Press enter to continue...")

    @staticmethod
    def ask_bool(question: str, default=False) -> bool:
        result = Input.ask_string(f"{question} (y/n)", default="y" if default else "n")
        return result.lower() == "y"
