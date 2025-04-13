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
        # 회원가입 폼에서 전달받은 데이터 처리
        name = request.form.get("name", "")
        birth = request.form.get("birth", "")
        calendar = request.form.get("calendar", "")
        gender = request.form.get("gender", "")
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <!-- 확대/축소 방지 -->
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
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
                location.href = "/result";
            </script>
        </body>
        </html>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <!-- 확대/축소 방지 -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
        <title>복토리 운세입력</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 20;
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
            .greeting {{
                position: fixed;
                top: 60px;
                width: 100%;
                text-align: center;
                font-size: 20px;
                color: #333;
                z-index: 30;
            }}
            .form-box {{
                background: rgba(255,255,255,0.95);
                padding: 40px 10px;
                border-radius: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
                /* 아이폰에서 좌우를 좀 더 좁게: 폭 80%, 최대폭 340px */
                width: 80%;
                max-width: 340px;
                z-index: 10;
                margin: 120px auto;
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
        <div class="greeting" id="greeting"></div>
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
            // 인삿말 타이핑 애니메이션 (계속 반복)
            const greetingText = "안녕하세요 주인님! 오늘도 방문해 주셔서 감사합니다!";
            let greetingIndex = 0;
            function typeGreeting() {{
                const greetingElem = document.getElementById("greeting");
                greetingElem.innerText = greetingText.slice(0, greetingIndex);
                greetingIndex++;
                if (greetingIndex > greetingText.length) {{
                    setTimeout(() => {{
                        greetingIndex = 0;
                        typeGreeting();
                    }}, 2000);
                }} else {{
                    setTimeout(typeGreeting, 150);
                }}
            }}
            typeGreeting();
            
            // 회원가입 정보가 이미 있다면 바로 결과 페이지로 이동
            const saved = localStorage.getItem("userData");
            const today = "{today}";
            if (saved) {{
                const lastDate = localStorage.getItem("lastFortuneDate");
                if (lastDate === today) {{
                    location.href = "/result?repeat=true";
                }} else {{
                    location.href = "/result";
                }}
            }}
            // 바둑판식 배치의 배경 이미지 생성 (6열 x 5행), animationDelay 0s, z-index 0로 설정
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
                img.style.zIndex = "0";
                const animationChoice = animations[Math.floor(Math.random() * animations.length)];
                const duration = 15 + Math.random() * 15;
                img.style.animation = animationChoice + " " + duration + "s linear infinite";
                img.style.animationDelay = "0s";
                document.body.appendChild(img);
            }}
        </script>
    </body>
    </html>
    '''

@app.route("/result")
def result():
    # 오늘의 운세 점수를 1~100 사이에서 랜덤 생성하고, 10단계의 메시지를 출력하는 스크립트
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
        if (score <= 10) {{
            msg = "오늘은 전반적으로 운세가 부진하여 예상치 못한 어려움과 방해가 많을 수 있는 날입니다. 자신을 돌보며 작은 성공에도 감사하는 마음을 잃지 않는다면, 어려움 속에서도 배움과 성장을 기대할 수 있습니다.";
        }} else if (score <= 20) {{
            msg = "비교적 운세가 부진한 편이나, 이는 새로운 도전을 준비할 수 있는 기회가 될 수 있습니다. 작은 실망이 오히려 더 큰 발전의 밑거름이 될 수 있으니, 차분히 상황을 받아들이고 자신감을 회복해보세요.";
        }} else if (score <= 30) {{
            msg = "비록 예상보다 운세가 좋지 않을 수 있으나, 이는 자기 내면을 돌아보고 작은 변화로 개선할 수 있는 가능성을 내포하고 있습니다. 긍정적인 자세로 어려움을 극복해 나가며 새로운 기회를 모색해보세요.";
        }} else if (score <= 40) {{
            msg = "약간의 어려움과 도전이 예상되지만, 이는 당신에게 더 깊은 경험과 성장을 가져다줄 수 있는 날입니다. 주변 사람들의 조언과 도움을 받아 한 걸음씩 나아간다면 뜻밖의 좋은 결과를 얻을 수 있을 것입니다.";
        }} else if (score <= 50) {{
            msg = "안정과 도전이 공존하는 하루가 예상되며, 평범해 보이는 순간 속에서도 특별한 기회가 숨어 있을 수 있습니다. 작지만 꾸준한 노력이 곧 큰 변화를 만들어낼 것입니다.";
        }} else if (score <= 60) {{
            msg = "약간 좋은 운세를 가진 날입니다. 작지만 의미 있는 성취를 이루며, 긍정적인 에너지가 당신의 주변을 감싸는 하루가 될 것입니다. 이번 경험을 바탕으로 더 큰 성공을 향해 나아갈 수 있는 자신감을 얻으시기 바랍니다.";
        }} else if (score <= 70) {{
            msg = "전반적으로 운이 따르는 날입니다. 여러모로 순조로운 일들이 벌어지며, 새로운 도전에서도 좋은 결과를 기대할 수 있습니다. 주변과의 협력과 소통이 당신에게 큰 힘이 되어 줄 것이며, 즐거운 기운이 넘치는 하루가 될 것입니다.";
        }} else if (score <= 80) {{
            msg = "긍정적이고 활기찬 에너지가 넘치는 만큼, 새로운 가능성과 도전을 향한 기회가 많을 것입니다. 자신감을 가지고 미래를 향해 나아간다면 뜻깊은 성취와 발전을 경험하게 될 것입니다.";
        }} else if (score <= 90) {{
            msg = "매우 좋은 운세를 자랑합니다. 열정과 창의력이 넘치며, 주어진 기회를 효과적으로 활용할 수 있는 날입니다. 당신의 노력과 주변의 응원이 결합되어 놀라운 성과와 발전을 이끌어낼 수 있습니다.";
        }} else {{
            msg = "모든 일이 당신의 뜻대로 순조롭게 진행되며, 특별한 행운과 성공이 가득한 하루가 될 것입니다. 당신의 열정과 노력이 결실을 맺어, 놀라운 성취와 기쁨을 맛보게 되는 최고의 날이 될 것입니다.";
        }}
        document.getElementById("name").innerText = saved.name;
        document.getElementById("score").innerText = score + "점";
        document.getElementById("msg").innerText = msg;
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <!-- 확대/축소 방지 -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no">
        <title>오늘의 운세</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 20;
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
            .greeting {{
                position: fixed;
                top: 60px;
                width: 100%;
                text-align: center;
                font-size: 20px;
                color: #333;
                z-index: 30;
            }}
            .fortune-box {{
                background: rgba(255,255,255,0.95);
                padding: 40px 10px;
                border-radius: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
                /* 아이폰에서 좌우 여백을 조금 더 축소 */
                width: calc(100% - 10mm);
                max-width: 340px;
                z-index: 10;
                margin: 120px auto;
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
        <div class="greeting" id="greeting"></div>
        <div class="fortune-box">
            <h2>오늘의 운세는 어떨까요?</h2>
            <h3>✨ <span id="name"></span>님의 운세 ✨</h3>
            <p id="score"></p>
            <p id="msg"></p>
        </div>
        <script>
            // 인삿말 타이핑 애니메이션 (계속 반복)
            const greetingText = "안녕하세요 주인님! 오늘도 방문해 주셔서 감사합니다!";
            let greetingIndex = 0;
            function typeGreeting() {{
                const greetingElem = document.getElementById("greeting");
                greetingElem.innerText = greetingText.slice(0, greetingIndex);
                greetingIndex++;
                if (greetingIndex > greetingText.length) {{
                    setTimeout(() => {{
                        greetingIndex = 0;
                        typeGreeting();
                    }}, 2000);
                }} else {{
                    setTimeout(typeGreeting, 150);
                }}
            }}
            typeGreeting();

            {script}
            // 바둑판식 배치된 배경 이미지 생성 (6열 x 5행), z-index 0, animationDelay 0s
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
                img.style.zIndex = "0";
                const animationChoice = animations[Math.floor(Math.random() * animations.length)];
                const duration = 15 + Math.random() * 15;
                img.style.animation = animationChoice + " " + duration + "s linear infinite";
                img.style.animationDelay = "0s";
                document.body.appendChild(img);
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
