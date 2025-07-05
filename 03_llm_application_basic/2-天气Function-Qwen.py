#!/usr/bin/env python
# coding: utf-8

"""
天气查询Function Calling示例脚本
功能：演示如何让大语言模型调用外部函数来获取实时天气信息

Function Calling（函数调用）是什么？
- 让大语言模型不仅能理解和生成文本，还能调用外部工具/函数
- 实现"思考-调用-回答"的智能交互模式
- 解决大模型无法获取实时数据的问题

工作流程：
1. 用户提问 → 2. 模型分析是否需要调用函数 → 3. 执行函数获取数据 → 4. 模型基于数据生成回答
"""

# In[3]:

# ==================== 导入必要的库 ====================
import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role

# ==================== API密钥配置 ====================
# 从环境变量中获取API密钥，确保安全性
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# ==================== 自定义函数定义 ====================
# 这个函数将被大模型调用，用于获取天气信息
# 注意：这里使用模拟数据，实际应用中应该调用真实的天气API
def get_current_weather(location, unit="摄氏度"):
    """
    获取指定城市的天气信息
    参数：
        location: 城市名称
        unit: 温度单位（摄氏度/华氏度）
    返回：
        JSON格式的天气信息
    """
    # 模拟天气数据（实际应用中应该调用天气API）
    temperature = -1  # 默认温度
    
    # 根据城市名称返回对应的模拟温度
    if '大连' in location or 'Dalian' in location:
        temperature = 10
    if '上海' in location or 'Shanghai' in location:
        temperature = 36
    if '深圳' in location or 'Shenzhen' in location:
        temperature = 37
    
    # 构建天气信息字典
    weather_info = {
        "location": location,        # 城市名称
        "temperature": temperature,  # 温度
        "unit": unit,               # 温度单位
        "forecast": ["晴天", "微风"], # 天气状况
    }
    
    # 返回JSON字符串，便于模型解析
    return json.dumps(weather_info, ensure_ascii=False)

# ==================== 大模型API调用封装 ====================
def get_response(messages):
    """
    调用大模型API，支持Function Calling
    参数：
        messages: 对话历史消息列表
    返回：
        API响应对象或None（如果出错）
    """
    try:
        # 调用通义千问API
        response = dashscope.Generation.call(
            model='qwen-turbo',           # 使用qwen-turbo模型
            messages=messages,            # 对话历史
            functions=functions,          # 可调用的函数定义（关键参数）
            result_format='message'       # 返回格式为message
        )
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

# ==================== 核心对话流程 ====================
def run_conversation():
    """
    执行完整的Function Calling对话流程
    这是整个脚本的核心函数，展示了Function Calling的完整工作流程
    """
    # 用户的问题
    query = "大连的天气怎样"
    print(f"用户问题: {query}")
    
    # 初始化对话历史，包含用户的问题
    messages = [{"role": "user", "content": query}]
    
    # ========== 第一步：第一次调用模型 ==========
    print("\n=== 第一步：模型分析用户问题 ===")
    response = get_response(messages)
    
    # 检查API调用是否成功
    if not response or not response.output:
        print("获取响应失败")
        return None
        
    print('API响应:', response)
    
    # 提取模型的回复
    message = response.output.choices[0].message
    messages.append(message)  # 将模型回复加入对话历史
    print('模型回复:', message)
    
    # ========== 第二步：检查是否需要调用函数 ==========
    print("\n=== 第二步：检查是否需要调用函数 ===")
    
    # 检查模型是否要求调用函数
    # 注意：这里使用字典方式安全访问，避免KeyError
    if isinstance(message, dict) and 'function_call' in message and message['function_call']:
        print("检测到函数调用请求！")
        
        # 提取函数调用信息
        function_call = message['function_call']
        tool_name = function_call['name']  # 函数名称
        print(f"需要调用的函数: {tool_name}")
        
        # ========== 第三步：执行函数调用 ==========
        print("\n=== 第三步：执行函数调用 ===")
        
        # 解析函数参数（JSON字符串转字典）
        arguments = json.loads(function_call['arguments'])
        print('函数参数:', arguments)
        
        # 根据函数名称调用对应的函数
        if tool_name == 'get_current_weather':
            tool_response = get_current_weather(
                location=arguments.get('location'),  # 城市名称
                unit=arguments.get('unit'),          # 温度单位
            )
        
        # 将函数执行结果包装成消息格式
        tool_info = {
            "role": "function",           # 角色：函数
            "name": tool_name,            # 函数名称
            "content": tool_response      # 函数返回结果
        }
        print('函数执行结果:', tool_info)
        
        # 将函数结果加入对话历史
        messages.append(tool_info)
        print('更新后的对话历史:', messages)
        
        # ========== 第四步：第二次调用模型 ==========
        print("\n=== 第四步：模型基于函数结果生成最终回答 ===")
        
        # 再次调用模型，这次模型会基于函数返回的真实数据生成回答
        response = get_response(messages)
        
        # 检查第二次调用是否成功
        if not response or not response.output:
            print("获取第二次响应失败")
            return None
            
        print('最终API响应:', response)
        
        # 提取最终回答
        message = response.output.choices[0].message
        return message
    
    # 如果没有函数调用，直接返回第一次的回答
    print("无需调用函数，直接返回模型回答")
    return message

# ==================== 函数定义配置 ====================
# 这个配置告诉大模型有哪些函数可以调用，以及如何调用
functions = [
    {
        'name': 'get_current_weather',                    # 函数名称
        'description': 'Get the current weather in a given location.',  # 函数描述
        'parameters': {                                   # 参数定义（JSON Schema格式）
            'type': 'object',                            # 参数类型：对象
            'properties': {                              # 属性定义
                'location': {                            # location参数
                    'type': 'string',                    # 类型：字符串
                    'description': 'The city and state, e.g. San Francisco, CA'  # 描述
                },
                'unit': {                                # unit参数
                    'type': 'string',                    # 类型：字符串
                    'enum': ['celsius', 'fahrenheit']    # 可选值：摄氏度或华氏度
                }
            },
            'required': ['location']                     # 必需参数：只有location是必需的
        }
    }
]

# ==================== 主程序入口 ====================
if __name__ == "__main__":
    print("开始执行天气查询Function Calling示例...")
    print("=" * 50)
    
    # 执行对话流程
    result = run_conversation()
    
    # 输出最终结果
    if result:
        print("\n" + "=" * 50)
        print("最终结果:", result)
        print("=" * 50)
    else:
        print("对话执行失败")

