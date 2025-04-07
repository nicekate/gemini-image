# Gemini 图像应用

这是一个基于Google Gemini API的图像处理Flask应用，提供多种图像相关功能。

## 功能

1. **图像问答** - 上传图片并提问关于图片内容的问题
2. **图像生成** - 使用Gemini或Imagen生成图像
3. **图像编辑** - 上传图片并进行编辑
4. **边界框检测** - 检测图像中的对象并显示边界框
5. **图像分割** - 对图像进行分割并显示分割结果

## 安装

1. 克隆仓库
```
git clone <repository-url>
cd <repository-directory>
```

2. 创建虚拟环境并激活
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖
```
pip install -r requirements.txt
```

4. 配置API密钥
   - 复制`.env.example`文件并重命名为`.env`
   ```
   cp .env.example .env
   ```
   - 在`.env`文件中设置你的Gemini API密钥
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   - 你也可以在应用运行后通过设置页面配置API密钥

## 运行应用

```
python app.py
```

然后在浏览器中访问 `http://127.0.0.1:5000/`

## 技术栈

- Flask - Web框架
- Google Generative AI (Gemini API) - AI模型
- Pillow - 图像处理
- Bootstrap - 前端样式

## 注意事项

- 需要有效的Google Gemini API密钥
- 图像生成功能中的Imagen模型仅在付费层级可用
- 图像分割功能需要使用Gemini 2.5 Pro实验版模型

## 隐私与安全

- API密钥存储在两个位置：`.env`文件和应用内部的`api_key.json`文件
- 这两个文件都已添加到`.gitignore`中，不会被提交到代码库
- 请勿在公共场合分享您的API密钥
- 应用中的设置页面提供了安全的API密钥管理功能

## 许可证

MIT
