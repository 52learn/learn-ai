from .. import lang_smith_config
from langchain.chat_models import init_chat_model

#llm = init_chat_model("gpt-3.5-turbo",model="openai")   

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel,Field

tagging_prompt = ChatPromptTemplate.from_template(
    '''Extract the desired information from the following passage.Only extract the properties mentioned in the 'Classification' function.
    Passage:{input}
    '''
)
class Classification(BaseModel):
    sentiment:str = Field(description="The sentiment of the text")
    aggressiveness:str = Field(description="The aggressiveness of the text on a scale of 1 to 10")
    language:str = Field(description="The language of the text")

llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo').with_structured_output(Classification,method="function_calling")
prompt = tagging_prompt.invoke({"input": "我现在感觉很难过"})
response = llm.invoke(prompt)
print(response)

'''
大模型情感检测：
input: Thank you for your help!
response: sentiment='positive' aggressiveness='5' language='English'

input： 我现在感觉很难过
response: sentiment='negative' aggressiveness='N/A' language='Chinese'
'''


class Classification2(BaseModel):
    sentiment: str = Field(..., enum=["happy", "sad", "neutral"])
    aggressiveness: str = Field(..., 
                                description="describes how aggressive the statement is, the higher the number the more aggressive",
                                enum=["1", "2", "3", "4", "5"])
    language: str = Field(..., enum=["Spanish","English", "Chinese","Japanese","French"])

tagging_prompt = ChatPromptTemplate.from_template(
    '''Extract the desired information from the following passage.Only extract the properties mentioned in the 'Classification' function.
    Passage:{input}
    '''
)

llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo').with_structured_output(Classification2,method="function_calling")
prompt = tagging_prompt.invoke({"input": "今天我很幸运，遇到了一个好心人。"})
response = llm.invoke(prompt)
print(response)