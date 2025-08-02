import pytest
from unittest.mock import patch, MagicMock
from .feishu import send_feishu_message, send_summary_to_feishu


# 测试发送文本消息
def test_send_text_message():
    # 使用mock替换requests.post，避免实际发送请求
    with patch('requests.post') as mock_post:
        # 设置模拟的响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "msg": "success"}
        mock_post.return_value = mock_response

        # 调用函数
        result = send_feishu_message("text", "测试文本消息")

        # 验证结果
        assert result == {"code": 0, "msg": "success"}
        mock_post.assert_called_once()


# 测试发送富文本消息
def test_send_post_message():
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "msg": "success"}
        mock_post.return_value = mock_response

        post_content = {
            "zh_cn": {
                "title": "测试标题",
                "content": [[{"tag": "text", "text": "测试内容"}]]
            }
        }
        result = send_feishu_message("post", post_content)

        assert result == {"code": 0, "msg": "success"}
        mock_post.assert_called_once()


# 测试发送不支持的的消息类型
def test_send_unsupported_message_type():
    with pytest.raises(ValueError) as excinfo:
        send_feishu_message("unsupported", "内容")

    assert "不支持的message_type" in str(excinfo.value)


# 测试发送摘要的便捷函数
def test_send_summary_to_feishu():
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "msg": "success"}
        mock_post.return_value = mock_response

        result = send_summary_to_feishu("测试摘要内容")

        assert result == {"code": 0, "msg": "success"}
        mock_post.assert_called_once()


# 如果需要实际发送测试消息（不推荐在自动化测试中使用）
def test_actual_send_message():
    # 注意：这会真的发送消息到飞书，仅用于手动测试
    TEST_MESSAGE = "这是一条自动化测试消息，请忽略"

    # 测试文本消息
    result = send_feishu_message("text", TEST_MESSAGE)
    print("文本消息发送结果:", result)
    assert result.get("code") == 0 or result.get("StatusCode") == 0

    # 测试富文本消息
    post_content = {
        "zh_cn": {
            "title": "测试标题",
            "content": [[{"tag": "text", "text": TEST_MESSAGE}]]
        }
    }
    result = send_feishu_message("post", post_content)
    print("富文本消息发送结果:", result)
    assert result.get("code") == 0 or result.get("StatusCode") == 0