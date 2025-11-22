"""
Модуль многочленов

Авторы:
- Кислица Сергей <andret23232347@mail.ru>
- Шарапов Даниил <sharapowdanya@gmail.com>
"""

from hestia.common.exceptions import UnknownIdentifierError
from hestia.common.types import Identifier, Module
from hestia.common.utils import ensure_args
from hestia.rational import RationalNumber, RationalModule
from hestia.integer import Integer, IntegerModule
from hestia.natural import NaturalNumber, NaturalModule


class Polynomial:
    """Класс для представления многочлена"""

    def __init__(self, coefficients):
        """
        Инициализация многочлена
        coefficients - список коэффициентов (RationalNumber или числа) от младших к старшим степеням
        """
        if not coefficients:
            self.coefficients = [RationalNumber(Integer(0), NaturalNumber(1))]
        else:
            self.coefficients = []
            for coef in coefficients:
                if hasattr(coef, "numerator") and hasattr(coef, "denominator"):
                    self.coefficients.append(
                        RationalNumber(coef.numerator, coef.denominator)
                    )
                elif isinstance(coef, (int, str)):
                    if isinstance(coef, str):
                        int_val = Integer.from_str(coef)
                    else:
                        int_val = Integer(coef)
                    self.coefficients.append(RationalNumber(int_val, NaturalNumber(1)))
                elif hasattr(coef, "sign") and hasattr(coef, "natural"):
                    self.coefficients.append(RationalNumber(coef, NaturalNumber(1)))
                else:
                    raise ValueError(f"Некорректный тип коэффициента: {type(coef)}")

        self._normalize()

    def _get_modules(self):
        """Получение экземпляров модулей"""
        natural_module = NaturalModule()
        integer_module = IntegerModule(natural_module)
        rational_module = RationalModule(natural_module, integer_module)
        return natural_module, integer_module, rational_module

    def _normalize(self):
        """Удаление ведущих нулевых коэффициентов"""
        _, integer_module, _ = self._get_modules()
        while len(self.coefficients) > 1:
            last_coef = self.coefficients[-1]
            if integer_module.sign_determination(last_coef.numerator) == 0:
                self.coefficients.pop()
            else:
                break

    def __str__(self):
        """Строковое представление многочлена"""
        _, integer_module, _ = self._get_modules()

        if not self.coefficients:
            return "0"

        terms = []
        for i in range(len(self.coefficients) - 1, -1, -1):
            coef = self.coefficients[i]

            if integer_module.sign_determination(coef.numerator) == 0:
                continue

            coef_str = str(coef)

            if i == 0:
                terms.append(coef_str)
            elif i == 1:
                if coef_str == "1":
                    terms.append("x")
                elif coef_str == "-1":
                    terms.append("-x")
                else:
                    terms.append(f"{coef_str}x")
            else:
                if coef_str == "1":
                    terms.append(f"x^{i}")
                elif coef_str == "-1":
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{coef_str}x^{i}")

        if not terms:
            return "0"

        result = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                result += " - " + term[1:]
            else:
                result += " + " + term

        return result

    def __repr__(self):
        return f"Polynomial({str(self)})"

    def copy(self):
        """Создание копии многочлена"""
        new_coeffs = []
        for coef in self.coefficients:
            new_coeffs.append(RationalNumber(coef.numerator, coef.denominator))
        return Polynomial(new_coeffs)

    @classmethod
    def from_str(cls, s: str) -> "Polynomial":
        """
        Создание многочлена из строки

        :param s: строка с коэффициентами через пробел (от младших к старшим)
        :returns: новый многочлен
        """
        terms = s.replace("-", "+-").split("+")
        # Старший член
        if terms[0] == "":
            terms.pop(0)
        leading_term = terms[0]
        
        if "x" in leading_term:
            if "^" in leading_term:
                leading_coef, leading_pow = leading_term.strip().split("x^")
            else:
                leading_coef, leading_pow = leading_term.strip().split("x")[0], "1"
        else:
            leading_coef, leading_pow = leading_term.strip(), "0"
        
        # "" -> 1, "-" -> -1
        leading_coef = leading_coef.strip()
        if leading_coef in ("", "-"):
            leading_coef += "1"
            
        
        # Список коэффициентов (индекс = степень члена)
        coefficients = [
            RationalNumber(Integer(0), NaturalNumber(1)) \
                for _ in range(int(leading_pow) + 1)
        ]
        
        coefficients[int(leading_pow)] = RationalNumber.from_str(leading_coef)
        
        # Остальные члены
        for term in terms[1:]:
            if "x" in term:
                if "^" in term:
                    coef, pow = term.strip().split("x^")
                else:
                    coef, pow = term.strip().split("x")[0], 1
            else:
                coef, pow = term.strip(), 0
            
            coef = coef.strip()
            if coef in ("", "-"):
                coef += "1"
            
            coefficients[int(pow)] = RationalNumber.from_str(coef)

        return cls(coefficients)


