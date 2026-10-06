"""Introduction to decisions and loops in Python."""

# if / elif / else chooses a block based on a condition.
temperature = 26
if temperature >= 30:
    print("It is hot today.")
elif temperature >= 20:
    print("The weather is mild.")
else:
    print("It is cool today.")

# A for loop visits each item in a sequence.
print("\nCounting with a for loop:")
for number in range(1, 4):  # range(1, 4) produces 1, 2, and 3.
    print(number)

# A while loop repeats as long as its condition remains true.
print("\nCounting with a while loop:")
count = 1
while count <= 3:
    print(count)
    count += 1  # Increase count so the loop eventually ends.

# break exits a loop early; continue skips to its next iteration.
print("\nOdd numbers only:")
for number in range(1, 6):
    if number % 2 == 0:
        continue
    print(number)
