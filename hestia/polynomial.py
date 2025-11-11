"""
Модуль полиномов.

Авторы:
- Кислица Сергей <andret23232347@mail.ru>
...
"""

class Polynomial:
    """Класс для представления многочлена"""
    
    def __init__(self, coefficients):
        """
        Инициализация многочлена
        coefficients - список коэффициентов (RationalNumber или числа) от младших к старшим степеням
        """
        if not coefficients:
            from rational import RationalNumber
            from integer import Integer
            from natural import NaturalNumber
            self.coefficients = [RationalNumber(Integer(0), NaturalNumber(1))]
        else:
            self.coefficients = []
            for coef in coefficients:
                if hasattr(coef, 'numerator') and hasattr(coef, 'denominator'): 
                    from rational import RationalNumber
                    self.coefficients.append(RationalNumber(coef.numerator, coef.denominator))
                elif isinstance(coef, (int, str)):
                    from rational import RationalNumber
                    from integer import Integer
                    from natural import NaturalNumber
                    if isinstance(coef, str):
                        int_val = Integer.from_str(coef)
                    else:
                        int_val = Integer(coef)
                    self.coefficients.append(RationalNumber(int_val, NaturalNumber(1)))
                elif hasattr(coef, 'sign') and hasattr(coef, 'natural'):
                    from rational import TRANS_Z_Q
                    self.coefficients.append(TRANS_Z_Q(coef))
                else:
                    raise ValueError(f"Некорректный тип коэффициента: {type(coef)}")
        
        self._normalize()
    
    def _get_modules(self):
        from natural import NaturalModule
        from integer import IntegerModule
        from rational import RationalModule
        
        natural_module = NaturalModule()
        integer_module = IntegerModule(natural_module)
        rational_module = RationalModule(natural_module, integer_module)
        return natural_module, integer_module, rational_module
    
    def _normalize(self):
        """Удаление ведущих нулевых коэффициентов"""
        natural_module, integer_module, rational_module = self._get_modules()
        while len(self.coefficients) > 1:
            last_coef = self.coefficients[-1]
            if integer_module.sign_determination(last_coef.numerator) == 0:
                self.coefficients.pop()
            else:
                break
    
    def __str__(self):
        """Строковое представление многочлена"""
        natural_module, integer_module, rational_module = self._get_modules()
        
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
            from rational import RationalNumber
            new_coeffs.append(RationalNumber(coef.numerator, coef.denominator))
        return Polynomial(new_coeffs)


def _get_rational_module():
    from natural import NaturalModule
    from integer import IntegerModule
    from rational import RationalModule
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    return RationalModule(natural_module, integer_module)


def _create_rational(value):
    from rational import RationalNumber
    from integer import Integer
    from natural import NaturalNumber
    
    if isinstance(value, str):
        int_val = Integer.from_str(value)
        return RationalNumber(int_val, NaturalNumber(1))
    elif isinstance(value, int):
        int_val = Integer(value)
        return RationalNumber(int_val, NaturalNumber(1))
    elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):
        return value
    else:
        raise ValueError(f"Невозможно создать рациональное число из {value}")


def ADD_PP_P(a, b):
    """Сложение многочленов"""
    rational_module = _get_rational_module()
    
    max_len = max(len(a.coefficients), len(b.coefficients))
    result_coefficients = []
    
    for i in range(max_len):
        coef_a = a.coefficients[i] if i < len(a.coefficients) else _create_rational(0)
        coef_b = b.coefficients[i] if i < len(b.coefficients) else _create_rational(0)
        
        result_coefficients.append(rational_module.addition(coef_a, coef_b))
    
    return Polynomial(result_coefficients)


def SUB_PP_P(a, b):
    """Вычитание многочленов"""
    rational_module = _get_rational_module()
    
    max_len = max(len(a.coefficients), len(b.coefficients))
    result_coefficients = []
    
    for i in range(max_len):
        coef_a = a.coefficients[i] if i < len(a.coefficients) else _create_rational(0)
        coef_b = b.coefficients[i] if i < len(b.coefficients) else _create_rational(0)
        
        result_coefficients.append(rational_module.subtraction(coef_a, coef_b))
    
    return Polynomial(result_coefficients)


def MUL_PQ_P(p, q):
    """Умножение многочлена на рациональное число"""
    rational_module = _get_rational_module()
    result_coefficients = []
    
    for coef in p.coefficients:
        result_coefficients.append(rational_module.multiplication(coef, q))
    
    return Polynomial(result_coefficients)


def MUL_Pxk_P(p, k):
    """Умножение многочлена на x^k"""
    if k < 0:
        raise ValueError("k должно быть неотрицательным")
    
    if k == 0:
        return p.copy()
    
    result_coefficients = [_create_rational(0) for _ in range(k)] + [coef for coef in p.coefficients]
    return Polynomial(result_coefficients)


def LED_P_Q(p):
    """Старший коэффициент многочлена"""
    from rational import RationalNumber
    last_coef = p.coefficients[-1]
    return RationalNumber(last_coef.numerator, last_coef.denominator)


def DEG_P_N(p):
    """Степень многочлена"""
    return len(p.coefficients) - 1


