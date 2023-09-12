import fitz
import re

from tasks.to_be_moved.land_grab.university_real_estate.entities import Parcel


def cauc_parser(l) -> Parcel:
    # take out - and spaces, concatenate
    # commas and semicolons are usually delimiters, but sometimes it separates the last few digits, which
    # technically are like additional parcel IDs, with a slight change at the end
    # sometimes it has "or" to also indicate new ID combo with the last few digits being different
    # weird adjustments need to be made for some of the strings (string descriptions include 'and', further desc. etc)
    # return cells with weird strings for additional parsing

    parcel_number = l[2]  # TODO
    p = Parcel(original_number=parcel_number)
    return p


def find_parcel_number_candidates(text):
    # text = text.replace('\n', ' ')
    delims = {',', ';'}
    # greedily consume,
    # tokenize at delims,
    # strip newlines before storing tokens,
    # three or more groups

    # parcel num & \d+
    c1 = re.findall(r'\d+-\d+\-\d+', text)


def experiment(pdf_location):
    doc = fitz.open(pdf_location)  # open a document
    with open('output.csv', 'wb') as fh:
        for page in doc:
            text = page.get_text()
            parcel_number_candidates = find_parcel_number_candidates(text)
            # fh.write(text.encode("utf8"))


if __name__ == '__main__':
    experiment('/Users/marcellebonterre/Downloads/university-of-california-real-property-portfolio-4-2020.pdf')
