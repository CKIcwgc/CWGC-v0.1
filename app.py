from flask import Flask

app = Flask(__name__)

@app.route('/')
def ask():
    return '''
        <!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CWGC實用文格式溫習機v0.1</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 10px;
            line-height: 1.4;
            background-color: #f5f5f5;
            font-size: 14px;
        }

        .container {
            background-color: white;
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }

        h1 {
            text-align: center;
            color: #333;
            margin: 3px 0;
            font-size: 16px;
        }

        h2 {
            color: #2c3e50;
            margin: 3px 0;
            font-size: 12px;
        }

        h3 {
            color: #3498db;
            margin: 3px 0 5px;
            border-left: 3px solid #3498db;
            padding-left: 5px;
            font-size: 12px;
        }

        .format-section {
            margin-bottom: 5px;
            padding: 5px;
            background-color: #f9f9f9;
            border-radius: 3px;
        }

        .option-container {
            display: flex;
            flex-wrap: nowrap;
            gap: 3px;
            margin-bottom: 5px;
            overflow-x: auto;
        }

        .option {
            background-color: #e0e0e0;
            border: 1px solid #ccc;
            border-radius: 3px;
            padding: 3px 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 12px;
            white-space: nowrap;
        }

        .option:hover {
            background-color: #d0d0d0;
        }

        .option.selected {
            background-color: #a5d6a7;
            border-color: #388e3c;
        }

        .option.incorrect {
            background-color: #ffcdd2;
            border-color: #d32f2f;
            animation: shake 0.5s;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-3px); }
            75% { transform: translateX(3px); }
        }

        .btn {
            display: inline-block;
            margin: 5px;
            padding: 8px 16px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .btn:hover {
            background-color: #1976d2;
        }

        .success-message, .correct-message {
            text-align: center;
            font-size: 18px;
            color: #388e3c;
            font-weight: bold;
            margin: 10px 0;
            display: none;
        }

        .progress {
            margin: 3px 0;
            text-align: center;
        }

        .progress-item {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #e0e0e0;
            margin: 0 3px;
        }

        .progress-item.completed {
            background-color: #4caf50;
        }

        .pyro {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            display: none;
        }

        .pyro > .before, .pyro > .after {
            position: absolute;
            width: 3px;
            height: 3px;
            border-radius: 50%;
            box-shadow: 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff, 0 0 #fff;
            animation: 1s bang ease-out infinite backwards, 1s gravity ease-in infinite backwards, 5s position linear infinite backwards;
        }

        .pyro > .after {
            animation-delay: 1.25s, 1.25s, 1.25s;
            animation-duration: 1.25s, 1.25s, 6.25s;
        }

        @keyframes bang {
            to {
                box-shadow: -50px -80px #ff00c8, 20px -70px #ff8000, 70px -80px #0400ff, 25px -70px #ea00ff, -60px -40px #00ff73;
            }
        }

        @keyframes gravity {
            to { transform: translateY(150px); opacity: 0; }
        }

        @keyframes position {
            0%, 19.9% { margin-top: 10%; margin-left: 40%; }
            20%, 39.9% { margin-top: 40%; margin-left: 30%; }
            40%, 59.9% { margin-top: 20%; margin-left: 70%; }
            60%, 79.9% { margin-top: 30%; margin-left: 20%; }
            80%, 99.9% { margin-top: 30%; margin-left: 80%; }
        }

        @media (max-width: 600px) {
            .container { padding: 5px; }
            h1 { font-size: 18px; }
            h2 { font-size: 14px; }
            h3 { font-size: 12px; }
            .option { font-size: 10px; padding: 2px 4px; }
            .option-container { flex-wrap: wrap; }
            .btn { padding: 6px 12px; font-size: 12px; margin: 3px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="pyro" id="fireworks">
            <div class="before"></div>
            <div class="after"></div>
        </div>

        <h1>CWGC實用文格式溫習機 v0.1</h1>

        <div class="progress" id="progress">
            <div class="progress-item" data-type="書信"></div>
            <div class="progress-item" data-type="建議書"></div>
            <div class="progress-item" data-type="報告"></div>
            <div class="progress-item" data-type="專題文章"></div>
            <div class="progress-item" data-type="演講辭"></div>
        </div>

        <h2>請選擇「<span id="current-type">書信</span>」應該包含的格式：</h2>

        <div id="format-sections"></div>

        <div class="correct-message" id="correct-message">對了！棒棒你真棒!</div>
        <div class="success-message" id="success-message">恭喜你通過了所有測驗！實用文達人是你!</div>

        <button class="btn" id="check-btn">確認答案</button>
        <button class="btn" id="show-answer-btn">顯示答案</button>
        <button class="btn" id="next-btn" style="display: none;">下一題</button>
        <button class="btn" id="restart-btn" style="display: none;">重新開始</button>
    </div>

    <script> <!--邊個偷睇。\ ^ /。  要靠自己背咗佢!-->
        const documentFormats = {
            '書信': {
                '受文者': ['受文團體', '姓', '身份', '知照語'],
                '標題': ['寫作目的', '年份/度', '活動/事件'],
                '引言': ['背景', '代表身份義務/組織的宗旨/與此文的關係', '寫作目的、立場'],
                '主體': ['五步曲'],
                '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）'],
                '下款': ['祝頌語', '發文者團體', '身份', '署名', '啓告語'],
                '日期': ['發文日期']
            },
            '建議書': {
                '受文者': ['受文團體', '姓', '身份', '知照語'],
                '標題': ['組織', '活動/事件', '文類名稱'],
                '引言': ['背景', '代表身份義務/組織的宗旨/與此文的關係', '寫作目的、立場'],
                '主體': ['五步曲'],
                '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）'],
                '下款': ['發文者團體', '身份', '署名', '啓告語'],
                '日期': ['發文日期']
            },
            '報告': {
                '受文者': ['受文團體', '姓', '身份', '知照語'],
                '標題': ['組織', '活動/事件', '文類名稱'],
                '引言': ['背景', '代表身份義務/組織的宗旨/與此文的關係', '寫作目的、立場'],
                '主體': ['五步曲'],
                '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）'],
                '下款': ['發文者團體', '身份', '署名', '啓告語'],
                '日期': ['發文日期']
            },
            '專題文章': {
                '受文者': ['(無)'],
                '標題': ['兩句結構相近、字數相同'],
                '引言': ['背景', '代表身份義務/組織的宗旨/與此文的關係', '寫作目的、立場'],
                '主體': ['五步曲'],
                '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）'],
                '下款': ['發文者團體', '身份', '署名'],
                '日期': ['(無)']
            },
            '演講辭': {
                '受文者': ['稱呼'],
                '標題': ['(無)'],
                '引言': ['介紹自己的身份、與場合的關係', '感謝場合', '背景', '寫作目的、立場'],
                '主體': ['五步曲'],
                '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）', '祝福、謝謝大家!'],
                '下款': ['(無)'],
                '日期': ['(無)']
            }
        };

        const formatDetails = {
            '受文者': ['受文團體', '姓', '身份', '知照語', '稱呼', '(無)'],
            '標題': ['寫作目的', '年份/度', '活動/事件', '組織', '文類名稱', '兩句結構相近、字數相同', '(無)'],
            '引言': ['背景', '代表身份義務/組織的宗旨/與此文的關係', '寫作目的、立場', '介紹自己的身份、與場合的關係', '感謝場合', '(無)'],
            '主體': ['五步曲', '(無)'],
            '結語': ['重申要旨', '表達期盼', '回應資料指定任務（如有）', '祝福、謝謝大家!', '(無)'],
            '下款': ['祝頌語', '發文者團體', '身份', '署名', '啓告語', '(無)'],
            '日期': ['發文日期', '(無)']
        };

        const allFormatCategories = ['受文者', '標題', '引言', '主體', '結語', '下款', '日期'];
        const completedTypes = new Set();
        let currentType = '';
        const selectedOptions = {};

        function init() {
            document.getElementById('success-message').style.display = 'none';
            document.getElementById('correct-message').style.display = 'none';
            document.getElementById('restart-btn').style.display = 'none';
            document.getElementById('next-btn').style.display = 'none';
            document.getElementById('check-btn').style.display = 'inline-block';
            document.getElementById('show-answer-btn').style.display = 'inline-block';
            document.getElementById('fireworks').style.display = 'none';
            completedTypes.clear();
            allFormatCategories.forEach(category => {
                selectedOptions[category] = new Set();
            });
            updateProgress();
            selectNextType();
        }

        function selectNextType() {
            const remainingTypes = Object.keys(documentFormats).filter(type => !completedTypes.has(type));
            if (remainingTypes.length === 0) {
                document.getElementById('success-message').style.display = 'block';
                document.getElementById('check-btn').style.display = 'none';
                document.getElementById('show-answer-btn').style.display = 'none';
                document.getElementById('next-btn').style.display = 'none';
                document.getElementById('restart-btn').style.display = 'inline-block';
                document.getElementById('fireworks').style.display = 'block';
                return;
            }
            currentType = remainingTypes[Math.floor(Math.random() * remainingTypes.length)];
            document.getElementById('current-type').textContent = currentType;
            document.getElementById('correct-message').style.display = 'none';
            document.getElementById('fireworks').style.display = 'none';
            document.getElementById('check-btn').style.display = 'inline-block';
            document.getElementById('show-answer-btn').style.display = 'inline-block';
            document.getElementById('next-btn').style.display = 'none';
            allFormatCategories.forEach(category => {
                selectedOptions[category] = new Set();
            });
            generateFormatSections();
        }

        function generateFormatSections() {
            const formatSectionsContainer = document.getElementById('format-sections');
            formatSectionsContainer.innerHTML = '';
            allFormatCategories.forEach(category => {
                const sectionDiv = document.createElement('div');
                sectionDiv.classList.add('format-section');
                const heading = document.createElement('h3');
                heading.textContent = category;
                sectionDiv.appendChild(heading);
                const optionsContainer = document.createElement('div');
                optionsContainer.classList.add('option-container');
                const allOptions = formatDetails[category];
                allOptions.forEach(option => {
                    const optionDiv = document.createElement('div');
                    optionDiv.classList.add('option');
                    optionDiv.textContent = option;
                    optionDiv.dataset.category = category;
                    optionDiv.dataset.option = option;
                    optionDiv.addEventListener('click', () => {
                        if (optionDiv.classList.contains('selected')) {
                            optionDiv.classList.remove('selected');
                            selectedOptions[category].delete(option);
                        } else {
                            optionDiv.classList.remove('incorrect');
                            optionDiv.classList.add('selected');
                            selectedOptions[category].add(option);
                        }
                    });
                    optionsContainer.appendChild(optionDiv);
                });
                sectionDiv.appendChild(optionsContainer);
                formatSectionsContainer.appendChild(sectionDiv);
            });
        }

        function checkAnswer() {
            let allCorrect = true;
            const currentFormat = documentFormats[currentType];
            allFormatCategories.forEach(category => {
                const correctOptions = currentFormat[category] ? new Set(currentFormat[category]) : new Set(['(無)']);
                const selectedOpts = selectedOptions[category] || new Set();
                if (selectedOpts.size !== correctOptions.size ||
                    ![...selectedOpts].every(opt => correctOptions.has(opt))) {
                    allCorrect = false;
                }
            });
            if (allCorrect) {
                document.getElementById('correct-message').style.display = 'block';
                document.getElementById('check-btn').style.display = 'none';
                document.getElementById('show-answer-btn').style.display = 'none';
                document.getElementById('next-btn').style.display = 'inline-block';
                document.getElementById('fireworks').style.display = 'block';
                completedTypes.add(currentType);
                updateProgress();
            } else {
                allFormatCategories.forEach(category => {
                    const correctOptions = currentFormat[category] ? new Set(currentFormat[category]) : new Set(['(無)']);
                    const selectedOpts = selectedOptions[category] || new Set();
                    selectedOpts.forEach(opt => {
                        if (!correctOptions.has(opt)) {
                            document.querySelectorAll(`.option[data-category="${category}"][data-option="${opt}"]`).forEach(option => {
                                option.classList.remove('selected');
                                option.classList.add('incorrect');
                            });
                            selectedOptions[category].delete(opt);
                        }
                    });
                });
                setTimeout(() => {
                    document.querySelectorAll('.option.incorrect').forEach(option => {
                        option.classList.remove('incorrect');
                    });
                }, 1000);
            }
        }

        function showAnswer() {
            const currentFormat = documentFormats[currentType];
            allFormatCategories.forEach(category => {
                selectedOptions[category].clear();
                document.querySelectorAll(`.option[data-category="${category}"]`).forEach(option => {
                    option.classList.remove('selected');
                });
                const correctOptions = currentFormat[category] ? currentFormat[category] : ['(無)'];
                correctOptions.forEach(opt => {
                    document.querySelectorAll(`.option[data-category="${category}"][data-option="${opt}"]`).forEach(option => {
                        option.classList.add('selected');
                        selectedOptions[category].add(opt);
                    });
                });
            });
            document.getElementById('check-btn').style.display = 'none';
            document.getElementById('show-answer-btn').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
        }

        function updateProgress() {
            document.querySelectorAll('.progress-item').forEach(item => {
                const type = item.dataset.type;
                if (completedTypes.has(type)) {
                    item.classList.add('completed');
                } else {
                    item.classList.remove('completed');
                }
            });
        }

        document.getElementById('check-btn').addEventListener('click', checkAnswer);
        document.getElementById('show-answer-btn').addEventListener('click', showAnswer);
        document.getElementById('next-btn').addEventListener('click', selectNextType);
        document.getElementById('restart-btn').addEventListener('click', init);
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
    '''