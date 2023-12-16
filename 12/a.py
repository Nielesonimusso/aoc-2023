import re
from itertools import product
from typing import Generator, Any

line_regex = re.compile(r'(?P<springs>[.?#]+)\s(?P<groups>(?:\d+,)*\d+)')
blank_regex = re.compile(r'\?')
broken_regex = re.compile(r'#')

def fillInBlanks(template: str, filling: str) -> str:
    blanks = template.count("?")
    if blanks != len(filling):
        raise AssertionError
    
    # create a generator that yields from the string; its `send` method is used 
    #  as the `repl` argument of `re.Pattern.sub`, so it should accept the 
    #  `re.Match` type. However, this means that the generator should first 
    #  be primed to accept values by calling __next__() once
    def popFilling() -> Generator[str, re.Match, None]:
        yield ""
        for filler in filling:
            _ = yield filler
    filler = popFilling()
    next(filler)

    template = blank_regex.sub(filler.send, template)
    return template

def regexFromGrouping(groups: list[int]) -> re.Pattern:
    checkRegex = r"\.*" \
        + r"\.+".join([rf"#{{{group}}}" for group in groups]) \
        + r"\.*"
    return re.compile(checkRegex)
        
with open("data.txt", "r") as file:
    total_options = 0
    for index, line in enumerate(file):
        if line_match := line_regex.match(line):
            springs = line_match["springs"]
            groups = [int(group) for group in line_match["groups"].split(",")]

            check_regex = regexFromGrouping(groups)

            blanks = springs.count("?")
            brokens = springs.count("#")
            expected_brokens = sum(groups)

            fill_options = ("".join(p) for p 
                            in product([".","#"], repeat=blanks))

            spring_options = (fillInBlanks(springs, filling) for filling 
                              in fill_options if brokens 
                              + filling.count("#") == expected_brokens)

            correct_options = [option for option in spring_options 
                               if check_regex.fullmatch(option) is not None]

            print(".", end="", flush=True)
            total_options += len(correct_options)
    print(total_options)