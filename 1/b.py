sum = 0

words = dict(
    zero="0", 
    one="1", 
    two="2", 
    three="3", 
    four="4", 
    five="5", 
    six="6", 
    seven="7", 
    eight="8", 
    nine="9")
numbers = { 
    "0": "0", 
    "1": "1", 
    "2": "2", 
    "3": "3", 
    "4": "4", 
    "5": "5", 
    "6": "6", 
    "7": "7", 
    "8": "8", 
    "9": "9"
    }

def raiseAtMatch(line, index):
    for mapping in (numbers, words):
        for entry, number in mapping.items():
            if len(line) - index >= len(entry) \
                    and line[index:index+len(entry)] == entry:
                raise StopIteration(number)


with open("data.txt", "r") as file:
    for line in file:
        # find left number by searching from left to right using the mappings
        left = ""
        try:
            for index in range(len(line)):
                raiseAtMatch(line, index)
        except StopIteration as e:
            left = e.value
        # find the right number by searching from right to left using the mappings
        right = ""
        try:
            for index in (i - 1 for i in range(len(line), 0, -1)):
                raiseAtMatch(line, index)
        except StopIteration as e:
            right = e.value

        concatenation = left + right
        number = int(concatenation)
        print(line.strip(), number)

        sum += number

print(sum)