#!/bin/bash

echo "========================================="
echo "Chatbot Quản lý Thời gian"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Kích hoạt virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Cài đặt dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================="
echo "🚀 Khởi động server..."
echo "========================================="
echo ""
echo "Truy cập ứng dụng tại: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Nhấn Ctrl+C để dừng server"
echo ""

# Run the application
python main.py
