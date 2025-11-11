"""
Модуль целых чисел.

Авторы:
- Кислица Сергей <andret23232347@mail.ru>
- Гриценко Кирилл <kirill.grizenko53@gmail.com>
"""

from common.exceptions import UnknownIdentifierError
from common.types import Identifier, Module
from common.utils import ensure_args
from typing import Any
from natural import NaturalNumber, NaturalModule


class Integer:
    """Класс для представления целых чисел."""

    def __init__(
        self, value: int = None, sign: int = None, natural: NaturalNumber = None
    ) -> None:
        """
        Инициализация целого числа.

        Args:
            value: целое число Python (альтернативный способ инициализации)
            sign: 0 - положительное, 1 - отрицательное
            natural: натуральное число (модуль)
        """
        if value is not None:
            if value < 0:
                self.sign = 1
                value = -value
            else:
                self.sign = 0
            self.natural = NaturalNumber(value)
        elif sign is not None and natural is not None:
            if sign not in (0, 1):
                raise ValueError(
                    "Знак должен быть 0 (положительное) или 1 (отрицательное)"
                )

            if self._is_zero(natural):
                self.sign = 0
            else:
                self.sign = sign

            self.natural = natural
        else:
            raise ValueError("Необходимо указать либо value, либо sign и natural")

    def _is_zero(self, n: NaturalNumber) -> bool:
        """Проверка, является ли натуральное число нулем"""
        return len(n.value) == 1 and n.value[0] == 0

    def __str__(self) -> str:
        """Строковое представление целого числа."""
        if self.sign == 1:
            return "-" + str(self.natural)
        return str(self.natural)

    def __eq__(self, other) -> bool:
        """Проверка на равенство."""
        if not isinstance(other, Integer):
            return False
        return self.sign == other.sign and self.natural.value == other.natural.value

    @classmethod
    def from_str(cls, s: str) -> "Integer":
        """Создание целого числа из строки."""
        if not s:
            raise ValueError("Пустая строка")

        if s[0] == "-":
            sign = 1
            digits_str = s[1:]
        else:
            sign = 0
            digits_str = s

        natural = NaturalNumber.from_str(digits_str)
        return cls(sign=sign, natural=natural)

    @classmethod
    def from_int(cls, n: int) -> "Integer":
        """Создание целого числа из целого Python."""
        return cls(value=n)

    @classmethod
    def from_natural(cls, natural: NaturalNumber) -> "Integer":
        """Создание целого числа из натурального (положительного)."""
        return cls(sign=0, natural=natural)


