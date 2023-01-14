Color = {
    "White": "\033[107m",
    "Red": "\033[41m",
    "Green": "\033[42m",
    "Yellow": "\033[43m",
    "Blue": "\033[44m",
    "Reset": "\033[0m",
}


def colored_square_string(name) -> str:
    return Color[name] + "  " + Color["Reset"]
