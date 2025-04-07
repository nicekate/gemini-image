import os
import base64
import io
import json
import logging
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 加载环境变量
load_dotenv()

# 获取Gemini API密钥
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logging.error("Gemini API密钥未设置，请在.env文件中设置GEMINI_API_KEY")
else:
    logging.info("Gemini API密钥已设置")

# 创建一个文件来存储API密钥
API_KEY_FILE = 'api_key.json'

# 如果文件不存在，则创建并存储环境变量中的API密钥
if not os.path.exists(API_KEY_FILE):
    with open(API_KEY_FILE, 'w') as f:
        json.dump({'api_key': api_key}, f)

# 从文件中读取API密钥
def get_api_key():
    try:
        with open(API_KEY_FILE, 'r') as f:
            data = json.load(f)
            return data.get('api_key')
    except (FileNotFoundError, json.JSONDecodeError):
        return api_key

# 更新API密钥
def update_api_key(new_api_key):
    with open(API_KEY_FILE, 'w') as f:
        json.dump({'api_key': new_api_key}, f)
    global api_key
    api_key = new_api_key

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB

# 创建上传目录
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 创建生成图像目录
GENERATED_FOLDER = 'static/generated'
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# API密钥设置页面
@app.route('/settings')
def settings():
    current_api_key = get_api_key()
    # 完全隐藏密钥，只显示星号
    has_key = bool(current_api_key)
    masked_key = '*' * 20 if has_key else ''
    return render_template('settings.html', masked_key=masked_key, has_key=has_key)

# 更新API密钥
@app.route('/update_api_key', methods=['POST'])
def update_api_key_route():
    new_api_key = request.form.get('api_key')
    if not new_api_key:
        return jsonify({
            'status': 'error',
            'message': 'API密钥不能为空'
        })

    update_api_key(new_api_key)
    logging.info("API密钥已更新")

    return jsonify({
        'status': 'success',
        'message': 'API密钥已成功更新'
    })

# 删除API密钥
@app.route('/delete_api_key', methods=['POST'])
def delete_api_key():
    update_api_key('')
    logging.info("API密钥已删除")

    return jsonify({
        'status': 'success',
        'message': 'API密钥已成功删除'
    })

# API密钥测试
@app.route('/test_api')
def test_api():
    current_api_key = get_api_key()
    if not current_api_key:
        return jsonify({
            'status': 'error',
            'message': 'API密钥未设置',
            'error_type': 'missing'
        })

    try:
        client = genai.Client(api_key=current_api_key)
        logging.info("测试API密钥: 成功创建Gemini客户端")

        # 发送简单的文本请求来测试API密钥
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Hello, this is a test."
        )
        logging.info("测试API密钥: 成功收到响应")

        return jsonify({
            'status': 'success',
            'message': '您的API密钥有效并可以正常使用',
            'response': response.text
        })
    except genai.types.api_error.ApiError as api_err:
        error_msg = str(api_err)
        logging.error(f"测试API密钥错误: {error_msg}")
        return jsonify({
            'status': 'error',
            'message': f'API错误: {error_msg}',
            'error_type': '403' if '403' in error_msg else 'other'
        }), 400
    except Exception as e:
        logging.error(f"测试API密钥时发生未知错误: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'未知错误: {str(e)}'
        }), 500

