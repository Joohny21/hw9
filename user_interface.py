from abc import ABC, abstractmethod
import keyboard
from database.models import Contacts
import sqlalchemy.orm
from database.repository import delete_contact, update_contact, add_contact, show, show_all
from database.db import session


def input_with_default(prompt_, default_):
    print(prompt_, end="\n")
    keyboard.write(default_)
    return input()


class IReply(ABC):
    @abstractmethod
    def reply(self):
        pass


class Contacts_Visuals(IReply):
    def __init__(self, session: sqlalchemy.orm.session):
        self.session = session

    def show_all(self):
        for each in show_all():
            print(f"Fullname: {each.fullname}")
            print(f"    Email: {each.email}")
            print(f"    Phone: {each.cell_phone}")
            if each.address:
                print(f"    Address: {each.address}")
            print(f"    Contact ID: {each.id}")

    def show_contact(self, data):
        contact = show(data)
        print(f"Fullname: {contact.fullname}")
        print(f"    Email: {contact.email}")
        print(f"    Phone: {contact.cell_phone}")
        if contact.address:
            print(f"    Address: {contact.address}")
        print(f"    Contact ID: {contact.id}")

    def reply(self):
        pass


class ManipulateContacts(IReply):
    def __init__(self, session: sqlalchemy.orm.Session):
        self.session = session

    def update_contact(self, id_):
        contact = self.session.query(Contacts).filter_by(id=id_)
        print(f"Redacting contact {contact.fullname} with id {id_}:")
        first_name = input_with_default("first name: ", contact.first_name)
        last_name = input_with_default("last name: ", contact.last_name)
        email = input_with_default("email: ", contact.email)
        phone = input_with_default("phone: ", contact.cell_phone)
        address = input_with_default("address: ", contact.address)
        if address == "" or address == " ":
            address = None
        update_contact(id_, first_name, last_name, email, phone, address)

    def remove_contact(self, id_):
        contact = self.session.query(Contacts).filter_by(id=id_)
        if input("Are you sure? y/n").lower() == "y":
            contact.delete()
            self.session.commit()
        else:
            print("Operation canceled")

    def add_contact(self, _):
        print(f"Creating new contact:")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        address = input("Address: ")
        if address == "" or address == " ":
            address = None
        add_contact(first_name, last_name, email, phone, address)
        print("Contact created")

    def reply(self):
        pass


def help_me(_):
    print("""
    hello: hello,
    good bye: closes app,
    add contact: adds a contact,
    delete contact []: deletes a contact
    show contact [contact first/last name or ID]: shows a certain contact
    show all: shows all contacts
    update contact [contact ID] updates contact with new data
    help: Shows this list"""
          )


visuals = Contacts_Visuals(session)
ch4nge = ManipulateContacts(session)

# if __name__ == '__main__':
#     # ch4nge = ManipulateContacts(session)
#     # ch4nge.add_contact()
#     my = Contacts_Visuals(session)
#     my.show_contact("John")
