#!/bin/bash

echo "🎁 启动二维码兑换码系统..."
echo ""

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖包..."
if ! python -c "import flask, qrcode, pandas, PIL" 2>/dev/null; then
    echo "📥 安装依赖包..."
    pip install -r requirements.txt
fi

echo ""
echo "🚀 启动服务器..."
echo "📍 访问地址: http://localhost:5001"
echo "🔧 管理后台: http://localhost:5001/admin"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动应用
python app.py 