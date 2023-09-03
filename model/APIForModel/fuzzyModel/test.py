from scipy import integrate


def test(result1, result2, result3):
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


def main():
    test(0.6, 0.3, 0.1)
    print('----------')
    test(0, 0.6, 0.2)
    print('----------')
    test(0.2, 0.4, 0.7)


if __name__ == "__main__":
    main()
