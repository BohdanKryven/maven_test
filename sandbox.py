def get_amount(amount):
    result = 0
    chars = [500, 200, 100, 50, 20, 10]

    if amount % 10 or amount < 10:
        return -1

    for char in chars:
        while amount >= char:
            amount -= char
            result += 1

    return result


print(get_amount(440))
