# -*- coding=utf-8
import logging
import os
import sys

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from .load_yml import read

YML_CONFIG = read()

g_client = None
secret_id = YML_CONFIG["cos"]["secret_id"]
secret_key = YML_CONFIG["cos"]["secret_key"]
region = YML_CONFIG["cos"]["bucket_region"]
bucket_name = YML_CONFIG["cos"]["bucket_name"]


def get_client():
    if g_client:
        return g_client
    # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
    # secret_id
    # secret_key = YML_CONFIG["cos"]["secret_key"]
    # region = YML_CONFIG["cos"]["bucket_region"]  # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
    # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
    token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
    scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    client = CosS3Client(config)
    return client


def upload_file_byte(file_byte: bytes, file_name: str) -> str:
    client = get_client()
    #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
    # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
    response = client.put_object(
        Bucket=bucket_name,
        Body=file_byte,
        Key=file_name,
        StorageClass='STANDARD',
        EnableMD5=False
    )
    return f'https://{bucket_name}.cos.{region}.myqcloud.com/{file_name}'


def upload_file_by_name(file_path: str, file_name: str = "") -> str:
    client = get_client()
    if file_name == "":
        file_name = os.path.basename(file_path)
    #### 高级上传接口（推荐）
    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    response = client.upload_file(
        Bucket=bucket_name,
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    if response['Location']:
        return response['Location']
    return f'https://{bucket_name}.cos.{region}.myqcloud.com/{file_name}'