# 图像问答
@app.route('/image_qa', methods=['GET', 'POST'])
def image_qa():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            return render_template('image_qa.html', error='没有选择图片')

        file = request.files['image']
        if file.filename == '':
            return render_template('image_qa.html', error='没有选择图片')

        # 保存上传的图片
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # 确保图片路径是相对于static目录的
        relative_image_path = image_path.replace('static/', '')
        logging.info(f"保存图片到: {image_path}, 相对路径: {relative_image_path}")

        # 获取问题
        question = request.form.get('question', '这张图片里有什么?')

        try:
            # 加载图片
            image = Image.open(image_path)
            logging.info(f"成功加载图片: {image_path}")

            # 获取API密钥
            current_api_key = get_api_key()
            if not current_api_key:
                return render_template('image_qa.html', error='API密钥未设置，请先设置API密钥')

            # 创建Gemini客户端
            client = genai.Client(api_key=current_api_key)
            logging.info("成功创建Gemini客户端")

            try:
                # 调用Gemini API进行图像问答
                logging.info(f"发送请求到Gemini API, 模型: gemini-2.0-flash, 问题: {question}")
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[question, image]
                )
                logging.info("成功收到Gemini API响应")

                return render_template('image_qa.html',
                                    image_path=relative_image_path,
                                    question=question,
                                    answer=response.text)
            except genai.types.api_error.ApiError as api_err:
                error_msg = str(api_err)
                logging.error(f"Gemini API错误: {error_msg}")
                if '403' in error_msg:
                    return render_template('image_qa.html',
                                        image_path=relative_image_path,
                                        question=question,
                                        error=f'API权限错误(403): 请检查您的API密钥是否有效或权限是否足够')
                else:
                    return render_template('image_qa.html',
                                        image_path=relative_image_path,
                                        question=question,
                                        error=f'Gemini API错误: {error_msg}')
        except Exception as e:
            logging.error(f"处理图片时出错: {str(e)}")
            return render_template('image_qa.html', error=f'处理图片时出错: {str(e)}')

    return render_template('image_qa.html')

# 图像生成
@app.route('/image_generation', methods=['GET', 'POST'])
def image_generation():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        model_type = request.form.get('model_type', 'gemini')

        if not prompt:
            return render_template('image_generation.html', error='请输入提示词')

        try:
            # 获取API密钥
            current_api_key = get_api_key()
            if not current_api_key:
                return render_template('image_generation.html', error='API密钥未设置，请先设置API密钥')

            client = genai.Client(api_key=current_api_key)

            if model_type == 'gemini':
                # 使用Gemini生成图像
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )

                # 保存生成的图像
                image_path = None
                description = None

                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        description = part.text
                    elif part.inline_data is not None:
                        # 保存图像
                        image = Image.open(io.BytesIO(part.inline_data.data))
                        image_filename = f"gemini_{base64.b64encode(prompt.encode()).decode()[:10]}.png"
                        image_path = os.path.join(app.config['GENERATED_FOLDER'], image_filename)
                        image.save(image_path)
                        image_path = image_path.replace('static/', '')

                return render_template('image_generation.html',
                                      prompt=prompt,
                                      image_path=image_path,
                                      description=description,
                                      model_type=model_type)
            else:
                # 使用Imagen生成图像
                response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                    )
                )

                # 保存生成的图像
                image = Image.open(io.BytesIO(response.generated_images[0].image.image_bytes))
                image_filename = f"imagen_{base64.b64encode(prompt.encode()).decode()[:10]}.png"
                image_path = os.path.join(app.config['GENERATED_FOLDER'], image_filename)
                image.save(image_path)
                image_path = image_path.replace('static/', '')

                return render_template('image_generation.html',
                                      prompt=prompt,
                                      image_path=image_path,
                                      model_type=model_type)

        except Exception as e:
            return render_template('image_generation.html', error=f'生成图像时出错: {str(e)}')

    return render_template('image_generation.html')

