#!/usr/bin/env python
# coding: utf-8

"""
运维事件处置系统 - Function Calling示例
功能：
1、告警内容理解。根据输入的告警信息，结合第三方接口数据，判断当前的异常情况（告警对象、异常模式）；
2、分析方法建议。根据当前告警内容，结合应急预案、运维文档和大语言模型自有知识，形成分析方法的建议；
3、分析内容自动提取。根据用户输入的分析内容需求，调用多种第三方接口获取分析数据，并进行总结；
4、处置方法推荐和执行。根据当前上下文的故障场景理解，结合应急预案和第三方接口，形成推荐处置方案，待用户确认后调用第三方接口进行执行。
"""

import json
import os
import random
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# 通过第三方接口获取数据库服务器状态
def get_current_status():
    """
    模拟获取数据库服务器当前状态
    返回：连接数、CPU使用率、内存使用率等性能指标
    """
    # 生成连接数数据
    connections = random.randint(10, 100)
    # 生成CPU使用率数据
    cpu_usage = round(random.uniform(1, 100), 1)
    # 生成内存使用率数据
    memory_usage = round(random.uniform(10, 100), 1)
    status_info = {
        "连接数": connections,
        "CPU使用率": f"{cpu_usage}%",
        "内存使用率": f"{memory_usage}%"
    }
    return json.dumps(status_info, ensure_ascii=False)

# 封装模型响应函数
def get_response(messages):
    """
    调用大模型API，支持工具调用
    """
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            tools=tools,
            result_format='message'  # 将输出设置为message形式
        )
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_status",
            "description": "调用监控系统接口，获取当前数据库服务器性能指标，包括：连接数、CPU使用率、内存使用率",
            "parameters": {},
            "required": []
        }                
    }
]

def run_ops_analysis():
    """
    执行运维事件分析流程
    """
    print("=== 运维事件处置系统启动 ===")
    
    # 告警信息
    query = """告警：数据库连接数超过设定阈值
时间：2024-08-03 15:30:00
"""
    print(f"收到告警信息：\n{query}")
    
    # 初始化对话
    messages = [
        {"role": "system", "content": "我是运维分析师，用户会告诉我们告警内容。我会基于告警内容，判断当前的异常情况（告警对象、异常模式），并提供分析和处置建议。"},
        {"role": "user", "content": query}
    ]
    
    print("\n=== 开始分析流程 ===")
    
    # 多轮对话处理
    max_iterations = 5  # 防止无限循环
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- 第{iteration}轮分析 ---")
        
        # 调用模型
        response = get_response(messages)
        if not response or not response.output:
            print("获取响应失败")
            break
            
        message = response.output.choices[0].message
        messages.append(message)
        
        # 显示模型回复
        if 'content' in message and message['content']:
            print(f"AI分析: {message['content']}")
        
        # 检查是否完成
        if response.output.choices[0].finish_reason == 'stop':
            print("分析完成")
            break
        
        # 检查是否需要调用工具
        if 'tool_calls' in message and message['tool_calls']:
            print("检测到工具调用请求...")
            
            for tool_call in message['tool_calls']:
                # 获取函数名称和参数
                fn_name = tool_call['function']['name']
                fn_arguments = tool_call['function']['arguments']
                
                print(f"调用工具: {fn_name}")
                print(f"参数: {fn_arguments}")
                
                # 解析参数
                arguments_json = json.loads(fn_arguments) if fn_arguments else {}
                
                # 调用对应的函数
                if fn_name == 'get_current_status':
                    tool_response = get_current_status()
                
                # 将工具响应加入对话
                tool_info = {
                    "role": "tool", 
                    "name": fn_name, 
                    "content": tool_response
                }
                messages.append(tool_info)
                
                print(f"工具响应: {tool_response}")
        else:
            print("无需调用工具，分析完成")
            break
    
    print("\n=== 分析流程结束 ===")
    return messages

if __name__ == "__main__":
    # 执行运维分析
    result = run_ops_analysis()
    
    print("\n=== 最终分析结果 ===")
    for i, msg in enumerate(result):
        if msg['role'] == 'assistant' and 'content' in msg:
            print(f"第{i+1}轮回复: {msg['content']}")
        elif msg['role'] == 'tool':
            print(f"工具调用结果: {msg['content']}")

