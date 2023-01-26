import re
import sys

from classes import convert_to_date, AddressBook, Record, Phone, Birthday, Name, Email
from notes import Note, Tags
import user_interface


phone_pattern = "\s\+?[-\s]?(?:\d{2,3})?[-\s]?(?:\([-\s]?\d{2,3}[-\s]?\)|\d{2,3})?[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3}\s"
no_number = "Sorry, I can't identify a phone number."
no_name = "Sorry, I can't identify a contact's name."


def decorator(func):
    """ Resets show_all function to start again from beginning of the contact list
    Should be used for all functions called in commands.py except show_all and empty."""
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(args[0], AddressBook):
            args[0].showing_records = False
            args[0].page = 0
        if isinstance(result, Exception):
            return str(Exception)
        else:
            return result
    return inner


def print_c(text: str, book: AddressBook):
    """makes all names in text green"""
    return text


@decorator
def save_to_file(book: AddressBook, text: str = ""):
    """ Saves all data to file. Called by function save or when you exit from the assistant.
    text (optional variable) is a name of file to save data"""
    text = text.strip()
    return book.write_to_file(text)


@decorator
def read_from_file(book: AddressBook, text: str = ""):
    """Reads all data from file text (optional) via function load or when you start the assistant"""
    text = text.strip()
    return book.read_from_file(text)


@decorator
def clear(book: AddressBook, *_):
    """Deletes all date from the AddressBook"""
    if confirm(f"Do you want to delete all contacts from your Address book? Type 'yes'/'no'.\n"):
        book.clear()
        return f"Done!"
    else:
        return f"Glad you changed your mind."


@decorator
def confirm(question):
    """Use it when user makes important changes to the AddressBook, for example deleting a contact"""
    while True:
        string = input(question)
        if string.strip().lower() in ("y", "yes"):
            return True
        if string.strip().lower() in ("n", "no"):
            return False


def find_name_number(text: str):
    """splits text into phone number and name"""
    text += " "
    pattern = re.compile(phone_pattern)
    only_name = text
    if not pattern.findall(text):
        return find_name(text), ""
    for x in pattern.findall(text):
        only_name = only_name[:only_name.find(x)]
    return find_name(only_name), str(pattern.findall(text)[0]).strip().replace(" ", "").replace("", ""),


def find_name(text: str):
    """converts sting into a valid name of contact"""
    return text.strip().lower().title()


@decorator
def find(book: AddressBook, text: str):
    """searches 'text' in names, numbers, emails, notes text, and notes by teg if 'text' is a list of tags"""
    text = text.strip()
    contacts = book.search_in_names(text)  # list of names
    numbers = book.search_in_phones(text)  # list of tuples (name, number)
    mails = book.search_in_emails(text)
    notes = book.notes.search_in_notes(text)
    notes_tags = book.notes.find_by_tags(text)
    notes_names = book.notes.find_by_name(text)
    result = ""
    if not text:
        return "Nothing to search"
    if not (contacts or numbers or mails or notes or notes_tags or notes_names):
        return "No matches found"
    else:
        if contacts:
            result += f"Matches in names:\n"
            for name in contacts:
                result += f"\t{name}\n"
        if numbers:
            result += f"Matches in phone numbers:\n"
            for pair in numbers:
                result += f"\t{pair[0]}: {pair[1]}\n"
        if mails:
            result += f"Matches in email addresses:\n"
            for pair in mails:
                result += f"\t{pair[0]}: {pair[1]}\n"
        if notes:
            result += f"Matches in notes:\n"
            for each in notes:
                result += f"\t{each._name()}\n"
        if notes_tags:
            result += f"Matches in notes tags:\n"
            for each in notes_tags:
                tags = ','.join(each._tags())
                result += f"{each._name()}: {tags}\n"
        if notes_names:
            result += f"Matches in notes names\n"
            for each in notes_names:
                result += f"\t{each._name()}\n"
        return result


