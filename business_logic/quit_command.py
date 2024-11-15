import sys

from business_logic import Command


class QuitCommand(Command):
    def execute(self, data=None) -> None:
        sys.exit(0)
