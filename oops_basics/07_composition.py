"""OOP note: composition builds an object by giving it other objects to use."""


class Battery:
    def __init__(self, capacity_percent):
        self.capacity_percent = capacity_percent

    def charge(self):
        self.capacity_percent = 100


class Phone:
    def __init__(self, model, battery):
        self.model = model
        # Phone contains a Battery object: this is a "has-a" relationship.
        self.battery = battery

    def show_status(self):
        print(f"{self.model}: battery at {self.battery.capacity_percent}%")


phone = Phone("ExamplePhone", Battery(35))
phone.show_status()
phone.battery.charge()
phone.show_status()

# Composition is useful when one object can be built from reusable components.
