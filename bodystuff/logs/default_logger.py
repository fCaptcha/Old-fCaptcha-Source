from .abstract_logger import AbstractLogger
import time
import colorama

class DefaultLogger(AbstractLogger):
    def __init__(self, show_time : bool = True) -> None:
        self.show_time = show_time

    def log(self, message, **kwargs):
        args = []
        for key, value in kwargs.items():
            args.append(f"{colorama.Fore.LIGHTBLACK_EX}{key}={colorama.Fore.WHITE}{value}")
        message = f"{colorama.Fore.WHITE}{message} {' '.join(args)}"
        if self.show_time:
            message = f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.WHITE}{time.strftime('%H:%M:%S')}{colorama.Fore.LIGHTBLACK_EX}] {message}"
        print(message)

    def success(self, message, **kwargs):
        self.log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.GREEN}success{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)

    def info(self, message, **kwargs):
        self.log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.BLUE}info{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)

    def error(self, message, **kwargs):
        self.log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.RED}error{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)
        

            