'''
description: Used to Named Entity Recognition, For vehicle parameter entity extraction
date: 2020-10-01
author: jtx

'''




from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser


def sentence_splitter(sentence):
    """
    分句，也就是将一片文本分割为独立的句子
    :param sentence:几句话
    :return: 单个单个句子
    """
    single_sentence = SentenceSplitter.split(sentence)  # 分句
    print('\n'.join(single_sentence))


def word_splitter(sentence):
    """
    分词
    :param sentence:
    :return:
    """
    segmentor = Segmentor()  # 初始化实例
    segmentor.load('D:\Python\python_code\Liangzhi\TianPengTrans-tmp\etl\ltp_triple_extraction\ltp_data/cws.model')  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    # 默认可以这样输出
    # print '\t'.join(words)
    # 可以转换成List 输出
    words_list = list(words)
    # for word in words_list:
    #     print word
    segmentor.release()  # 释放模型
    return words_list


def word_tag(words):
    """
    词性标注
    :param words: 已切分好的词
    :return:
    """
    postagger = Postagger()  # 初始化实例
    postagger.load('D:\Python\python_code\Liangzhi\TianPengTrans-tmp\etl\ltp_triple_extraction\ltp_data/pos.model')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    for word, tag in zip(words, postags):
        print(word+'/'+tag)
    postagger.release()  # 释放模型
    return postags


def name_recognition(words, postags):
    """
    命名实体识别
    :param words:分词
    :param postags:标注
    :return:
    """
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load('D:\Python\python_code\Liangzhi\TianPengTrans-tmp\etl\ltp_triple_extraction\ltp_data/ner.model')  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别

    # 地名标签为 ns
    result = ''
    for i in range(0, len(netags)):
        if i < len(words) - 2:
            if 's' in netags[i]:
                if 'O' in netags[i + 1] and words[i + 1] != ',' and words[i + 1] != '，':
                    if 's' in netags[i + 2]:
                        result += words[i] + words[i + 1] + words[i + 2] + " "
    print(result)
    # for word, ntag in zip(words, netags):
    #     print word + '/' + ntag
    recognizer.release()  # 释放模型
    return netags


def parse(words, postags):
    """
    依存句法分析
    :param words:
    :param postags:
    :return:
    """
    parser = Parser()  # 初始化实例
    parser.load('D:\Python\python_code\Liangzhi\TianPengTrans-tmp\etl\ltp_triple_extraction\ltp_data/parser.model')  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parser.release()  # 释放模型


# 测试命名实体识别
print('命名实体识别')
words = word_splitter('屏幕尺寸：10.8英寸*显示屏采用圆角设计，按照标准矩形测量时，屏幕的对角线长度是 10.8英寸（实际可视区域略小）。屏幕色彩：1670万色，DCI-P3广色域，屏幕类型：LCD，分辨率：WQXGA 2560 x 1600像素*该分辨率对应标准矩形，实际屏幕采用圆角和珍珠屏设计，有效像素略少。')
tags = word_tag(words)
name_recognition(words, tags)
# parse(words,tags)


'''动力总成	230TCI手动	230TCI自动	290TGDI自动，型号	都市版	时尚版	精英版	时尚版	精英版	时尚版	精英版	豪华版	尊贵版	旗舰版，指导价	88800.0	97900.0	105900.0	109900.0	115900.0	119900.0	126900.0	134900.0	144900.0	155900.0
长×宽×高(mm)	4700×1860×1746
轴距(mm)	2710.0
座位数	5座	5/7座	5座	5/6/7座	5座	5/6/7座	5/7座
行李箱容积(L)	889-1930(5座)；193-1930（6/7座）
整备质量(kg)	1509(5座)/1541(7座)	1541(5座)/1556(6/7座)	1544(5座)/1587(6/7座)
悬架系统	麦弗逊式独立悬架/多连杆独立悬架
驱动方式	前置前驱
制动器类型(前/后)	通风盘/盘式
转向系统	双模EPS电子助力转向模式（舒适/运动）
轮胎规格	225/65 R17	235/55 R18	235/50 R19
（马牌轮胎）'''