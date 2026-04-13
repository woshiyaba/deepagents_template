import asyncio
from pathlib import Path

from src.common.utils.llm_util import ReadOnlyFilesystemBackend, create_app_deep_agent
from src.common.utils.writer import StreamCollector, astream_agent_collect

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = PROJECT_ROOT / "skills"

SYSTEM_PROMPT = """\
你的名字是洛克龙虾，你会使用你拥有的技能去处理不同的事情
"""

agent = create_app_deep_agent(
    system_prompt=SYSTEM_PROMPT,
    skills_dir=SKILLS_DIR,
    backend=ReadOnlyFilesystemBackend(root_dir=PROJECT_ROOT, virtual_mode=True),
)


async def build_user_input(
        skill_name: str,
) -> str:
    """组装鼓励话语生成的输入 prompt。"""
    parts = f"帮我下载并安装：{skill_name} skills"
    return parts


async def main():
    """流式调用 agent 并收集完整结果（异步版）。

    同时订阅 messages（流式推送思考过程）和 updates（提取最终结果）。
    node_name 非空时同时推送 start/streaming/end 状态事件。
    """
    raw_content = await astream_agent_collect(agent,
                                              await build_user_input("frontend-design"),
                                              thread_id="thread_123",
                                              node_name='skills_find')
    return raw_content


if __name__ == '__main__':
    asyncio.run(main())
