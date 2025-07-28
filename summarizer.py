 # 调用 OpenAI 接口生成摘要
import gradio as gr
from config import OPENAI_API_KEY  # 从配置文件导入 OpenAI API 密钥
from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def summarize_code(diff: str):

#    调用 OpenAI ChatCompletion 生成摘要
    response = client.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {"role": "developer", "content": "你是一个热爱分享的程序员博主，请你根据以下 Git diff 输出一段小红书风格的文案，用中文写，语气轻松自然，可以加一些 emoji 和开发心得，适合发布在开发者社区或朋友圈。请包含：1. 本次改动做了什么（通俗易懂地解释）2. 涉及的文件或函数3. 一点点开发者心情或思考（比如“踩了个坑”或“为了优化用户体验～”）4. 代码更改相关语言知识点总结介绍（拓展一点地解释）5. 用 markdown 表示代码块（可选）"},
        {"role": "user", "content": diff}
    ],
    temperature=0.5, max_tokens=300
    )
    return response.choices[0].message.content

demo = gr.Interface(fn=summarize_code,
                    inputs=gr.Textbox(lines=10, placeholder="代码变更 diff"),
                    outputs="text",
                    title="代码变更摘要",
                    description="接收 GitHub Pull Request 的 diff 内容，输出自然语言说明")

if __name__ == "__main__":
    demo.launch(mcp_server=True)
    # print(summarize_code("diff --git a/example.py b/example.py\nindex 83db48f..f735c3e 100644\n--- a/example.py\n+++ b/example.py\n@@ -1,3 +1,4 @@\n+print('Hello World')\n print('This is an example file.')\n print('It has some changes.')"))