class PolynomialModule(Module):
    """
    Модуль для работы с многочленами
    """

    def __init__(
        self,
        natural_module: NaturalModule,
        integer_module: IntegerModule,
        rational_module: RationalModule,
    ):
        """
        Инициализация модуля многочленов

        :param rational_module: модуль рациональных чисел
        """
        self.natural_module = natural_module
        self.integer_module = integer_module
        self.rational_module = rational_module

    def _create_rational(self, value):
        """
        Создание рационального числа из различных типов

        :param value: значение для преобразования
        :returns: рациональное число
        """
        if isinstance(value, str):
            int_val = Integer.from_str(value)
            return self.rational_module.integer_to_rational(int_val)
        elif isinstance(value, int):
            int_val = Integer(value)
            return self.rational_module.integer_to_rational(int_val)
        elif hasattr(value, "numerator") and hasattr(value, "denominator"):
            return value
        else:
            raise ValueError(f"Невозможно создать рациональное число из {value}")

    def addition(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        Сложение многочленов

        :param a: первый многочлен
        :param b: второй многочлен
        :returns: сумма многочленов
        """
        max_len = max(len(a.coefficients), len(b.coefficients))
        result_coefficients = []

        for i in range(max_len):
            coef_a = (
                a.coefficients[i]
                if i < len(a.coefficients)
                else self._create_rational(0)
            )
            coef_b = (
                b.coefficients[i]
                if i < len(b.coefficients)
                else self._create_rational(0)
            )

            result_coefficients.append(self.rational_module.addition(coef_a, coef_b))

        return Polynomial(result_coefficients)

    def subtraction(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        Вычитание многочленов

        :param a: первый многочлен
        :param b: второй многочлен
        :returns: разность многочленов
        """
        max_len = max(len(a.coefficients), len(b.coefficients))
        result_coefficients = []

        for i in range(max_len):
            coef_a = (
                a.coefficients[i]
                if i < len(a.coefficients)
                else self._create_rational(0)
            )
            coef_b = (
                b.coefficients[i]
                if i < len(b.coefficients)
                else self._create_rational(0)
            )

            result_coefficients.append(self.rational_module.subtraction(coef_a, coef_b))

        return Polynomial(result_coefficients)

    def multiply_by_rational(self, p: Polynomial, q: RationalNumber) -> Polynomial:
        """
        Умножение многочлена на рациональное число

        :param p: многочлен
        :param q: рациональное число
        :returns: произведение многочлена на число
        """
        result_coefficients = []

        for coef in p.coefficients:
            result_coefficients.append(self.rational_module.multiplication(coef, q))

        return Polynomial(result_coefficients)

    def multiply_by_x_power(self, p: Polynomial, k: int) -> Polynomial:
        """
        Умножение многочлена на x^k

        :param p: многочлен
        :param k: степень
        :returns: многочлен, умноженный на x^k
        """
        if k < 0:
            raise ValueError("k должно быть неотрицательным")

        if k == 0:
            return p.copy()

        result_coefficients = [self._create_rational(0) for _ in range(k)] + [
            coef for coef in p.coefficients
        ]
        return Polynomial(result_coefficients)

    def leading_coefficient(self, p: Polynomial) -> RationalNumber:
        """
        Старший коэффициент многочлена

        :param p: многочлен
        :returns: старший коэффициент
        """
        last_coef = p.coefficients[-1]
        return RationalNumber(last_coef.numerator, last_coef.denominator)

    def degree(self, p: Polynomial) -> int:
        """
        Степень многочлена

        :param p: многочлен
        :returns: степень многочлена
        """
        return len(p.coefficients) - 1

    def factorize_coefficients(self, p: Polynomial) -> RationalNumber:
        """
        Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей

        :param p: многочлен
        :returns: рациональное число (НОК знаменателей / НОД числителей)
        """
        if not p.coefficients:
            return self._create_rational(1)

        denominators = []
        for coef in p.coefficients:
            if self.integer_module.sign_determination(coef.numerator) != 0:
                denominators.append(coef.denominator)

        if not denominators:
            return self._create_rational(1)

        lcm_denom = denominators[0]
        for denom in denominators[1:]:
            lcm_denom = self.natural_module.lcm(lcm_denom, denom)

        numerators = []
        for coef in p.coefficients:
            if self.integer_module.sign_determination(coef.numerator) != 0:
                abs_num = self.integer_module.absolute_value(coef.numerator)
                if not self.natural_module.is_zero(abs_num):
                    numerators.append(abs_num)

        if not numerators:
            return self._create_rational(1)

        gcd_num = numerators[0]
        for num in numerators[1:]:
            gcd_num = self.natural_module.gcd(gcd_num, num)

        return RationalNumber(
            self.integer_module.natural_to_integer(gcd_num), lcm_denom
        )

    def multiplication(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        Умножение многочленов

        :param a: первый многочлен
        :param b: второй многочлен
        :returns: произведение многочленов
        """
        result_degree = self.degree(a) + self.degree(b)
        result_coefficients = [
            self._create_rational(0) for _ in range(result_degree + 1)
        ]

        for i, coef_a in enumerate(a.coefficients):
            for j, coef_b in enumerate(b.coefficients):
                product = self.rational_module.multiplication(coef_a, coef_b)
                result_coefficients[i + j] = self.rational_module.addition(
                    result_coefficients[i + j], product
                )

        return Polynomial(result_coefficients)

    def division(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        Частное от деления многочлена на многочлен при делении с остатком

        :param a: делимое
        :param b: делитель
        :returns: частное
        """
        if all(
            self.integer_module.sign_determination(coef.numerator) == 0
            for coef in b.coefficients
        ):
            raise ValueError("Деление на нулевой полином")

        deg_a = self.degree(a)
        deg_b = self.degree(b)

        if deg_a < deg_b:
            return Polynomial([self._create_rational(0)])

        remainder = a.copy()
        quotient_coefficients = [
            self._create_rational(0) for _ in range(deg_a - deg_b + 1)
        ]

        while self.degree(remainder) >= deg_b:
            current_deg_rem = self.degree(remainder)
            current_deg_div = deg_b

            lead_rem = self.leading_coefficient(remainder)
            lead_div = self.leading_coefficient(b)

            coef = self.rational_module.division(lead_rem, lead_div)
            shift = current_deg_rem - current_deg_div

            quotient_coefficients[shift] = coef

            term = self.multiply_by_rational(b, coef)
            term = self.multiply_by_x_power(term, shift)

            remainder = self.subtraction(remainder, term)

        return Polynomial(quotient_coefficients)

    def modulus(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        Остаток от деления многочлена на многочлен при делении с остатком

        :param a: делимое
        :param b: делитель
        :returns: остаток от деления
        """
        if all(
            self.integer_module.sign_determination(coef.numerator) == 0
            for coef in b.coefficients
        ):
            raise ValueError("Деление на нулевой полином")

        deg_a = self.degree(a)
        deg_b = self.degree(b)

        if deg_a < deg_b:
            return a.copy()

        quotient = self.division(a, b)
        product = self.multiplication(quotient, b)
        remainder = self.subtraction(a, product)

        return remainder

    def gcd(self, a: Polynomial, b: Polynomial) -> Polynomial:
        """
        НОД многочленов (алгоритм Евклида)

        :param a: первый многочлен
        :param b: второй многочлен
        :returns: НОД многочленов
        """
        a_copy = a.copy()
        b_copy = b.copy()

        while self.degree(b_copy) >= 0 and not all(
            self.integer_module.sign_determination(coef.numerator) == 0
            for coef in b_copy.coefficients
        ):
            temp = self.modulus(a_copy, b_copy)
            a_copy = b_copy
            b_copy = temp

        if (
            a_copy.coefficients
            and self.integer_module.sign_determination(
                self.leading_coefficient(a_copy).numerator
            )
            == 1
        ):
            a_copy = self.multiply_by_rational(a_copy, self._create_rational(-1))

        return a_copy

    def derivative(self, p: Polynomial) -> Polynomial:
        """
        Производная многочлена

        :param p: многочлен
        :returns: производная многочлена
        """
        if self.degree(p) == 0:
            return Polynomial([self._create_rational(0)])

        result_coefficients = []

        for i in range(1, len(p.coefficients)):
            coef = p.coefficients[i]
            new_coef = self.rational_module.multiplication(
                coef, self._create_rational(i)
            )
            result_coefficients.append(new_coef)

        return Polynomial(result_coefficients)

    def remove_multiples(self, p: Polynomial) -> Polynomial:
        """
        Преобразование многочлена — кратные корни в простые

        :param p: многочлен
        :returns: многочлен без кратных корней
        """
        derivative = self.derivative(p)
        gcd = self.gcd(p, derivative)
        result = self.division(p, gcd)

        return result

    def call(self, identifier: Identifier, args: list[str]) -> object:
        """
        Вызов метода по идентификатору

        :param identifier: идентификатор метода
        :param args: аргументы метода
        :returns: результат выполнения метода
        """
        match identifier:
            case Identifier.ADD_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.addition(a, b)

            case Identifier.SUB_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.subtraction(a, b)

            case Identifier.MUL_PQ_P:
                ensure_args(identifier, args, 2)
                p = Polynomial.from_str(args[0])
                q = RationalNumber.from_str(args[1])
                return self.multiply_by_rational(p, q)

            case Identifier.MUL_Pxk_P:
                ensure_args(identifier, args, 2)
                p = Polynomial.from_str(args[0])
                k = int(args[1])
                return self.multiply_by_x_power(p, k)

            case Identifier.LED_P_Q:
                ensure_args(identifier, args, 1)
                p = Polynomial.from_str(args[0])
                return self.leading_coefficient(p)

            case Identifier.DEG_P_N:
                ensure_args(identifier, args, 1)
                p = Polynomial.from_str(args[0])
                return self.degree(p)

            case Identifier.FAC_P_Q:
                ensure_args(identifier, args, 1)
                p = Polynomial.from_str(args[0])
                return self.factorize_coefficients(p)

            case Identifier.MUL_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.multiplication(a, b)

            case Identifier.DIV_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.division(a, b)

            case Identifier.MOD_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.modulus(a, b)

            case Identifier.GCF_PP_P:
                ensure_args(identifier, args, 2)
                a = Polynomial.from_str(args[0])
                b = Polynomial.from_str(args[1])
                return self.gcd(a, b)

            case Identifier.DER_P_P:
                ensure_args(identifier, args, 1)
                p = Polynomial.from_str(args[0])
                return self.derivative(p)

            case Identifier.NMR_P_P:
                ensure_args(identifier, args, 1)
                p = Polynomial.from_str(args[0])
                return self.remove_multiples(p)

            case _:
                raise UnknownIdentifierError(identifier)

    def methods(self) -> set[Identifier]:
        """
        Получение множества идентификаторов методов

        :returns: множество идентификаторов методов модуля
        """
        return {
            Identifier.ADD_PP_P,
            Identifier.SUB_PP_P,
            Identifier.MUL_PQ_P,
            Identifier.MUL_Pxk_P,
            Identifier.LED_P_Q,
            Identifier.DEG_P_N,
            Identifier.FAC_P_Q,
            Identifier.MUL_PP_P,
            Identifier.DIV_PP_P,
            Identifier.MOD_PP_P,
            Identifier.GCF_PP_P,
            Identifier.DER_P_P,
            Identifier.NMR_P_P,
        }
