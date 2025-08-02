import requests
import json
from MCP_PRDairy.config import FEISHU_WEBHOOK_URL


def send_feishu_message(message_type="text", content=""):
    """
    发送消息到飞书群组

    :param message_type: 消息类型，可以是 "text" 或 "post"
    :param content: 消息内容，根据message_type不同格式不同
    :return: 返回飞书API的响应
    """
    headers = {
        "Content-Type": "application/json"
    }

    if message_type == "text":
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
    elif message_type == "post":
        payload = {
            "msg_type": "post",
            "content": {
                "post": content
            }
        }
    else:
        raise ValueError("不支持的message_type，目前只支持 'text' 或 'post'")

    response = requests.post(
        FEISHU_WEBHOOK_URL,
        headers=headers,
        data=json.dumps(payload))

    return response.json()


def send_summary_to_feishu(summary_text):
    """发送摘要到飞书"""
    return send_feishu_message("text", summary_text)