@decorator
def find_birthdays(book: AddressBook, text: str):
    """find contacts whose birthday in int('text') days"""
    text = text.strip()
    try:
        days = int(text)
    except ValueError:
        return "invalid format of the numbers of days"
    if isinstance(days, int):
        output = []
        for contact in book.data.keys():
            if book.data.get(contact).birthday is not None:
                if book.data.get(contact).birthday.days_to_next_birthday is not None and \
                        book.data.get(contact).birthday.days_to_next_birthday == days:
                    output.append(contact)

        start_of_phrase = ""
        if not output:
            start_of_phrase = "Nobody has a birthday"
        elif len(output) == 1:
            start_of_phrase = f"{output[0]} has a birthday"
        elif len(output) == 2:
            start_of_phrase = f"{output[0]} and {output[1]} have a birthday"
        elif len(output) > 2:
            start_of_phrase = f"{', '.join(output[:-1]) + ', and ' + output[-1]} have a birthday"

        end_of_phrase = ""
        if days >= 2:
            end_of_phrase = f" in {days} days"
        elif days == 1:
            end_of_phrase = f" tomorrow"
        elif days == 0:
            end_of_phrase = f" today"
        return start_of_phrase + end_of_phrase
        # if not output:
        #     if days >= 2:
        #         return f"Nobody has birthday in {days} days"
        #     elif days == 1:
        #         return f"Nobody has birthday tomorrow"
        #     elif days == 0:
        #         return f"Nobody has birthday today"
        #     else:
        #         return ""
        # elif len(output) == 1:
        #     if days >= 2:
        #         return f"{output[0]} has birthday in {days} days"
        #     elif days == 1:
        #         return f"{output[0]} has birthday tomorrow"
        #     elif days == 0:
        #         return f"{output[0]} has birthday today"
        # elif len(output) == 2:
        #     if days >= 2:
        #         return f"{output[0]} and {output[1]} have birthday in {days} days"
        #     if days == 1:
        #         return f"{output[0]} and {output[1]} have birthday tomorrow"
        #     if days == 0:
        #         return f"{output[0]} and {output[1]} have birthday roday"
        # else:
        #     if days >= 2:
        #         return f"{','.join(output[:-1]) + ', and ' + output[-1]} have birthday in {days} days"


def name_birthday(book: AddressBook, text: str):
    """splits 'text' into contact name and a date"""
    for contact in book.data.keys():
        if contact.lower() in text.lower():
            return contact, text.lower().replace(contact.lower(), "", 1).strip()
    return None, None


def name_email(book: AddressBook, text: str):
    """splits 'text' into name and email"""
    for contact in book.data.keys():
        if contact.lower() in text.lower():
            template = re.compile(r"[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z][a-zA-Z]+")
            mails = text.lower().replace(contact.lower(), "", 1).strip()
            mail_list = re.findall(template, mails)
            if mail_list and mail_list[0]:
                return contact, mail_list[0]
            else:
                return contact, None
    return None, None


