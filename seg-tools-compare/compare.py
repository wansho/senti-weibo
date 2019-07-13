# -*- coding: utf-8 -*-
"""
@author: wanshuo
"""
import fastText

def get_model_accuracy(model_path, test_path):
    model_classifier = fastText.load_model(model_path)
    result = model_classifier.test(test_path)
    return result[1]


model_path = "senti-model.bin" # Available at Google Drive: http://bit.ly/2XvGJfJ

# cleaned and seged by different segmentation tool
jieba_path = "jieba.txt"
hanlp_path = "HanLP.txt"
pkuseg_path = "pkuseg.txt"
thulac_path = "THULAC.txt"
snownlp_path = "SnowNLP.txt"
foolnltk_path = "FoolNLTK.txt"

test_path_list = [jieba_path, hanlp_path, pkuseg_path, thulac_path, snownlp_path, foolnltk_path]
for path in test_path_list:
    precision = get_model_accuracy(model_path, test_path=path)
    print(path, precision)
