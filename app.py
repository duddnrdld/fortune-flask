from flask import Flask, request, send_from_directory
from datetime import date

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

@app.route("/", methods=["GET", "POST", "HEAD"])
def home():
    today = str(date.today())
    if request.method == "POST":
        # 회원가입 폼으로부터 전달받은 데이터 처리
        name = request.form.get("name", "")
        birth = request.form.get("birth", "")
        calendar = request.form.get("calendar", "")
        gender = request.form.get("gender", "")
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>회원가입 완료</title>
        </head>
        <body>
            <script>
                const userData = {{
                    name: "{name}",
                    birth: "{birth}",
                    calendar: "{calendar}",
                    gender: "{gender}"
                }};
                localStorage.setItem("userData", JSON.stringify(userData));
                localStorage.setItem("hasVisited", "true");
                // 오늘의 운세 생성은 /result 페이지에서 진행
                location.href = "/result";
            </script>
        </body>
        </html>
        '''

    # GET 또는 HEAD 요청 시, localStorage에 회원가입 정보가 있을 경우 바로 /result 페이지로 이동
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>복토리 운세입력</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
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
            }}
            .form-box {{
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
            input, select, button {{
                width: 100%;
                padding: 12px;
                margin-top: 12px;
                font-size: 16px;
                border-radius: 20px;
                border: none;
            }}
            button {{
                background-color: #ff9caa;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}
            .rotating-floating {{
                position: absolute;
                width: 60px;
                opacity: 0.8;
                pointer-events: none;
            }}
            /* 네 방향 애니메이션 keyframes */
            @keyframes floatRotateBottomToTop {{
                0% {{ transform: translateY(100vh) rotate(0deg); }}
                100% {{ transform: translateY(-150px) rotate(360deg); }}
            }}
            @keyframes floatRotateTopToBottom {{
                0% {{ transform: translateY(-150px) rotate(0deg); }}
                100% {{ transform: translateY(100vh) rotate(360deg); }}
            }}
            @keyframes floatRotateLeftToRight {{
                0% {{ transform: translateX(-150px) rotate(0deg); }}
                100% {{ transform: translateX(100vw) rotate(360deg); }}
            }}
            @keyframes floatRotateRightToLeft {{
                0% {{ transform: translateX(100vw) rotate(0deg); }}
                100% {{ transform: translateX(-150px) rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="form-box">
            <form method="post">
                <input name="name" id="name" placeholder="이름 입력" required>
                <input type="date" name="birth" id="birth" required>
                <select name="calendar" id="calendar">
                    <option value="양력">양력</option>
                    <option value="음력">음력</option>
                </select>
                <select name="gender" id="gender">
                    <option value="여성">여성</option>
                    <option value="남성">남성</option>
                </select>
                <button type="submit">입력 완료</button>
            </form>
        </div>
        <script>
            // 이미 회원가입된 경우 바로 /result 페이지로 리다이렉트
            const saved = localStorage.getItem("userData");
            if (saved) {{
                const lastDate = localStorage.getItem("lastFortuneDate");
                const today = "{today}";
                if (lastDate === today) {{
                    location.href = "/result?repeat=true";
                }} else {{
                    location.href = "/result";
                }}
            }}
            // 바둑판식으로 배치된 이미지 생성 (6열 x 5행)
            const numCols = 6;
            const numRows = 5;
            const animations = [
                "floatRotateBottomToTop",
                "floatRotateTopToBottom",
                "floatRotateLeftToRight",
                "floatRotateRightToLeft"
            ];
            for (let i = 0; i < numCols * numRows; i++) {{
                const img = document.createElement("img");
                img.src = "/image.png";
                img.className = "rotating-floating";
                const col = i % numCols;
                const row = Math.floor(i / numCols);
                // 각 이미지를 그리드 좌표에 배치
                img.style.left = (col * (100 / numCols)) + "%";
                img.style.top = (row * (100 / numRows)) + "%";
                img.style.zIndex = 1;
                // 무작위 애니메이션 선택 및 지속시간/딜레이 적용
                const animationChoice = animations[Math.floor(Math.random() * animations.length)];
                const duration = 15 + Math.random() * 15;
                img.style.animation = animationChoice + " " + duration + "s linear infinite";
                img.style.animationDelay = Math.random() * 10 + "s";
                document.body.appendChild(img);
            }}
        </script>
    </body>
    </html>
    '''

