from typing import Callable


class Option:
    def __init__(
        self,
        name: str,
        command: object,
        prep_call: Callable = None,
        success_message="{result}",
    ) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message

    def choose(self) -> None:
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data) if data else self.command.execute()

        if success:
            print(self.success_message.format(result=result))

    def __str__(self) -> str:
        return self.name
