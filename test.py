'''
test.py
By: Guo Yuanbo, 03/2020
'''
from math import log


def test(src, mode, model, alpha):
    '''
    Use input dataset src (list [({"from": "...", ..., "bags": {"...": 1, ...}}, True/False), ...]) to test.
    mode: 0 for basic train, 1 for add from, ...
    model: trained model, dict {True: [{"word1": 123, ...}, 1233, {"163.com", 233}, 2344, {"1": 234, ...}, 1000, {"Microsoft": 345, ...}, 2000], False: [...]}
    alpha: for zero-probabilities
    Print accuracy, precision, recall and F1.
    Return list [accuracy, precision, recall, F1].
    '''
    p_true_base = model[True][1] / (model[True][1] + model[False][1])
    p_false_base = model[False][1] / (model[True][1] + model[False][1])
    tp = 0 # True, positive report positive
    tn = 0 # True, negative report negative
    fp = 0 # False, negative report positive
    fn = 0 # False, positive report negative
    M_true = len(model[True][0]) + len(model[True][2]) + len(model[True][4]) + len(model[True][6])
    M_false = len(model[False][0]) + len(model[False][2]) + len(model[False][4]) + len(model[False][6])
    N_true = model[True][1] + model[True][3] + model[True][5] + model[True][7]
    N_false = model[False][1] + model[False][3] + model[False][5] + model[False][7]
    for (mail, is_spam) in src:
        p_true = log(p_true_base)
        p_false = log(p_false_base)
        if "from" in mail.keys() and ((mode >= 1 and mode <= 100) or mode >= 1000000): # handle from
            word = mail["from"]
            power = 1
            if mode <= 100:
                power = mode
            else:
                power += (mode % 100)
            if word not in model[True][2].keys():
                p_true += power * log(alpha / (N_true + alpha * M_true))
            else:
                p_true += power * log((model[True][2][word] + alpha) / (N_true + alpha * M_true))
            if word not in model[False][2].keys():
                p_false += power * log(alpha / (N_false + alpha * M_false))
            else:
                p_false += power * log((model[False][2][word] + alpha) / (N_false + alpha * M_false))
        if "priority" in mail.keys() and ((mode >= 101 and mode <= 200) or mode >= 1000000): # handle priority
            word = mail["priority"]
            power = 1
            if mode <= 200:
                power = mode - 100
            else:
                power += ((mode // 100) % 100)
            if word not in model[True][4].keys():
                p_true += power * log(alpha / (N_true + alpha * M_true))
            else:
                p_true += power * log((model[True][4][word] + alpha) / (N_true + alpha * M_true))
            if word not in model[False][4].keys():
                p_false += power * log(alpha / (N_false + alpha * M_false))
            else:
                p_false += power * log((model[False][4][word] + alpha) / (N_false + alpha * M_false))
        if "mailer" in mail.keys() and (mode <= 100 or mode >= 1000000): # handle mailer
            word = mail["mailer"]
            power = 1
            if mode <= 300:
                power = mode - 200
            else:
                power += ((mode // 10000) % 100)
            if word not in model[True][6].keys():
                p_true += power * log(alpha / (N_true + alpha * M_true))
            else:
                p_true += power * log((model[True][6][word] + alpha) / (N_true + alpha * M_true))
            if word not in model[False][6].keys():
                p_false += power * log(alpha / (N_false + alpha * M_false))
            else:
                p_false += power * log((model[False][6][word] + alpha) / (N_false + alpha * M_false))
        for word in mail["bags"].keys():
            if word not in model[True][0].keys():
                p_true += log(alpha / (N_true + alpha * M_true))
            else:
                p_true += log((model[True][0][word] + alpha) / (N_true + alpha * M_true))
            if word not in model[False][0].keys():
                p_false += log(alpha / (N_false + alpha * M_false))
            else:
                p_false += log((model[False][0][word] + alpha) / (N_false + alpha * M_false))
        if is_spam:
            if p_true > p_false:
                tp += 1
            else:
                fn += 1
        else:
            if p_true > p_false:
                fp += 1
            else:
                tn += 1
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = (2 * precision * recall) / (precision + recall)
    print("**** Accuracy = " + str(accuracy))
    print("**** Precision = " + str(precision))
    print("**** Recall = " + str(recall))
    print("**** F1 = " + str(F1))
    return [accuracy, precision, recall, F1]