# 图像编辑
@app.route('/image_editing', methods=['GET', 'POST'])
def image_editing():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            return render_template('image_editing.html', error='没有选择图片')

        file = request.files['image']
        if file.filename == '':
            return render_template('image_editing.html', error='没有选择图片')

        # 保存上传的图片
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # 获取编辑指令
        edit_prompt = request.form.get('edit_prompt', '给这张图片添加一些效果')

        try:
            # 加载图片
            image = Image.open(image_path)

            # 获取API密钥
            current_api_key = get_api_key()
            if not current_api_key:
                return render_template('image_editing.html', error='API密钥未设置，请先设置API密钥')

            # 创建Gemini客户端
            client = genai.Client(api_key=current_api_key)

            # 调用Gemini API进行图像编辑
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=[edit_prompt, image],
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )

            # 保存编辑后的图像
            edited_image_path = None
            description = None

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    description = part.text
                elif part.inline_data is not None:
                    # 保存图像
                    edited_image = Image.open(io.BytesIO(part.inline_data.data))
                    edited_filename = f"edited_{os.path.basename(image_path)}"
                    edited_image_path = os.path.join(app.config['GENERATED_FOLDER'], edited_filename)
                    edited_image.save(edited_image_path)
                    edited_image_path = edited_image_path.replace('static/', '')

            return render_template('image_editing.html',
                                  original_image=image_path.replace('static/', ''),
                                  edited_image=edited_image_path,
                                  edit_prompt=edit_prompt,
                                  description=description)
        except Exception as e:
            return render_template('image_editing.html', error=f'编辑图片时出错: {str(e)}')

    return render_template('image_editing.html')

# 边界框检测
@app.route('/bounding_box', methods=['GET', 'POST'])
def bounding_box():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            return render_template('bounding_box.html', error='没有选择图片')

        file = request.files['image']
        if file.filename == '':
            return render_template('bounding_box.html', error='没有选择图片')

        # 保存上传的图片
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # 获取检测对象
        detect_object = request.form.get('detect_object', '检测图片中的所有对象')

        try:
            # 加载图片
            image = Image.open(image_path)
            width, height = image.size

            # 获取API密钥
            current_api_key = get_api_key()
            if not current_api_key:
                return render_template('bounding_box.html', error='API密钥未设置，请先设置API密钥')

            # 创建Gemini客户端
            client = genai.Client(api_key=current_api_key)

            # 构建提示词
            prompt = f"返回图片中{detect_object}的边界框坐标，格式为[ymin, xmin, ymax, xmax]。坐标值应该在0到1000之间。"

            # 调用Gemini API进行边界框检测
            response = client.models.generate_content(
                model="gemini-1.5-pro",
                contents=[image, prompt]
            )

            # 解析边界框坐标
            bbox_text = response.text.strip()

            # 尝试提取坐标
            import re
            coords = re.findall(r'\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]', bbox_text)

            if not coords:
                return render_template('bounding_box.html',
                                      image_path=image_path.replace('static/', ''),
                                      detect_object=detect_object,
                                      error=f'无法解析边界框坐标: {bbox_text}')

            # 创建带边界框的图像
            draw = ImageDraw.Draw(image)

            bboxes = []
            for coord in coords:
                y_min, x_min, y_max, x_max = map(int, coord)

                # 归一化坐标
                x_min_norm = (x_min / 1000) * width
                y_min_norm = (y_min / 1000) * height
                x_max_norm = (x_max / 1000) * width
                y_max_norm = (y_max / 1000) * height

                # 绘制边界框
                draw.rectangle([(x_min_norm, y_min_norm), (x_max_norm, y_max_norm)],
                              outline="red", width=3)

                bboxes.append({
                    'coordinates': [y_min, x_min, y_max, x_max],
                    'normalized': [y_min_norm, x_min_norm, y_max_norm, x_max_norm]
                })

            # 保存带边界框的图像
            bbox_filename = f"bbox_{os.path.basename(image_path)}"
            bbox_image_path = os.path.join(app.config['GENERATED_FOLDER'], bbox_filename)
            image.save(bbox_image_path)

            return render_template('bounding_box.html',
                                  image_path=image_path.replace('static/', ''),
                                  bbox_image=bbox_image_path.replace('static/', ''),
                                  detect_object=detect_object,
                                  bboxes=bboxes,
                                  raw_response=bbox_text)
        except Exception as e:
            return render_template('bounding_box.html', error=f'检测边界框时出错: {str(e)}')

    return render_template('bounding_box.html')

