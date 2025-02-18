import os
import pandas as pd
#from langchain import OpenAI

from IPython.display import Markdown, HTML, display
from langchain.schema import HumanMessage
from langchain_community.llms.openai import OpenAI

df = pd.read_csv("./data/all-states-history.csv").fillna(value = 0)

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
#from langchain.agents import create_pandas_dataframe_agent
llm = OpenAI(model="text-davinci-003")
agent = create_pandas_dataframe_agent(llm=None,df=df,verbose=True)
result = agent.invoke("how many rows are there?")
print(result)
