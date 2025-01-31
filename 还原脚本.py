import subprocess

def git_checkout(commit_hash):
    try:
        # 使用 subprocess.run 来执行 git checkout 命令，并使用 --force 选项
        result = subprocess.run(['git', 'checkout', commit_hash, '--force'], check=True, text=True, capture_output=True)
        # 打印命令的输出
        return "Output:", result.stdout
    except subprocess.CalledProcessError as e:
        # 打印错误信息
        return "Error:", e.stderr

# 用实际的 commit-hash 替换 'commit-hash' 字符串
commit_hash = '75a4a834538c5f8467d171140cf287f5d8fb3cd0'
git_checkout(commit_hash)