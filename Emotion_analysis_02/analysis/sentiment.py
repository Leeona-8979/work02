# -*- coding: utf-8 -*-
from snownlp import SnowNLP
import jieba.analyse


def analyze_sentiment(text):
    """返回情感得分（0-1）和关键词"""
    s = SnowNLP(text)

    return {
        "sentiment": s.sentiments,
        "keywords": jieba.analyse.extract_tags(text, topK=5)
    }


def batch_analyze(comments):
    """批量分析评论数据"""
    return [{
        **comment,
        **analyze_sentiment(comment["text"])
    } for comment in comments]
