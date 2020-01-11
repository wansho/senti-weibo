#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
requirements

$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ pip install .

Attention: The model trained by fastText can not be reproduced, we performed multiple trainings on the training set and selected the best classifier as our final classifier.
"""

import pandas as pd
import fastText

"""training"""
corpus_path = "senti_corpus.csv"
df_corpus = pd.read_csv(corpus_path, encoding="utf-8")
train_list = (df_corpus["label"] + " , " + df_corpus["seged_weibo"]).tolist()
# input must be a filepath
train_path = "train.txt" 
model_path = "senti-model.bin"
with open(train_path, "w", encoding="utf_8_sig") as fw:
    for line in train_list:
        fw.write(u"{}\n".format(line))
# train
model_classifier = fastText.train_supervised(train_path,
                                             label="__label__",
                                             dim=200,
                                             lr=0.2, 
                                             epoch=25,
                                             wordNgrams=2,
                                             )
model_classifier.save_model(model_path)

"""test"""
test_path = "senti_test.csv"
df_test = pd.read_csv(test_path, encoding="utf-8")
test_list = (df_test["label"] + " , " + df_test["seged_weibo"]).tolist()
test_path2 = "test.txt"
with open(test_path2, "w", encoding="utf_8_sig") as fw:
    for line in test_list:
        fw.write(u"{}\n".format(line))
model_path = "senti-model.bin"
model_classifier = fastText.load_model(model_path) # input must be a filepath
result = model_classifier.test(test_path2)
print(result[1]) # accuracy