#!/usr/bin/env python

import sys
from lxml import etree

def subject_to_uri(subject):
    try:
        if subject.split()[-1].startswith('http'):
            return subject.split()[-1]
    except IndexError:
        return None
    return None


# Function to parse oai_dc record
def parse_record(record):
    namespaces = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/'}
    try:
        root = etree.fromstring(record)
    except etree.XMLSyntaxError:
        return

    try:
        # Get language
        language = root.find('.//{http://purl.org/dc/elements/1.1/}language').text
        # Get title
        title = root.find('.//{http://purl.org/dc/elements/1.1/}title').text
        # Get subjects
        subjects = root.findall('.//{http://purl.org/dc/elements/1.1/}subject')
    except AttributeError:
        return

    if language != 'est':
        return

    title = " ".join(title.split())  # normalize whitespace
    subjects_list = [subject_to_uri(subject.text) for subject in subjects]
    subjects_list = list(filter(None, subjects_list))
    if not subjects_list:
        return

    subjects_str = " ".join(subjects_list)
    print(f"{title}\t{subjects_str}")

# Read from stdin
for line in sys.stdin:
    parse_record(line)
