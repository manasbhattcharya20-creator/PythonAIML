"""Introduction to creating, inspecting, and formatting strings."""

message = "  Learn Python step by step  "

# String methods return useful results; strip removes edge whitespace.
clean_message = message.strip()
print("Clean text:", clean_message)
print("Uppercase:", clean_message.upper())
print("Lowercase:", clean_message.lower())

# Strings can be indexed and sliced like other sequences.
print("First character:", clean_message[0])
print("First five characters:", clean_message[:5])
print("Number of characters:", len(clean_message))

# Use in to check whether a smaller string appears inside another string.
print("Contains 'Python'?:", "Python" in clean_message)

# f-strings insert variable values directly into readable text.
language = "Python"
version = 3
print(f"I am learning {language} {version}.")

# split breaks text into a list; join combines items into a string.
words = clean_message.split()
print("Words:", words)
print("Joined with hyphens:", "-".join(words))
