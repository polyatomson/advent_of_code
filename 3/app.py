import re

keep_positive = lambda x: x if x >= 0 else 0
keep_within_range = lambda x, length: x if x < length else length

def get_spans(lines):
    number = re.compile("[0-9]+")
    character = re.compile("[^0-9\.]")

    numbers = list()
    characters = list()

    for l in lines:
        numbers.append([{"span": n.span(), "number": n.group()} for n in number.finditer(l)])
        characters.append([{"span": (keep_positive(c.start()-1), keep_within_range(c.end()+1, len(l))), "char": c.group()} for c in character.finditer(l)])

    return numbers, characters

def compare_two_spans(span1: tuple[int, int], span2: tuple[int, int]):
    span1 = list(range(span1[0], span1[1]))
    span2 = list(range(span2[0], span2[1]))
    for i in span1:
        if i in span2:
            return True
    return False

def main():
    with open("3/input.txt", "r") as fn:
        dat = fn.readlines()
    dat = [line.strip("\n") for line in dat]
    
    numbers, characters = get_spans(dat)
    good_numbers = []
    bad_numbers = []

    for i, line in enumerate(numbers):
        if line == []:
            continue
        else:
            if i == 0:
                all_characters_spans = [ char["span"] for line in characters[i:i+2] for char in line]
            elif i == len(dat)-2:
                all_characters_spans = [ char["span"] for line in characters[i-1:i+1] for char in line]
            else:
                all_characters_spans = [ char["span"] for line in characters[i-1:i+2] for char in line]

            for number in line:
                for char_span in all_characters_spans:
                    adjacency = compare_two_spans(number["span"], char_span)
                    if adjacency is True:
                        good_numbers.append(int(number["number"]))
                        break
                if adjacency is False:
                    bad_numbers.append((number["number"], i+1))

    print("result:", sum(good_numbers))

if __name__ == '__main__':
    main()