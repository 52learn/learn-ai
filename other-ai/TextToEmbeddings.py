from openai import OpenAI
from MyLogger import logger
import os

#加载环境变量
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI()


# 将文本转换为向量
def get_embeddings(texts,model='text-embedding-ada-002',dimensions=None):
    '''封装OpenAI的embedding模型接口，返回embedding列表和embedding向量维度'''
    if model == 'text-embedding-ada-002':
        dimensions = None
    if dimensions:
        data = client.embeddings.create(input=texts,model=model,dimensions=dimensions).data
    else:
        data = client.embeddings.create(input=texts,model=model).data
    #print(data)
    return [x.embedding for x in data]