def FAC_P_Q(p):
    """Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей"""
    from natural import NaturalModule
    from integer import IntegerModule
    from rational import RationalNumber
    
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    
    if not p.coefficients:
        return _create_rational(1)
    
    denominators = []
    for coef in p.coefficients:
        if integer_module.sign_determination(coef.numerator) != 0:  
            denominators.append(coef.denominator)
    
    if not denominators:
        return _create_rational(1)
    
    lcm_denom = denominators[0]
    for denom in denominators[1:]:
        lcm_denom = natural_module.lcm(lcm_denom, denom)
    
    numerators = []
    for coef in p.coefficients:
        if integer_module.sign_determination(coef.numerator) != 0:  
            abs_num = integer_module.absolute_value(coef.numerator)
            if not natural_module.is_zero(abs_num): 
                numerators.append(abs_num)
    
    if not numerators:
        return _create_rational(1)
    

    gcd_num = numerators[0] 
    for num in numerators[1:]:
        gcd_num = natural_module.gcd(gcd_num, num)
    
    return RationalNumber(integer_module.natural_to_integer(gcd_num), lcm_denom)


def MUL_PP_P(a, b):
    """Умножение многочленов"""
    rational_module = _get_rational_module()
    
    result_degree = DEG_P_N(a) + DEG_P_N(b)
    result_coefficients = [_create_rational(0) for _ in range(result_degree + 1)]
    
    for i, coef_a in enumerate(a.coefficients):
        for j, coef_b in enumerate(b.coefficients):
            product = rational_module.multiplication(coef_a, coef_b)
            result_coefficients[i + j] = rational_module.addition(result_coefficients[i + j], product)
    
    return Polynomial(result_coefficients)


def DIV_PP_P(a, b):
    """Частное от деления многочлена на многочлен при делении с остатком"""
    from natural import NaturalModule
    from integer import IntegerModule
    
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    rational_module = _get_rational_module()
    
    if all(integer_module.sign_determination(coef.numerator) == 0 for coef in b.coefficients):
        raise ValueError("Деление на нулевой полином")
    
    deg_a = DEG_P_N(a)
    deg_b = DEG_P_N(b)
    
    if deg_a < deg_b:
        return Polynomial([_create_rational(0)])
    
    remainder = a.copy()
    quotient_coefficients = [_create_rational(0) for _ in range(deg_a - deg_b + 1)]
    
    while DEG_P_N(remainder) >= deg_b:
        current_deg_rem = DEG_P_N(remainder)
        current_deg_div = deg_b
        
        lead_rem = LED_P_Q(remainder)
        lead_div = LED_P_Q(b)
        
        coef = rational_module.division(lead_rem, lead_div)
        shift = current_deg_rem - current_deg_div
        
        quotient_coefficients[shift] = coef
        
        term = MUL_PQ_P(b, coef)
        term = MUL_Pxk_P(term, shift)
        
        remainder = SUB_PP_P(remainder, term)
    
    return Polynomial(quotient_coefficients)


def MOD_PP_P(a, b):
    """Остаток от деления многочлена на многочлен при делении с остатком"""
    from natural import NaturalModule
    from integer import IntegerModule
    
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    
    if all(integer_module.sign_determination(coef.numerator) == 0 for coef in b.coefficients):
        raise ValueError("Деление на нулевой полином")
    
    deg_a = DEG_P_N(a)
    deg_b = DEG_P_N(b)
    
    if deg_a < deg_b:
        return a.copy()
    
    quotient = DIV_PP_P(a, b)
    
    product = MUL_PP_P(quotient, b)
    
    remainder = SUB_PP_P(a, product)
    
    return remainder


def GCF_PP_P(a, b):
    """НОД многочленов (алгоритм Евклида)"""
    from natural import NaturalModule
    from integer import IntegerModule
    
    natural_module = NaturalModule()
    integer_module = IntegerModule(natural_module)
    
    a_copy = a.copy()
    b_copy = b.copy()
    
    while DEG_P_N(b_copy) >= 0 and not all(integer_module.sign_determination(coef.numerator) == 0 for coef in b_copy.coefficients):
        temp = MOD_PP_P(a_copy, b_copy)
        a_copy = b_copy
        b_copy = temp
    
    if a_copy.coefficients and integer_module.sign_determination(LED_P_Q(a_copy).numerator) == 1:  # Если старший коэффициент отрицательный
        a_copy = MUL_PQ_P(a_copy, _create_rational(-1))
    
    return a_copy


def DER_P_P(p):
    """Производная многочлена"""
    rational_module = _get_rational_module()
    
    if DEG_P_N(p) == 0:
        return Polynomial([_create_rational(0)])
    
    result_coefficients = []
    
    for i in range(1, len(p.coefficients)):
        coef = p.coefficients[i]
        new_coef = rational_module.multiplication(coef, _create_rational(i))
        result_coefficients.append(new_coef)
    
    return Polynomial(result_coefficients)


def NMR_P_P(p):
    """Преобразование многочлена — кратные корни в простые"""
    derivative = DER_P_P(p)
    
    gcd = GCF_PP_P(p, derivative)
    
    result = DIV_PP_P(p, gcd)
    
    return result
