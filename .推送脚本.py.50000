import subprocess

def run_command(command):
    """
    运行 shell 命令并打印输出。
    如果命令执行失败，打印错误信息。
    """
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Warning: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")

# 1. 检查 Git 状态
run_command('git status')

# 2. 添加所有文件到暂存区
run_command('git add .')

# 3. 提交更改
run_command('git commit -m "deepseekai"')

# 4. 拉取远程仓库的最新内容（避免冲突）
run_command('git pull origin main')

# 5. 推送到远程仓库
run_command('git push -u origin main')