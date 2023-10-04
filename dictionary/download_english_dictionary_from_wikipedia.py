import os.path
import hashlib
import lxml.etree as etree
import lxml.html as html
import urllib.request
import re
try:
    from tqdm import tqdm as pbar
except:
    pbar = lambda x:x

def download_html(url):
    cache_folder_name = ".site_cache"
    if not os.path.exists(cache_folder_name):
        os.mkdir(cache_folder_name)
    hash_val = str(int(hashlib.sha1(url.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
    cache_file_name = os.path.join(cache_folder_name,hash_val)

    # look for cache
    if os.path.exists(cache_file_name):
        # read from cache
        with open(cache_file_name,"r+",encoding="utf-8") as f:
            # here I assume I'm not going to have any hashing collisions, if there will be, then bugs will happen.
            html_text = f.read()
    else:
        # download from the internet
        with urllib.request.urlopen(url) as f:
            html_text = f.read().decode('utf-8')
        # write file to cache
        with open(cache_file_name,"w+",encoding="utf-8") as f:
            f.write(html_text)

    html_tree = html.fromstring(bytes(html_text, "utf-8"))
    return html_tree


def get_link_list():
    html_tree: etree._Element
    html_tree = download_html('https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/TV_and_Movie_Scripts_(2006)')

    table_root = html_tree.find(".//*[@class='derivedterms ul-column-count']")

    links_list = []
    for elem in table_root.findall(".//a"):  # iterate over all links in table
        links_list.append(elem.attrib["href"])

    return links_list


def make_word_map(link_list):
    out_dict = dict()
    for url in pbar(link_list):
        html_tree = download_html("https://en.wiktionary.org/" + url)
        html_tree: etree._Element
        tabel = html_tree.find(".//table")

        for row in tabel.findall(".//tr"):
            row: etree._Element
            if row[0].text is None:
                continue
            rank = extract_number(row[0].text)
            count = extract_number(row[2].text)
            try:
                word = row[1][0].text
            except:
                continue
            try:
                definition_url = row[1][0].attrib["href"]
            except:
                definition_url = None

            if str.isupper(word[0]):
                # don't add names
                continue

            if not str.isalpha(word):
                continue

            assert rank not in out_dict
            out_dict[rank] = {"word": word, "count": count, "definition_url": definition_url}

    return out_dict

def save_word_dict_to_json(word_dict):
    import json
    with open('word_dictionary.json', 'w') as fp:
        json.dump(word_dict, fp)

def extract_number(text)->int:
    return int(re.sub('[^0-9]', '', text))


if __name__ == "__main__":
    link_list = get_link_list()
    word_dict = make_word_map(link_list)
    save_word_dict_to_json(word_dict)