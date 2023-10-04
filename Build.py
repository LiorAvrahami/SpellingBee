import re
from tkinter import N
import GUI.html_gui_inator

find_includes_regex = re.compile("<include file=\"([^\"]*)\"></include>")


def compile_file(file_name):
    """do some basic text manipulation on text in given html file and return the result string.
    for example replace <include file=""> tags with the compiled version of the text in the  file to be included.
    @note this function does not write to files

    Args:
        file_name (str): the file to be compiled
    """
    return compile_file_recursive(file_name, [])


def compile_file_recursive(file_name, include_tree_branch):
    """recursive part of "compile_file"

    Args:
        file_name (str): the file to be compiled
        include_tree_branch (list of strings): the file_names hierarchy that included this file
    """
    # clone the include_tree_branch
    include_tree_branch = list(include_tree_branch)
    # first check file_name not already in include_tree_branch, and then add it
    assert (file_name not in include_tree_branch)
    include_tree_branch.append(file_name)

    with open(file_name, "r") as f:
        file_text = f.read()

    while True:
        match = find_includes_regex.search(file_text)
        if match is None:
            break
        included_file = match.group(1)
        text_to_paste = compile_file_recursive(
            included_file, include_tree_branch)
        file_text = file_text[:match.start()] + \
            text_to_paste + file_text[match.end():]

    return file_text


if __name__ == "__main__":
    GUI.html_gui_inator.run("GUI")
    compiled_html = compile_file("index.html")
    with open("Release.html", "w+") as f:
        f.write(compiled_html)
