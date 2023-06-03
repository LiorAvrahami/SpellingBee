import os.path
import typing

import lxml.etree as etree
import lxml.html as html
import formation
import re

RESOURCE_PATH_PREFIX = ""

# remove "tkinter." and "ttk." prefixes if exists.
remove_prefix = re.compile("(?:tkinter\.)?(?:ttk\.)?(.*)")

EMPTY_TEXT = ""


def run(path_from_root):
    global RESOURCE_PATH_PREFIX
    RESOURCE_PATH_PREFIX = path_from_root

    with open(set_path_to_from_root("a.xml"), "r") as f:
        xml_text = f.read()

    xml_text = xml_text.replace("attr:", "").replace("layout:", "")

    r: etree._Element = etree.fromstring(bytes(xml_text, "utf-8"))
    # r = t.getroot()
    root_rect = get_xywh(r)
    root_size = root_rect[2], root_rect[3]

    new_r = convert_element_recursive(r, root_size)

    with open(set_path_to_from_root("AppGui.html"), "wb+") as f:
        f.write(etree.tostring(new_r, pretty_print=True))


def convert_element_recursive(old_element: etree._Element, root_size):
    new_element: etree._Element = etree.Element("NOT_FILLED_IN")
    # add children
    for i in range(len(old_element)):
        a = convert_element_recursive(old_element[i], root_size)
        if a is not None:
            new_element.append(a)

    new_element.set("id", old_element.attrib["name"])

    tag = remove_prefix.match(old_element.tag).group(1).lower()
    if tag == "frame":
        new_element.tag = "div"
        set_position_and_size(new_element, old_element, root_size)
        add_text_if_exists(new_element, old_element)
    elif tag == "button":
        new_element.tag = "button"
        set_position_and_size(new_element, old_element, root_size)
        add_text_if_exists(new_element, old_element)
    elif tag == "label":
        if "image" in old_element.attrib:
            new_element.tag = "img"
            set_position_and_size(new_element, old_element, root_size, is_max_size=True)
            new_element.set("src", set_path_to_from_root(old_element.attrib["image"]))
        else:
            new_element.tag = "label"
            set_position_and_size(new_element, old_element, root_size)
            new_element.text = old_element.attrib["text"]
            add_text_if_exists(new_element, old_element)
    elif tag == "entry":
        new_element.tag = "input"
        set_position_and_size(new_element, old_element, root_size)
        add_text_if_exists(new_element, old_element)
    elif tag == "notebook":
        new_element.tag = "div"
        set_position_and_size(new_element, old_element, root_size)
        make_tab_view(new_element)
    else:
        return None

    return new_element


def add_text_if_exists(new_element, old_element):
    if "text" in old_element.attrib:
        new_element.text = old_element.attrib["text"]
    elif len(old_element) == 0:
        # if no text and no children, then the tag still shouldn't close itself, we know this because this function should only be called on non-self closing
        # brackets.
        new_element.text = EMPTY_TEXT


def set_position_and_size(new_element: etree._Element, old_element: etree._Element, root_size, is_max_size=False):
    def format_x(length):
        return "{:.3f}".format(100 * length / root_size[0])

    def format_y(length):
        return "{:.3f}".format(100 * length / root_size[1])

    if not does_have_xywh(old_element):
        return
    x, y, width, height = get_xywh(old_element)

    location_txt = f"left: {format_x(x)}vw; top: {format_y(y)}vh; "
    if is_max_size:
        size_txt = f"max-width: {format_x(width)}vw; max-height: {format_y(height)}vh"
    else:
        size_txt = f"width: {format_x(width)}vw; height: {format_y(height)}vh"

    new_element.set("style", "position: absolute; " + location_txt + size_txt)


def does_have_xywh(element: etree._Element):
    return "x" in element.attrib and "y" in element.attrib and "width" in element.attrib and "height" in element.attrib


def get_xywh(element: etree._Element):
    get = lambda a: element.attrib[a]
    return float(get("x")), float(get("y")), float(get("width")), float(get("height"))


def make_tab_view(new_base: etree._Element):
    # change children id's, add buttons, generate js file.
    buttons_row: etree._Element = etree.Element("div")
    buttons_row.set("class", "tab_bar")

    btn_children = []
    for child_idx in range(len(new_base)):
        child: etree._Element = new_base[child_idx]
        child.set("id", new_base.attrib["id"] + f"_frame{child_idx}")

        new_button = etree.Element("button")
        new_button.set("class", "tab_button")
        on_click_func_name = child.attrib["id"] + "_Btn_Clicked"
        new_button.set("onclick", f"{on_click_func_name}()")
        new_button.text = child.text
        child.text = None if len(child) > 0 else EMPTY_TEXT
        buttons_row.append(new_button)

    # make script tag
    script_element: etree._Element = etree.Element("script")
    script_file_name = make_tab_view_script_file(new_base)
    script_element.set("src", script_file_name)
    script_element.text = " "
    new_base.append(script_element)

    new_base.insert(0, buttons_row)


def make_tab_view_script_file(base: etree._Element) -> str:
    """
    :param base: the div element at the root of the tab view
    :return: the name of the new script file
    """
    file_name = os.path.join("TabViewScripts", base.attrib["id"] + ".js")
    file_name = set_path_to_from_root(file_name)
    script_to_write = []

    with open(set_path_to_from_root("tab_view_script_generator_template"), "r") as f:
        template = f.readlines()

    for line in template:
        line = line.replace("#Id#", base.attrib["id"])
        if "#TabId#" in line:
            for child in base:
                new_line = line.replace("#TabId#", child.attrib["id"]) + "\n\n"
                script_to_write.append(new_line)
        else:
            script_to_write.append(line)

    with open(file_name, "w+") as f:
        f.writelines(script_to_write)

    return file_name


def set_path_to_from_root(local_path):
    return os.path.join(RESOURCE_PATH_PREFIX, local_path)
