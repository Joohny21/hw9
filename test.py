# def raw(string: str, replace: bool = False) -> str:
#     """Returns the raw representation of a string. If replace is true, replace a single backslash's repr \\ with \."""
#     r = repr(string)[1:-1]  # Strip the quotes from representation
#     if replace:
#         r = r.replace('\\\\', '\\')
#     return r

# s = input()
# print(s)
# print(raw())
import codecs

s = input()
s = repr(s).replace("\\\\", "\\").replace("'", "")
s = codecs.decode(s, 'unicode_escape')
print(s)