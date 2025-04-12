from flask import Flask, request, send_from_directory
from datetime import date
import random

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

@app.route("/", methods=["GET", "POST", "HEAD"])
def home():
    if request.method == "HEAD":
        return '', 200

    if request.method == "POST":
        name = request.form.get("name")
        birth = request.form.get("birth")
        gender = request.form.get("gender")
        calendar = request.form.get("calendar")
        today = str(date.today())
        score = random.randint(1, 100)

        if score <= 20:
            msg = "오늘은 조심이 필요한 날이에요. 무리한 계획보다는 쉬엄쉬엄, 스스로를 돌보는 하루로 만들어봐요."
        elif score <= 50:
            msg = "평범한 하루가 펼쳐질 거예요. 작은 기쁨이나 우연한 행운이 찾아올지도 몰라요! 마음의 여유를 가져보세요."
        elif score <= 80:
            msg = "오늘은 좋은 기운이 가득해요! 새로운 시도를 하거나 중요한 결정을 내리기 딱 좋은 날이에요. 당신을 응원할게요."
        else:
            msg = "행운이 쏟아지는 날이에요! 하는 일마다 술술 풀리고, 좋은 소식이 들릴 수 있어요. 주위 사람들과 행복을 나눠보는 것도 좋겠어요."

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
                    alert("링크가 복사되었어요! 친구에게도 알려줘요 ✨");
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
                localStorage.setItem("hasVisited", "true");
            </script>
            <style>
                body {{
                    margin: 0; padding: 0; overflow: hidden;
                    font-family: 'Poor Story', 'Jua', sans-serif;
                    background: #fff7ed; height: 100vh; position: relative;
                }}
                .fixed-header {{
                    position: fixed; top: 20px; width: 100%;
                    text-align: center; font-size: 28px; font-weight: bold;
                    z-index: 20; color: #333; font-family: 'Jua', sans-serif;
                }}
                .fortune-box {{
                    background: rgba(255,255,255,0.95); padding: 40px 30px;
                    border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    text-align: center; width: 90%; max-width: 400px;
                    z-index: 10; position: relative; top: 80px; margin: 0 auto;
                }}
                .fortune-box h2 {{
                    font-size: 26px; color: #aa5c5c; margin-bottom: 12px;
                }}
                .fortune-box p {{
                    font-size: 20px; color: #5c5c5c; margin: 10px 0; line-height: 1.6;
                }}
                .btn {{
                    margin: 10px 5px; display: inline-block; padding: 10px 16px;
                    background-color: #ff9caa; color: white;
                    border-radius: 20px; text-decoration: none; font-weight: bold;
                }}
                .rotating-floating {{
                    position: absolute; width: 60px; opacity: 0.8;
                    pointer-events: none; animation: floatRotate linear infinite;
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
                <a href="/" class="btn">다시 보기</a>
                <a class="btn" href="javascript:kakaoShare()">카카오톡 공유하기</a>
                <a class="btn" onclick="copyURL()">링크 복사하기</a>
            </div>
            <script>
                for (let i = 0; i < 30; i++) {{
                    const img = document.createElement("img");
                    img.src = "/image.png";
                    img.className = "rotating-floating";
                    img.style.left = Math.random() * 100 + "%";
                    img.style.zIndex = 1;
                    img.style.animationDuration = (15 + Math.random() * 15) + "s";
                    img.style.animationDelay = Math.random() * 10 + "s";
                    document.body.appendChild(img);
                }}
            </script>
        </body>
        </html>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>복토리 운세입력</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0; padding: 0; overflow: hidden;
                font-family: 'Poor Story', 'Jua', sans-serif;
                background: #fff7ed; height: 100vh; position: relative;
            }
            .fixed-header {
                position: fixed; top: 20px; width: 100%;
                text-align: center; font-size: 28px; font-weight: bold;
                z-index: 20; color: #333; font-family: 'Jua', sans-serif;
            }
            .form-box {
                background: rgba(255,255,255,0.95); padding: 40px 30px;
                border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center; width: 90%; max-width: 400px;
                z-index: 10; position: relative; top: 80px; margin: 0 auto;
            }
            .form-box input, .form-box select, .form-box button {
                width: 100%; padding: 12px; margin-top: 12px;
                font-size: 16px; border-radius: 20px; border: none;
                box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
            }
            .form-box button {
                background-color: #ff9caa; color: white;
                font-weight: bold; cursor: pointer;
            }
            .reset-btn {
                background-color: #ccc; color: #333;
                margin-top: 10px;
            }
            .rotating-floating {
                position: absolute; width: 60px; opacity: 0.8;
                pointer-events: none; animation: floatRotate linear infinite;
            }
            @keyframes floatRotate {
                0% { transform: translateY(100vh) rotate(0deg); }
                100% { transform: translateY(-150px) rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="form-box">
            <form method="post" id="fortuneForm">
                <input name="name" id="name" placeholder="이름 입력">
                <input type="date" name="birth" id="birth">
                <select name="calendar" id="calendar">
                    <option>양력</option><option>음력</option>
                </select>
                <select name="gender" id="gender">
                    <option>여성</option><option>남성</option>
                </select>
                <button type="submit">입력 완료</button>
            </form>
            <button class="reset-btn" onclick="resetData()">저장된 정보 지우기</button>
        </div>
        <script>
            const form = document.getElementById('fortuneForm');
            const today = new Date().toISOString().split('T')[0];
            window.onload = () => {
                const saved = JSON.parse(localStorage.getItem("userData"));
                const lastDate = localStorage.getItem("lastFortuneDate");
                const hasVisited = localStorage.getItem("hasVisited") === "true";
                if (saved) {
                    document.getElementById("name").value = saved.name;
                    document.getElementById("birth").value = saved.birth;
                    document.getElementById("gender").value = saved.gender;
                    document.getElementById("calendar").value = saved.calendar;
                }
                if (hasVisited && lastDate === today) {
                    alert(`${saved.name}님의 오늘의 운세는 이미 확인하셨어요!\\n점수: ${saved.score}점`);
                    form.style.display = "none";
                }
                if (hasVisited) {
                    form.style.display = "none";
                }
                for (let i = 0; i < 30; i++) {
                    const img = document.createElement("img");
                    img.src = "/image.png";
                    img.className = "rotating-floating";
                    img.style.left = Math.random() * 100 + "%";
                    img.style.zIndex = 1;
                    img.style.animationDuration = (15 + Math.random() * 15) + "s";
                    img.style.animationDelay = Math.random() * 10 + "s";
                    document.body.appendChild(img);
                }
            };
            form.addEventListener("submit", () => {
                const score = Math.floor(Math.random() * 100) + 1;
                const data = {
                    name: document.getElementById("name").value,
                    birth: document.getElementById("birth").value,
                    gender: document.getElementById("gender").value,
                    calendar: document.getElementById("calendar").value,
                    score: score
                };
                localStorage.setItem("userData", JSON.stringify(data));
                localStorage.setItem("lastFortuneDate", today);
                localStorage.setItem("hasVisited", "true");
            });
            function resetData() {
                localStorage.clear();
                alert("저장된 정보가 모두 삭제되었어요! 다시 입력해주세요 :)");
                location.reload();
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
