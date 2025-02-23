# # utils/download_models_fix.py
# from huggingface_hub import snapshot_download
# import requests
# import os
#
# from torch.testing._internal.common_utils import download_file
# from tqdm import tqdm
#
# # 强制使用国内镜像
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
#
# REQUIRED_FILES = [
#     "config.json",
#     "pytorch_model.bin",
#     "tokenizer_config.json",
#     "vocab.txt",
#     "special_tokens_map.json",
#     "tokenizer.json"
# ]
#
#
# def download_bert_model():
#     os.makedirs("../models/bert-base-chinese", exist_ok=True)
#
#     # 从清华镜像站下载
#     base_url = "https://hf-mirror.com/bert-base-chinese/resolve/main/"
#
#     for file in REQUIRED_FILES:
#         url = base_url + file
#         save_path = f"../models/bert-base-chinese/{file}"
#         print(f"正在下载 {file}...")
#         download_file(url, save_path)
#
#     print("所有文件下载完成！路径：../models/bert-base-chinese")
#
#
# if __name__ == "__main__":
#     download_bert_model()

import os
import requests
from tqdm import tqdm

# 强制使用国内镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

REQUIRED_FILES = [
    "config.json",
    "pytorch_model.bin",
    "tokenizer_config.json",
    "vocab.txt",
    "special_tokens_map.json",
    "tokenizer.json"
]


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    # 使用 tqdm 显示下载进度
    with open(save_path, 'wb') as file, tqdm(
            desc=save_path,
            total=total_size,
            unit='B',
            unit_scale=True
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))


def download_bert_model():
    # 创建模型保存目录
    model_dir = "../models/bert-base-chinese"
    os.makedirs(model_dir, exist_ok=True)

    # 设置基础镜像站 URL
    base_url = "https://hf-mirror.com/bert-base-chinese/resolve/main/"

    # 下载所需文件
    for file in REQUIRED_FILES:
        url = base_url + file
        save_path = os.path.join(model_dir, file)  # 保存到对应路径
        print(f"正在下载 {file}...")
        download_file(url, save_path)

    print("所有文件下载完成！路径：", model_dir)


if __name__ == "__main__":
    download_bert_model()
