from flask import Flask, request, send_from_directory
from datetime import date
import random

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        calendar = request.form.get("calendar")
        today = str(date.today())
        score = random.randint(1, 100)

        if score <= 20:
            msg = "오늘은 조심이 필요해요."
        elif score <= 50:
            msg = "보통의 하루가 예상돼요."
        elif score <= 80:
            msg = "좋은 기운이 들어오고 있어요!"
        else:
            msg = "행운이 가득한 하루가 될 거예요!"

        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>오늘의 운세</title>
            <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
            <script src="https://developers.kakao.com/sdk/js/kakao.js"></script>
            <script>
                Kakao.init("f29ff24b0feeb75f41f51f0c939c0f9f");
                function kakaoShare() {{
                    Kakao.Link.sendDefault({{
                        objectType: 'text',
                        text: '{name}님의 운세는 {score}점이에요! 💖 {msg}',
                        link: {{
                            mobileWebUrl: window.location.href,
                            webUrl: window.location.href
                        }}
                    }});
                }}
                function copyURL() {{
                    navigator.clipboard.writeText(window.location.href);
                    alert("링크가 복사되었어요! 인스타에 공유해보세요 💌");
                }}
                const today = new Date().toISOString().split('T')[0];
                const data = {{
                    name: "{name}",
                    birth: "{birth}",
                    gender: "{gender}",
                    calendar: "{calendar}",
                    score: {score}
                }};
                localStorage.setItem("userData", JSON.stringify(data));
                localStorage.setItem("lastFortuneDate", today);
            </script>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    font-family: 'Poor Story', 'Jua', sans-serif;
                    background: #fff7ed;
                    height: 100vh;
                    position: relative;
                }}
                .fixed-header {{
                    position: fixed;
                    top: 20px;
                    width: 100%;
                    text-align: center;
                    font-size: 28px;
                    font-weight: bold;
                    z-index: 20;
                    color: #333;
                    font-family: 'Jua', sans-serif;
                }}
                .fortune-box {{
                    background: rgba(255,255,255,0.95);
                    padding: 40px 30px;
                    border-radius: 30px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    text-align: center;
                    width: 90%;
                    max-width: 400px;
                    z-index: 10;
                    position: relative;
                    top: 80px;
                    margin: 0 auto;
                }}
                .fortune-box h2 {{
                    font-size: 26px;
                    color: #aa5c5c;
                    margin-bottom: 12px;
                }}
                .fortune-box p {{
                    font-size: 20px;
                    color: #5c5c5c;
                    margin: 10px 0;
                }}
                .btn {{
                    margin: 10px 5px;
                    display: inline-block;
                    padding: 10px 16px;
                    background-color: #ff9caa;
                    color: white;
                    border-radius: 20px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .floating, .rotating-floating {{
                    position: absolute;
                    width: 60px;
                    opacity: 0.8;
                    pointer-events: none;
                }}
                .floating {{
                    animation: floatUp linear infinite;
                }}
                .rotating-floating {{
                    animation: floatRotate linear infinite;
                }}
                @keyframes floatUp {{
                    0% {{ transform: translateY(100vh); }}
                    100% {{ transform: translateY(-150px); }}
                }}
                @keyframes floatRotate {{
                    0% {{ transform: translateY(100vh) rotate(0deg); }}
                    100% {{ transform: translateY(-150px) rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="fixed-header">복토리</div>
            <div class="fortune-box">
                <h2>✨ {name}님의 운세 ✨</h2>
                <p>{today}</p>
                <p><strong>{score}점</strong></p>
                <p>{msg}</p>
                <a href="/" class="btn">돌아가기</a>
                <a class="btn" href="javascript:kakaoShare()">카카오톡 공유</a>
                <a class="btn" onclick="copyURL()">링크복사</a>
            </div>
            <script>
                for (let i = 0; i < 20; i++) {{
                    const img = document.createElement("img");
                    img.src = "/image.png";
                    img.className = i < 10 ? "floating" : "rotating-floating";
                    img.style.left = Math.random() * 100 + "%";
                    img.style.zIndex = 1;
                    img.style.animationDuration = (15 + Math.random() * 15) + "s";
                    img.style.animationDelay = Math.random() * 10 + "s";
                    document.body.appendChild(img);
                }}
            </script>
        </body>
        </html>
        '

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
