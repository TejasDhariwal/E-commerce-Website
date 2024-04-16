""" Will generate a unique id for T-mart account of the seller. """
import random

def generate_unique_number():
    # Initialize an empty set to store generated numbers
    generated_numbers = set()

    # Loop until a unique number is generated
    while True:
        # Generate a random 6-digit number
        random_number = random.randint(100000, 999999)
        
        # Check if the number is unique
        if random_number not in generated_numbers:
            # Add the number to the set
            generated_numbers.add(random_number)
            return random_number

# Generate a unique 6-digit number
unique_number = generate_unique_number()
print("Unique 6-digit number:", unique_number)