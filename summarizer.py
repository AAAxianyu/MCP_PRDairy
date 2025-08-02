 # 调用 OpenAI 接口生成摘要
import gradio as gr
from config import OPENAI_API_KEY
from openai import OpenAI
from publisher.feishu import send_summary_to_feishu

client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_code(diff: str):
    """调用 OpenAI 生成摘要并发送到飞书"""
    # 调用 OpenAI ChatCompletion 生成摘要
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "developer", "content": "你是一个热爱分享的程序员博主..."},
            {"role": "user", "content": diff}
        ],
        temperature=0.5,
        max_tokens=300
    )

    summary = response.choices[0].message.content

    # 发送到飞书
    feishu_response = send_summary_to_feishu(summary)
    print("飞书发送结果:", feishu_response)

    return summary


demo = gr.Interface(
    fn=summarize_code,
    inputs=gr.Textbox(lines=10, placeholder="代码变更 diff"),
    outputs="text",
    title="代码变更摘要",
    description="接收 GitHub Pull Request 的 diff 内容，输出自然语言说明"
)

# if __name__ == "__main__":
#     demo.launch(mcp_server=True)
#     # print(summarize_code("diff --git a/example.py b/example.py\nindex 83db48f..f735c3e 100644\n--- a/example.py\n+++ b/example.py\n@@ -1,3 +1,4 @@\n+print('Hello World')\n print('This is an example file.')\n print('It has some changes.')"))