
import lang_smith_config

from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-3.5-turbo", model_provider="openai")
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START,StateGraph
from typing_extensions import TypedDict,Annotated

class State(TypedDict):
    messages:Annotated[list[HumanMessage|AIMessage|SystemMessage|ToolMessage],
                       "The messages to be sent to the model"]
    language:Annotated[str,"The language of the messages"]

workflow = StateGraph(state_schema=State)

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability in {language}."),
    MessagesPlaceholder(variable_name="messages"),
])

def call_model(state:State):
    prompts = prompt_template.invoke(state)
    return model.invoke(prompts)
    

workflow.add_edge(
    START, "model"
)
workflow.add_node(
    "model",
    call_model
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable":{"thread_id":"abc123"}}

query = "Hi I am kim"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages":input_messages},config)
output["messages"][-1].pretty_print()
query = "What's my name?"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
