from .. import lang_smith_config

from langchain.chat_models import init_chat_model

model=init_chat_model("gpt-3.5-turbo",model_provider="openai")

from langchain_core.messages import HumanMessage,SystemMessage

messages=[
    SystemMessage(content="Translate the following from English into  Chinese."),
    HumanMessage(content="hi")
]
print(model.invoke(messages))


for token in model.stream(messages):
    print(token.content,end="|")



from langchain.prompts import ChatPromptTemplate
system_template ="Translate the following from English into  {language}"
prompt_template=ChatPromptTemplate.from_messages([
    ("system",system_template),("user","{text}")
])

prompt = prompt_template.invoke({"language":"Chinese","text":"hi"})
model.invoke(prompt)