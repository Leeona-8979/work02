# """
# 抓取评论并预处理训练模型
# """
# import Component.comments as comments
# import Component.preprocess as preprocess
# import Component.sentimentComments as sentimentComments
# import Component.trainLogisticModel as trainLogisticModel
# import Component.trainNNModel as trainNNModel
#
# if __name__ == '__main__':
#     # 抓取老君山评论，对应同程旅游和携程的景点ID分别为 100
#     comments_path = comments.get_comments(ly_poi_id=8472, ctrip_poi_id=77806, page_size=50,
#                                           output_path='./output/Comments.csv')
#     print(f"\033[34m [Log] Comments fetched and saved successfully at {comments_path} \033[0m")
#
#     # 预处理评论数据
#     preprocess_path = preprocess.process_data(file_path=comments_path, output_path='./output/ProcessData.csv')
#     print(f"\033[34m [Log] Data processed and saved successfully at {preprocess_path} \033[0m")
#
#     # 标注情感
#     sentimentComments_path = sentimentComments.get_sentiment(file_path=preprocess_path,
#                                                              output_path='./output/SentimentAnnotatedComments.csv')
#
#     # 训练模型
#     # 训练逻辑回归模型
#     logistic_model_path = trainLogisticModel.train_logistic_model(file_path=sentimentComments_path,
#                                                                   output_path='./output/LogisticModel.joblib')
#     print(f"\033[34m [Log] Logistic Model trained and saved successfully at {logistic_model_path} \033[0m")
#
#     # 训练神经网络模型
#     nn_model_path = trainNNModel.train_neural_network_model(file_path=sentimentComments_path,
#                                                             output_path='./output/NNModel.pt')
#     print(f"\033[34m [Log] Neural Network Model trained and saved successfully at {nn_model_path} \033[0m")
#
#

"""
自动抓取衢州景点评论并进行预处理和模型训练
"""


# 第二版
# import os
# import  pandas as pd
# from utils.amap_provider import AMapAttractionProvider
# from utils.ctrip_crawler import CtripCrawler
# from Component.preprocess import process_data
# from Component.sentimentComments import get_sentiment
# from Component.trainLogisticModel import train_logistic_model
# from Component.trainNNModel import train_neural_network_model
#
# def fetch_attractions(api_key):
#     amap_provider = AMapAttractionProvider(api_key)
#     attractions = amap_provider.get_attractions()
#     attractions_df = pd.DataFrame(attractions)
#     attractions_df.to_csv('output/attractions.csv', index=False)
#     return attractions_df
#
# def crawl_comments(attractions_df):
#     comments_dict = {}
#     ctrip_crawler = CtripCrawler()
#     for index, row in attractions_df.iterrows():
#         comments = ctrip_crawler.crawl_comments(row['name'])
#         comments_df = pd.DataFrame(comments)
#         comments_df.to_csv(f'output/{row["name"]}.csv', index=False)
#         comments_dict[row['name']] = comments
#     return comments_dict
#
# def main():
#     api_key = 'YOUR_AMAP_API_KEY'  # 替换为您的高德地图API密钥
#     attractions_df = fetch_attractions(api_key)
#     comments_dict = crawl_comments(attractions_df)
#
#     # 预处理评论数据
#     preprocess_path = './output/ProcessData.csv'
#     for filename, comments_df in comments_dict.items():
#         comments_df.to_csv(f'{preprocess_path}_{filename}.csv', index=False)
#         process_data(file_path=f'{preprocess_path}_{filename}.csv', output_path=f'{preprocess_path}_{filename}_clean.csv')
#
#     # 标注情感
#     sentiment_path = './output/SentimentAnnotatedComments.csv'
#     for filename, comments_df in comments_dict.items():
#         sentiment_comments_df = get_sentiment(file_path=f'{preprocess_path}_{filename}_clean.csv',
#                                                                  output_path=f'{sentiment_path}_{filename}.csv')
#         sentiment_comments_df.to_csv(f'{sentiment_path}_{filename}.csv', index=False)
#
#     # 训练模型
#     # 训练逻辑回归模型
#     logistic_model_path = train_logistic_model(file_path=sentiment_path,
#                                                               output_path='./output/LogisticModel.joblib')
#     print(f"\033[34m [Log] Logistic Model trained and saved successfully at {logistic_model_path} \033[0m")
#
#     # 训练神经网络模型
#     nn_model_path = train_neural_network_model(file_path=sentiment_path,
#                                                         output_path='./output/NNModel.pt')
#     print(f"\033[34m [Log] Neural Network Model trained and saved successfully at {nn_model_path} \033[0m")
#
#     print("数据已获得，可以进行网页可视化")
#
# if __name__ == '__main__':
#     main()

