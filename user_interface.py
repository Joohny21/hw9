from abc import ABC, abstractmethod
import classes


class IReply(ABC):
    @abstractmethod
    def reply(self):
        pass


class ShowNoteList(IReply):
    def __init__(self, addrbook: classes.AddressBook):
        self.notes = addrbook.notes.data

    def reply(self):
        to_print = ""
        for each in self.notes.values():
            to_print += each._name()
            to_print += "\n"
        return to_print

class ShowAllNotes(IReply):
    def __init__(self, addrbook: classes.AddressBook):
        self.notes = addrbook.notes.data

    def reply(self):
        to_print = ""
        for note_id, note in self.notes.items():
            to_print += f"Note ID: {note_id}\n"
            to_print += f"{note}\n"
        return to_print


class ShowNote(IReply):
    def __init__(self, addrbook: classes.AddressBook):
        self.book = addrbook

    def reply(self):
        try:
            note_id = self.book.notes.enter_name_id()
            print(self.book.notes.data[note_id])
        except KeyError:
            print("This note does not exists!")
        return ""

class ShowRecord(IReply):
    def __init__(self, record: classes.Record):
        self.record = record

    def reply(self):
        string = ""
        if self.record:
            string += f"{self.record.name.value}:"
            if self.record.phones:
                string += f"\n\tPhone numbers: {', '.join([x.value for x in self.record.phones])}"
            if self.record.emails:
                string += f"\n\tE-mails: {', '.join([x.value for x in self.record.emails])}"
            if self.record.birthday:
                birthday = self.record.birthday.value
                if birthday.year > 2:
                    string += f"\n\tBirthday: {birthday.strftime('%d %B %Y')}"
                else:
                    string += f"\n\tBirthday: {birthday.strftime('%d %B')}"
                when_to_congratulate = self.record.birthday.days_to_next_birthday
                if when_to_congratulate is not None:
                    if when_to_congratulate == 0:
                        string += f"\n\tToday is {self.record.name.value}'s birthday."
                    elif when_to_congratulate == 1:
                        string += f"\n\t{self.record.name.value} has birthday tomorrow."
                    else:
                        string += f"\n\t{self.record.name.value}'s birthday is in {when_to_congratulate} days."
            string += "\n"
        return string


