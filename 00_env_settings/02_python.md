# 学习环境的python 配置

## 安装前置系统依赖
```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
```

## 安装pyenv
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

source ~/.bashrc
pyenv --version
```

## 安装学习使用的python 版本
```bash
mkdir /home/ubuntu/.pyenv/cache

curl https://mirrors.aliyun.com/python-release/source/Python-3.11.9.tar.xz --output ~/.pyenv/cache/Python-3.11.9.tar.xz

pyenv install 3.11.9
```

## pyenv常用命令
```bash
pyenv version
pyenv versions

# 进入相应的学习目录，执行下面的命令可以设置学习使用指定版本的python
pyenv local 3.11.9
```



