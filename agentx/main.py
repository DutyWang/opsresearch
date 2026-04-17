import os
import logging
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

# ===================== 日志 =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== 加载配置 =====================
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# ===================== 状态定义 =====================
class AssistantState(TypedDict):
    messages: Annotated[list, add_messages]

# ===================== 工具（已修复：必须加 docstring）=====================
@tool
def calculator(expression: str) -> str:
    """数学计算器，支持加减乘除表达式计算"""
    try:
        return f"计算结果：{eval(expression)}"
    except Exception as e:
        return f"计算错误：{str(e)}"

@tool
def file_writer(file_name: str, content: str) -> str:
    """将内容写入本地文本文件"""
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        return f"文件 {file_name} 写入成功！"
    except Exception as e:
        return f"写入失败：{str(e)}"

# 联网搜索工具
search_tool = DuckDuckGoSearchRun()

# 工具列表
tools = [calculator, file_writer, search_tool]

# ===================== 模型 =====================
llm = ChatOpenAI(
    model=DEEPSEEK_MODEL,
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=0,
).bind_tools(tools)

# ===================== 节点 =====================
def call_llm(state: AssistantState):
    logger.info("调用 LLM...")
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: AssistantState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# ===================== 构建图 =====================
workflow = StateGraph(AssistantState)
workflow.add_node("llm", call_llm)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("llm")
workflow.add_conditional_edges("llm", should_continue)
workflow.add_edge("tools", "llm")

# ===================== ✅ 集成开源可视化调试：LangGraphics =====================
try:
    from langgraphics import watch
    graph = watch(workflow.compile())
    logger.info("✅ 已启用开源可视化调试（LangGraphics）")
except ImportError:
    graph = workflow.compile()
    logger.info("ℹ️ 未安装 langgraphics，跳过可视化调试")

# ===================== 本地运行 =====================
if __name__ == "__main__":
    print("\n🎉 开源本地个人助理启动成功！")
    print("输入 'exit' 退出\n")

    while True:
        user_input = input("你：")
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("👋 再见！")
            break

        result = graph.invoke({"messages": [("user", user_input)]})
        print("\n助理：", result["messages"][-1].content)