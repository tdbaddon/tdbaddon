'''
Created on 22 jan 2012

@author: Batch
'''
import re

def regex_from_to(text, from_string, to_string, excluding=True):
    #print "regex_from_to: " + text
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    #print "regex_get_all: " + text
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	

