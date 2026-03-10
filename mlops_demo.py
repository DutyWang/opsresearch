from PIL import Image, ImageDraw, ImageFont
import math

# 画布设置
width = 1600
height = 900
background = (245, 247, 250)
img = Image.new('RGB', (width, height), background)
draw = ImageDraw.Draw(img)

# 配色
colors = {
    'data': (78, 123, 191),
    'dev': (142, 100, 182),
    'eval': (224, 133, 56),
    'model': (56, 182, 143),
    'deploy': (203, 82, 82),
    'infer': (60, 163, 214),
    'monitor': (156, 91, 76),
    'iterate': (90, 90, 90)
}

# 尝试加载合适的字体，默认备用
try:
    font_title = ImageFont.truetype("arialbd.ttf", 36)
    font_sub = ImageFont.truetype("arialbd.ttf", 20)
    font_text = ImageFont.truetype("arial.ttf", 16)
except:
    font_title = ImageFont.load_default(size=36)
    font_sub = ImageFont.load_default(size=20)
    font_text = ImageFont.load_default(size=16)

# 标题
title = "MLOps 全生命周期 — 业务流程 & 技术栈 & 定位关联图"
draw.text((width//2, 40), title, fill=(30,30,30), font=font_title, anchor="mm")

# 8个模块
stages = [
    {"name": "1 数据与特征",    "y": 150, "color": colors['data'],
     "biz": "数据采集 → 清洗 → 标注 → 特征工程 → 特征存储",
     "tech": "MinIO/HDFS/S3 | Spark/Flink | Feast | DVC/LakeFS",
     "pos": "统一数据与特征，保证训练上线一致"},

    {"name": "2 模型开发实验",  "y": 250, "color": colors['dev'],
     "biz": "模型构建 → 训练调试 → 实验跟踪 → 超参优化",
     "tech": "PyTorch/TensorFlow | MLflow/W&B | Optuna/Ray",
     "pos": "实验可复现，高效迭代模型"},

    {"name": "3 模型评估验收",  "y": 350, "color": colors['eval'],
     "biz": "离线评估 → 效果验证 → AB测试 → 合规审核",
     "tech": "Evidently AI | 自定义评估脚本 | ABTest平台",
     "pos": "量化效果，提供上线决策依据"},

    {"name": "4 模型版本管理",  "y": 450, "color": colors['model'],
     "biz": "模型标准化 → 打包 → 注册 → 版本状态管理",
     "tech": "ONNX/TorchScript | MLflow Registry | BentoML",
     "pos": "模型可信源，可版本、可回滚"},

    {"name": "5 CI/CD 部署",    "y": 550, "color": colors['deploy'],
     "biz": "代码提交 → 自动构建 → 镜像打包 → 灰度发布",
     "tech": "GitLab CI/GitHub Actions | Docker | K8s/ArgoCD",
     "pos": "自动化发布，环境一致"},

    {"name": "6 模型推理服务",  "y": 650, "color": colors['infer'],
     "biz": "在线推理 → 批量推理 → 流式推理 → 多模型调度",
     "tech": "Triton | TorchServe | TFServing | Ray/Volcano",
     "pos": "高性能、低延迟统一推理入口"},

    {"name": "7 监控运维",      "y": 750, "color": colors['monitor'],
     "biz": "服务监控 → 日志 → 漂移检测 → 模型退化 → 告警",
     "tech": "Prometheus/Grafana | ELK | Evidently AI",
     "pos": "保障稳定，提前发现效果衰减"},
]

# 绘制每一行模块
x_left = 60
box_width = 1480
box_height = 80

for i, s in enumerate(stages):
    y = s['y']
    color = s['color']
    # 矩形背景
    draw.rounded_rectangle([x_left, y, x_left + box_width, y + box_height],
                           radius=8, fill=color + (40,), outline=color, width=2)
    # 文字
    draw.text((x_left + 20, y + 12), s['name'], fill=color, font=font_sub)
    draw.text((x_left + 240, y + 12), f"业务：{s['biz']}", fill=(30,30,30), font=font_text)
    draw.text((x_left + 240, y + 42), f"技术：{s['tech']}", fill=(40,60,90), font=font_text)
    draw.text((x_left + 1000, y + 25), f"定位：{s['pos']}", fill=(60,60,60), font=font_text)

# 闭环箭头
cx = 1400
cy_top = stages[0]['y'] + box_height//2
cy_bot = stages[-1]['y'] + box_height//2
draw.line([cx, cy_top, cx, cy_bot], fill=(100,100,100), width=3)
draw.polygon([(cx-8, cy_bot-12), (cx+8, cy_bot-12), (cx, cy_bot)], fill=(100,100,100))

# 底部闭环标注
draw.text((width//2, height-30), "形成闭环：监控触发 → 自动重训练 → 持续迭代",
          fill=(80,80,80), font=font_sub, anchor="mm")

img.save("/Users/wangjun/Documents/files/dev/mlflow/mlops_business_tech_flowchart.png")
print("图片已生成：mlops_business_tech_flowchart.png")
