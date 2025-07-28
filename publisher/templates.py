
# 推文模板构造工具（emoji、话术包装等）
from datetime import datetime

def generate_xhs_post(summary: str, diff_code: str, filename="example.py") -> str:
    # 获取当前日期
    date_str = datetime.now().strftime("%Y年%m月%d日")

    # 模拟一些内容模板
    title = f"# 我的第一个Python程序终于跑通啦！🎉\n\n{date_str} 更新\n\n"
    
    body_intro = (
        f"今天终于把第一个Python脚本跑起来了！虽然只是加了一行简单的打印语句，"
        f"但对新手来说真的超有成就感！✨\n"
    )

    what_changed = (
        f"## 这次改了啥？\n"
        f"{summary}\n\n"
    )

    thoughts = (
        "## 开发小心得 💡\n"
        "作为一个编程新手，从零开始配置环境到写出第一个程序真的踩了好多坑... "
        "（Python版本问题就折腾了我半天😅）"
        "但是看到终端输出的那一刻，一切都值得了！\n\n"
    )

    knowledge = (
        "## Python知识点小课堂\n"
        "这里用到了Python最基础的 `print()` 函数，它：\n"
        "1. 是Python内置函数，不需要额外导入\n"
        "2. 可以打印字符串、数字等各种类型\n"
        "3. 会自动在输出末尾添加换行符\n\n"
    )

    code_block = f"```python\n{diff_code.strip()}\n```\n\n"

    closing = (
        "虽然是很小的进步，但每个大神都是从 \"Hello World\" 开始的不是吗？继续加油！💪\n"
        "#编程新手 #Python入门 #程序员日常\n"
    )

    return title + body_intro + what_changed + thoughts + knowledge + code_block + closing
