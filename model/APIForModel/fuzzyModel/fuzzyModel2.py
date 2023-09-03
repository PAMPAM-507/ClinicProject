from scipy import integrate


def solveInputValue(x1: int, x2: int,
                    border1: int, border2: int, border3: int,
                    norm: int, hours: int):
    """
    x1 - опыт работы
    x2 - кол-во пациентов
    border1, border2, border3 используются для опыта работы
    norm - максимально возможное кол-во пациентов в час
    hours - длительность рабочего дня в часах
    """

    result1, result2, result3 = 0, 0, 0

    if border1 <= x1 <= border2:
        result1 = (border2 - (abs(x1 - border1))) / border2

    if border1 <= x1 <= border3:
        result2 = (border2 - (abs(x1 - border2))) / border2

    if border2 <= x1 <= border3:
        result3 = (border2 - (abs(x1 - border3))) / border2

    if x1 > 10:
        result1, result2, result3 = 0, 0, 1

    print(result1, result2, result3)

    t = hours * norm

    if x2 > t:
        raise ValueError("Превышено максимальное кол-во посещений")

    print("Кол-во возможных посещений: ", t)

    border1, border2, border3 = 0, t / 2, t

    result11, result22, result33 = 0, 0, 0

    if border1 <= x2 <= border2:
        result11 = (border2 - (abs(x2 - border1))) / border2

    if border1 <= x2 <= border3:
        result22 = (border2 - (abs(x2 - border2))) / border2

    if border2 <= x2 <= border3:
        result33 = (border2 - (abs(x2 - border3))) / border2

    print(result11, result22, result33)

    return result1, result2, result3, result11, result22, result33


def ruleBase(A1: int, A2: int, A3: int,
             B1: int, B2: int, B3: int):
    # print([{"C2": A1 * B1},
    #        {"C3": A1 * B2},
    #        {"C3": A1 * B3},
    #        {"C1": A2 * B1},
    #        {"C2": A2 * B2},
    #        {"C3": A2 * B3},
    #        {"C1": A3 * B1},
    #        {"C1": A3 * B2},
    #        {"C2": A3 * B3}])

    return [{"C1": A1 * B1},
            {"C2": A1 * B2},
            {"C3": A1 * B3},
            {"C1": A2 * B1},
            {"C2": A2 * B2},
            {"C3": A2 * B3},
            {"C1": A3 * B1},
            {"C2": A3 * B2},
            {"C2": A3 * B3}]


def getDefuzzification(listDictionary: list):
    C1maxi, C2maxi, C3maxi = 0, 0, 0

    for i in listDictionary:
        if i.get("C1") is not None and i.get("C1") >= C1maxi:
            C1maxi = i.get("C1")
    for i in listDictionary:
        if i.get("C2") is not None and i.get("C2") >= C2maxi:
            C2maxi = i.get("C2")
    for i in listDictionary:
        if i.get("C3") is not None and i.get("C3") >= C3maxi:
            C3maxi = i.get("C3")

    return {"C1": C1maxi, "C2": C2maxi, "C3": C3maxi}


def firstMax(result: dict):
    print(result)

    val = list(result.values())
    key = list(result.keys())
    maxi = max(result.values())

    for i in range(len(val)):
        if val[i] == maxi:
            index = i
            break

    key = key[index]

    print(key, maxi)

    # return key, maxi
    
    y1 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x1 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
    )
    y2 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x2 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5
    )
    y3 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x3 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )
    y4 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x4 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )
    
    maxi = round(maxi, 1)
    print(key, maxi)
    
    if key == "C1":
        maxi = 0
    elif key == "C2":
        for i in range(len(y2)):
            if y2[i] == maxi:
                maxi = x2[i]
    elif key == "C3":
        for i in range(len(y3)):
            if y3[i] == maxi:
                maxi = x3[i]

    return maxi


def middleMax(result: dict):
    print(result)

    val = list(result.values())
    key = list(result.keys())
    maxi = max(result.values())

    for i in range(len(val)):
        if val[i] == maxi:
            index = i
            break

    key = key[index]

    print(key, maxi)

    # return key, maxi
    
    y1 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x1 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
    )
    y2 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x2 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5
    )
    y3 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x3 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )
    y4 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x4 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )
    
    maxi = round(maxi, 1)
    print(key, maxi)
    x11, x22 = 0, 0
    
    if key == "C1":
        for i in range(len(y1)):
            if y1[i] == maxi:
                x22 = x1[i]
        x11 = 0
    elif key == "C2":
        for i in range(len(y2)):
            if y2[i] == maxi:
                x11 = x2[i]
        for i in range(len(y3)):
            if y3[i] == maxi:
                x22 = x3[i]
    elif key == "C3":
        x22 = 1
        for i in range(len(y4)):
            if y4[i] == maxi:
                x11 = x4[i]

    return (x11 + x22)/2


