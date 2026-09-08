from flask_cors import CORS
from openai import OpenAI
import os 
from dotenv import load_dotenv
from flask import Flask,request,jsonify,render_template

# 从 .env 文件加载 DeepSeek API 密钥等环境变量。
load_dotenv()

# 创建 Flask 应用，并允许前端页面跨域访问接口。
app = Flask(__name__)
CORS(app)

# 统一配置 DeepSeek 客户端，避免在每次请求时重复创建连接配置。
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 不同使用场景对应不同的润色要求。
SCENES = {
    "academic": "You are an academic writing tutor. Polish the given paragraph to be formal, rigorous, and suitable for university essays. Use advanced academic vocabulary where appropriate. Provide your response in three sections: 1. Polished Version 2. Explanation of Changes 3. Alternative Expressions.",
    "email": "You are a professional email editor. Polish the given paragraph to be polite, concise, and clear. Suitable for workplace or academic correspondence. Provide your response in three sections: 1. Polished Version 2. Explanation of Changes 3. Alternative Expressions.",
    "job": "You are a career coach helping with cover letters. Polish the given paragraph to be confident, professional, and achievement-oriented. Highlight the candidate's strengths. Provide your response in three sections: 1. Polished Version 2. Explanation of Changes 3. Alternative Expressions.",
    "daily": "You are a native English speaker helping a friend. Polish the given paragraph to sound natural, casual, and friendly. Use colloquial expressions where appropriate. Provide your response in three sections: 1. Polished Version 2. Explanation of Changes 3. Alternative Expressions."
}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/polish", methods=["POST"])
def polish():
    data = request.json
    # 从前端请求中读取待润色文本和场景；未传场景时默认使用学术写作。
    text = data.get("text", "")
    scene = data.get("scene", "academic")

    # 没有输入文本时直接返回客户端错误，避免无效调用 AI 接口。
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # 找不到对应场景时回退到学术写作提示词。
    system_prompt = SCENES.get(scene, SCENES["academic"])

    # 将场景要求和用户文本一起发送给 DeepSeek。
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )

    # 提取模型生成的文本，并以 JSON 形式返回前端。
    result = response.choices[0].message.content
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)