import logging

import pandas as pd
from tqdm import tqdm

from Component.preprocess import process_data
from Component.sentimentComments import get_sentiment
from Component.trainLogisticModel import train_logistic_model
from Component.trainNNModel import train_neural_network_model
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils.amap_provider import AMapAttractionProvider
from utils.ctrip_crawler import CtripCrawler

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_chrome_driver():
    # 设置 ChromeDriver 路径
    driver_manager = ChromeDriverManager()
    driver = webdriver.Chrome()
    return driver

def fetch_attractions(api_key):
    logging.info("开始爬取衢州景点信息...")
    amap_provider = AMapAttractionProvider(api_key)
    attractions = amap_provider.get_attractions()
    attractions_df = pd.DataFrame(attractions)
    attractions_df.to_csv('output/attractions.csv', index=False)
    logging.info("景点信息爬取完成，保存到 output/attractions.csv")
    return attractions_df

def crawl_comments(attractions_df, driver):
    logging.info("开始爬取评论...")
    ctrip_crawler = CtripCrawler()
    comments_dict = {}
    for index, row in tqdm(attractions_df.iterrows(), desc="爬取评论"):
        logging.info(f"正在爬取 {row['name']} 的评论...")
        comments = ctrip_crawler.crawl_comments(row['name'])
        comments_df = pd.DataFrame(comments)
        comments_df.to_csv(f'output/{row["name"]}.csv', index=False)
        comments_dict[row['name']] = comments
    logging.info("评论爬取完成")
    return comments_dict

def main():
    api_key = '3ca688e2bb98c73693388e859c86e1a9'  # 替换为您的高德地图API密钥
    driver = setup_chrome_driver()
    try:
        attractions_df = fetch_attractions(api_key)
        print("景点信息获取完成。")

        print("开始爬取评论...")
        comments_dict = crawl_comments(attractions_df, driver)
        print("评论爬取完成。")

        # 预处理评论数据
        preprocess_path = './output/ProcessData.csv'
        for filename, comments_df in tqdm(comments_dict.items(), desc="预处理评论数据"):
            comments_df.to_csv(f'{preprocess_path}_{filename}.csv', index=False)
            process_data(file_path=f'{preprocess_path}_{filename}.csv', output_path=f'{preprocess_path}_{filename}_clean.csv')

        # 标注情感
        sentiment_path = './output/SentimentAnnotatedComments.csv'
        for filename, comments_df in tqdm(comments_dict.items(), desc="标注情感"):
            sentiment_comments_df = get_sentiment(file_path=f'{preprocess_path}_{filename}_clean.csv',
                                                              output_path=f'{sentiment_path}_{filename}.csv')
            sentiment_comments_df.to_csv(f'{sentiment_path}_{filename}.csv', index=False)

        # 训练模型
        # 训练逻辑回归模型
        try:
            logistic_model_path = train_logistic_model(file_path=sentiment_path,
                                                              output_path='./output/LogisticModel.joblib')
            logging.info(f"逻辑回归模型训练完成并保存到 {logistic_model_path}")
        except Exception as e:
            logging.error(f"逻辑回归模型训练失败: {e}")

        # 训练神经网络模型
        try:
            nn_model_path = train_neural_network_model(file_path=sentiment_path,
                                                        output_path='./output/NNModel.pt')
            logging.info(f"神经网络模型训练完成并保存到 {nn_model_path}")
        except Exception as e:
            logging.error(f"神经网络模型训练失败: {e}")

    finally:
        driver.quit()
        print("数据已获得，可以进行网页可视化")

if __name__ == '__main__':
    main()