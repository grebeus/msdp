from random import randint

number = randint(1,100)
guess = 0

while guess != number:
    try:
        guess = int(input('I made up a number.Can you guess it?\n'))
    except Exception:
        print('Input is not a number, please enter again.\n')
        break
    if guess > number:
        print('Too high')
    elif guess < number:
        print('Too low')
else:
    print('Congratulations you won!')
