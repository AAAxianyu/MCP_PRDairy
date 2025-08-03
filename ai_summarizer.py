import openai
import logging
from datetime import datetime

class AISummarizer:
    """
    AI 总结器，使用 OpenAI API 来总结 PR 内容
    """
    
    def __init__(self, api_key):
        """
        初始化 AI 总结器
        
        Args:
            api_key (str): OpenAI API Key
        """
        self.api_key = api_key
        openai.api_key = api_key
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def summarize_pr(self, pr_info):
        """
        总结 PR 内容
        
        Args:
            pr_info (dict): PR 信息
            
        Returns:
            str: 总结文本
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(pr_info)
            
            # 调用 OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的开发日记记录员，负责将 GitHub PR 信息转换为简洁的日记格式。请用中文简体记录，格式为：'今天 [作者] 提交了一个 PR，主要完成了 [总结]...'"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            self.logger.info(f"AI 总结完成，长度: {len(summary)} 字符")
            
            return summary
            
        except Exception as e:
            self.logger.error(f"AI 总结失败: {str(e)}")
            # 返回备用总结
            return self._fallback_summary(pr_info)
    
    def _build_prompt(self, pr_info):
        """
        构建 AI 提示词
        
        Args:
            pr_info (dict): PR 信息
            
        Returns:
            str: 提示词
        """
        # 格式化时间
        created_time = datetime.fromisoformat(pr_info['created_at'].replace('Z', '+00:00'))
        formatted_time = created_time.strftime('%Y年%m月%d日 %H:%M')
        
        # 构建文件列表
        files_text = ""
        if pr_info.get('changed_files_list'):
            files_text = "\n修改的文件：\n" + "\n".join([f"- {file}" for file in pr_info['changed_files_list'][:10]])
            if len(pr_info['changed_files_list']) > 10:
                files_text += f"\n... 还有 {len(pr_info['changed_files_list']) - 10} 个文件"
        
        prompt = f"""
请根据以下 GitHub PR 信息，生成一段简洁的开发日记：

PR 标题：{pr_info['title']}
PR 描述：{pr_info['description']}
作者：{pr_info['author']} ({pr_info.get('author_name', '')})
PR 编号：#{pr_info['number']}
创建时间：{formatted_time}
分支信息：{pr_info['head_branch']} → {pr_info['base_branch']}
统计信息：+{pr_info['additions']} -{pr_info['deletions']} 修改了 {pr_info['changed_files']} 个文件
PR 链接：{pr_info['url']}{files_text}

请生成一段简洁的日记，格式为：
"今天 [作者] 提交了一个 PR，主要完成了 [根据标题和描述总结主要工作]..."

 要求：
 1. 使用中文简体
 2. 语言自然流畅
 3. 突出主要工作内容
 4. 包含作者和 PR 编号信息
 5. 如果有重要文件修改，可以简要提及
 6. 长度控制在 100-200 字之间
"""
        
        return prompt
    
    def _fallback_summary(self, pr_info):
        """
        备用总结方法（当 AI API 调用失败时使用）
        
        Args:
            pr_info (dict): PR 信息
            
        Returns:
            str: 备用总结
        """
        author = pr_info['author']
        title = pr_info['title']
        number = pr_info['number']
        changed_files = pr_info['changed_files']
        
        # 简单的模板总结
        summary = f"今天 {author} 提交了一个 PR (#{number})，主要完成了 {title}。"
        
        if changed_files > 0:
            summary += f" 共修改了 {changed_files} 个文件"
        
        if pr_info['additions'] > 0 or pr_info['deletions'] > 0:
            summary += f"，新增 {pr_info['additions']} 行，删除 {pr_info['deletions']} 行。"
        
        summary += f" PR 链接：{pr_info['url']}"
        
        return summary
    
    def test_connection(self):
        """
        测试 OpenAI API 连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": "测试连接"}
                ],
                max_tokens=10
            )
            return True
        except Exception as e:
            self.logger.error(f"OpenAI API 连接测试失败: {str(e)}")
            return False 