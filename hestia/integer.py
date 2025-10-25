"""
Модуль целых чисел
Авторы:
- Кислица Сергей <andret23232347@mail.ru>
...
"""

from common.exceptions import UnknownIdentifierError
from common.types import Identifier, Module
from common.utils import ensure_args
from typing import Any
from natural import NaturalNumber, NaturalModule


class Integer:
    def __init__(self, sign: int, natural: NaturalNumber) -> None:
        """
        Инициализация целого числа.
        sign: 0 - положительное, 1 - отрицательное
        natural: натуральное число (модуль)
        """
        if sign not in (0, 1):
            raise ValueError("Знак должен быть 0 (положительное) или 1 (отрицательное)")
        
        self.sign = sign
        self.natural = natural
        
        if natural.value == [0]:
            self.sign = 0

    def __str__(self) -> str:
        """Строковое представление целого числа"""
        if self.sign == 1:
            return "-" + str(self.natural)
        return str(self.natural)

    @classmethod
    def from_str(cls, s: str) -> "Integer":
        """Создание целого числа из строки"""
        if not s:
            raise ValueError("Пустая строка")
        
        if s[0] == '-':
            sign = 1
            digits_str = s[1:]
        else:
            sign = 0
            digits_str = s
        
        natural = NaturalNumber.from_str(digits_str)
        return cls(sign, natural)

    @classmethod
    def from_int(cls, n: int) -> "Integer":
        """Создание целого числа из целого Python"""
        if n < 0:
            sign = 1
            n = -n
        else:
            sign = 0
        
        natural = NaturalNumber(n)
        return cls(sign, natural)

    @classmethod
    def from_natural(cls, natural: NaturalNumber) -> "Integer":
        """Создание целого числа из натурального (положительного)"""
        return cls(0, natural)


class IntegerModule(Module):
    def __init__(self, natural_module: NaturalModule):
        """
        Инициализация модуля целых чисел.
        natural_module: модуль натуральных чисел для использования его функций
        """
        self.natural_module = natural_module

    def absolute_value(self, z: Integer) -> NaturalNumber:
        """
        Z-1. Абсолютная величина числа, результат - натуральное
        """
        ...

    def sign_determination(self, z: Integer) -> int:
        """
        Z-2. Определение положительности числа.
        Возвращает:
         2 - положительное, 0 - равное нулю, 1 - отрицательное
        """
        ...

    def multiply_by_minus_one(self, z: Integer) -> Integer:
        """
        Z-3. Умножение целого на (-1)
        """
        ...

    def natural_to_integer(self, n: NaturalNumber) -> Integer:
        """
        Z-4. Преобразование натурального в целое
        """
        ...

    def integer_to_natural(self, z: Integer) -> NaturalNumber:
        """
        Z-5. Преобразование целого неотрицательного в натуральное
        """
        ...

    def addition(self, z1: Integer, z2: Integer) -> Integer:
        """
        Z-6. Сложение целых чисел
        """
        ...

    def subtraction(self, z1: Integer, z2: Integer) -> Integer:
        """
        Z-7. Вычитание целых чисел
        """
        ...

    def multiplication(self, z1: Integer, z2: Integer) -> Integer:
        """
        Z-8. Умножение целых чисел
        """
        ...

    def quotient(self, z1: Integer, z2: Integer) -> Integer:
        """
        Z-9. Частное от деления целого на целое (делитель отличен от нуля)
        """
        ...

    def modulus(self, z1: Integer, z2: Integer) -> Integer:
        """
        Z-10. Остаток от деления целого на целое (делитель отличен от нуля)
        """
        ...

    def call(self, identifier: Identifier, args: list[str]) -> Any:
        """
        Вызывает метод модуля по идентификатору.
        identifier - идентификатор вызываемого метода
        args - аргументы метода в виде строк
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
        """
        Возвращает множество идентификаторов методов, поддерживаемых модулем.
        """
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