class IntegerModule(Module):
    """Модуль для работы с целыми числами."""

    def __init__(self, natural_module: NaturalModule):
        """
        Инициализация модуля целых чисел.

        Args:
            natural_module: модуль натуральных чисел для использования его функций
        """
        self.natural_module = natural_module

    def absolute_value(self, z: Integer) -> NaturalNumber:
        """Z-1. Абсолютная величина числа, результат - натуральное."""
        return z.natural

    def sign_determination(self, z: Integer) -> int:
        """
        Z-2. Определение положительности числа.

        Returns:
            2 - положительное, 0 - равное нулю, 1 - отрицательное
        """
        if self.natural_module.is_zero(z.natural):
            return 0
        return 2 if z.sign == 0 else 1

    def multiply_by_minus_one(self, z: Integer) -> Integer:
        """Z-3. Умножение целого на (-1)."""
        if self.natural_module.is_zero(z.natural):
            return z
        new_sign = 1 - z.sign
        return Integer(sign=new_sign, natural=z.natural)

    def natural_to_integer(self, n: NaturalNumber) -> Integer:
        """Z-4. Преобразование натурального в целое."""
        return Integer(sign=0, natural=n)

    def integer_to_natural(self, z: Integer) -> NaturalNumber:
        """Z-5. Преобразование целого неотрицательного в натуральное."""
        if z.sign == 1:
            raise ValueError(
                "Запрещено преобразовывать отрицательные числа в натуральные"
            )
        return z.natural

    def addition(self, z1: Integer, z2: Integer) -> Integer:
        """Z-6. Сложение целых чисел."""
        if z1.sign == 0 and z2.sign == 0:
            result_natural = self.natural_module.adding(z1.natural, z2.natural)
            return Integer(sign=0, natural=result_natural)

        if z1.sign == 1 and z2.sign == 1:
            result_natural = self.natural_module.adding(z1.natural, z2.natural)
            return Integer(sign=1, natural=result_natural)

        if z1.sign == 0 and z2.sign == 1:
            comparison = self.natural_module.comparison(z1.natural, z2.natural)
            if comparison == 2:  # z1 > z2
                result_natural = self.natural_module.subtracting(z1.natural, z2.natural)
                return Integer(sign=0, natural=result_natural)
            elif comparison == 0:  # z1 == z2
                return Integer(sign=0, natural=NaturalNumber(0))
            else:  # z1 < z2
                result_natural = self.natural_module.subtracting(z2.natural, z1.natural)
                return Integer(sign=1, natural=result_natural)

        if z1.sign == 1 and z2.sign == 0:
            return self.addition(z2, z1)

    def subtraction(self, z1: Integer, z2: Integer) -> Integer:
        """Z-7. Вычитание целых чисел."""
        z2_negative = self.multiply_by_minus_one(z2)
        return self.addition(z1, z2_negative)

    def multiplication(self, z1: Integer, z2: Integer) -> Integer:
        """Z-8. Умножение целых чисел."""
        result_natural = self.natural_module.multiplication(z1.natural, z2.natural)

        if self.natural_module.is_zero(result_natural):
            return Integer(sign=0, natural=result_natural)

        result_sign = 0 if z1.sign == z2.sign else 1
        return Integer(sign=result_sign, natural=result_natural)

    def quotient(self, z1: Integer, z2: Integer) -> Integer:
        """Z-9. Частное от деления целого на целое (делитель отличен от нуля)."""
        if self.natural_module.is_zero(z2.natural):
            raise ValueError("Деление на ноль")

        comparison = self.natural_module.comparison(z1.natural, z2.natural)

        if comparison == 1:  # |z1| < |z2|
            return Integer(sign=0, natural=NaturalNumber(0))

        quotient_natural = self.natural_module.quotient(z1.natural, z2.natural)

        if self.natural_module.is_zero(quotient_natural):
            return Integer(sign=0, natural=quotient_natural)

        result_sign = 0 if z1.sign == z2.sign else 1
        return Integer(sign=result_sign, natural=quotient_natural)

    def modulus(self, z1: Integer, z2: Integer) -> Integer:
        """Z-10. Остаток от деления целого на целое (делитель отличен от нуля)."""
        if self.natural_module.is_zero(z2.natural):
            raise ValueError("Деление на ноль")

        quotient = self.quotient(z1, z2)
        product = self.multiplication(quotient, z2)
        remainder = self.subtraction(z1, product)

        if remainder.sign == 1:
            remainder = self.addition(remainder, z2)

        return remainder

    def call(self, identifier: Identifier, args: list[str]) -> Any:
        """
        Вызывает метод модуля по идентификатору.

        Args:
            identifier: идентификатор вызываемого метода
            args: аргументы метода в виде строк

        Returns:
            Результат выполнения метода
        """
        match identifier:
            case Identifier.ABS_Z_N:
                ensure_args(identifier, args, 1)
                z = Integer.from_str(args[0])
                return self.absolute_value(z)

            case Identifier.POZ_Z_D:
                ensure_args(identifier, args, 1)
                z = Integer.from_str(args[0])
                return self.sign_determination(z)

            case Identifier.MUL_ZM_Z:
                ensure_args(identifier, args, 1)
                z = Integer.from_str(args[0])
                return self.multiply_by_minus_one(z)

            case Identifier.TRANS_N_Z:
                ensure_args(identifier, args, 1)
                n = NaturalNumber.from_str(args[0])
                return self.natural_to_integer(n)

            case Identifier.TRANS_Z_N:
                ensure_args(identifier, args, 1)
                z = Integer.from_str(args[0])
                return self.integer_to_natural(z)

            case Identifier.ADD_ZZ_Z:
                ensure_args(identifier, args, 2)
                z1 = Integer.from_str(args[0])
                z2 = Integer.from_str(args[1])
                return self.addition(z1, z2)

            case Identifier.SUB_ZZ_Z:
                ensure_args(identifier, args, 2)
                z1 = Integer.from_str(args[0])
                z2 = Integer.from_str(args[1])
                return self.subtraction(z1, z2)

            case Identifier.MUL_ZZ_Z:
                ensure_args(identifier, args, 2)
                z1 = Integer.from_str(args[0])
                z2 = Integer.from_str(args[1])
                return self.multiplication(z1, z2)

            case Identifier.DIV_ZZ_Z:
                ensure_args(identifier, args, 2)
                z1 = Integer.from_str(args[0])
                z2 = Integer.from_str(args[1])
                return self.quotient(z1, z2)

            case Identifier.MOD_ZZ_Z:
                ensure_args(identifier, args, 2)
                z1 = Integer.from_str(args[0])
                z2 = Integer.from_str(args[1])
                return self.modulus(z1, z2)

            case _:
                raise UnknownIdentifierError(identifier)

    def methods(self) -> set[Identifier]:
        """Возвращает множество идентификаторов методов, поддерживаемых модулем."""
        return {
            Identifier.ABS_Z_N,
            Identifier.POZ_Z_D,
            Identifier.MUL_ZM_Z,
            Identifier.TRANS_N_Z,
            Identifier.TRANS_Z_N,
            Identifier.ADD_ZZ_Z,
            Identifier.SUB_ZZ_Z,
            Identifier.MUL_ZZ_Z,
            Identifier.DIV_ZZ_Z,
            Identifier.MOD_ZZ_Z,
        }
