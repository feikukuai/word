import subprocess

def run_command(command):
    """
    运行 shell 命令并打印输出。
    如果命令执行失败，打印错误信息。
    """
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")

# 1. 初始化 Git 仓库（如果尚未初始化）
# run_command('git init')

# 2. 添加所有文件到暂存区
run_command('git add .')

# 3. 提交更改
run_command('git commit -m "deepseekai"')

# 4. 配置远程仓库
# 4.1 删除旧的远程仓库配置（如果需要）
run_command('git remote remove origin')  # 如果已有旧配置

# 4.2 添加新的远程仓库（SSH 格式）
run_command('git remote add origin git@github.com:feikukuai/little.git')
# 如果使用 HTTPS 格式，取消注释以下行
# run_command('git remote add origin https://github.com/feikukuai/little.git')

# 5. 推送到远程仓库
# 5.1 如果当前分支是 main，直接推送
run_command('git push -u origin main')
# 5.2 如果当前分支不是 main，但想推送到远程的 main 分支，取消注释以下行
# run_command('git push -u origin HEAD:main')