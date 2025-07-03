# Devground工作实例创建完整教程

## 📖 使用说明

本教程包含详细的文字说明和配套的视频演示，帮助您快速掌握Devground工作实例的创建和管理。

### 🎥 视频说明
- 所有视频均为WebM格式，支持现代浏览器直接播放
- 如果视频无法播放，请点击链接直接下载查看
- 建议配合文字说明一起学习，效果更佳

## 目录
1. [环境准备](#环境准备)
2. [安装命令行工具](#安装命令行工具)
3. [创建开发实例](#创建开发实例)
4. [配置远程连接](#配置远程连接)
5. [Github配置](#github配置)
6. [公网访问配置](#公网访问配置)
7. [实例管理](#实例管理)
8. [故障排除](#故障排除)
9. [最佳实践](#最佳实践)

## 环境准备

### 系统要求
- 操作系统：Linux、macOS、Windows
- 网络：稳定的互联网连接
- 权限：管理员权限（用于安装命令行工具）

### 前置条件
- 已注册 easylearning.vip 账户
- 已购买相应的实例配额
- 本地已安装 SSH 客户端

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

### 验证安装
```bash
# 检查工具是否安装成功
ez --version

# 如果出现版本信息，说明安装成功
```

### 终端登陆验证
```bash
# ez user login 登录，用户名密码与平台相同
ez user login -u elm

# 验证登录状态
ez user info

# 查看账户配额信息
ez user quota
```

### Ubuntu 终端示范

**📹 视频演示：Ubuntu系统下安装ez命令行工具**

<video width="100%" controls>
  <source src="../captures/ubuntu_ez_install.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/ubuntu_ez_install.webm">ubuntu_ez_install.webm</a>
</video>

> 💡 **视频内容说明**：演示在Ubuntu系统中下载、安装ez命令行工具，并进行基本的登录验证操作。

### 常见安装问题
- **权限不足**：确保使用 sudo 权限执行安装命令
- **网络问题**：检查网络连接，可能需要配置代理
- **路径问题**：确保 /usr/bin 在系统 PATH 中


## 创建开发实例

### 方式一：Web 端创建实例
通过 easylearning.vip 网站用户中心创建 dg 实例，适合初学者使用。

**📹 视频演示：Web端创建Devground实例**

<video width="100%" controls>
  <source src="../captures/web_dg_create.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/web_dg_create.webm">web_dg_create.webm</a>
</video>

> 💡 **视频内容说明**：展示如何通过easylearning.vip网站界面创建新的Devground实例，包括选择配置、区域等步骤。

### 方式二：命令行创建实例
使用 ez 命令行工具创建实例，适合熟练用户和自动化场景。
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
ez dg create -m 3001 -r hk -t 6 -n nginx
#Success, Devground instance has been created

# 5. ez 查看创建的 dg实例, dg实例ID 463 
ez dg ls
#== My Devgrounds ==
#id 	Name          	Note 	Size  	Image       	IP           	State  
#377	hk1-133-20-100	     	S4C8G 	ubuntu-22.04	10.133.20.100	running
#408	hk1-133-20-101	zhihu	S8C24G	ubuntu-22.04	10.133.20.101	running
#462	hk1-133-20-102	dev  	S4C8G 	ubuntu-22.04	10.133.20.102	running
#463	hk1-133-20-104	nginx	S4C8G 	ubuntu-22.04	10.133.20.104	running

```

**📹 视频演示：命令行创建Devground实例**

<video width="100%" controls>
  <source src="../captures/ez_dg_create.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/ez_dg_create.webm">ez_dg_create.webm</a>
</video>

> 💡 **视频内容说明**：演示使用ez命令行工具创建Devground实例的完整过程，包括查看可用配置、创建实例、查看实例列表等操作。

### 实例创建最佳实践
- **选择合适的规格**：根据项目需求选择CPU和内存配置
- **选择合适的镜像**：
  - `ubuntu-22.04`：通用开发环境
  - `ubuntu20-k3d`：Kubernetes开发环境
  - `ubuntu20-k3d-ckad`：CKAD认证学习环境
- **选择合适的区域**：
  - `hk`：香港区域，网络延迟较低
  - `gz`：广州区域，国内访问速度快
- **合理命名**：使用有意义的备注名称，便于管理

## 配置远程连接
### SSH 密钥配置

**📹 视频演示：配置SSH密钥和连接**

<video width="100%" controls>
  <source src="../captures/ez_dg_keygen.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/ez_dg_keygen.webm">ez_dg_keygen.webm</a>
</video>

> 💡 **视频内容说明**：展示如何使用ez工具自动生成SSH密钥并配置SSH连接，包括测试连接是否成功。
```bash
# ez 自动配置ssh key和ssh config
ez dg keygen -i 463

# 测试SSH连接
ssh dg-463

# 查看生成的SSH配置
cat ~/.ssh/config | grep -A 5 "dg-463"
```

### VSCode Remote-SSH 配置

**📹 视频演示：VSCode远程SSH连接配置**

<video width="100%" controls>
  <source src="../captures/vscode_dg_remote_ssh.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/vscode_dg_remote_ssh.webm">vscode_dg_remote_ssh.webm</a>
</video>

> 💡 **视频内容说明**：演示如何在VSCode中配置和使用Remote-SSH扩展连接到Devground实例，包括连接过程和验证步骤。

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

### 创建Github专用密钥

**📹 视频演示：创建Github SSH密钥**

<video width="100%" controls>
  <source src="../captures/dg_github_keygen.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/dg_github_keygen.webm">dg_github_keygen.webm</a>
</video>

> 💡 **视频内容说明**：展示如何在Devground实例中生成Github专用的SSH密钥，包括密钥生成和SSH配置文件设置。
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

# 测试Github连接
ssh -T git@github.com
```

### Github SSH密钥配置
```bash
# 复制公钥内容
cat ~/.ssh/github.pub
```

**📹 视频演示：Github SSH密钥配置**

<video width="100%" controls>
  <source src="../captures/github_sshkey_setting.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/github_sshkey_setting.webm">github_sshkey_setting.webm</a>
</video>

> 💡 **视频内容说明**：演示如何在Github网站上添加SSH公钥，包括导航到设置页面、添加新密钥、验证配置等步骤。

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

# 克隆仓库测试
git clone git@github.com:username/repository.git
```


## 公网访问配置

### 创建公网访问端口
以nginx为例，演示如何配置公网访问。具体配置需根据项目需求调整。

**📹 视频演示：创建公网访问端口**

<video width="100%" controls>
  <source src="../captures/ez_ingress_create.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/ez_ingress_create.webm">ez_ingress_create.webm</a>
</video>

> 💡 **视频内容说明**：展示如何使用ez命令创建公网访问端口映射，包括端口创建和查看映射信息的操作。
```bash
# 创建公网端口访问,--ip 10.133.20.102 为内网地址，-p80 为内网端口
ez ing create --ip 10.133.20.104 -p80

# 查看公网地址和端口信息
ez ing ls
#== List view of Ingress ==
#id 	IP           	Port	Private IP   	Private Port	CreatedAt          	TTL	Time Used
#217	8.138.156.231	5008	10.133.20.100	80          	2025-05-22 16:45:09	0
```

### 部署应用服务

**📹 视频演示：安装和配置Nginx服务**

<video width="100%" controls>
  <source src="../captures/dg_nginx_install.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/dg_nginx_install.webm">dg_nginx_install.webm</a>
</video>

> 💡 **视频内容说明**：演示在Devground实例中安装Nginx服务器，包括安装、启动服务和本地测试访问的完整过程。
```bash
# 安装nginx
sudo apt update
sudo apt install nginx -y

# 启动nginx服务
sudo systemctl start nginx
sudo systemctl enable nginx

# 检查服务状态
sudo systemctl status nginx

# 测试本地访问
curl localhost:80
curl 0.0.0.0:80
```

### 访问公网服务

**📹 视频演示：通过公网访问Nginx服务**

<video width="100%" controls>
  <source src="../captures/dg_nginx_access.webm" type="video/webm">
  您的浏览器不支持视频播放。请直接查看文件：<a href="../captures/dg_nginx_access.webm">dg_nginx_access.webm</a>
</video>

> 💡 **视频内容说明**：展示如何通过公网地址和端口访问部署在Devground实例上的Nginx服务，验证端口映射配置是否正确。
```bash
# 通过公网地址访问
curl 8.138.156.231:5008

# 或在浏览器中访问
# http://8.138.156.231:5008
```

### 端口映射说明
- **内网地址**: 10.133.20.104:80 (nginx服务)
- **公网地址**: 8.138.156.231:5008 (外部访问)
- **映射关系**: 公网5008端口 → 内网80端口

## 实例管理

### 查看实例状态
```bash
# 查看所有实例
ez dg ls

# 查看特定实例详情
ez dg info -i 463
```

### 实例操作
```bash
# 启动实例
ez dg start -i 463

# 停止实例
ez dg stop -i 463

# 重启实例
ez dg restart -i 463

# 删除实例（谨慎操作）
ez dg delete -i 463
```

### 端口管理
```bash
# 查看所有端口映射
ez ing ls

# 删除端口映射
ez ing delete -i 217

# 修改端口映射（删除后重新创建）
ez ing delete -i 217
ez ing create --ip 10.133.20.104 -p 8080
```

## 故障排除

### 常见问题及解决方案

#### 1. SSH连接失败
```bash
# 检查SSH配置
cat ~/.ssh/config | grep -A 10 "dg-463"

# 重新生成SSH密钥
ez dg keygen -i 463

# 测试连接
ssh -v dg-463
```

#### 2. 端口访问失败
```bash
# 检查服务是否运行
sudo systemctl status nginx

# 检查端口监听
sudo netstat -tlnp | grep :80

# 检查防火墙设置
sudo ufw status

# 检查端口映射
ez ing ls
```

#### 3. Github连接问题
```bash
# 检查SSH密钥
ls -la ~/.ssh/

# 测试Github连接
ssh -T git@github.com

# 检查SSH配置
cat ~/.ssh/config | grep -A 5 "github.com"
```

#### 4. 实例创建失败
```bash
# 检查配额
ez user quota

# 检查可用资源
ez dg types
ez dg images
ez dg regions

# 重试创建
ez dg create -m 3001 -r hk -t 6 -n test
```

## 最佳实践

### 安全建议
1. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **配置防火墙**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 80/tcp
   ```

3. **使用强密码和密钥**
   - SSH密钥长度至少2048位
   - 定期轮换密钥
   - 不要共享私钥

### 性能优化
1. **选择合适的实例规格**
   - 开发环境：S2C4G 或 S4C4G
   - 生产环境：S4C8G 或 S8C24G

2. **优化网络配置**
   - 选择就近的区域
   - 使用CDN加速静态资源

3. **资源监控**
   ```bash
   # 监控系统资源
   htop
   df -h
   free -h
   ```

### 开发工作流
1. **代码管理**
   ```bash
   # 初始化Git仓库
   git init
   git remote add origin git@github.com:username/repo.git

   # 定期提交代码
   git add .
   git commit -m "feat: add new feature"
   git push origin main
   ```

2. **环境隔离**
   - 使用不同实例进行开发、测试、生产
   - 使用Docker容器隔离应用环境

3. **备份策略**
   - 定期备份重要数据
   - 使用Git管理代码版本
   - 导出数据库和配置文件

### 成本控制
1. **合理使用资源**
   - 不使用时及时停止实例
   - 选择合适的实例规格
   - 定期清理无用的端口映射

2. **监控使用情况**
   ```bash
   # 查看配额使用情况
   ez user quota

   # 查看实例运行时间
   ez dg ls
   ```

---

## 总结

本教程涵盖了Devground工作实例的完整创建和配置流程，包括：
- 命令行工具安装和配置
- 实例创建和管理
- 远程连接配置
- Github集成
- 公网访问设置
- 故障排除和最佳实践

通过遵循本教程，您可以快速搭建一个完整的云端开发环境，提高开发效率和协作能力。

## 📹 视频索引

为了方便查找，以下是本教程中所有视频的索引：

| 序号 | 视频名称 | 文件名 | 内容描述 |
|------|----------|--------|----------|
| 1 | Ubuntu系统安装ez工具 | `ubuntu_ez_install.webm` | 演示在Ubuntu系统中安装和配置ez命令行工具 |
| 2 | Web端创建实例 | `web_dg_create.webm` | 通过网站界面创建Devground实例 |
| 3 | 命令行创建实例 | `ez_dg_create.webm` | 使用ez命令行工具创建和管理实例 |
| 4 | SSH密钥配置 | `ez_dg_keygen.webm` | 自动生成SSH密钥并配置连接 |
| 5 | VSCode远程连接 | `vscode_dg_remote_ssh.webm` | 配置VSCode Remote-SSH扩展连接实例 |
| 6 | Github密钥生成 | `dg_github_keygen.webm` | 在实例中生成Github专用SSH密钥 |
| 7 | Github密钥配置 | `github_sshkey_setting.webm` | 在Github网站上添加SSH公钥 |
| 8 | 创建公网端口 | `ez_ingress_create.webm` | 创建公网访问端口映射 |
| 9 | 安装Nginx服务 | `dg_nginx_install.webm` | 在实例中安装和配置Nginx服务器 |
| 10 | 公网访问测试 | `dg_nginx_access.webm` | 通过公网地址访问部署的服务 |

### 🔗 快速访问链接
- [所有视频文件目录](../captures/)
- [项目主页](../README.md)
- [系统设计文档](../doc/SYSTEM.md)

---

如有问题，请参考故障排除章节或联系技术支持。
