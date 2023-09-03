def solveInputValue(x1: int, x2: int,
                    border1: int, border2: int, border3: int,
                    norm: int, ):
    result1, result2, result3 = 0, 0, 0

    if border1 <= x1 <= border2:
        result1 = (border2 - (abs(x1 - border1))) / border2

    if border1 <= x1 <= border3:
        result2 = (border2 - (abs(x1 - border2))) / border2

    if border2 <= x1 <= border3:
        result3 = (border2 - (abs(x1 - border3))) / border2

    print(result1, result2, result3)

    t = x1 * norm
    print("Кол-во возможных посещений: ", t)

    border2, border3 = t / 2, t

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

    print([{"C1": A1 * B1},
           {"C2": A1 * B2},
           {"C3": A1 * B3},
           {"C1": A2 * B1},
           {"C2": A2 * B2},
           {"C3": A2 * B3},
           {"C1": A3 * B1},
           {"C2": A3 * B2},
           {"C3": A3 * B3}])

    return [{"C1": A1 * B1},
            {"C2": A1 * B2},
            {"C3": A1 * B3},
            {"C1": A2 * B1},
            {"C2": A2 * B2},
            {"C3": A2 * B3},
            {"C1": A3 * B1},
            {"C2": A3 * B2},
            {"C3": A3 * B3}]


def getDefuzzification(listDictionary: [{}]):
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
    return key, maxi


# def main():
#
#     print('-----------------------')
#     A1, A2, A3, B1, B2, B3 = solveInputValue(8, 10, 0, 5, 10, 5)
#     middleMax(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3)))
#
#     print('-----------------------')
#     A1, A2, A3, B1, B2, B3 = solveInputValue(8, 35, 0, 5, 10, 5)
#     middleMax(getDefuzzification(ruleBase(A1, A2, A3, B1, B2, B3)))
#
#
# if __name__ == "__main__":
#     main()
