"""
    Модуль натуральных чисел
    Авторы:
    - Калениченко Светлана <calenichenko.s@yandex.ru>
    - Донцова Ирина
    - Митин Георгий
"""
from common.exceptions import UnknownIdentifierError
from common.types import Identifier, Module
from common.utils import ensure_args
from typing import Any

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
            value //=10
        self.value = res

    def __str__(self) -> str:
        return ''.join(str(n) for n in reversed(self.value))
    
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

class NaturalModule(Module):
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
        if len(n1.value) > len(n2.value):
            return 2
        elif len(n2.value) > len(n1.value):
            return 1
        for i in range(len(n1.value)-1, -1, -1):
            if n1.value[i] > n2.value[i]:
                return 2
            elif n2.value[i] > n1.value[i]:
                return 1
        return 0

    def is_zero(self, n: NaturalNumber) -> bool:
        """
        N-2. Проверка на 0.
        Возвращает:
        "да", если n = 0
        "нет", иначе
        """
        return len(n.value) == 1 and n.value[0] == 0
    
    def add_one(self, n: NaturalNumber) -> NaturalNumber:
        """
        N-3. Добавляет к числу n единицу.
        """
        digits = n.value.copy()
        carry = 1
        for i in range(len(digits)):
            s = digits[i] + carry
            digits[i] = s % 10
            carry = s // 10
            if carry == 0:
                break
        if carry > 0:
            digits.append(carry)
        return NaturalNumber.from_digits(digits)

    def adding(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-4. Складывает два натуральных числа n1 и n2.
        """
        a = n1.value
        b = n2.value
        max_len = max(len(a), len(b))
        result = []
        carry = 0
        for i in range(max_len):
            d1 = a[i] if i < len(a) else 0
            d2 = b[i] if i < len(b) else 0
            s = d1 + d2 + carry
            result.append(s % 10)
            carry = s // 10
        if carry > 0:
            result.append(carry)
        return NaturalNumber.from_digits(result)
    
    def subtracting(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-5. Вычитает из первого большего натурального числа n1 второе меньшее или равное n2.
        """
        cmp = self.comparison(n1, n2)

        a = n1.value[:]
        b = n2.value[:]
        result = []
        borrow = 0 

        for i in range(len(a)):
            d1 = a[i]
            d2 = b[i] if i < len(b) else 0

            diff = d1 - d2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0

            result.append(diff)
        while len(result) > 1 and result[-1] == 0:
            result.pop()

        return NaturalNumber.from_digits(result)
    
    def multiply_by_digit(self, n: NaturalNumber, digit: int) -> NaturalNumber:
        """
        N-6. Умножает натуральное число n на цифру digit.
        """
        if digit == 0:
            return NaturalNumber.from_digits([0])
        digits = n.value.copy()
        result = []
        carry = 0
        for i in range(len(digits)):
            product = digits[i] * digit + carry
            result.append(product % 10)
            carry = product // 10
        if carry > 0:
            result.append(carry)
        return NaturalNumber.from_digits(result)
    
    def multiply_by_power_of_10(self, n: NaturalNumber, k: int) -> NaturalNumber:
        """
        N-7. Умножает натуральное число n на 10^k.
        """
        if k == 0:
            return NaturalNumber(n.value.copy())
        result = [0] * k + n.value
        return NaturalNumber.from_digits(result)
    
    def multiplication(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-8. Умножает два натуральных числа n1 и n2.
        """
        if self.is_zero(n1) or self.is_zero(n2):
            return NaturalNumber.from_digits([0])
        result = NaturalNumber.from_digits([0])
        for i in range(len(n2.value)):
            partial_product = self.multiply_by_digit(n1, n2.value[i])
            shifted_product = self.multiply_by_power_of_ten(partial_product, i)
            result = self.adding(result, shifted_product)

        return result
    
    def subtract_with_digit(self, n1: NaturalNumber, n2: NaturalNumber, digit: int) -> NaturalNumber:
        """
        N-9. Вычитание из натурального n1 другого натурального n2, умноженного на цифру digit
        для случая с неотрицательным результатом.
        """
        n2d = self.multiply_by_digit(n2, digit)
        return self.subtracting(n1, n2d)

    def first_digit(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-10. Вычисление первой цифры деления большего натурального на меньшее, 
        домноженное на 10^k,где k - номер позиции этой цифры (номер считается с нуля).
        """
        if self.comparison(n1, n2) == 1:
            return NaturalNumber(0)

        k = len(n1.value) - len(n2.value)
        n2k = self.multiply_by_power_of_10(n2, k)
        if self.comparison(n1, n2k) == 1:
            k -= 1
            n2k = self.multiply_by_power_of_10(n2, k)
        d = 0
        while d < 9 and self.comparison(n1, self.multiply_by_digit(n2k, d + 1)) != 1:
            d += 1
        return NaturalNumber(d)
    
    def quotient(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-11. Неполное частное от деления первого натурального числа n1 на второе n2>0 с остатком.
        """
        if self.comparison(n1, n2) == 1:
            return NaturalNumber(0)

        q = [0] * (len(n1.value) - len(n2.value) + 1)
        r = NaturalNumber.from_digits(n1.value[:])
        while self.comparison(r, n2) in (2, 0):
            c = self.first_digit(r, n2)
            d = c.value[0]
            k = len(r.value) - len(n2.value)
            n2k = self.multiply_by_power_of_10(n2, k)
            if self.comparison(r, n2k) == 1 and k > 0:
                k -= 1
                n2k = self.multiply_by_power_of_10(n2, k)

            r = self.subtract_with_digit(r, n2k, d)
            q[k] += d
        while len(q) > 1 and q[-1] == 0:
            q.pop()

        return NaturalNumber.from_digits(q)
    
    def modulus(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-12. Остаток от деления первого натурального числа n1 на второе натуральное n2>0.
        """
        if self.comparison(n1, n2) == 1:
            return NaturalNumber.from_digits(n1.value[:])
        r = NaturalNumber.from_digits(n1.value[:])
        while self.comparison(r, n2) in (2, 0):
            c = self.first_digit(r, n2)
            d = c.value[0]
            k = len(r.value) - len(n2.value)
            n2k = self.multiply_by_power_of_10(n2, k)

            if self.comparison(r, n2k) == 1 and k > 0:
                k -= 1
                n2k = self.multiply_by_power_of_10(n2, k)

            r = self.subtract_with_digit(r, n2k, d)
        while len(r.value) > 1 and r.value[-1] == 0:
            r.value.pop()

        return r
    
    def gcd(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-13. НОД натуральных чисел n1 и n2.
        """
        a = NaturalNumber.from_digits(n1.value.copy())
        b = NaturalNumber.from_digits(n2.value.copy())
        while not self.is_zero(b):
            r = self.modulus(a, b)
            a, b = b, r
        return a
    
    def lcm(self, n1: NaturalNumber, n2: NaturalNumber) -> NaturalNumber:
        """
        N-14. НОК натуральных чисел n1 и n2.
        """
        if self.is_zero(n1) or self.is_zero(n2):
            return NaturalNumber.from_digits([0])
        g = self.gcd(n1, n2)
        product = self.multiplication(n1, n2)
        return self.quotient(product, g)  

    def call(self, identifier: Identifier, args: list[str]) -> Any:
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
            Identifier.LCM_NN_N
        }
