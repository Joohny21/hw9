import sys

from user_interface import visuals, ch4nge, help_me

commands = {
    "hello": lambda *_: "How can I help you?",
    "bye": lambda *_: "Good bye!",
    "add_contact": ch4nge.add_contact,
    "delete_contact": ch4nge.remove_contact,
    "update_contact": ch4nge.update_contact,
    "show all": visuals.show_all,
    "show": visuals.show_contact,
    "help": help_me,
    0: lambda *_: "Sorry I can't understand you. Try 'help' command to see what I can.",
}


def def_mod(string: str):
    try:
        mods = {
            "hello": "hello",
            "good bye": "bye",
            "close": "bye",
            "exit": "bye",
            "add contact": "add_contact",
            "delete contact": "delete_contact",
            "show contact": "show",
            "show all": "show_all",
            "update contact":"update_contact",
            "help": "help",
        }
        if not string:
            return "empty", ""
        for key_word in mods.keys():
            if key_word in string.lower():
                return mods[key_word], string.replace(key_word, "", 1)
        return 0, ""
    except Exception as err:
        return err


if __name__ == '__main__':
    print("Hello! What can I do?", end="\n")
    while True:
        command = input(">>")
        mode, data = def_mod(command)
        output = commands.get(mode)(data)
        if output == "Good bye!":
            sys.exit()
