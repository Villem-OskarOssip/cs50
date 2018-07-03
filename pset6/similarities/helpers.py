def lines(a, b):

    similars = []
    lines_a = a.split("\n").strip()
    lines_b = b.split("\n").strip()

    for line_a in lines_a:
        for line_b in lines_b:
            if line_b == line_a and line_a not in similars:
                similars.append(line_a)

    return similars


def sentences(a, b):

    similars = []
    sentences_a = a.split(".").strip()
    sentences_b = b.split(".").strip()

    for sentence_a in sentences_a:
        for sentence_b in sentences_b:
            if sentence_a == sentence_b:
                if sentence_a + "." not in similars:
                    similars.append(sentence_a + ".")

    return similars


def substrings(a, b, n):

    possible_substrings_a = set()
    possible_substrings_b = set()
    similars = []

    a = a.replace("\n", "")
    b = b.replace("\n", "")

    for i in range(len(a) - n - 1):
        possible_substrings_a.add(a[i:i+n])
        i += 1

    for i in range(len(b) - n - 1):
        possible_substrings_b.add(b[i:i+n])
        i += 1

    for substring_a in possible_substrings_a:
        for substring_b in possible_substrings_b:
            if substring_a == substring_b:
                similars.append(substring_a)

    print(similars)
    return similars
1