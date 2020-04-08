'''
email_handler.py
By: Guo Yuanbo, 03/2020
'''
import os, re, string
from data_io import label_dir
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


pattern = r"""(?x)                       # set flag to allow verbose regexps 
	              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
	              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
	              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
	              |\.\.\.                # ellipsis 
	              |(?:[.,;"'?():-_`])    # special characters with meanings 
	       """
stopworddic = set(stopwords.words("english"))
translate_table = dict((ord(char), " ") for char in string.punctuation) # Replace punctuation to space
snowball_stemmer = SnowballStemmer("english")

def parse_data(f_in_label):
    '''
    Open file according to f_in_label from label directory.
    Return dict {"from": "...", ..., "bags": {"...": 1, ...}}
    '''
    f = open(os.path.join(label_dir, f_in_label))
    line = f.readline().strip("\n")
    ans = {}
    words = []
    while line != "":
        if line.startswith("From: "):
            parse_1 = re.match(r"(.*)<(.*)@(.*)>", line)
            if parse_1 != None:
                ans["from"] = parse_1.group(3)
            else:
                parse_2 = re.match(r"(.*)@(.*)", line)
                if parse_2 != None:
                    ans["from"] = parse_2.group(2)
        elif line.startswith("Subject: "):
            subject = re.match(r"Subject: (.*)", line).group(1)
            subject = subject.translate(translate_table)
            words.extend(nltk.regexp_tokenize(subject, pattern))
        elif line.startswith("X-Priority: "):
            parse_3 = re.match(r"X-Priority: ([0-9]*)(.*)", line)
            if parse_3 != None:
                ans["priority"] = parse_3.group(1)
        elif line.startswith("X-Mailer: "):
            parse_4 = re.match(r"X-Mailer: (.*)", line)
            if parse_4 != None:
                ans["mailer"] = parse_4.group(1)
        # If necessary, add other features here.
        line = f.readline().strip("\n")
    lines = f.readlines()
    for line in lines:
        line = line.strip("\n")
        if line == "" or line.startswith("--")\
            or line.startswith("Content-Type: ")\
            or line.startswith("Mail-from: ")\
            or line.startswith("Return-Path: ")\
            or line.startswith("Received: ")\
            or line.startswith("	id ")\
            or line.startswith("Date: ")\
            or line.startswith("From: ")\
            or line.startswith("Message-Id: ")\
            or line.startswith("To: ")\
            or line.startswith("In-Reply-To: ")\
            or line.startswith("Subject: ")\
            or line.startswith("Reply-To: ")\
            or line.startswith("Content-Transfer-Encoding: ")\
            or line.startswith("This is a multi-part message in MIME format.")\
            or line.startswith("Summary-line: "):
            continue
        line = line.translate(translate_table)
        words.extend(nltk.regexp_tokenize(line, pattern))
    words = [word for word in words if word not in stopworddic] # Omit stop words
    words = [snowball_stemmer.stem(word) for word in words] # Stemming
    bags = {}
    for word in words:
        if word not in bags.keys():
            bags[word] = 1
        else:
            bags[word] += 1
    ans["bags"] = bags
    return ans
