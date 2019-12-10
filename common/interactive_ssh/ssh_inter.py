import paramiko
import interactive

# 记录日志
paramiko.util.log_to_file('./test')
# 建立ssh连接
ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.135.52.138', port=22, username='itw_shenzl', password='Pass654321', compress=True)
# 建立交互式shell连接
channel = ssh.invoke_shell()
# 建立交互式管道
interactive.interactive_shell(channel)
# 关闭连接
channel.close()
ssh.close()
