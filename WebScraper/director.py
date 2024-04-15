#Write a program to generate 20 random different 5 digit numbers.

import random

def generate_random_numbers():
    random_numbers = []
    while len(random_numbers) < 20:
        random_number = random.randint(100000, 999999)
        if random_number not in random_numbers:
            random_numbers.append(random_number)
    return random_numbers   

if __name__ == "__main__":
    print(generate_random_numbers())