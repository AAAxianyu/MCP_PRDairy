 # 从 GitHub 拉取 PR、组装 diff
from github import Github
from summarizer import summarize_code
from publisher.xhs import publish
from config import GITHUB_TOKEN

g = Github(GITHUB_TOKEN)

def handle_pull_request(owner, repo_name, pr_number):
    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    diff_text = ""
    for f in files:
        if f.patch:
            diff_text += f"File: {f.filename}\n{f.patch}\n\n"

    if diff_text:
        summary = summarize_code(diff_text)
        publish(summary)  # 将结果推送（由C模块处理）
        print(f"[✅] Summary for PR #{pr_number}:\n{summary}")
    else:
        print(f"[ℹ️] PR #{pr_number} has no code diff.")
