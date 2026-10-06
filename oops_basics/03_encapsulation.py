"""OOP note: encapsulation keeps an object's data and rules together."""


class BankAccount:
    def __init__(self, owner, starting_balance=0):
        self.owner = owner
        # A leading underscore signals that balance is intended for internal use.
        # It is a convention in Python, not strict access protection.
        self._balance = starting_balance

    def deposit(self, amount):
        """Add a positive amount, keeping the balance rule in one place."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def get_balance(self):
        """Provide a controlled way to read the current balance."""
        return self._balance


account = BankAccount("Meera", 100)
account.deposit(50)
print(f"{account.owner}'s balance: {account.get_balance()}")

# In larger programs, callers should use deposit() instead of changing _balance
# directly, so the class can enforce rules such as positive deposits.
