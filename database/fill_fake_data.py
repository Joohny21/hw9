from faker import Faker

from database.db import session
from database.models import Contacts

fake = Faker()


def add_contacts():
    for _ in range(20):
        contact = Contacts(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            cell_phone=fake.phone_number(),
            address=fake.address(),
        )
        session.add(contact)
        session.commit()
    return None


if __name__ == '__main__':
    add_contacts()
