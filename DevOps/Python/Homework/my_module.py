def contains_200(lookup_dict):
    lookup_value = 200
    return lookup_value in lookup_dict.values()

def divisible_in_range(from_number, to_number):
    numbers = []
    for number in range(from_number, to_number + 1):
        if number % 7 == 0 and number % 5 != 0:
            numbers.append(number)
    return numbers

def find_long_words(string, number):
    words = []
    for word in string.split(" "):
        if len(word) >= number:
            words.append(word)
    return words
    
def divide_nums(divisor, denominator):
    try:
        return divisor / denominator
    except ZeroDivisionError:
        print('You cannot divide by 0')
    
