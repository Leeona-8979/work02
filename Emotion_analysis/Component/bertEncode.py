import os

from tqdm import tqdm

# 设置transformers的缓存目录
os.environ["TRANSFORMERS_CACHE"] = "./data/cache/"

import numpy as np

import torch


def batch_encode(texts, tokenizer, model, device, batch_size=64):
    model.eval()  # 将模型设置为评估模式
    input_ids = []
    attention_masks = []
    features = []

    for i in tqdm(range(0, len(texts), batch_size), desc='批处理编码'):
        batch_texts = texts[i:i + batch_size]
        encoded = tokenizer.batch_encode_plus(
            batch_texts,
            max_length=512,
            add_special_tokens=True,
            return_token_type_ids=False,
            padding=True,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids = encoded['input_ids'].to(device)
        attention_masks = encoded['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_masks)

        # 只取[CLS]的输出
        batch_features = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        features.append(batch_features)

    return np.concatenate(features, axis=0)


from transformers import BertTokenizer, BertModel
from pathlib import Path


def encode_text(texts, device, batch_size=64):
    # 获取绝对路径
    project_root = Path(__file__).resolve().parent.parent
    model_path = project_root / "models" / "bert-base-chinese"

    # 验证关键文件是否存在
    required_files = ["tokenizer_config.json", "vocab.txt", "tokenizer.json"]
    for file in required_files:
        if not (model_path / file).exists():
            raise FileNotFoundError(f"关键文件 {file} 缺失！请重新下载模型")

    # 强制从本地加载，禁用任何网络请求
    tokenizer = BertTokenizer.from_pretrained(
        str(model_path),
        local_files_only=True,  # 禁止在线下载
        use_fast=True  # 使用快速分词器（兼容性更好）
    )
    model = BertModel.from_pretrained(
        str(model_path),
        local_files_only=True
    )
    model.to(device)

    # 原有编码逻辑
    encoded_comments = batch_encode(texts, tokenizer, model, device, batch_size)
    return encoded_comments
