""" 使用已废弃的fabric3，适用于 centos7 amd64  """
from fabric.api import env, run
from fabric.operations import sudo
from fabric.colors import *

GIT_REPO = "https://github.com/bpzj/linux.conf"
repo = "git@github.com:bpzj/linux.conf.git"
repo_folder = '/home/bpzj/linux.conf'
env.user = 'root'
# 使用 本机私钥登录
env.key_filename = '~/.ssh/id_rsa'
# env.hosts = ['www.lqtblog.com']
# env.port = '29183'

# env.password = '4260'
env.hosts = ['120.79.47.191']
env.port = '22'


def insgit():
    # 安装ftp
    sudo('yum install git')


def cloneconf():
    """复制所有配置文件"""
    home_folder = '/home/bpzj'
    run('cd %s && git clone https://github.com/bpzj/linux.conf.git ' % home_folder)


def instools():
    """ 安装必备工具 """
    # 安装 netstat 工具
    sudo('yum install net-tools')
    # 安装 wget 
    sudo('yum install wget')
    # 安装ftp
    sudo('yum install ftp')


def inspip2():
    # 安装pip  ( python2.7 的 pip ) 
    sudo('yum install python-setuptools')
    sudo('easy_install pip')


def insss():
    """ 安装shadowsshocks """
    sudo('pip install shadowsocks')
    sudo('cp -rf /home/bpzj/linux.conf/shadowsocks/shadowsocks.json /etc/shadowsocks.json')
    sudo('ssserver -c /etc/shadowsocks.json -d start')


def insjdk8152():
    """安装 jdk-8u152 """
    # 更新配置文件
    run('cd %s && git pull' % repo_folder)
    sudo('wget http://mirrors.linuxeye.com/jdk/jdk-8u152-linux-x64.tar.gz')
    sudo('mkdir /usr/lib/jvm')
    sudo('tar -zxvf jdk-8u152-linux-x64.tar.gz -C /usr/lib/jvm')
    run('source /home/bpzj/linux.conf/jdk/8u152.bashrc', pty=False)


def insmaven():
    # 更新配置文件
    run('cd %s && git pull' % repo_folder)
    # 下载maven
    sudo('wget https://mirrors.cnnic.cn/apache/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz')
    # 新建 maven 安装目录
    sudo('mkdir /usr/local/maven')
    # 解压
    sudo('tar -xvzf apache-maven-3.5.2-bin.tar.gz -C /usr/local/maven')
    # 复制配置文件
    sudo('cp -rf /home/bpzj/linux.conf/profile /etc/profile')
    # 配置环境变量，source 命令没作用
    run('source /etc/profile', pty=False)


def centinsmysql5720():
    """ 安装 mysql5.7.20 """
    # 
    # 更新配置文件
    run('cd %s && git pull' % repo_folder)
    # 下载 mysql 源安装包
    run('curl -LO http://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm')
    # 安装 mysql 源
    sudo('yum localinstall mysql57-community-release-el7-11.noarch.rpm')
    # 检查 yum 源是否安装成功
    # sudo("""yum repolist enabled | grep "mysql.*-community.*"""")

    # 安装
    sudo('yum install mysql-community-server')
    # 复制配置文件
    sudo('cp -rf /home/bpzj/linux.conf/mysql/my.cnf /etc/my.cnf')
    # 安装服务
    sudo('systemctl enable mysqld')
    # 启动服务
    sudo('systemctl start mysqld')
    # 重新启动
    sudo('systemctl restart mysqld')


def insvsftpd():
    """ 安装 vsftpd """
    # 更新配置文件
    run('cd %s && git pull' % repo_folder)
    # 安装
    sudo('yum install -y vsftpd')
    # 复制、更新配置文件
    sudo('cp -rf /home/bpzj/linux.conf/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf')
    sudo('cp -rf /home/bpzj/linux.conf/vsftpd/vsftpd.chroot_list /etc/vsftpd/vsftpd.chroot_list')
    # 重启服务
    sudo('service vsftpd restart')
    # 新建ftp文件夹
    sudo('mkdir /home/bpzj/ftp')
    # 新建这个文件夹
    sudo('mkdir /var/run/vsftpd')
    sudo('mkdir /var/run/vsftpd/empty')


def instomcat():
    """安装Tomcat 8.0 """
    # 更新配置文件
    run('cd %s && git pull' % repo_folder)
    # 下载 tomcat
    sudo('wget http://mirrors.shu.edu.cn/apache/tomcat/tomcat-8/v8.0.49/bin/apache-tomcat-8.0.49.tar.gz')
    # 删除原有的tomcat
    sudo('rm -rf /usr/local/tomcat')
    # 解压
    sudo('tar -xvzf apache-tomcat-8.0.49.tar.gz')
    # 注意这个mv命令，直接重名了，要保证local文件下没有tomcat才能重命名
    # 所以上面删除了原有的 tomcat 文件夹
    sudo('mv /home/bpzj/apache-tomcat-8.0.49 /usr/local/tomcat')
    # 复制配置文件：profile、setenv.sh、catalina.sh、tomcat.service
    sudo('cp -rf /home/bpzj/linux.conf/profile /etc/profile')
    sudo('cp -rf /home/bpzj/linux.conf/tomcat/8.0.48-catalina/catalina.sh /usr/local/tomcat/bin/catalina.sh')
    # 配置环境变量，这一句执行不成功，暂时未解决
    run('source /etc/profile', pty=False)
    # 更新 catalina.sh 配置文件
    sudo('/usr/local/tomcat/bin/startup.sh', pty=False)
    # 备用命令
    # sudo /usr/local/tomcat/bin/shutdown.sh


def insresin():
    # 下载 resin
    sudo('wget http://caucho.com/download/resin-4.0.55.tar.gz')
    # 删除原有的resin
    sudo('rm -rf /usr/local/resin')
    # 注意这个mv命令，直接重名了，要保证local文件下没有resin才能重命名
    # 所以上面删除了原有的 resin 文件夹
    sudo('mv ./resin-4.0.55 /usr/local/resin')
    sudo('rm -rf ./*resin*.gz')
    sudo('cd /usr/local/resin && ./resin.sh start')
