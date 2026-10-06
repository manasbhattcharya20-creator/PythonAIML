"""Introduction to handling errors and working with text files."""

# try / except lets a program respond to an error without crashing.
text_number = "42"
try:
    number = int(text_number)
    print("Converted number:", number)
except ValueError:
    print("That text cannot be converted to an integer.")

# Change text_number to something like "hello" to see the except branch.

# A with block opens a file and closes it automatically when the block ends.
# This example writes beside this script, then reads the same file back.
file_name = "python_basics_example.txt"

try:
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("Python makes file handling straightforward.\n")
        file.write("The with block closes this file automatically.\n")

    with open(file_name, "r", encoding="utf-8") as file:
        contents = file.read()

    print("\nText read from the file:")
    print(contents)
except OSError as error:
    # OSError covers common file problems such as permission or path errors.
    print("Could not work with the file:", error)
