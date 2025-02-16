'''
功能描述：
通过定义function tool，同自然语言一同作为大模型的参数，发起调用，由大模型计算后返回匹配的function信息。

使用场景：
后续可加上agent，调用function，实现自然语言调用function的功能交互。

'''
import json
from openai import OpenAI
from MyLogger import logger
from WeatherApi import get_n_day_weather_forecast_mock
import sys
tools = [
{
        "type": "function",
        "function": {
            "name": "get_n_day_weather_forecast_mock",
            "description": "获取最近n天的天气预报",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或镇区 如：深圳市南山区",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "要使用的温度单位，摄氏度 or 华氏度",
                    },
                    "num_days": {
                        "type": "integer",
                        "description": "预测天数",
                    }
                },
                "required": ["location", "format", "num_days"]
            },
        }
    }
]


client = OpenAI()
def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        logger.debug("chat_completion_request send >>>>>>>>>>>>>>>> ： ")
        logger.debug(f"messages:{messages}")
        logger.debug(f"tools:{tools}")
        logger.debug("chat_completion_request receive >>>>>>>>>>>>>>>> ： ")
        logger.debug(str(response))
        logger.debug("<<<<<<<<<<<<<<<<<<<<<<< ")
        return response
    except Exception as e:
        logger.error("Unable to generate ChatCompletion response")
        logger.error(f"Exception: {e}")
        return e

def do_execute(input_msg):
        
    messages = []
    messages.append({"role": "system", "content": "不要假设将哪些值输入到函数中。如果用户请求不明确，请要求澄清"})
    #messages.append({"role": "user", "content": "未来5天深圳南山区的天气怎么样"})
    #messages.append({"role": "user", "content": "想知道深圳南山区今后5天的天气"})
    messages.append({"role": "user", "content": input_msg})
    logger.info(f"===[LLM]自然语言识别函数名称开始...===")
    chat_response = chat_completion_request(
        messages, tools=tools
    )

    tool_calls=chat_response.choices[0].message.tool_calls
    if tool_calls is None and len(chat_response.choices[0].message.content) > 0:
        logger.warning(chat_response.choices[0].message.content)
        return

        
    logger.debug("===LLM chat with tool 回复 >>>>>>>>>>>>>>>>>>>>>>>>>>")
    logger.debug(tool_calls)

    # 定义键名称映射表
    args_key_map = {
        "format": "units",
        "location": "city",
        "num_days": "n_days"
    }

    # 执行函数
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments_list = json.loads(tool_call.function.arguments)
        function_to_call = globals().get(function_name)
        logger.debug(f"function_to_call: {function_to_call}")
        _args_list = {args_key_map.get(k):v for k,v in arguments_list.items()}
        logger.info(f"===[程序]函数调用开始...===")
        result = function_to_call(**_args_list)

        # 把函数调用结果加入到对话历史中
        messages.append(
            {
                "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                "role": "user",
                "name": function_name,
                "content": "函数执行结果为:" + str(result)
            }
        )
        logger.info(f"===[LLM]结合函数调用结果回复用户开始...===")
        # 函数执行结果传给LLM，组织成自然语言回复用户
        chat_response = chat_completion_request(
            messages, tools=tools
        )
        logger.info(f"===回复用户：...===")
        logger.info(chat_response.choices[0].message.content)
if __name__ == "__main__":
    tip = "我是天气预报助手，请您描述你知道最近几天某个城市的天气情况（目前城市只支持深圳、杭州、上海、北京）";
    while True:
        input_msg = input(tip)
        cities = "深圳、杭州、上海、北京".split("、")
        
        if len([x for x in cities if x in input_msg]) == 0:
            print("请描述你要查询的城市天气预报")
            continue
        else:
            do_execute(input_msg)
            #get_n_day_weather_forecast(input_msg,3)
            



        

# 函数执行结果传给LLM，组织成自然语言回复用户
# chat_response = chat_completion_request(
#     messages, tools=tools
# )
# logger.debug("===回复===")
# logger.debug(chat_response.choices[0].message.content)    
'''
提问：深圳南山区的天气怎么样 
回复：（表明若不指定未来几天，则默认为未来一天即明天）
[ChatCompletionMessageToolCall(
    id='call_981OHHhCJSd6BurWGHckv2h5', 
    function=Function(
        arguments='{"format":"celsius","location":"深圳市南山区","num_days":1}', 
        name='get_n_day_weather_forecast'), 
    type='function')]

提问：未来5天深圳南山区的天气怎么样   
回复：
[ChatCompletionMessageToolCall(
    id='call_h38vlTKRlwGz54t29dYoAplm', 
    function=Function(
        arguments='{"format":"celsius","location":"深圳市南山区","num_days":5}', 
        name='get_n_day_weather_forecast'), 
    type='function')]

提问：想知道深圳南山区今后5天的天气
回复：
[ChatCompletionMessageToolCall(
    id='call_ZCU6uBTr4DjkZUZvx76AkqwJ', 
    function=Function(
        arguments='{"format":"celsius","location":"深圳市南山区","num_days":5}', 
        name='get_n_day_weather_forecast'), 
    type='function')]

LLM能够完全理解“未来5天深圳南山区的天气怎么样” 和 “想知道深圳南山区今后5天的天气” 的文字含义是相同的，所以得出的回复也一样。
WOW !!!

提问：天气怎么样
回复：（表明没有指定城市区域，LLM无法理解，直接返回None）
None

'''
 
