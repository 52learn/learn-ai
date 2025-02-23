import lang_smith_config

from langchain_core.tools import tool

from langchain.chat_models import init_chat_model

from langchain.schema import HumanMessage

from langchain_core.messages import ToolMessage

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


model = init_chat_model("gpt-3.5-turbo",model_provider="openai")
model_with_tools = model.bind_tools([multiply])

messages=[
    HumanMessage(content="What is 2 * 3?")
]
response = model_with_tools.invoke(messages)
tool_calls = response.tool_calls
print(response)


for tool_call in tool_calls:
    result = globals().get(tool_call['name']).invoke(tool_call['args'])
    print(result)
    # ??????????????
    # messages.append(ToolMessage(content=f"The answer is {result}", tool_call_id=tool_call['id']))
    # response = model.invoke(messages)
    # print(response)


print(f"tool multiply ... name: {multiply.name} , description： {multiply.description}, args： {multiply.args}")
 