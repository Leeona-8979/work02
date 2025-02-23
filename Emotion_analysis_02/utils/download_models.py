from huggingface_hub import snapshot_download
import os


def download_bert_model():
    # 创建 models 目录（如果不存在）
    os.makedirs("../models", exist_ok=True)

    # 下载完整模型文件
    snapshot_download(
        repo_id="bert-base-chinese",
        local_dir="../models/bert-base-chinese",
        local_dir_use_symlinks=False,
        ignore_patterns=["*.h5", "*.ot", "*.msgpack"],  # 可选：跳过非必要文件
    )


if __name__ == "__main__":
    download_bert_model()
    print("BERT模型下载完成！路径：../models/bert-base-chinese")