@app.route("/result")
def result():
    # 오늘의 운세 생성 스크립트
    script = """
        let saved = JSON.parse(localStorage.getItem("userData"));
        const today = new Date().toISOString().split('T')[0];
        let score;
        if (saved && localStorage.getItem("lastFortuneDate") === today && saved.score !== undefined) {
            score = saved.score;
        } else {
            score = Math.floor(Math.random() * 100) + 1;
            saved.score = score;
            localStorage.setItem("userData", JSON.stringify(saved));
            localStorage.setItem("lastFortuneDate", today);
        }
        let msg = "";
        if (score <= 20) msg = "오늘은 조심이 필요한 날이에요. 무리한 계획보다는 쉬엄쉬엄, 스스로를 돌보는 하루로 만들어봐요.";
        else if (score <= 50) msg = "평범한 하루가 펼쳐질 거예요. 작은 기쁨이나 우연한 행운이 찾아올지도 몰라요! 마음의 여유를 가져보세요.";
        else if (score <= 80) msg = "오늘은 좋은 기운이 가득해요! 새로운 시도를 하거나 중요한 결정을 내리기 딱 좋은 날이에요. 당신을 응원할게요.";
        else msg = "행운이 쏟아지는 날이에요! 하는 일마다 술술 풀리고, 좋은 소식이 들릴 수 있어요. 주위 사람들과 행복을 나눠보는 것도 좋겠어요.";
        document.getElementById("name").innerText = saved.name;
        document.getElementById("score").innerText = score + "점";
        document.getElementById("msg").innerText = msg;
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>오늘의 운세</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
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
                top: 100px;
                margin: 0 auto;
            }}
            .fortune-box h2 {{
                font-size: 20px;
                color: #999;
                margin-bottom: 10px;
            }}
            .fortune-box h3 {{
                font-size: 24px;
                color: #aa5c5c;
                margin-bottom: 12px;
            }}
            .fortune-box p {{
                font-size: 20px;
                color: #5c5c5c;
                margin: 10px 0;
                line-height: 1.6;
            }}
            .rotating-floating {{
                position: absolute;
                width: 60px;
                opacity: 0.8;
                pointer-events: none;
            }}
            /* 네 방향 애니메이션 keyframes */
            @keyframes floatRotateBottomToTop {{
                0% {{ transform: translateY(100vh) rotate(0deg); }}
                100% {{ transform: translateY(-150px) rotate(360deg); }}
            }}
            @keyframes floatRotateTopToBottom {{
                0% {{ transform: translateY(-150px) rotate(0deg); }}
                100% {{ transform: translateY(100vh) rotate(360deg); }}
            }}
            @keyframes floatRotateLeftToRight {{
                0% {{ transform: translateX(-150px) rotate(0deg); }}
                100% {{ transform: translateX(100vw) rotate(360deg); }}
            }}
            @keyframes floatRotateRightToLeft {{
                0% {{ transform: translateX(100vw) rotate(0deg); }}
                100% {{ transform: translateX(-150px) rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="fortune-box">
            <h2>오늘의 운세는 어떨까요?</h2>
            <h3>✨ <span id="name"></span>님의 운세 ✨</h3>
            <p id="score"></p>
            <p id="msg"></p>
        </div>
        <script>
            {script}
            // 바둑판식으로 배치된 이미지 생성 (6열 x 5행)
            const numCols = 6;
            const numRows = 5;
            const animations = [
                "floatRotateBottomToTop",
                "floatRotateTopToBottom",
                "floatRotateLeftToRight",
                "floatRotateRightToLeft"
            ];
            for (let i = 0; i < numCols * numRows; i++) {{
                const img = document.createElement("img");
                img.src = "/image.png";
                img.className = "rotating-floating";
                const col = i % numCols;
                const row = Math.floor(i / numCols);
                img.style.left = (col * (100 / numCols)) + "%";
                img.style.top = (row * (100 / numRows)) + "%";
                img.style.zIndex = 1;
                const animationChoice = animations[Math.floor(Math.random() * animations.length)];
                const duration = 15 + Math.random() * 15;
                img.style.animation = animationChoice + " " + duration + "s linear infinite";
                img.style.animationDelay = Math.random() * 10 + "s";
                document.body.appendChild(img);
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
