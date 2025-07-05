## 环境准备

### 系统要求
- 操作系统：Linux、macOS、Windows
- 网络：稳定的互联网连接
- 权限：管理员权限（用于安装命令行工具）

### 前置条件
- 已注册 easylearning.vip 账户
- 已购买相应的实例配额
- 本地已安装 SSH 客户端，Vscode 客户端

## 安装命令行工具
### 终端操作命令
```bash
# Linux
sudo curl https://get-ez.easylearning.vip/latest/linux-ez --output /usr/bin/ez
sudo chmod +x /usr/bin/ez

# Darwin
sudo curl https://get-ez.easylearning.vip/latest/darwin-ez --output /usr/bin/ez
sudo chmod +x /usr/bin/ez

# Windows
$url = "https://get-ez.easylearning.vip/latest/windows-ez.exe"
$output = "ez.exe"
Invoke-WebRequest -Uri $url -OutFile $output
```

### 终端登陆验证
```bash
# ez user login 登录，用户名密码与平台相同
ez user login -u elm

# 验证登录状态
ez user info
```

### 命令行创建实例
使用 ez 命令行工具创建实例，推荐8核24G
```bash
# 1. ez 查看可使用的实例规格
ez dg types
#== List of instance types ==
#ID	Name  	CPU	Memory
#6 	S4C8G 	4C 	8G
#7 	S4C4G 	4C 	4G
#8 	S2C4G 	2C 	4G
#9 	S1C2G 	1C 	2G
#10	S8C24G	8C 	24G

# 2. ez 查看可使用的系统镜像
ez dg images
#== List of images ==
#Code	Name
#3000	ubuntu-20.04
#3001	ubuntu-22.04
#3003	ubuntu-24.10
#3100	ubuntu20-k3d
#3101	ubuntu20-k3d-ckad

# 3. ez 查看可使用的区域
ez dg regions
#== List of regions ==
#Code	Name
#gz  	广州
#hk  	香港

# 4. ez 创建 dg实例，-m 镜像Code，-r 区域Code，-t 实例规格ID，-n 备注
ez dg create -m 3001 -r gz -t 10 -n llm_dev_learning
#Success, Devground instance has been created

# 5. ez 查看创建的 dg实例, dg实例ID 463
ez dg ls
#== My Devgrounds ==
#id 	Name          	Note 	Size  	Image       	IP           	State
#463	hk1-133-20-104	llm_dev_learning	S4C8G 	ubuntu-22.04	10.133.20.104	running
```

## 配置远程连接
### SSH 密钥配置
```bash
# ez 自动配置ssh key和ssh config
ez dg keygen -i 463

# 测试SSH连接
ssh dg-463
# 退出dg-463
exit

# 查看添加的SSH配置
cat ~/.ssh/config | grep -A 5 "dg-463"
```

### VSCode Remote-SSH 配置

#### 配置步骤
1. 安装 VSCode Remote-SSH 扩展
2. 按 `Ctrl+Shift+P` 打开命令面板
3. 输入 "Remote-SSH: Connect to Host"
4. 选择 `dg-463` 连接
5. 等待连接建立完成

#### 连接验证
```bash
# 在VSCode终端中验证连接
whoami
hostname
ip addr show
```

## Github配置
dg 实例上配置，可选择在本地终端连接 dg实例配置，或者Vscode 远程上实例配置

### 创建Github专用密钥

```bash
ssh-keygen -t ed25519 -C "liangyu6262@outlook.com" -f ~/.ssh/github

sudo tee >> ~/.ssh/config << EOF
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github
    IdentitiesOnly yes
EOF

cat ~/.ssh/github.pub
```

#### 配置步骤
1. 登录 Github 账户
2. 进入 Settings > SSH and GPG keys
3. 点击 "New SSH key"
4. 粘贴公钥内容
5. 添加描述性标题
6. 点击 "Add SSH key"

#### 验证配置
```bash
# 测试Github SSH连接
ssh -T git@github.com

# 应该看到类似输出：
# Hi username! You've successfully authenticated, but GitHub does not provide shell access.

# 克隆仓库测试，这里选择配置自己github仓库
git clone git@github.com:ElmLeung/llm_dev_learning.git
```

## 公网访问配置

### 创建公网访问端口
具体配置需根据项目需求调整，这里开发的应用选择使用内网端口3380暴露服务。
```bash
# 创建公网端口访问,--ip 10.133.20.102 为内网地址，-p80 为内网端口
ez ing create --ip 10.133.20.104 -p3380

# 查看公网地址和端口信息
ez ing ls
#== List view of Ingress ==
#id 	IP           	Port	Private IP   	Private Port	CreatedAt          	TTL	Time Used
#217	8.138.156.231	5008	10.133.20.100	3380          	2025-05-22 16:45:09	0
```
