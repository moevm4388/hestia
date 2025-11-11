import argparse
import sys
from enum import Enum
from typing import Any

from common.exceptions import InvalidArgumentsError, UnknownIdentifierError
from common.module_group import ModuleGroup
from common.types import Identifier
from natural import NaturalModule
from integer import IntegerModule
from rational import RationalModule
from polynomial import PolynomialModule


class ExitCode(int, Enum):
    INVALID_IDENTIFIER = 1
    NOT_IMPLEMENTED = 2
    INVALID_ARGS = 3


def build_module_group() -> ModuleGroup:
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    rational_module = RationalModule(natural_module, integer_module)
    polynomial_module = PolynomialModule(
        natural_module, integer_module, rational_module
    )

    return ModuleGroup(
        natural_module,
        integer_module,
        rational_module,
        polynomial_module,
    )


def pretty_print(v: Any) -> None:
    if isinstance(v, bool):
        print("Да" if v else "Нет")
        return

    print(v)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Система компьютерной алгебры",
        epilog="В качестве идентификатора можно передать как название функции (например COM_NN_D), так и номер (N-1).",
    )

    parser.add_argument(
        "-f",
        "--function",
        metavar="NAME",
        help="Идентификатор функции, которая будет вызвана",
        required=True,
    )
    parser.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        help="Аргументы для вызываемой функции",
        required=True,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    module_group = build_module_group()

    try:
        identifier = Identifier.from_str(args.function)
    except ValueError:
        print(f"Неверный идентификатор функции: '{args.function}'", file=sys.stderr)
        exit(ExitCode.INVALID_IDENTIFIER)

    try:
        result = module_group.call(identifier, args.args)
    except InvalidArgumentsError as e:
        message = (
            "Слишком много аргументов"
            if e.actual > e.expected
            else "Недостаточно аргументов"
        )
        print(
            f"{message} (ожидалось {e.actual}, получено {e.expected})", file=sys.stderr
        )
        exit(1)
    except UnknownIdentifierError:
        print(f"Функция '{args.function}' не реализована", file=sys.stderr)
        exit(ExitCode.NOT_IMPLEMENTED)

    pretty_print(result)


if __name__ == "__main__":
    main()
