'''
main.py
By: Guo Yuanbo, 03/2020
'''
import argparse
from data_io import read_all, data_divide, random_set
from email_handler import parse_data
from train import train
from test import test


train_round = 5

def sampled_train_test(seed, fold, mode, alpha, all_data, total_num, sample_rate):
    accuracy_results = []
    precision_results = []
    recall_results = []
    F1_results = []
    for cnt in range(train_round):
        print("[INFO] Cycle time 【#" + str(cnt + 1) + "】 begin...")
        part_data = random_set(all_data, seed + cnt, int(round(total_num * sample_rate)))
        data_folds = data_divide(part_data, seed + cnt, fold)
        mail_info = [[] for _ in range(fold)]
        for part in range(fold):
            for (path, is_spam) in data_folds[part]:
                mail_info[part].append((parse_data(path), is_spam))
        local_results = []
        for test_part in range(fold):
            print("[INFO] Train-test round 【" + str(test_part + 1) + "】 begin...")
            train_result = {True: [{}, 0, {}, 0, {}, 0, {}, 0], False: [{}, 0, {}, 0, {}, 0, {}, 0]}
            for train_iter in range(fold):
                if train_iter != test_part:
                    train_result = train(mail_info[train_iter], mode, train_result)
            print("[INFO] Train finished. Testing...")
            local_results.append(test(mail_info[test_part], mode, train_result, alpha))
            print("[INFO] Train-test round 【" + str(test_part + 1) + "】 finished.")
        print("[INFO] Train result:")
        local_accuracy = 0.0
        local_precision = 0.0
        local_recall = 0.0
        local_F1 = 0.0
        for local_result in local_results:
            local_accuracy += local_result[0]
            local_precision += local_result[1]
            local_recall += local_result[2]
            local_F1 += local_result[3]
        local_accuracy /= fold
        local_precision /= fold
        local_recall /= fold
        local_F1 /= fold
        print("** Accuracy = " + str(local_accuracy))
        print("** Precision = " + str(local_precision))
        print("** Recall = " + str(local_recall))
        print("** F1 = " + str(local_F1))
        accuracy_results.append(local_accuracy)
        precision_results.append(local_precision)
        recall_results.append(local_recall)
        F1_results.append(local_F1)
        print("[INFO] Cycle time 【#" + str(cnt + 1) + "】 finished.")
    print("[INFO] sample rate " + str(int(round(sample_rate * 100))) + "%", "results:")
    print(" Accuracy: max = " + str(max(accuracy_results)) + ", min = " + str(min(accuracy_results)) + ", average = " + str(sum(accuracy_results) / train_round))
    print(" Precision: max = " + str(max(precision_results)) + ", min = " + str(min(precision_results)) + ", average = " + str(sum(precision_results) / train_round))
    print(" Recall: max = " + str(max(recall_results)) + ", min = " + str(min(recall_results)) + ", average = " + str(sum(recall_results) / train_round))
    print(" F1: max = " + str(max(F1_results)) + ", min = " + str(min(F1_results)) + ", average = " + str(sum(F1_results) / train_round))

def main(seed, fold, mode, alpha):
    print("[INFO] Reading labels...")
    all_data = read_all()
    print("[INFO] Labels loaded.")
    total_num = len(all_data)
    if mode == 0:
        # 1. sample rate 5%, repeat 5 times
        print("[INFO] 1: sample rate 5%")
        sampled_train_test(seed, fold, mode, alpha, all_data, total_num, 0.05)
        print("========================")
        # 2. sample rate 50%, repeat 5 times
        print("[INFO] 2: sample rate 50%")
        sampled_train_test(seed, fold, mode, alpha, all_data, total_num, 0.5)
        print("========================")
    # 3. sample rate 100%, repeat 5 times
    print("[INFO] 3: sample rate 100%")
    sampled_train_test(seed, fold, mode, alpha, all_data, total_num, 1)
    print("========================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to train and test Naïve Bayes Classifier with email files."
        )
    parser.add_argument("-s", "--seed", type=int,
                        default=0,
                        help="random seed; default 0",
                        required=False
                        )
    parser.add_argument("-f", "--fold", type=int,
                        default=5,
                        help="cross validation fold number, must > 1; default 5",
                        required=False
                        )
    parser.add_argument("-m", "--mode", type=int,
                        default=0,
                        help="mode: 0 for basic train, ... more see README.md; default 0",
                        required=False
                        )
    parser.add_argument("-a", "--alpha", type=float,
                        default=1.0,
                        help="alpha value for smoothing, 0.0 for no smoothing(MAY CAUSE ERROR), 1.0 for laplace, other values acceptable; default 1.0",
                        required=False
                        )

    args = parser.parse_args()
    if args.fold <= 1:
        print("[ERROR] fold must > 1")
    elif args.mode < 0 or (args.mode > 300 and args.mode < 1000000) or args.mode > 1999999: # Add mode if necessary
        print("[ERROR] Illegal mode input!")
    else:
        main(args.seed, args.fold, args.mode, args.alpha)
