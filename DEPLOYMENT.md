# 部署指南

## 🚀 快速部署方案

### 方案1: 本地网络部署（推荐新手）

这是最简单的部署方式，适合在局域网内使用：

```bash
# 运行部署脚本
./deploy.sh
# 选择方案2: 本地网络部署
```

**优点：**
- 无需注册账号
- 无需配置复杂设置
- 适合家庭、办公室等局域网环境

**缺点：**
- 只能在局域网内访问
- 需要其他设备与你在同一网络

### 方案2: ngrok公网部署（推荐测试）

适合临时测试，可以让任何人通过互联网访问：

```bash
# 1. 注册ngrok账号
# 访问: https://dashboard.ngrok.com/signup

# 2. 获取authtoken
# 访问: https://dashboard.ngrok.com/get-started/your-authtoken

# 3. 配置authtoken
ngrok config add-authtoken YOUR_TOKEN

# 4. 运行部署脚本
./deploy.sh
# 选择方案1: ngrok公网部署
```

**优点：**
- 可以公网访问
- 配置简单
- 适合临时测试

**缺点：**
- 需要注册账号
- 免费版有连接数限制
- 链接会定期变化

### 方案3: 云服务器部署（推荐生产）

适合正式使用，稳定可靠：

#### 3.1 阿里云/腾讯云部署

1. **购买云服务器**
   - 配置：1核2G以上
   - 系统：Ubuntu 20.04/22.04
   - 带宽：1Mbps以上

2. **连接服务器**
   ```bash
   ssh root@你的服务器IP
   ```

3. **上传代码**
   ```bash
   # 方法1: 使用scp
   scp -r ./qrcode root@你的服务器IP:/root/
   
   # 方法2: 使用git
   git clone 你的代码仓库
   ```

4. **安装依赖**
   ```bash
   cd qrcode
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```

5. **运行应用**
   ```bash
   python3 app_production.py
   ```

6. **配置防火墙**
   ```bash
   sudo ufw allow 80
   sudo ufw enable
   ```

7. **访问系统**
   - 主页: http://你的服务器IP
   - 管理后台: http://你的服务器IP/admin

#### 3.2 Docker部署（推荐）

1. **安装Docker**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   ```

2. **构建并运行**
   ```bash
   cd qrcode
   docker-compose up -d
   ```

3. **访问系统**
   - 主页: http://你的服务器IP
   - 管理后台: http://你的服务器IP/admin

### 方案4: 免费云平台部署

#### 4.1 Railway部署

1. 注册Railway账号: https://railway.app
2. 连接GitHub仓库
3. 自动部署

#### 4.2 Render部署

1. 注册Render账号: https://render.com
2. 连接GitHub仓库
3. 选择Web Service
4. 自动部署

#### 4.3 Heroku部署

1. 注册Heroku账号: https://heroku.com
2. 安装Heroku CLI
3. 部署应用

## 🔧 配置说明

### 端口配置

- **开发环境**: 5001端口
- **生产环境**: 80端口（HTTP）或443端口（HTTPS）

### 环境变量

```bash
# 生产环境
export FLASK_ENV=production
export FLASK_APP=app_production.py

# 自定义端口
export PORT=8080
```

### 数据库配置

当前使用CSV文件存储数据，如需使用数据库：

1. 安装数据库（MySQL/PostgreSQL）
2. 修改app.py中的数据库连接
3. 创建数据表结构

## 📱 移动端访问

### 二维码生成

系统会自动生成包含当前访问地址的二维码，支持：

- 手机扫码直接访问
- 微信、支付宝等APP扫码
- 浏览器扫码

### 响应式设计

- 自动适配手机屏幕
- 触摸友好的按钮设计
- 优化的移动端体验

## 🔒 安全配置

### 生产环境安全

1. **关闭调试模式**
   ```python
   app.run(debug=False, host='0.0.0.0', port=80)
   ```

2. **配置防火墙**
   ```bash
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw deny 22  # 关闭SSH（可选）
   ```

3. **使用HTTPS**
   ```bash
   # 安装SSL证书
   sudo apt install certbot
   sudo certbot --nginx
   ```

4. **设置访问密码**
   - 修改admin路由添加认证
   - 使用环境变量存储密码

### 数据备份

```bash
# 备份CSV文件
cp codes.csv codes_backup_$(date +%Y%m%d).csv

# 自动备份脚本
#!/bin/bash
cp codes.csv /backup/codes_$(date +%Y%m%d_%H%M%S).csv
find /backup -name "codes_*.csv" -mtime +7 -delete
```

## 🚨 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   lsof -i :5001
   
   # 杀死进程
   kill -9 PID
   ```

2. **权限问题**
   ```bash
   # 修改文件权限
   chmod +x *.sh
   chmod 644 *.py
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

4. **防火墙问题**
   ```bash
   # 检查防火墙状态
   sudo ufw status
   
   # 开放端口
   sudo ufw allow 5001
   ```

### 日志查看

```bash
# 查看应用日志
tail -f app.log

# 查看系统日志
journalctl -u qrcode-system -f

# 查看Docker日志
docker logs qrcode-system
```

## 📞 技术支持

如果遇到问题，请检查：

1. 系统依赖是否完整
2. 端口是否被占用
3. 防火墙配置是否正确
4. 网络连接是否正常

更多帮助请查看README.md文件。 