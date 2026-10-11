"""Store and display student addresses using a dictionary."""

student_addresses = {
    "Ravi": {
        "street": "12 Lake Road",
        "city": "Guntur",
        "state": "Andhra Pradesh",
        "postal_code": "522001",
    },
    "Anita": {
        "street": "8 Green Park",
        "city": "Vijayawada",
        "state": "Andhra Pradesh",
        "postal_code": "520010",
    },
}

for student, address in student_addresses.items():
    print(f"{student}'s address:")
    print(
        f"{address['street']}, {address['city']}, "
        f"{address['state']} {address['postal_code']}"
    )
