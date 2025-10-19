from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any


class Identifier(str, Enum):
    """
    Идентификаторы функций (методов), реализуемых в рамках модулей системы
    компьютерной алгебры.
    """

    COM_NN_D = "N-1"
    NZER_N_B = "N-2"
    ADD_1N_N = "N-3"
    ADD_NN_N = "N-4"
    SUB_NN_N = "N-5"
    MUL_ND_N = "N-6"
    MUL_Nk_N = "N-7"
    MUL_NN_N = "N-8"
    SUB_NDN_N = "N-9"
    DIV_NN_Dk = "N-10"
    DIV_NN_N = "N-11"
    MOD_NN_N = "N-12"
    GCF_NN_N = "N-13"
    LCM_NN_N = "N-14"

    ABS_Z_N = "Z-1"
    POZ_Z_D = "Z-2"
    SGN_Z_D = "Z-2"
    MUL_ZM_Z = "Z-3"
    TRANS_N_Z = "Z-4"
    TRANS_Z_N = "Z-5"
    ADD_ZZ_Z = "Z-6"
    SUB_ZZ_Z = "Z-7"
    MUL_ZZ_Z = "Z-8"
    DIV_ZZ_Z = "Z-9"
    MOD_ZZ_Z = "Z-10"

    RED_Q_Q = "Q-1"
    INT_Q_B = "Q-2"
    TRANS_Z_Q = "Q-3"
    TRANS_Q_Z = "Q-4"
    ADD_QQ_Q = "Q-5"
    SUB_QQ_Q = "Q-6"
    MUL_QQ_Q = "Q-7"
    DIV_QQ_Q = "Q-8"

    ADD_PP_P = "P-1"
    SUB_PP_P = "P-2"
    MUL_PQ_P = "P-3"
    MUL_Pxk_P = "P-4"
    LED_P_Q = "P-5"
    DEG_P_N = "P-6"
    FAC_P_Q = "P-7"
    MUL_PP_P = "P-8"
    DIV_PP_P = "P-9"
    MOD_PP_P = "P-10"
    GCF_PP_P = "P-11"
    DER_P_P = "P-12"
    NMR_P_P = "P-13"


class Module(metaclass=ABCMeta):
    """
    Абстрактный базовый класс для модулей системы.

    Определяет интерфейс, который должны реализовывать все модули системы.
    Каждый модуль предоставляет набор методов, которые могут быть вызваны.
    """

    @abstractmethod
    def call(self, identifier: Identifier, args: list[str]) -> Any:
        """
        Вызывает указанную функцию (метод) с заданными аргументами и возвращает
        полученное значение.

        :param identifier: идентификатор функции
        :param args: аргументы функции
        :returns: результат вызова функции с заданными аргументами
        """
        ...

    @abstractmethod
    def methods(self) -> set[Identifier]:
        """
        Возвращает множество функций (методов), которые реализует данный
        модуль.

        :returns: идентификаторы функций, реализуемых данным модулем.
        """
        ...
