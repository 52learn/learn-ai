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

class Data(BaseModel):
    """Extracted data about people"""
    # Creates a model so that we can extract multiple entities
    people: List[Person]

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
system = '''你是一个专家提取算法。仅从文本中提取相关信息。如果您不知道要求提取的属性的值就返回null'''
prompt_tempalte = ChatPromptTemplate.from_messages([
    ("system","{system}"),
    ("human","{input}")
])


from langchain.chat_models import init_chat_model

llm=init_chat_model("gpt-3.5-turbo",model_provider="openai")


# structured_llm = llm.with_structured_output(schema=Person,method="function_calling")
# prompt=prompt_tempalte.invoke(
#     {"input":"我叫张三花名Tom身高17325岁喜欢运动健身旅游看电影联系方式15824135596现在就职于华云科技股份常驻地江苏省南京市","system":system}
# )
# print(f"prompt: {prompt}")
# response = structured_llm.invoke(prompt)

# print(response)


# messages = [
#     {"role": "user", "content": "2 🦜 2"},
#     {"role": "assistant", "content": "4"},
#     {"role": "user", "content": "2 🦜 3"},
#     {"role": "assistant", "content": "5"},
#     {"role": "user", "content": "3 🦜 4"},
# ]

# response = llm.invoke(messages)
# print(response.content)


from langchain_core.utils.function_calling import tool_example_to_messages

examples = [
    ("The ocean is blue",Data(p=[])),
    (
        "27岁的Tom很热爱音乐棒球篮球，作为一名音乐教师，每天工作5小时",
        Data(p=[Person(name="Tom",age=27,hobbies=["音乐","棒球","篮球"],work="音乐教师",height=None,address=None,phone=None,nickName=None)])
    )
]

messages = []
for txt,tool_call in examples:
    if tool_call.people:
        ai_response = "Detected people"
    else:
        ai_response = "No people detected"

    messages.extend(tool_example_to_messages(txt,[tool_call],ai_response))

for msg in messages:
    print(msg.pretty_print())