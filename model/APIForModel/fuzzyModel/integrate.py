# подключим пакет интегрирования из библиотеки scipy
from scipy import integrate


# опишем подынтегральную функцию
def target_function_f(x):
    return x * 0.6

def target_function_f2(x):
    return 0.6
# выполним интегрирование
result = integrate.quad(target_function_f, 0.0, 3.0)
result = integrate.quad(target_function_f2, 0.0, 3.0)
# посмотрим результат
print(result)

print('--------------')

y = 0.5

x = 0.5 * y - 0.5


def integrationWithX(x, value: float):
    return x * value


def integration(value: float):
 return value