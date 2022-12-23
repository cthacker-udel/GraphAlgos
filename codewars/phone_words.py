def phone_words(string_of_nums: str) -> str:
    """
    Translate the string into text, mimicing the string of numbers into a simulation of pressing digits on the phone

    :param string_of_nums: The numerical sequence to generate a string from
    :return: The translated message
    """
    print("string = [{}]".format(string_of_nums))
    letters: dict[str, dict[int, str]] = {
        "0": {
            1: " "
        },
        "1": {
            1: ""
        },
        "2": {
            1: "a",
            2: "b",
            3: "c"
        },
        "3": {
            1: "d",
            2: "e",
            3: "f"
        },
        "4": {
            1: "g",
            2: "h",
            3: "i"
        },
        "5": {
            1: "j",
            2: "k",
            3: "l"
        },
        "6": {
            1: 'm',
            2: 'n',
            3: 'o'
        },
        "7": {
            1: 'p',
            2: 'q',
            3: 'r',
            4: 's'
        },
        "8": {
            1: 't',
            2: 'u',
            3: 'v'
        },
        "9": {
            1: 'w',
            2: 'x',
            3: 'y',
            4: 'z'
        }
    }
    running_total: int = 0
    curr_number: str = string_of_nums[0] if len(string_of_nums) > 0 else ""
    translated_message: str = ""
    for each_number in string_of_nums:
        if each_number != curr_number:
            # found different sequence, change numbers
            translated_message += letters[curr_number][running_total]
            running_total = 1
            curr_number = each_number
        else:
            running_total += 1
            if running_total not in letters[curr_number]:
                # exceeding max
                translated_message += letters[curr_number][running_total - 1]
                running_total = 1
    return translated_message + letters[curr_number][running_total] if curr_number in letters else ''


if __name__ == '__main__':
    print(phone_words(""))


