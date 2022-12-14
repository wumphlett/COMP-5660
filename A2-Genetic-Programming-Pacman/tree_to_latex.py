import sys


formatters = {
    "+": "({0} + {1})",
    "-": "({0} + {1})",
    "*": "{0} * {1}",
    "/": "\\frac{{{0}}}{{{1}}}",
    # \\, is used to slightly increase the spacing between RAND operands
    "RAND": "RAND({0},\\, {1})"
}


def to_latex(filename):
    with open(filename, 'r') as file:
        tree_text = [line.strip().replace("|", "") for line in file]

    i = 0

    def recursive_latex(_ = None):
        nonlocal i
        if tree_text[i] in formatters:
            return formatters[tree_text[i]].format(recursive_latex(i := i + 1), recursive_latex(i := i + 1))
        elif not tree_text[i].isalpha():
            return f"{float(tree_text[i]):.3f}"
        else:
            return tree_text[i]

    print("V(s') = " + recursive_latex())


def main():
    if len(sys.argv) != 2:
        print("Please pass in a world file")
    else:
        to_latex(sys.argv[1])


if __name__ == "__main__":
    main()
