"""
Модуль натуральных чисел
Авторы:
- Калениченко Светлана <calenichenko.s@yandex.ru>
...
"""

from common.exceptions import UnknownIdentifierError
from common.types import Identifier, Module
from common.utils import ensure_args


class NaturalNumber:
    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError("Натуральные числа не могут быть меньше 0")

        if value == 0:
            self.value = [0]
            return
        res = []
        while value > 0:
            res.append(value % 10)
            value //= 10
        self.value = res

    def __str__(self) -> str:
        return "".join(str(n) for n in reversed(self.value))

    @classmethod
    def from_str(cls, s: str) -> "NaturalNumber":
        try:
            n = int(s)
        except ValueError:
            raise ValueError("Невозможно создать натуральное число из поданной строки")
        if n < 0:
            raise ValueError("Натуральное число не может быть отрицательным")
        return cls(n)

    @classmethod
    def from_digits(cls, digits: list[int]) -> "NaturalNumber":
        v = cls(0)
        v.value = digits
        return v


class NaturalModul(Module):
    def __init__(self):
        """
        Инициализация модуля натуральных чисел.
        """
        pass

    def comparison(self, n1: NaturalNumber, n2: NaturalNumber) -> int:
        """
        N-1. Сравнивает 2 натуральных числа n1 и n2.
        Возвращает:
         2, если n1 > n2
         0, если n1 = n2
         1, иначе
        """
        ...

    def is_zero(self, n: NaturalNumber) -> bool:
        """
        N-2. Проверка на 0.
        Возвращает:
        "да", если n = 0
        "нет", иначе
        """
        ...

    def add_one(self, n: NaturalNumber) -> NaturalNumber:
        """
        N-3. Добавляет к числу n единицу.
        """

    def adding(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-4. Складывает два натуральных числа n1 и n2.
        """
        ...

    def subtracting(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-5. Вычитает из первого большего натурального числа n1 второе меньшее или равное n2.
        """
        ...

    def multiply_by_digit(self, n: NaturalNumber, digit: int) -> NaturalNumber:
        """
        N-6. Умножает натуральное число n на цифру digit.
        """
        ...

    def multiply_by_power_of_10(self, n: NaturalNumber, k: int) -> NaturalNumber:
        """
        N-7. Умножает натуральное число n на 10^k.
        """
        ...

    def multiplication(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-8. Умножает два натуральных числа n1 и n2.
        """
        ...

    def subtract_with_digit(
        self, n1: NaturalNumber, n2: NaturalNumber, digit: int
    ) -> NaturalNumber:
        """
        N-9. Вычитание из натурального n1 другого натурального n2, умноженного на цифру digit
        для случая с неотрицательным результатом.
        """
        ...

    def first_digit(self, n1: NaturalNumber, n2: NaturalNumber) -> int:
        """
        N-10. Вычисление первой цифры деления большего натурального на меньшее,
        домноженное на 10^k,где k - номер позиции этой цифры (номер считается с нуля).
        """
        ...

    def quotient(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-11. Неполное частное от деления первого натурального числа n1 на второе n2>0 с остатком.
        """
        ...

    def modulus(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-12. Остаток от деления первого натурального числа n1 на второе натуральное n2>0.
        """
        ...

    def gcd(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-13. НОД натуральных чисел n1 и n2.
        """
        ...

    def lcm(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-14. НОК натуральных чисел n1 и n2.
        """
        ...

    def call(self, identifier: Identifier, args: list[str]) -> any:
        """
        Вызывает метод модуля по идентификатору.
        identifier - идентификатор вызываемого метода
        args - аргументы метода в виде строк
        """
        match identifier:
            case Identifier.COM_NN_D:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.comparison(n1, n2)

            case Identifier.NZER_N_B:
                ensure_args(identifier, args, 1)
                n = NaturalNumber.from_str(args[0])
                return self.is_zero(n)

            case Identifier.ADD_1N_N:
                ensure_args(identifier, args, 1)
                n = NaturalNumber.from_str(args[0])
                return self.add_one(n)

            case Identifier.ADD_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.adding(n1, n2)

            case Identifier.SUB_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.subtracting(n1, n2)

            case Identifier.MUL_ND_N:
                ensure_args(identifier, args, 2)
                n = NaturalNumber.from_str(args[0])
                digit = int(args[1])
                return self.multiply_by_digit(n, digit)

            case Identifier.MUL_Nk_N:
                ensure_args(identifier, args, 2)
                n = NaturalNumber.from_str(args[0])
                k = int(args[1])
                return self.multiply_by_power_of_10(n, k)

            case Identifier.MUL_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.multiplication(n1, n2)

            case Identifier.SUB_NDN_N:
                ensure_args(identifier, args, 3)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                digit = int(args[2])
                return self.subtract_with_digit(n1, n2, digit)

            case Identifier.DIV_NN_Dk:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.first_digit(n1, n2)

            case Identifier.DIV_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.quotient(n1, n2)

            case Identifier.MOD_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.modulus(n1, n2)

            case Identifier.GCF_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.gcd(n1, n2)

            case Identifier.LCM_NN_N:
                ensure_args(identifier, args, 2)
                n1 = NaturalNumber.from_str(args[0])
                n2 = NaturalNumber.from_str(args[1])
                return self.lcm(n1, n2)

            case _:
                raise UnknownIdentifierError(identifier)

    def methods(self) -> set[Identifier]:
        """
        Возвращает множество идентификаторов методов, поддерживаемых модулем.
        """
        return {
            Identifier.COM_NN_D,
            Identifier.NZER_N_B,
            Identifier.ADD_1N_N,
            Identifier.ADD_NN_N,
            Identifier.SUB_NN_N,
            Identifier.MUL_ND_N,
            Identifier.MUL_Nk_N,
            Identifier.MUL_NN_N,
            Identifier.SUB_NDN_N,
            Identifier.DIV_NN_Dk,
            Identifier.DIV_NN_N,
            Identifier.MOD_NN_N,
            Identifier.GCF_NN_N,
            Identifier.LCM_NN_N,
        }