# 图像分割
@app.route('/image_segmentation', methods=['GET', 'POST'])
def image_segmentation():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'image' not in request.files:
            return render_template('image_segmentation.html', error='没有选择图片')

        file = request.files['image']
        if file.filename == '':
            return render_template('image_segmentation.html', error='没有选择图片')

        # 保存上传的图片
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        # 获取分割对象
        segment_object = request.form.get('segment_object', '分割图片中的所有对象')

        try:
            # 加载图片
            image = Image.open(image_path).convert("RGBA")

            # 获取API密钥
            current_api_key = get_api_key()
            if not current_api_key:
                return render_template('image_segmentation.html', error='API密钥未设置，请先设置API密钥')

            # 创建Gemini客户端
            client = genai.Client(api_key=current_api_key)

            # 构建提示词
            prompt = f"""
            给出图片中{segment_object}的分割掩码。
            输出一个JSON列表，每个条目包含2D边界框（键为"box_2d"），分割掩码（键为"mask"），
            以及文本标签（键为"label"）。使用描述性标签。
            """

            # 调用Gemini API进行图像分割
            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=[image, prompt]
            )

            # 解析JSON响应
            response_text = response.text

            # 提取JSON部分
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "[" in response_text and "]" in response_text:
                start = response_text.find("[")
                end = response_text.rfind("]") + 1
                json_str = response_text[start:end]
            else:
                json_str = response_text

            try:
                mask_data = json.loads(json_str)
            except:
                return render_template('image_segmentation.html',
                                      image_path=image_path.replace('static/', ''),
                                      segment_object=segment_object,
                                      error=f'无法解析JSON响应: {response_text}')

            if not mask_data:
                return render_template('image_segmentation.html',
                                      image_path=image_path.replace('static/', ''),
                                      segment_object=segment_object,
                                      error='未找到分割掩码')

            # 处理第一个掩码
            first_mask = mask_data[0]

            # 提取base64编码的掩码
            mask_base64 = first_mask.get("mask", "")
            if "base64," in mask_base64:
                mask_base64 = mask_base64.split("base64,")[1]

            # 解码并加载掩码图像
            mask_bytes = base64.b64decode(mask_base64)
            mask_image = Image.open(io.BytesIO(mask_bytes))

            # 转换图像为RGBA
            mask_image = mask_image.convert("L")  # 转换掩码为灰度

            # 创建一个彩色覆盖层（亮粉色）
            overlay = Image.new("RGBA", mask_image.size, (255, 0, 255, 128))  # 亮粉色，半透明

            # 使用掩码确定应用颜色的位置
            overlay.putalpha(mask_image)

            # 调整覆盖层大小以匹配原始图像（如果需要）
            if overlay.size != image.size:
                overlay = overlay.resize(image.size)

            # 将彩色掩码覆盖在原始图像上
            result = Image.alpha_composite(image, overlay)

            # 保存掩码图像
            mask_filename = f"mask_{os.path.basename(image_path)}"
            mask_image_path = os.path.join(app.config['GENERATED_FOLDER'], mask_filename)
            mask_image.save(mask_image_path)

            # 保存合并后的图像
            merged_filename = f"segmented_{os.path.basename(image_path)}"
            merged_image_path = os.path.join(app.config['GENERATED_FOLDER'], merged_filename)
            result.save(merged_image_path)

            return render_template('image_segmentation.html',
                                  image_path=image_path.replace('static/', ''),
                                  mask_image=mask_image_path.replace('static/', ''),
                                  segmented_image=merged_image_path.replace('static/', ''),
                                  segment_object=segment_object,
                                  raw_response=response_text)
        except Exception as e:
            return render_template('image_segmentation.html', error=f'图像分割时出错: {str(e)}')

    return render_template('image_segmentation.html')

if __name__ == '__main__':
    app.run(debug=True)
