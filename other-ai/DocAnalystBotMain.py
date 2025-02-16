'''
conda env:  rag

'''


import sys
from TextToEmbeddings import get_embeddings
from MyVectorDBConnector import *
from openai import OpenAI
import os
from MyLogger import logger

#加载环境变量
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())
 

def get_completion(promt,model="gpt-3.5-turbo"):
    messages = [{"role":"user","content":promt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def build_prompt(promt_template, **kwargs):
    ''' 将prompt模板和参数拼接起来 '''
    inputs = {}
    for k,v in kwargs.items():
        if isinstance(v, list) and all(isinstance(i, str) for i in v):
            val = '\n\n'.join(v)
        else:
            val = v
        inputs[k] = val
    return promt_template.format(**inputs)  


prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
已知信息：
{context}
用户问：
{query}

如果已知信息不包含用户问题的答案，请直接说"不知道"。
请用中文回答。
"""

class DocAnalystBot:
    def __init__(self,vector_db,llm_api,n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results
    def chat(self,user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query,self.n_results,{"$and":[{"len": {"$gt": 100}},{"bizCode":{"$eq":"CWZT"}}]})
        # 2. 构建Promt
        prompt = build_prompt(prompt_template,context=search_results['documents'][0],query=user_query)
        # 3. 调用LLM
        response = self.llm_api(prompt)
        logger.debug(f"LLM prompt >>>>>>>>>: {prompt}")
        logger.debug(f"LLM results >>>>>>>>>>>>>>: \n{response}\n<<<<<<<<<<<<<<<<<<<")
        return response

if __name__ == "__main__":
    client = OpenAI()    
    vector_db = MyVectorDBConnector("rag_demo",get_embeddings)
    # 创建一个RAG机器人
    bot = DocAnalystBot(vector_db,llm_api=get_completion)
    #user_query = "目录名最大多少位"
    #user_query = "Llama 2有多少个参数"
    user_query = "请详细描述财务中台建设过程"
    #user_query = "请详细描述财务中台背景"
    response = bot.chat(user_query)