def CenterOfGravity2(result1, result2, result3):
    print("результаты перед CenterOfGravity2", round(result1, 1), round(result2, 1), round(result3, 1))
    result1, result2, result3 = round(result1, 1), round(result2, 1), round(result3, 1)
    x1_value, x2_value, x3_value, x4_value = 0, 0, 0, 0
    y1 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x1 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5,
    )
    y2 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x2 = (
        0,
        0.05,
        0.1,
        0.15,
        0.2,
        0.25,
        0.3,
        0.35,
        0.4,
        0.45,
        0.5
    )
    y3 = (
        1,
        0.9,
        0.8,
        0.7,
        0.6,
        0.5,
        0.4,
        0.3,
        0.2,
        0.1,
        0
    )
    x3 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )
    y4 = (
        0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1
    )
    x4 = (
        0.5,
        0.55,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    )

    def integrationWithX1(x):
        return x * result1

    def integrationWithX2(x):
        return x * result2

    def integrationWithX3(x):
        return x * result3

    def integration1(x):
        return result1

    def integration2(x):
        return result2

    def integration3(x):
        return result3

    index = 0

    if result1 > result2:
        compare = 'C1>C2'
        if result2 > result3:
            compare = 'C1>C2C2>C3'
            for i in range(len(y1)):
                if y1[i] == result1:
                    print(result1)
                    index = i
            x1_value = x1[index]

            for i in range(len(y1)):
                if y1[i] == result2:
                    index = i
            x2_value = x1[index]

            for i in range(len(y3)):
                if y1[i] == result2:
                    index = i
            x3_value = x3[index]

            for i in range(len(y3)):
                if y1[i] == result3:
                    index = i
            x4_value = x3[index]

            numerator = integrate.quad(integrationWithX1, 0, x2_value)[0] + \
                        integrate.quad(integrationWithX2, x2_value, x4_value)[0] + \
                        integrate.quad(integrationWithX3, x4_value, 1)[0]

            denominator = integrate.quad(integration1, 0, x2_value)[0] + \
                          integrate.quad(integration2, x2_value, x4_value)[0] + \
                          integrate.quad(integration3, x4_value, 1)[0]

        if result3 > result2:
            compare = 'C1>C2C3>C2'

    if result2 > result1:
        compare = 'C2>C1'
        if result2 > result3:
            compare = 'C2>C1C2>C3'

            for i in range(len(y2)):
                if y2[i] == result1:
                    index = i
            x1_value = x2[index]

            for i in range(len(y2)):
                if y2[i] == result2:
                    index = i
            x2_value = x2[index]

            for i in range(len(y3)):
                if y3[i] == result2:
                    index = i
            x3_value = x3[index]

            for i in range(len(y3)):
                if y3[i] == result3:
                    index = i
            x4_value = x3[index]

            numerator = integrate.quad(integrationWithX1, 0, x2_value)[0] + \
                        integrate.quad(integrationWithX2, x2_value, x4_value)[0] + \
                        integrate.quad(integrationWithX3, x4_value, 1)[0]

            denominator = integrate.quad(integration1, 0, x2_value)[0] + \
                          integrate.quad(integration2, x2_value, x4_value)[0] + \
                          integrate.quad(integration3, x4_value, 1)[0]

        if result3 > result2:
            compare = 'C2>C1C3>C2'

            for i in range(len(y2)):
                if y2[i] == result1:
                    index = i
            x1_value = x2[index]

            for i in range(len(y2)):
                if y2[i] == result2:
                    index = i
            x2_value = x2[index]

            for i in range(len(y4)):
                if y4[i] == result2:
                    index = i
            x3_value = x4[index]

            for i in range(len(y4)):
                if y4[i] == result3:
                    index = i
            x4_value = x4[index]

            numerator = integrate.quad(integrationWithX1, 0, x1_value)[0] + \
                        integrate.quad(integrationWithX2, x1_value, x3_value)[0] + \
                        integrate.quad(integrationWithX3, x3_value, 1)[0]

            denominator = integrate.quad(integration1, 0, x1_value)[0] + \
                          integrate.quad(integration2, x1_value, x3_value)[0] + \
                          integrate.quad(integration3, x3_value, 1)[0]

    print(x1_value, x2_value, x3_value, x4_value)
    print(compare)

    try:
        result_value = numerator / denominator
    except:
        result_value = 0

    print("результат CGЖ: ", result_value)

    return result_value


