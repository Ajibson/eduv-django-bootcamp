# Standard Python library imports.
import math
import re

# Core Django imports.
from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    # Get a list of the characters in the blog post
    matching_words = re.findall(r'\w+', word_string)
    # get the count of the characters
    count = len(matching_words)  # joincfe.com/projects/
    return count


def read_time(html_string):
    # This returns the length of the text i.e number of characters in the text
    count = count_words(html_string)
    # assuming 200wpm reading, rounding the result upward to the nearest integer
    read_time_min = math.ceil(count/200.0)
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)
