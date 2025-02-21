import os,sys
import pandas as pd
from langchain_openai import ChatOpenAI

current_dir=os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(current_dir,"./data/all-states-history.csv")
df = pd.read_csv(csv_file).fillna(value = 0)

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
agent = create_pandas_dataframe_agent(llm,df,verbose=True,allow_dangerous_code=True)
result = agent.invoke("总死亡数多少?")
print(result)