def CenterOfGravity(result: dict, border1=0, border2=0.5, border3=1):
    result1, result2, result3 = 0, 0, 0
    x1 = result.get("C1")
    x2 = result.get("C2")
    x3 = result.get("C3")

    print(x1, x2, x3)

    if border1 <= x1 <= border2:
        result1 = (border2 - (abs(x1 - border1))) / border2

    if border1 <= x2 <= border3:
        result2 = (border2 - (abs(x2 - border2))) / border2

    if border2 <= x3 <= border3:
        result3 = (border2 - (abs(x3 - border3))) / border2

    print(result1, result2, result3)

    if result1 == 0:
        result1 = result2
    if result3 == 0:
        result3 = result2

    def integrationWithX1(x):
        return x * result1

    def integrationWithX2(x):
        return x * result2

    def integrationWithX3(x):
        return x * result3

    def integration1(x):
        return result1

    def integration2(x):
        return result2

    def integration3(x):
        return result3

    numerator = integrate.quad(integrationWithX1, 0.0, 0.25)[0] + integrate.quad(integrationWithX2, 0.25, 0.75)[0] + \
                integrate.quad(integrationWithX3, 0.75, 1)[0]

    denominator = integrate.quad(integration1, 0.0, 0.25)[0] + integrate.quad(integration2, 0.25, 0.75)[0] + \
                  integrate.quad(integration3, 0.75, 1)[0]

    try:
        result_value = numerator / denominator
    except:
        result_value = 0

    print("результат CGЖ: ", result_value)

    return result_value


def out_class(y: float, border1=0, border2=0.5, border3=1):
    result1, result2, result3 = 0, 0, 0

    if border1 <= y <= border2:
        result1 = (border2 - (abs(y - border1))) / border2

    if border1 <= y <= border3:
        result2 = (border2 - (abs(y - border2))) / border2

    if border2 <= y <= border3:
        result3 = (border2 - (abs(y - border3))) / border2

    print("Степень принадлежности к терму 'Низкая загрузка': ", result1)
    print("Степень принадлежности к терму 'Средняя загрузка': ", result2)
    print("Степень принадлежности к терму 'Высокая загрузка': ", result3)

    result = {'C1': result1, 'C2': result2, 'C3': result3}

    val = list(result.values())
    key = list(result.keys())
    maxi = max(result.values())

    for i in range(len(val)):
        if val[i] == maxi:
            index = i
            break

    key = key[index]

    return key, y


def Height(values: dict, border1=0, border2=0.5, border3=1):
    result = []
    valC1 = []
    valC2 = []
    valC3 = []
    
    for i in values:
        if i.get("C1") != 0.0 and i.get("C2") != 0.0 and i.get("C3") != 0.0:
            result.append(i)
    for i in result:
        if i.get("C1", False):
            valC1.append(i.get("C1"))
        elif i.get("C2", False):
            valC2.append(i.get("C2"))
        elif i.get("C3", False):
            valC3.append(i.get("C3"))      

    denominator = sum(valC1) + sum(valC2) + sum(valC3)
    
    valC1, valC2, valC3 = list(map(lambda x: x*border1, valC1)), list(map(lambda x: x*border2, valC2)), list(map(lambda x: x*border3, valC3))
    
    numerator = sum(valC1) + sum(valC2) + sum(valC3)
    
    return numerator/denominator
    

def main():
    
    # print('firstMax')
    A1, A2, A3, B1, B2, B3 = solveInputValue(7, 5, 0, 5, 10, 5, 8)
    # print(out_class(firstMax(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3)))))

    print('-----------------------')
    print('middleMax')
    print(out_class(middleMax(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3)))))

    print('CenterOfGravity')
    print(out_class(CenterOfGravity2(*list(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3)).values()))))

    print('-----------------------')
    print('Height')

    print(out_class(Height(ruleBase(A1, A2, A3, B1, B2, B3))))
    print('-----------------------')
    print('Height')
    A1, A2, A3, B1, B2, B3 = solveInputValue(7, 5, 0, 5, 10, 5, 8)
    print(out_class(Height(ruleBase(A1, A2, A3, B1, B2, B3))))

if __name__ == "__main__":
    main()
