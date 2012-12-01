"""
Converts the table of case citation data from the cornell website:

http://www.law.cornell.edu/citation/

Into computer friendly XML.

Infile = case_citations.txt
Outfile = case_citations.xml
"""
from lxml import etree as ET

INFILE_NAME = 'case_citations.txt'
OUTFILE_NAME = 'case_citations.xml'

def preprocess(text):
    """
    convert the text into a list of line strings.
    """
    lines = text.splitlines()

    # strip whitespace
    lines = [l.strip() for l in lines]

    # kill comments 
    lines = filter(lambda l: not l.startswith('#'), lines)

    # filter out blank lines
    lines = filter(lambda l: len(l) > 0, lines)

    return lines



def build_data(lines):
    """
    Build a dictionary that will be converted into xml. main key of
    the dictionary will be a <Section> node of the xml file. 
    """
    current_section = ""
    data = {}

    for line in lines:
        if not current_section or line in sections:
            current_section = line
            data[current_section] = {'citations' : [], 'comments' : []}
            continue
    
        if line.startswith('*'):
            data[current_section]['comments'].append(line)
            continue
        
        data[current_section]['citations'].append(line)
        
    return data



def build_xml(data):
    root = ET.Element("CitationData")
    root.set('type', 'case')

    for section, elems in data.items():
        sect_node = ET.SubElement(root, "Section")
        sect_node.set("id", section);
        for cite in elems['citations']:
            cite_node = ET.SubElement(sect_node, "Citation")

            if cite.endswith('*'): 
                cite = cite[:-1]
                cite_node.set("comment", "True")

            cite_node.text = cite

        for comment in elems['comments']:
            comment_node = ET.SubElement(sect_node, "Comment")
            comment_node.text = comment
            
    return root



def get_text(filepath):
    with open(filepath, 'r') as infile:
        text = infile.read()
    return text



def write_xml(filepath, xml):
    text = ET.tostring(xml, pretty_print=True, encoding="unicode")

    with open(filepath, 'w') as outfile:
        outfile.write(text)




def main():
    text = get_text(INFILE_NAME)
    lines = preprocess(text)
    data = build_data(lines)
    xml = build_xml(data)
    write_xml(OUTFILE_NAME, xml)


# The set of sections from the table. Some are federal courts but
# other indicate case citations for state jurisdictions.
# 
# Generated from the case_citations.txt w/iPython.
#
sections = ['Supreme Court',
 'Courts of Appeals',
 'District Courts',
 'Court of Federal Claims',
 'Bankruptcy Courts and Bankruptcy Panels',
 'Tax Court',
 'Military Service Courts of Criminal Appeals',
 'Alabama',
 'Alaska',
 'Arizona',
 'Arkansas',
 'California',
 'Colorado',
 'Connecticut',
 'Delaware',
 'District of Columbia',
 'Florida',
 'Georgia',
 'Hawaii',
 'Idaho',
 'Illinois',
 'Indiana',
 'Iowa',
 'Kansas',
 'Louisiana',
 'Maine',
 'Maryland',
 'Massachusetts',
 'Michigan',
 'Minnesota',
 'Mississippi',
 'Missouri',
 'Montana',
 'Nebraska',
 'Nevada',
 'New Hampshire',
 'New Jersey',
 'New Mexico',
 'New York',
 'North Carolina',
 'North Dakota',
 'Ohio',
 'Oklahoma',
 'Oregon',
 'Pennsylvania',
 'South Carolina',
 'South Dakota',
 'Tennessee',
 'Texas',
 'Utah',
 'Vermont',
 'Virginia',
 'Washington',
 'West Virginia',
 'Wisconsin',
 'Wyoming']


if __name__ == '__main__':
    main()
