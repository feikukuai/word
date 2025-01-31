import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")

# 初始化Git仓库
#run_command('git pull origin main')
#run_command('git init')

# 添加所有文件到暂存区
run_command('git add .')

# 提交更改
run_command('git commit -m "deepseekai"')

# 添加远程仓库
# 清除旧的 origin 配置（可选）
run_command('git remote remove origin')  # 如果已有旧配置

# 添加正确的远程仓库（SSH 格式）
#run_command('git remote add git@github.com:feikukuai/xxl.git')
# 或使用 HTTPS 格式
run_command('git remote add origin https://github.com/feikukuai/little.git')

# 推送到远程仓库
# 注意：这里没有使用 -u 参数，如果需要可以添加
#run_command('git push -u origin main --force')
run_command('git push origin HEAD:main')
# 如果你使用的是 'main' 分支，请使用以下命令
# run_command('git push origin main')
