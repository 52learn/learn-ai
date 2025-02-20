from lang_smith_config import *
from typing import Optional,List
from pydantic import BaseModel,Field

class Person(BaseModel):
    name: Optional[str] = Field(default=None,description="姓名")
    age: Optional[int] = Field(default=None,description="年龄")
    work: Optional[str] = Field(default=None,description="工作")
    address: Optional[str] = Field(default=None,description="住址")
    phone: Optional[str] = Field(default=None,description="电话")
    nickName: Optional[str] = Field(default=None,description="昵称")
    height: Optional[float] = Field(default=None,description="身高")
    hobbies: Optional[List[str]] = Field(default=None,description="兴趣爱好")

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
system = '''你是一个专家提取算法。仅从文本中提取相关信息。如果您不知道要求提取的属性的值就返回null'''
prompt_tempalte = ChatPromptTemplate.from_messages([
    ("system","{system}"),
    ("human","{input}")
])


from langchain.chat_models import init_chat_model

llm=init_chat_model("gpt-3.5-turbo",model_provider="openai")
structured_llm = llm.with_structured_output(schema=Person,method="function_calling")
prompt=prompt_tempalte.invoke(
    {"input":"我叫张三花名Tom身高17325岁喜欢运动健身旅游看电影住浙江省杭州市滨江区联系方式15824135596现在就职于华云科技股份","system":system}
)
print(f"prompt: {prompt}")
response = structured_llm.invoke(prompt)

print(response)