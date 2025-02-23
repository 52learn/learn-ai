
import lang_smith_config

from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-3.5-turbo", model_provider="openai")

from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
# response = model.invoke([HumanMessage(content="Hi! I'm Bob")])
# print(response)
# response = model.invoke([HumanMessage(content="What's my name?")])
# print(response)


# response = model.invoke(
#     [HumanMessage(content="Hi! I'm Bob"),
#     HumanMessage(content="What's my name?")
#     ])
# print(response)


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START,MessagesState,StateGraph

workflow = StateGraph(state_schema=MessagesState)

def call_model(state:MessagesState):
    response = model.invoke(state["messages"])
    return {"messages":response}

workflow.add_edge(START,"model")
workflow.add_node("model",call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable":{"thread_id":"abc123"}}

query= "Hi I am kim"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages":input_messages},config)
output["messages"][-1].pretty_print()

query="What's my name?"
input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()

