from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
import pandas as pd
import qrcode
import os
import uuid
from datetime import datetime
import threading
import time

app = Flask(__name__)

# 全局变量
CSV_FILE = 'codes.csv'
USED_CODES_FILE = 'used_codes.txt'
LOCK = threading.Lock()

def init_csv():
    """初始化CSV文件，如果不存在则创建"""
    if not os.path.exists(CSV_FILE):
        # 创建示例兑换码
        sample_codes = [
            'CODE001',
            'CODE002', 
            'CODE003',
            'CODE004',
            'CODE005',
            'CODE006',
            'CODE007',
            'CODE008',
            'CODE009',
            'CODE010'
        ]
        df = pd.DataFrame({
            'code': sample_codes,
            'status': ['未领取'] * len(sample_codes),
            'claimed_time': [''] * len(sample_codes),
            'claimed_by': [''] * len(sample_codes)
        })
        df.to_csv(CSV_FILE, index=False, encoding='utf-8')
        print(f"已创建示例CSV文件: {CSV_FILE}")

def get_available_code():
    """获取一个可用的兑换码"""
    with LOCK:
        try:
            df = pd.read_csv(CSV_FILE, encoding='utf-8')
            available = df[df['status'] == '未领取']
            
            if available.empty:
                return None
            
            # 获取第一个未领取的码
            code_row = available.iloc[0]
            code = code_row['code']
            
            # 更新状态
            df.loc[df['code'] == code, 'status'] = '已领取'
            df.loc[df['code'] == code, 'claimed_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.loc[df['code'] == code, 'claimed_by'] = str(uuid.uuid4())[:8]  # 生成唯一标识
            
            df.to_csv(CSV_FILE, index=False, encoding='utf-8')
            return code
            
        except Exception as e:
            print(f"获取兑换码时出错: {e}")
            return None

def check_all_codes_claimed():
    """检查是否所有兑换码都被领取了"""
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        return df['status'].eq('已领取').all()
    except Exception as e:
        print(f"检查兑换码状态时出错: {e}")
        return False

def generate_qr_code():
    """生成二维码"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # 生成访问链接
    base_url = request.host_url.rstrip('/')
    qr_url = f"{base_url}/claim"
    
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = 'static/qr_code.png'
    os.makedirs('static', exist_ok=True)
    img.save(qr_path)
    return qr_path

@app.route('/')
def index():
    """主页 - 显示二维码"""
    qr_path = generate_qr_code()
    return render_template('index.html', qr_path=qr_path)

@app.route('/claim')
def claim():
    """兑换码领取页面"""
    return render_template('claim.html')

@app.route('/api/claim', methods=['POST'])
def api_claim():
    """API接口：领取兑换码"""
    try:
        # 检查是否还有可用的兑换码
        if check_all_codes_claimed():
            return jsonify({
                'success': False,
                'message': '手慢了，兑换码已经被领取完了！',
                'code': None
            })
        
        # 获取一个可用的兑换码
        code = get_available_code()
        
        if code:
            return jsonify({
                'success': True,
                'message': '恭喜！您成功领取了兑换码',
                'code': code
            })
        else:
            return jsonify({
                'success': False,
                'message': '暂时无法获取兑换码，请稍后再试',
                'code': None
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'系统错误: {str(e)}',
            'code': None
        })

@app.route('/admin')
def admin():
    """管理员页面 - 查看兑换码状态"""
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        total_codes = len(df)
        claimed_codes = len(df[df['status'] == '已领取'])
        available_codes = total_codes - claimed_codes
        
        return render_template('admin.html', 
                             codes=df.to_dict('records'),
                             total=total_codes,
                             claimed=claimed_codes,
                             available=available_codes)
    except Exception as e:
        return f"读取数据时出错: {e}"

@app.route('/admin/reset', methods=['POST'])
def reset_codes():
    """重置所有兑换码状态"""
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        df['status'] = '未领取'
        df['claimed_time'] = ''
        df['claimed_by'] = ''
        df.to_csv(CSV_FILE, index=False, encoding='utf-8')
        return jsonify({'success': True, 'message': '所有兑换码已重置'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'重置失败: {str(e)}'})

@app.route('/admin/upload', methods=['POST'])
def upload_csv():
    """上传新的CSV文件"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        if file and file.filename.endswith('.csv'):
            # 保存上传的文件
            file.save(CSV_FILE)
            return jsonify({'success': True, 'message': 'CSV文件上传成功'})
        else:
            return jsonify({'success': False, 'message': '请上传CSV格式的文件'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})

@app.route('/codes.csv')
def download_csv():
    """下载CSV文件"""
    try:
        return send_file(CSV_FILE, as_attachment=True, download_name='codes.csv')
    except Exception as e:
        return f"下载失败: {str(e)}", 404

if __name__ == '__main__':
    # 初始化CSV文件
    init_csv()
    
    # 创建static目录
    os.makedirs('static', exist_ok=True)
    
    print("启动兑换码系统（生产环境）...")
    print("访问 http://localhost:80 查看二维码")
    print("访问 http://localhost:80/admin 管理兑换码")
    
    # 生产环境配置
    app.run(debug=False, host='0.0.0.0', port=80) 