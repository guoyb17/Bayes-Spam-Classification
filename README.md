# Naïve Bayes Classifier

Introduction to Machine Learning Experiment 1

## Introduction

A Naïve Bayes Classifier. Use `data/` and `label/` to train. Identify spam.

## Dependancy

After `pip3 install -r requirements.txt`, open python3, and download resources:

```python
import nltk
nltk.download('stopwords')
```

The program uses the `data` and `label` folders within the **same** directory of the program to access data and labels. It does **NOT** accept file directory modification from command line.

## Usage

Use `python3 main.py -h` to see options.

Use all default settings:

```
python3 main.py
```

mode: 

0 for basic train (default 0);

1 for add from, 2, 3, ..., 100 for add from more times (power);

101 for add priority, 102, 103, ..., 200 for more times (power);

201 for add mailer, 202, 203, ..., 300 for more times (power);

1000000, ..., 1999999 for add all, ...

Parts of 1 00 00 00 and more: 1 for add all; 00s for from(lower 00), priority(middle 00), and mailer(higher 00), 00 for power 01, 01 for power 02, ..., 99 for power 100.

## LICENSE

特别声明：程序作者，即本人，不对代码二次使用者的一切学术或非学术行为负责。对本人开源的代码的一切包括但不限于复制、参考、修改、运行等的使用行为，由此产生的一切包括但不限于学术、经济、法律等的后果，本人概不负责，且由此对本人造成的一切损害，保留追究责任权利。（ 在法律允许的范围内， ）一切解释权归本人所有。
