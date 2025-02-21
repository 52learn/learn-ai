import pandas as pd
import sys

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import init_chat_model

from langchain.schema import HumanMessage,SystemMessage
from typing import Optional,List
from pydantic import BaseModel,Field

df = pd.read_csv("./data/nl_to_csv.csv")
# 定义Person模型
class Person(BaseModel):
    name: Optional[str] = Field(default=None, description="姓名")
    age: Optional[int] = Field(default=None, description="年龄")
    work: Optional[str] = Field(default=None, description="工作")
    address: Optional[str] = Field(default=None, description="住址")
    phone: Optional[str] = Field(default=None, description="电话")
    nickName: Optional[str] = Field(default=None, description="昵称")
    height: Optional[float] = Field(default=None, description="身高")
    hobbies: Optional[List[str]] = Field(default=None, description="兴趣爱好")


llm = init_chat_model("gpt-3.5-turbo", model_provider="openai")
# 定义系统消息
system_message = SystemMessage(content="""
你是一个专家提取算法。仅从文本中提取相关信息。如果您不知道要求提取的属性的值就返回null。
你将帮助用户查询和统计CSV文件中的数据。用户将用自然语言描述他们的需求。
""")


# messages=[
#     SystemMessage(content="Translate the following from English into  Chinese."),
#     #HumanMessage(content="{text}")
#     ("human", "Hello, how are you?")
# ]
# prompt_messages = ChatPromptTemplate.from_messages(messages)
# print(prompt_messages.invoke({"text":"hi"}))

prompt_template  = ChatPromptTemplate.from_messages([
    system_message,
    #MessagesPlaceholder(variable_name="history"),
    #HumanMessage(content="{input}")
    ("human","{input}")
])

def process_input(user_input:str)->str:
    # 构建对话历史
    history = []
    prompt = prompt_template.format_messages(**{"input":user_input,"history":history});
    print(prompt)
    # 调用语言模型获取回复
    response = llm.invoke(prompt)
    # 提取结构化输出
    #structured_response = response.content.strip()
    return response


user_input = "统计所有人的平均年龄"

print(process_input(user_input))


agent = create_pandas_dataframe_agent(llm=None,df=df,verbose=True)