"""OOP note: initialize each object with its own data and useful methods."""


class Student:
    def __init__(self, name, score):
        # __init__ runs automatically when Student(...) creates an object.
        # self.name and self.score are instance attributes: each student has its own.
        self.name = name
        self.score = score

    def introduce(self):
        # Instance methods use self to read or change the current object's data.
        print(f"I am {self.name}, and my score is {self.score}.")

    def add_points(self, points):
        """Update this student's score."""
        self.score += points


asha = Student("Asha", 84)
ravi = Student("Ravi", 91)

asha.introduce()
ravi.introduce()
asha.add_points(5)
print("Asha's score after improvement:", asha.score)
