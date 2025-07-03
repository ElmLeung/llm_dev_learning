# llm_dev_learning
llm应用展示

## 开发环境
### easylearning.vip 8核16G
easylearning.vip 可购买学习实验用途的实例，使用ez 命令行工具进行管理

### 安装命令行工具

#### Linux
sudo curl https://get-ez.easylearning.vip/latest/linux-ez --output /usr/bin/ez
sudo chmod +x /usr/bin/ez

#### Darwin
sudo curl https://get-ez.easylearning.vip/latest/darwin-ez --output /usr/bin/ez
sudo chmod +x /usr/bin/ez

#### Windows
$url = "https://get-ez.easylearning.vip/latest/windows-ez.exe"
$output = "ez.exe"
Invoke-WebRequest -Uri $url -OutFile $output

### ez 命令使用
```bash
# 用户名密码与平台相同
ez user login -u elm

# 列出可创建的实例规格，可创建总量无法超过可使用量
ez dg types
#== List of instance types ==
#ID	Name  	CPU	Memory
#6 	S4C8G 	4C 	8G    
#7 	S4C4G 	4C 	4G    
#8 	S2C4G 	2C 	4G    
#9 	S1C2G 	1C 	2G    
#10	S8C24G	8C 	24G  

# 列出可以使用的系统镜像
ez dg images
#== List of images ==
#Code	Name             
#3000	ubuntu-20.04     
#3001	ubuntu-22.04     
#3003	ubuntu-24.10     
#3100	ubuntu20-k3d     
#3101	ubuntu20-k3d-ckad

# 列出可用区
ez dg regions
#== List of regions ==
#Code	Name
#gz  	广州
#hk  	香港

# 创建香港入口的开发实例，虽为香港但无法作为代理使用
# 使用ubuntu-22.04，区域香港，类型为4核8G
ez dg create -m 3001 --region hk -t 6 -n dify

# 查看已创建开发实例
ez dg list
#== My Devgrounds ==
#id 	Name          	Note                 	Size  	Image       	IP           	State  
#377	hk1-133-20-100	                     	S4C8G 	ubuntu-22.04	10.133.20.100	running
#403	hk1-133-20-104	fastgpt              	S4C8G 	ubuntu-22.04	10.133.20.104	running
#404	hk1-133-20-106	mcp-feedback-enhanced	S4C8G 	ubuntu-22.04	10.133.20.106	running
#405	hk1-133-20-102	dify                 	S4C8G 	ubuntu-22.04	10.133.20.102	running

# 创建vscode Remote-SSH 远程连接
ez dg keygen -i 405
# 打开vscode 远程连接可以看到dg-405 选项，点击即可远程

# 创建公网访问,--ip 10.133.20.102 为dify内网地址，-p80 为dify内网端口
ez ing create --ip 10.133.20.102 -p80

# 查看公网信息
ez ing ls
#== List view of Ingress ==
#id 	IP           	Port	Private IP   	Private Port	CreatedAt          	TTL	Time Used
#217	8.138.156.231	5008	10.133.20.100	80          	2025-05-22 16:45:09	0  

# 部署好dify后，浏览器访问即可
http://8.138.156.231:5008
```