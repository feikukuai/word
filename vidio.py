from docx import Document
# 获取当前脚本所在目录的绝对路径
import os

# 获取Python解释器（或exe）所在目录
exe_dir = os.path.dirname(sys.executable)
print(exe_dir)
script_dir = os.path.dirname(sys.executable)
print(script_dir)
# 改变当前工作目录到exe文件所在的目录
os.chdir(exe_dir)
source_dir = os.path.dirname(sys.executable)
print(f"正确工作路径 directory: {os.getcwd()}")
# 需要检查和创建的文件列表

import numpy as np 

from moviepy.editor import *
from moviepy.config import change_settings 

def load_parameters(doc_path):
    doc = Document(doc_path)
    params = {"background": {}, "dialog": {}, "text": {}, "output": {}}
    current_section = None  # 类型转换规则 
    converters = {
        "int": int, 
        "float": float,
        "rgb": lambda x: tuple(map(int, x.split(','))),
        "bool": lambda x: x.lower() == "true"
    }
    
    # 参数类型映射表 
    TYPE_MAP = {
        "background": {
            "default_duration": "float",
            "resolution": "optional"
        },
        "dialog": {
            "width_ratio": "float", 
            "height_ratio": "float",
            "position_y": "float", 
            "bg_alpha": "float",
            "border_size": "int", 
            "border_radius": "int"
        },
        "text": {
            "size": "int", 
            "speed": "int",
            "padding_x": "int", 
            "padding_y": "int",
            "line_spacing": "float"
        },
        "output": {
            "fps": "int", 
            "threads": "int",
            "audio_enabled": "bool"
        }
    }

    for para in doc.paragraphs:
        line = para.text.strip()
        if not line or line.startswith("#"):
            continue 
        
        # 识别段落分类 
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].lower()
            continue
            
        if "=" in line and current_section:
            key, value = map(str.strip, line.split("=", 1))
            param_type = TYPE_MAP.get(current_section, {}).get(key, "str")
            
            try:
                if param_type in converters:
                    params[current_section][key] = converters[param_type](value)
                elif "_color" in key:
                    params[current_section][key] = converters["rgb"](value)
                else:
                    params[current_section][key] = value 
            except:
                print(f"参数解析失败：{current_section}.{key} = {value}")
                params[current_section][key] = value 
                
    return params 

def generate_video(script_dir):  # 🆕 修改1：添加参数 
    # 🆕 修改2：参数文件路径锚定 
    params = load_parameters(os.path.join(script_dir, "Parameter.docx"))
    
    # 🆕 修改3：背景路径锚定 
    bg_path = os.path.join(script_dir, params["background"]["background_path"])
    
    if bg_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        bg_clip = ImageClip(bg_path).set_duration(
            params["background"].get("default_duration", 10)
        )
    else:
        bg_clip = VideoFileClip(bg_path)
    
    # 分辨率处理 
    if "resolution" in params["background"]:
        w, h = map(int, params["background"]["resolution"].split('x'))
        bg_clip = bg_clip.resize((w, h))
    
    # 创建动态对话框 
    dialog_w = int(bg_clip.w * params["dialog"]["width_ratio"])
    dialog_h = int(bg_clip.h * params["dialog"]["height_ratio"])
    
    def create_dialog(t):
        return (ColorClip(size=(dialog_w, dialog_h), color=params["dialog"]["bg_color"])
                .set_opacity(params["dialog"]["bg_alpha"])
                .set_position(('center', bg_clip.h * params["dialog"]["position_y"]))
                .margin(
                    top=params["text"]["padding_y"], 
                    bottom=params["text"]["padding_y"],
                    left=params["text"]["padding_x"],
                    right=params["text"]["padding_x"],
                    color=params["dialog"]["border_color"]
                )
                .set_duration(bg_clip.duration))
    
    # 文字动画生成 
    text_content = params["text"]["content"]
    def text_animation(t):
        chars_show = min(int(t * params["text"]["speed"]), len(text_content))
        current_text = text_content[:chars_show]
        
        return (TextClip(
            txt=current_text,
            font=params["text"]["font"],
            fontsize=params["text"]["size"],
            color=params["text"]["color"],
            align='west',
            size=(dialog_w - 2*params["text"]["padding_x"], None),
            method='caption',
            print_cmd=True 
        )
        .set_position((
            params["text"]["padding_x"], 
            params["text"]["padding_y"]
        )))
    
    # 合成最终视频 
    final_clip = CompositeVideoClip([
        bg_clip,
        create_dialog(0).crossfadein(0.5),
        text_animation(0).set_start(0.5)
    ], use_bgclip=True).set_duration(bg_clip.duration)
    
    # 音频处理 
    if params["output"].get("audio_enabled", True) and hasattr(bg_clip, 'audio'):
        final_clip = final_clip.set_audio(bg_clip.audio)
    
    # 🆕 修改4：输出路径锚定 
    output_path = os.path.join(script_dir, params["output"]["path"])
    final_clip.write_videofile(
        output_path, # 使用锚定后的路径 
        fps=params["output"]["fps"],
        codec=params["output"]["codec"],
        threads=params["output"]["threads"],
        preset='slow',
        audio_codec='aac' if params["output"]["audio_enabled"] else None 
    )

if __name__ == "__main__":
    # 🆕 修改5：传递已定义的根目录变量 
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 示例定义（实际由用户定义）
    generate_video(script_dir)