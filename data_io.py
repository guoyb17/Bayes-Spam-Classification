'''
data_io.py
By: Guo Yuanbo, 03/2020
'''
import os, sys, random, chardet


label_dir = os.path.join(os.path.dirname(__file__), "label")
label_file = os.path.join(label_dir, "index")

def get_encoding(test_file):
    with open(os.path.join(label_dir, test_file), "rb") as f:
        return chardet.detect(f.read())["encoding"]

def random_set(dataset, seed, num):
    '''
    Randomly (according to seed) select some data from dataset, total number according to num.
    num must > 0, < len(dataset).
    Return list [("filepath", True), ...], True for spam, False for not spam
    '''
    total = len(dataset)
    if num <= 0 or num > total:
        print("[ERROR] num must > 0, < len(dataset).")
        return []
    elif num == total:
        return dataset[:]
    ans = []
    random.seed(seed)
    dataset_copy = dataset[:]
    for i in range(num):
        ans.append(dataset_copy.pop(random.randint(0, total - 1 - i)))
    return ans

def data_divide(dataset, seed, k):
    '''
    Randomly (according to seed) divide dataset into k parts.
    k must > 1.
    Return list [[("filepath", True), ...], ...]
    '''
    if k <= 1:
        print("[ERROR] k must > 1.")
        return []
    ans = [[] for _ in range(k)]
    total = len(dataset)
    random.seed(seed)
    dataset_copy = dataset[:]
    for i in range(total):
        ans[i % k].append(dataset_copy.pop(random.randint(0, total - 1 - i)))
    return ans

def read_all():
    '''
    Read all labels.
    Return list [("filepath", True), ...]. True for spam, False for not spam
    '''
    f = open(label_file)
    src = f.readlines()
    f.close()
    ans = []
    max_num = len(src)
    d = 0
    for line in src:
        elements = line.strip("\n").split(" ")
        encoding = get_encoding(elements[1])
        if encoding == "utf-8" or encoding == "ascii":
            if elements[0] == "spam":
                ans.append((elements[1], True))
            else:
                ans.append((elements[1], False))
        d += 1
        done = int(50 * d / max_num)
        sys.stdout.write("\r[%s%s] %.2f%%" % ('█' * done, ' ' * (50 - done), 100 * d / max_num))
        sys.stdout.flush()
    print("")
    return ans
