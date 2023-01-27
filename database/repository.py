from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.models import Contacts
from database.db import session


def add_contact(firstname: str, lastname: str, email: str, phone: str, address=None):
    new_contact = Contacts(
        first_name=firstname,
        last_name=lastname,
        email=email,
        cell_phone=phone,
        address=address
    )
    session.add(new_contact)
    session.commit()


def delete_contact(id_: int):
    contact = session.query(Contacts).filter_by(id=id_)
    contact.delete()
    session.commit()


def update_contact(id_, firstname: str, lastname: str, email: str, phone: str, address):
    contact = session.query(Contacts).filter_by(id=id_)
    contact.update(
        {"first_name": firstname, "last_name": lastname, "email": email, "cell_phone": phone, "address": address}
    )
    session.commit()


def show_all():
    contacts = session.query(Contacts).all()
    return contacts


def show(data):
    try:
        contact = session.query(Contacts).filter_by(id=int(data)).first()
        return contact
    except:
        contact = session.query(Contacts).filter(Contacts.fullname.like(f"%{data}%")).first()
        return contact


# if __name__ == '__main__':
    # add_contact("hehe", "hoho", "haoeoa", "aoeaoe", "aeaoe")
    # delete_contact(21)
    # update_contact(21, "tj", "pj", "php", "who", "me")
    # print("Das ist Fantastisch!")
    # for each in show_all():
    #     print(each.first_name)
    # [print(x.fullname) for x in show("j")]
    # print(show("1").fullname)
