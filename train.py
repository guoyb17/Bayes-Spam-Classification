'''
train.py
By: Guo Yuanbo, 03/2020
'''
def train(src, mode, ans):
    '''
    Use input dataset src (list [({"from": "...", ..., "bags": {"...": 1, ...}}, True/False), ...]) to calculate.
    mode: 0 for basic train, 1 for add from, ...
    ans: data to continue, should start from {True: [{}, 0, {}, 0, {}, 0, {}, 0], False: [{}, 0, {}, 0, {}, 0, {}, 0]}
    Return dict {True: [{"word1": 123, ...}, 1233, {"163.com", 233}, 2344, {"1": 234, ...}, 1000, {"Microsoft": 345, ...}, 2000], False: [...]}
    '''
    for (mail, is_spam) in src:
        if "from" in mail.keys() and ((mode >= 1 and mode <= 100) or mode >= 1000000):
            word = mail["from"]
            if word not in ans[is_spam][2].keys():
                ans[is_spam][2][word] = 1
            else:
                ans[is_spam][2][word] += 1
            ans[is_spam][3] += 1
        if "priority" in mail.keys() and ((mode >= 101 and mode <= 200) or mode >= 1000000):
            word = mail["priority"]
            if word not in ans[is_spam][4].keys():
                ans[is_spam][4][word] = 1
            else:
                ans[is_spam][4][word] += 1
            ans[is_spam][5] += 1
        if "mailer" in mail.keys() and ((mode >= 201 and mode <= 300) or mode >= 1000000):
            word = mail["mailer"]
            if word not in ans[is_spam][6].keys():
                ans[is_spam][6][word] = 1
            else:
                ans[is_spam][6][word] += 1
            ans[is_spam][7] += 1
        for word in mail["bags"].keys():
            if word not in ans[is_spam][0].keys():
                ans[is_spam][0][word] = mail["bags"][word]
            else:
                ans[is_spam][0][word] += mail["bags"][word]
            ans[is_spam][1] += 1
    return ans