@decorator
def add_contact(book: AddressBook, data: str):
    """add contact from 'text' to your AddressBook"""
    # name, number = find_name_number(data)
    name = find_name(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        return f"Contact '{name}' already exists"
    else:
        # #phone_number = Phone(number)
        # if phone_number.value:
        #     record = Record(Name(name), [phone_number])
        #     book.add_record(record)
        #     return f"Created contact '{name}': '{number}'"
        # else:
        record = Record(Name(name), [])
        book.add_record(record)
        return f"Created contact a new contact '{name}'"


@decorator
def rename(book: AddressBook, data: str):
    """finds an existing contact in 'text' and changes its name """
    name = find_name(data)
    if not name:
        return "Name has not been found"
    elif name not in book.data.keys():
        return f"Contact '{name}' already exists"
    else:
        while True:
            new_name = input(f"Please enter a new name for the contact {name}\n")
            new_name = find_name(new_name)
            print(name, new_name)
            if new_name not in book.data.keys():
                add_contact(book, new_name)
                book.data[new_name] = book.data.get(name)
                book.data.get(new_name).name.value = new_name
                delete_contact(book, name)
                return "Done"
            else:
                print(f"Contact '{new_name}' has already exist")


@decorator
def show_contact(book: AddressBook, data: str):
    """shows a contact by its name"""
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return str(book.data.get(name))


def empty(book: AddressBook, *_):
    """called if an empty command is passed to assistant.
    works differently if the assistant is in the show records mode.
    shouldn't be decorated ny decorator to work properly"""
    if not book.showing_records:
        return "Sorry I can't understand you. Try 'help' command to see what I can."
    else:
        return show_all(book)


@decorator
def reset(book: AddressBook, text: str = ""):
    """resets the show records mode"""
    try:
        n = int(text.strip())
    except ValueError:
        n = book.contacts_per_page
    book.reset_iterator(n)
    return "Done!"


def show_all(book: AddressBook, text: str = ""):
    """show all contact by 'n' contact per page
    default value for n is 10
    to work properly should not be decorated with the 'decorator'"""
    try:
        n = int(text.strip())
        book.contacts_per_page = n
    except ValueError:
        n = book.contacts_per_page
    if not book.data:
        return "Your phone book is empty."
    else:
        first = book.page * n + 1  # first contact to show
        last = min(book.page * n + n, book.size)  # last contact to show
        if book.size == last:
            pass
        zero_line = f"Showing contacts {first}-{last} from {book.size} records:\n"
        if not book.showing_records:
            book.showing_records = True
            book.reset_iterator(n)
        try:
            output_line = zero_line + next(book.show)
            if last == book.size:
                output_line += f"End of the address book"
                book.page = 0
            else:
                output_line += f"Press 'Enter' to show next {n} contacts"
                book.page += 1
            return output_line
        except StopIteration:
            book.showing_records = False
            book.reset_iterator(n)
            book.page = 0
            return ""


@decorator
def phone(book: AddressBook, data: str):
    """shows phone number of contact from 'data'"""
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return f"{name}: {', '.join([x.value for x in book.data.get(name).phones])}"


@decorator
def add_number(book: AddressBook, data: str):
    """adds a number from 'text' to an existing contact from 'text'"""
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif not number:
        return no_number
    elif name not in book.data.keys():
        return f"Contact '{name}' does not exists"
    # to create a new contact if it does not exist
    # elif name not in book.data.keys():
    #     add_contact(book, data)
    #     return f"Created a new contact '{name}' with number '{number}'"
    else:
        phone_number = Phone(number)
        if phone_number.value:
            book.data[name].add_number(phone_number)
            return f"Number '{number}' has been added to contact '{name}'"
        else:
            return f"Invalid phone number"


@decorator
def delete_number(book: AddressBook, data: str):
    """deletes a number of contact from 'data'"""
    name, number = find_name_number(data)
    if name and not number:
        if name in book.data.keys():
            if confirm(f"Do you want to delete all numbers from contact '{name}'? Type 'yes'/'no'.\n"):
                for number in book.data.get(name).phones:
                    book.data.get(name).del_number(number)
                return f"Done!"
            else:
                return f"Nothing changed"
        else:
            return f"Contact {name} does not exist."
    elif name and number:
        if name in book.data.keys():
            if number in [x.value for x in book.data.get(name).phones]:
                book.data.get(name).del_number(Phone(number))
                return f"Number '{number}' has been deleted from contact '{name}'"
            else:
                return f"Contact '{name}' has no phone number '{number}'."
    else:
        return no_name


@decorator
def delete_contact(book: AddressBook, data: str):
    """deletes an existing contact"""
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        if confirm(f"Contact '{name}' will be deleted/renamed. "
                   f"Are you sure? Type 'yes' or 'no'.\n"):
            book.delete_record(name)
            return "Done!"
        else:
            return f"Glad you changed your mind."


@decorator
def set_birthday(book: AddressBook, data: str):
    """changes or sets a birthday of the contact"""
    name, birthday = name_birthday(book, data)
    if not name:
        return no_name
    elif not birthday:
        return "No date specified"
    else:
        date = convert_to_date(birthday)
        if date:
            book.data.get(name).set_birthday(Birthday(birthday))
            return "Done"
        else:
            return "Invalid value of date"


@decorator
def delete_birthday(book: AddressBook, data: str):
    """clears a birthday field of the contact from 'data'"""
    if not name_birthday(book, data):
        return "Contact does not exist"
    else:
        name, birthday = name_birthday(book, data)
        book.data.get(name).set_birthday(None)
        return "Done"


@decorator
def add_email(book: AddressBook, data: str):
    """adds email to the existing contact"""
    name, email = name_email(book, data)
    if not name:
        return "Can't find a valid contact"
    if not email:
        return "Can't find a valid email address"
    else:
        name, email = name_email(book, data)
        book.data.get(name).add_email(Email(email))
        return "Done"


@decorator
def delete_email(book: AddressBook, data: str):
    """deletes one email"""
    name, email = name_email(book, data)
    if not name:
        return "Can't find a valid contact"
    else:
        if not email:
            if name in book.data.keys():
                if confirm(f"Do you want to delete all emails from contact '{name}'? Type 'yes'/'no'.\n"):
                    for mail in book.data.get(name).emails:
                        book.data.get(name).del_email(mail)
                    return "Done"
                else:
                    return "Nothing has been deleted"
            else:
                return "Can't find a valid contact"
        else:
            if email in [x.value for x in book.data.get(name).emails]:
                book.data.get(name).del_email(Email(email))
                return f"Email '{email}' has been deleted from the contact '{name}'"
            else:
                return f"Contact '{name}' has no email '{email}'."


@decorator
def create_note(book: AddressBook, *_):
    """creates a new note"""
    name = input('Enter name: ')
    print("Enter note: ", end="") 
    text = '\n'.join(iter(input, "")),
    tags = Tags(input('Enter tags or press ENTER: ').split(','))
    book.notes.add_note(Note(name, text, tags))
    return 'Note created'


@decorator
def delete_note(book: AddressBook, *_):
    """deletes an existing note"""
    book.notes.delete_note()
    return ""


@decorator
def edit_note(book: AddressBook, *_):
    """Edits note"""
    book.notes.edit_note()
    return "Operation successful!"


@decorator
def show_all_notes(book: AddressBook, *_):
    """just shows all the notes to the user"""
    return user_interface.ShowAllNotes(book).reply()


@decorator
def show_note_list(book: AddressBook, *_):
    """shows list of notes"""
    return user_interface.ShowNoteList(book).reply()

@decorator
def show_note(book: AddressBook, *_):
    """shows certain note"""
    return user_interface.ShowNote(book).reply()

def help_me(*_):
    return "Hi! Here is the list of known commands:\n" + \
           "\tshow all: shows all your contacts by '2' on page\n" + \
           "\t\tor try:\tshow all 'n': to show all your contacts by 'n' on page\n" + \
           "\treset 'n': return to the start of the contacts, sets showed number of contacts on page to 'n'\n" + \
           "\tshow contact 'name': shows information about contact\n" + \
           "\tphone 'name': shows all phone numbers of the contact\n" + \
           "\tadd contact 'name' 'phone number': creates a new contact\n" + \
           "\tset birthday 'name' 'birthday': sets contacts birthday\n" + \
           "\t\t 'birthday' should be in forman 'mm.dd' or 'mm.dd.year'\n" + \
           "\tdelete birthday 'name': deletes birthday from the contact\n" + \
           "\tdelete contact 'name': deletes contact 'name'\n" + \
           "\tadd phone 'name' 'phone numer': adds the phone number to the existing contact\n" + \
           "\t\tphone number should be 7 digits long + optional 3 digits of city code\n" + \
           "\t\t+ optional 2 digits of country code + optional '+' sight\n" + \
           "\tdelete phone 'name': deletes all phone numbers from the contact" +\
           "\tdelete phone 'name' 'phone number': deletes the phone number from the contact\n" + \
           "\tsave 'file name': saves you Address book to 'file name'\n" + \
           "\tload 'file name': loads existing Address book from 'file name'\n" + \
           "\tfind 'string': searches 'string' in names and phone numbers\n" + \
           "\tclear: clears your Address book\n" + \
           "\texit: close the assistant\n" + \
           "\tcreate note: creates new note\n" + \
           "\tdelete note: deletes existing note\n" + \
           "\tshow notes: shows all notes content\n" + \
           "\tshow note list: shows list of notes\n" + \
           "\tedit note: edits note\n" + \
           "\tshow note: shows certain note"
