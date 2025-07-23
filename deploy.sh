#!/bin/bash

echo "🚀 二维码兑换码系统部署脚本"
echo "================================"
echo ""

# 检查Python应用是否运行
check_app_running() {
    if curl -s http://localhost:5001 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 启动应用
start_app() {
    echo "📦 启动Flask应用..."
    if ! check_app_running; then
        python app.py &
        sleep 3
        if check_app_running; then
            echo "✅ Flask应用已启动在 http://localhost:5001"
        else
            echo "❌ Flask应用启动失败"
            exit 1
        fi
    else
        echo "✅ Flask应用已在运行"
    fi
}

# 方案1: ngrok部署
deploy_ngrok() {
    echo ""
    echo "🌐 方案1: 使用ngrok部署到公网"
    echo "--------------------------------"
    
    if ! command -v ngrok &> /dev/null; then
        echo "❌ ngrok未安装，请先安装ngrok"
        echo "   安装命令: brew install ngrok/ngrok/ngrok"
        return 1
    fi
    
    start_app
    
    echo ""
    echo "🔗 启动ngrok隧道..."
    echo "📱 其他人可以通过以下链接访问:"
    echo ""
    echo "💡 注意: ngrok需要注册账号并配置authtoken"
    echo "   1. 访问 https://dashboard.ngrok.com/signup 注册账号"
    echo "   2. 获取authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "   3. 配置authtoken: ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "配置完成后重新运行此脚本"
    echo ""
    
    # 启动ngrok
    ngrok http 5001
}

# 方案2: 本地网络部署
deploy_local_network() {
    echo ""
    echo "🏠 方案2: 本地网络部署"
    echo "----------------------"
    
    start_app
    
    # 获取本机IP
    local_ip=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
    
    echo ""
    echo "📱 其他人可以通过以下地址访问:"
    echo "   主页: http://$local_ip:5001"
    echo "   管理后台: http://$local_ip:5001/admin"
    echo ""
    echo "💡 确保其他设备与你在同一网络下"
    echo ""
    
    # 保持应用运行
    wait
}

# 方案3: 云服务器部署指南
show_cloud_deploy_guide() {
    echo ""
    echo "☁️ 方案3: 云服务器部署指南"
    echo "--------------------------"
    echo ""
    echo "推荐使用以下云服务:"
    echo "1. 阿里云 ECS"
    echo "2. 腾讯云 CVM"
    echo "3. 华为云 ECS"
    echo "4. 国外: AWS EC2, Google Cloud, DigitalOcean"
    echo ""
    echo "部署步骤:"
    echo "1. 购买云服务器（建议1核2G以上）"
    echo "2. 安装Python和依赖:"
    echo "   sudo apt update"
    echo "   sudo apt install python3 python3-pip"
    echo "   pip3 install -r requirements.txt"
    echo ""
    echo "3. 修改app.py中的端口配置:"
    echo "   app.run(debug=False, host='0.0.0.0', port=80)"
    echo ""
    echo "4. 启动应用:"
    echo "   python3 app.py"
    echo ""
    echo "5. 配置防火墙开放80端口"
    echo ""
    echo "6. 通过公网IP访问:"
    echo "   http://你的服务器IP"
    echo ""
}

# 方案4: Docker部署
show_docker_deploy() {
    echo ""
    echo "🐳 方案4: Docker部署"
    echo "-------------------"
    echo ""
    echo "创建Dockerfile:"
    cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
EOF

    echo "✅ 已创建Dockerfile"
    echo ""
    echo "构建和运行Docker容器:"
    echo "docker build -t qrcode-system ."
    echo "docker run -p 5001:5001 qrcode-system"
    echo ""
    echo "部署到云服务器:"
    echo "1. 上传代码到服务器"
    echo "2. 构建Docker镜像"
    echo "3. 运行容器"
    echo "4. 配置反向代理（可选）"
    echo ""
}

# 主菜单
show_menu() {
    echo "请选择部署方案:"
    echo "1) 🌐 ngrok公网部署（推荐测试用）"
    echo "2) 🏠 本地网络部署"
    echo "3) ☁️ 云服务器部署指南"
    echo "4) 🐳 Docker部署指南"
    echo "5) ❌ 退出"
    echo ""
    read -p "请输入选择 (1-5): " choice
    
    case $choice in
        1)
            deploy_ngrok
            ;;
        2)
            deploy_local_network
            ;;
        3)
            show_cloud_deploy_guide
            ;;
        4)
            show_docker_deploy
            ;;
        5)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选择，请重新输入"
            show_menu
            ;;
    esac
}

# 检查依赖
echo "🔍 检查系统依赖..."
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python"
    exit 1
fi

if ! python -c "import flask, qrcode, pandas, PIL" 2>/dev/null; then
    echo "📥 安装Python依赖..."
    pip install -r requirements.txt
fi

echo "✅ 依赖检查完成"
echo ""

# 显示菜单
show_menu 