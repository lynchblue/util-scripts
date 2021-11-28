#!/usr/bin/python3

import sys, getopt

from lxml import html
import requests


def is_element_present(url_pattern, page_number, text_to_search, html_element):
    page = requests.get(url_pattern.format(page=str(page_number)))
    tree = html.fromstring(page.content)
    elements = tree.xpath(".//{html_element}[contains(text(),'{text_to_search}')]".format(html_element=html_element,
                                                                                          text_to_search=text_to_search))
    found = False
    try:
        elements[0]
        found = True
    except IndexError:
        pass
    if found:
        print ("Page where it was found: " + str(page_number))


def main(argv):
    url_pattern = ''
    num_of_pages = ''
    html_element = ''
    text_to_search = ''
    try:
        opts, args = getopt.getopt(argv, "hu:p:e:t:", ["url=", "pages=", "element", "text"])
    except getopt.GetoptError:
        print ('test.py -u "https://example.com/page={page}" -p <pages> -e <html_element> -t <text_to_search>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -u "https://example.com/page={page}" -p <pages> -e <html_element> -t <text_to_search>')
            sys.exit()
        elif opt in ("-u", "--url"):
            url_pattern = arg
        elif opt in ("-p", "--pages"):
            num_of_pages = arg
        elif opt in ("-e", "--element"):
            html_element = arg
        elif opt in ("-t", "--text"):
            text_to_search = arg
    print ('URL pattern is: ', url_pattern)
    print ('Number of pages is:', num_of_pages)
    print ('Html element is: ', html_element)
    print ('Text to search is: ', text_to_search)
    for page_number in range(1, int(num_of_pages)):
        is_element_present(url_pattern=url_pattern,
                           page_number=page_number,
                           text_to_search=text_to_search,
                           html_element=html_element)


if __name__ == "__main__":
    main(sys.argv[1:])
