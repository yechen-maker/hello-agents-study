import requests
from tavily import TavilyClient
from openai import OpenAI
import re
import os

# 1. 系统提示词
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
"""

# 2. 天气工具 get_weather
def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实的天气信息。
    """
    # API端点，我们请求JSON格式的数据
    url = f'https://wttr.in/{city}?format=j1'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # print(data)
        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]['value']
        temp_c = current_condition["temp_C"]

        return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
    
    except requests.exceptions.RequestException as e:
        return f'错误，网络问题 - {e}'
    except (KeyError, IndexError) as e:
        return f'解析数据失败，可能是城市名无效 - {e}'

# 3. 景点推荐工具 get_attraction
def get_attraction(city: str, weather: str) -> str:
    api_key = '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'
    if not api_key:
        return "apikey配置错误"
    
    # 2. 初始化Tavily客户端
    tavily = TavilyClient(api_key= api_key)

    # 3. 构造一个精确的查询
    query = f"'{city}'在'{weather}'天气下最值得去的旅游景点推荐"

    try:
        # 4. 调用API，include_answer=True会返回一个综合性的回答
        response = tavily.search(query= query, search_depth= "basic", include_answer= True)

        # 5. Tavily返回的结果已经非常干净，可以直接使用
        # response['answer'] 是一个基于所有搜索结果的总结性回答
        if response.get("answer"):
            return response['answer']

        # 如果没有综合性回答，则格式化原始结果
        formatted_results = []
        for result in response.get('results', []):
            formatted_results.append(f"-{result['title']}: {result['content']}")

        if not formatted_results:
            return "抱歉，没有找到相关景点"

        return "根据搜索，为你找到信息:\n" + "\n".join(formatted_results)

    except Exception as e:
        return f'出现问题 - {e}'

# 4. 工具注册表 available_tools
# 将所有工具函数放入一个字典，方便后续调用
available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

# 5. 大语言模型客户端
class OpenAICompatibleClient:
    """
    一个用于调用任何兼容OpenAI接口的LLM服务的客户端。
    """
    def __init__(self, model: str, api_key: str, base_url: str):
        self.model = model
        self.client = OpenAI(api_key= api_key, base_url= base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应。"""
        print("正在调用大模型")

        try:
            messages = [
                {"role": 'system', "content": system_prompt},
                {"role": 'user', "content": prompt},
            ]

            respoense = self.client.chat.completions.create(
                model= self.model,
                messages= messages,
                stream= False
            )

            answer = respoense.choices[0].message.content
            print("大模型响应成功")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"
        

# 6. Agent 行动循环
# --- 1. 配置LLM客户端 ---
# 请根据您使用的服务，将这里替换成对应的凭证和地址
API_KEY = "AIzaSyCBv_UgLhmx9tB7RqMYi3QtLbil6YkfMDU"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
MODEL_ID = "gemini-2.5-flash-lite"
TAVILY_API_KEY="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"
os.environ['TAVILY_API_KEY'] = "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"

llm = OpenAICompatibleClient(
    model= MODEL_ID,
    api_key= API_KEY,
    base_url= BASE_URL
)
# --- 2. 初始化 ---
user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f'用户请求{user_prompt}']

print(f'用户输入{user_prompt}\n' + '=' * 40)

# --- 3. 运行主循环 ---
for i in range(5):
    print(f'循环{i + 1}\n')
    # 3.1. 构建Prompt
    full_prompt = '\n'.join(prompt_history)

    # 3.2. 调用LLM进行思考
    llm_output = llm.generate(full_prompt, system_prompt= AGENT_SYSTEM_PROMPT)
    # 模型可能会输出多余的Thought-Action，需要截断
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|/Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余Thought-Action对")

    print(f'模型输出:\n{llm_output}\n')
    prompt_history.append(llm_output)

    # 3.3. 解析并执行行动
    action_match = re.search(r'Action:(.*)', llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue

    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r'Finish[(.*)\]', action_str).group(1)
        print(f'任务完成，最终答案{final_answer}')
        break

    tool_name = re.search(r'(\w+)\(', action_str).group(1)
    args_str = re.search(r'\((.*)\)', action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"未定义的工具：'{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
        
# if __name__ == "__main__":
#     # result = get_weather("成都")
#     result = get_attraction("成都", "晴天")
#     print(result)