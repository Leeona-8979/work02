import os


class Config:
    # 高德API配置
    AMAP_WEB_KEY = "3ca688e2bb98c73693388e859c86e1a9"  # Web服务Key
    AMAP_JS_KEY = "baf36e706ba493a5b9352202bd934e62"  # JS API Key（必须配置）

    # 路径配置（根据实际情况修改）
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TEMPLATE_DIR = os.path.join(BASE_DIR, '../app/templates')


config = Config()
