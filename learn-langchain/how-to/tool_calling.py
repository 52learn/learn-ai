from typing_extensions import Annotated,TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticToolsParser
 

class add(TypedDict):
    """Add two integers."""

    # Annotations must have the type and can optionally include a default value and description (in that order).
    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


class multiply(TypedDict):
    """Multiply two integers."""

    a: Annotated[int, ..., "First integer"]
    b: Annotated[int, ..., "Second integer"]


tools = [add, multiply]

# from dotenv import load_dotenv,find_dotenv
# _ = load_dotenv(find_dotenv())
OPENAI_GPT_MODEL="gpt-3.5-turbo" 
llm = init_chat_model(OPENAI_GPT_MODEL, model_provider="openai")
llm_with_tools = llm.bind_tools(tools)
message = llm_with_tools.invoke("What is 3 * 12? Also, what is 11 + 49?" )
tool_calls = message.tool_calls
print(tool_calls)
'''
[{
	'name': 'multiply',
	'args': {
		'a': 3,
		'b': 12
	},
	'id': 'call_hRZAKDhbYxGTwlsORLHYLUTa',
	'type': 'tool_call'
}, {
	'name': 'add',
	'args': {
		'a': 11,
		'b': 49
	},
	'id': 'call_Xfqpe2AWywCCSmWicpLlFV0q',
	'type': 'tool_call'
}]
'''

chain = llm_with_tools|PydanticToolsParser(tools=tools)
message = chain.invoke( "What is 3 * 12? Also, what is 11 + 49?" )
print(message)
'''
[{'a': 3, 'b': 12}, {'a': 11, 'b': 49}]
'''