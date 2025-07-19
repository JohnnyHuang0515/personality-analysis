from typing import List, Any
from dataclasses import dataclass

@dataclass
class Question:
    id: int
    text: str
    category: str
    test_type: str
    options: List[str]
    weight: Any

# MBTI 題庫
mbti_questions = [
    Question(
        id=1,
        text="在社交場合中，我傾向於：",
        category="E-I",
        test_type="MBTI",
        options=["主動與他人交談", "安靜觀察他人"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=2,
        text="我更容易從以下哪個獲得能量：",
        category="E-I",
        test_type="MBTI",
        options=["與朋友聚會", "獨處休息"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=3,
        text="在團體活動中，我通常：",
        category="E-I",
        test_type="MBTI",
        options=["積極參與討論", "聆聽他人想法"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=4,
        text="遇到問題時，我傾向於：",
        category="E-I",
        test_type="MBTI",
        options=["與他人討論", "自己思考解決"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=5,
        text="週末時，我比較喜歡：",
        category="E-I",
        test_type="MBTI",
        options=["參加聚會活動", "在家放鬆休息"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=6,
        text="在會議中，我通常：",
        category="E-I",
        test_type="MBTI",
        options=["主動發言表達", "仔細聆聽記錄"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=7,
        text="認識新朋友時，我：",
        category="E-I",
        test_type="MBTI",
        options=["主動打招呼", "等待對方先開口"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=8,
        text="在陌生環境中，我：",
        category="E-I",
        test_type="MBTI",
        options=["很快融入群體", "需要時間適應"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=9,
        text="我比較喜歡的工作環境是：",
        category="E-I",
        test_type="MBTI",
        options=["開放式辦公室", "獨立工作空間"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=10,
        text="當我需要充電時，我會：",
        category="E-I",
        test_type="MBTI",
        options=["找朋友聊天", "獨自安靜休息"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=11,
        text="在團隊合作中，我傾向於：",
        category="E-I",
        test_type="MBTI",
        options=["擔任發言人", "負責幕後工作"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=12,
        text="我比較喜歡的學習方式是：",
        category="E-I",
        test_type="MBTI",
        options=["小組討論", "個人自學"],
        weight={"E": 1, "I": -1}
    ),

    # S-N 維度 (13-24 Question(
    Question(
        id=13,
        text="我偏好處理：",
        category="S-N",
        test_type="MBTI",
        options=["具體事實", "可能性與創意"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=14,
        text="我更喜歡：",
        category="S-N",
        test_type="MBTI",
        options=["按部就班", "靈活應變"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=15,
        text="在解決問題時，我傾向於：",
        category="S-N",
        test_type="MBTI",
        options=["使用已知方法", "嘗試創新方案"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=16,
        text="我比較喜歡的書籍類型是：",
        category="S-N",
        test_type="MBTI",
        options=["實用指南", "科幻小說"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=17,
        text="在規劃時，我注重：",
        category="S-N",
        test_type="MBTI",
        options=["實際可行性", "未來可能性"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=18,
        text="我比較喜歡的電影類型是：",
        category="S-N",
        test_type="MBTI",
        options=["真實故事", "奇幻冒險"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=19,
        text="在學習新事物時，我偏好：",
        category="S-N",
        test_type="MBTI",
        options=["具體步驟", "概念理解"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=20,
        text="我比較相信：",
        category="S-N",
        test_type="MBTI",
        options=["經驗證明", "直覺判斷"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=21,
        text="在描述事物時，我傾向於：",
        category="S-N",
        test_type="MBTI",
        options=["詳細具體", "概括抽象"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=22,
        text="我比較喜歡的遊戲類型是：",
        category="S-N",
        test_type="MBTI",
        options=["策略模擬", "角色扮演"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=23,
        text="在創新時，我傾向於：",
        category="S-N",
        test_type="MBTI",
        options=["改進現有", "完全重新設計"],
        weight={"S": 1, "N": -1}
    ),
    Question(
        id=24,
        text="我比較喜歡的旅行方式是：",
        category="S-N",
        test_type="MBTI",
        options=["詳細規劃", "隨興探索"],
        weight={"S": 1, "N": -1}
    ),

    # T-F 維度 (25-36 Question(
    Question(
        id=25,
        text="做決定時，我更依賴：",
        category="T-F",
        test_type="MBTI",
        options=["邏輯分析", "個人感受"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=26,
        text="我認為更重要的是：",
        category="T-F",
        test_type="MBTI",
        options=["公平公正", "和諧關係"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=27,
        text="在批評他人時，我傾向於：",
        category="T-F",
        test_type="MBTI",
        options=["直接指出問題", "委婉表達建議"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=28,
        text="我比較重視：",
        category="T-F",
        test_type="MBTI",
        options=["能力表現", "人際關係"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=29,
        text="在衝突中，我傾向於：",
        category="T-F",
        test_type="MBTI",
        options=["理性討論", "情感溝通"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=30,
        text="我比較喜歡的領導風格是：",
        category="T-F",
        test_type="MBTI",
        options=["效率導向", "關懷導向"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=31,
        text="在評價他人時，我注重：",
        category="T-F",
        test_type="MBTI",
        options=["客觀標準", "個人特質"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=32,
        text="我比較喜歡的工作環境是：",
        category="T-F",
        test_type="MBTI",
        options=["競爭激烈", "合作和諧"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=33,
        text="在解決人際問題時，我傾向於：",
        category="T-F",
        test_type="MBTI",
        options=["分析原因", "安撫情緒"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=34,
        text="我比較重視的價值觀是：",
        category="T-F",
        test_type="MBTI",
        options=["真理正義", "關愛包容"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=35,
        text="在團隊中，我傾向於：",
        category="T-F",
        test_type="MBTI",
        options=["追求效率", "維護和諧"],
        weight={"T": 1, "F": -1}
    ),
    Question(
        id=36,
        text="我比較喜歡的溝通方式是：",
        category="T-F",
        test_type="MBTI",
        options=["直接明確", "委婉體貼"],
        weight={"T": 1, "F": -1}
    ),

    # J-P 維度 (37-48 Question(
    Question(
        id=37,
        text="我傾向於：",
        category="J-P",
        test_type="MBTI",
        options=["提前計劃", "隨機應變"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=38,
        text="我喜歡：",
        category="J-P",
        test_type="MBTI",
        options=["有明確期限", "保持選項開放"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=39,
        text="我的工作方式是：",
        category="J-P",
        test_type="MBTI",
        options=["按時完成", "靈活調整"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=40,
        text="我比較喜歡的環境是：",
        category="J-P",
        test_type="MBTI",
        options=["整齊有序", "自由隨意"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=41,
        text="在面對變化時，我：",
        category="J-P",
        test_type="MBTI",
        options=["需要時間適應", "很快接受"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=42,
        text="我比較喜歡的學習方式是：",
        category="J-P",
        test_type="MBTI",
        options=["系統規劃", "隨興探索"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=43,
        text="我的生活節奏是：",
        category="J-P",
        test_type="MBTI",
        options=["規律穩定", "變化多樣"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=44,
        text="我比較喜歡的購物方式是：",
        category="J-P",
        test_type="MBTI",
        options=["列出清單", "隨意瀏覽"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=45,
        text="在旅行時，我傾向於：",
        category="J-P",
        test_type="MBTI",
        options=["詳細規劃", "隨興探索"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=46,
        text="我比較喜歡的會議方式是：",
        category="J-P",
        test_type="MBTI",
        options=["有明確議程", "自由討論"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=47,
        text="我的決策方式是：",
        category="J-P",
        test_type="MBTI",
        options=["快速決定", "持續考慮"],
        weight={"J": 1, "P": -1}
    ),
    Question(
        id=48,
        text="我比較喜歡的休閒活動是：",
        category="J-P",
        test_type="MBTI",
        options=["有計劃的活動", "隨興的活動"],
        weight={"J": 1, "P": -1}
    ),

    # 額外2題平衡各維度
    Question(
        id=49,
        text="在面對新挑戰時，我：",
        category="E-I",
        test_type="MBTI",
        options=["尋求他人建議", "自己思考解決"],
        weight={"E": 1, "I": -1}
    ),
    Question(
        id=50,
        text="我比較喜歡的藝術類型是：",
        category="S-N",
        test_type="MBTI",
        options=["寫實主義", "抽象表現"],
        weight={"S": 1, "N": -1}
    ),
]

disc_questions = [
    Question(
        id=51,
        text="在團隊中，你最常的表現是？",
        category="DISC",
        test_type="DISC",
        options=[
            "主動提出計畫並推動執行",
            "帶動氣氛、鼓勵大家參與",
            "維持團隊和諧、協助協調",
            "仔細檢查細節、確保品質"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=52,
        text="遇到困難時，你通常會？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接面對並嘗試解決問題",
            "尋求他人協助或討論",
            "保持冷靜，等待時機",
            "分析原因，規劃步驟"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=53,
        text="在會議中，你通常會？",
        category="DISC",
        test_type="DISC",
        options=[
            "主導討論方向",
            "活躍氣氛、分享想法",
            "聆聽各方意見",
            "提出具體建議"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=54,
        text="與同事相處時，你傾向於？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接表達意見",
            "建立友好關係",
            "保持和諧氛圍",
            "注重專業合作"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=55,
        text="面對新任務時，你會？",
        category="DISC",
        test_type="DISC",
        options=[
            "立即開始行動",
            "與團隊討論方案",
            "仔細了解需求",
            "制定詳細計畫"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=56,
        text="在壓力下工作時，你？",
        category="DISC",
        test_type="DISC",
        options=[
            "加快節奏完成",
            "尋求支持鼓勵",
            "保持穩定步調",
            "重新評估優先級"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=57,
        text="處理衝突時，你通常？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接面對問題",
            "調解各方關係",
            "尋求共識",
            "分析根本原因"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=58,
        text="你比較喜歡的工作環境是？",
        category="DISC",
        test_type="DISC",
        options=[
            "競爭激烈、目標明確",
            "活潑熱鬧、充滿創意",
            "穩定和諧、互相支持",
            "安靜有序、注重細節"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=59,
        text="在學習新技能時，你？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速上手實踐",
            "與他人交流學習",
            "按部就班掌握",
            "深入研究理論"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=60,
        text="你比較重視的價值是？",
        category="DISC",
        test_type="DISC",
        options=[
            "成就與效率",
            "人際關係",
            "和諧穩定",
            "品質與準確"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=61,
        text="在團隊中遇到不同意見時，你？",
        category="DISC",
        test_type="DISC",
        options=[
            "堅持自己的觀點",
            "尋求大家共識",
            "避免衝突發生",
            "分析各種方案"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=62,
        text="你比較喜歡的領導風格是？",
        category="DISC",
        test_type="DISC",
        options=[
            "果斷決策型",
            "激勵鼓舞型",
            "關懷支持型",
            "專業指導型"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=63,
        text="面對變化時，你通常？",
        category="DISC",
        test_type="DISC",
        options=[
            "積極適應新環境",
            "與他人分享感受",
            "需要時間調整",
            "仔細評估影響"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=64,
        text="你比較喜歡的溝通方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接明確",
            "生動有趣",
            "溫和友善",
            "詳細完整"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=65,
        text="在專案中，你比較擅長？",
        category="DISC",
        test_type="DISC",
        options=[
            "推動執行進度",
            "激勵團隊士氣",
            "協調各方關係",
            "確保品質標準"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=66,
        text="你比較喜歡的休閒活動是？",
        category="DISC",
        test_type="DISC",
        options=[
            "競技運動",
            "社交聚會",
            "放鬆休息",
            "學習研究"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=67,
        text="你比較重視的工作回饋是？",
        category="DISC",
        test_type="DISC",
        options=[
            "成果與成就",
            "認可與讚賞",
            "支持與理解",
            "專業與準確"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=68,
        text="面對失敗時，你通常？",
        category="DISC",
        test_type="DISC",
        options=[
            "立即重新開始",
            "尋求他人安慰",
            "需要時間恢復",
            "分析失敗原因"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=69,
        text="你比較喜歡的決策方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速決定",
            "集思廣益",
            "謹慎考慮",
            "詳細分析"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=70,
        text="你比較擅長的角色是？",
        category="DISC",
        test_type="DISC",
        options=[
            "領導者",
            "激勵者",
            "協調者",
            "專家"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=71,
        text="你比較喜歡的學習環境是？",
        category="DISC",
        test_type="DISC",
        options=[
            "競爭激烈",
            "互動活潑",
            "溫馨支持",
            "安靜專注"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=72,
        text="你比較重視的人際關係是？",
        category="DISC",
        test_type="DISC",
        options=[
            "互相尊重",
            "親密友誼",
            "和諧相處",
            "專業合作"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=73,
        text="你比較喜歡的挑戰類型是？",
        category="DISC",
        test_type="DISC",
        options=[
            "高難度目標",
            "創新嘗試",
            "穩定發展",
            "精準執行"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=74,
        text="你比較喜歡的獎勵方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "實質成果",
            "公開表揚",
            "溫馨鼓勵",
            "專業認可"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=75,
        text="你比較擅長的解決問題方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接行動",
            "集體討論",
            "耐心等待",
            "深入分析"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=76,
        text="你比較喜歡的團隊氛圍是？",
        category="DISC",
        test_type="DISC",
        options=[
            "目標導向",
            "活力四射",
            "溫馨和諧",
            "專業嚴謹"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=77,
        text="你比較重視的工作特質是？",
        category="DISC",
        test_type="DISC",
        options=[
            "效率與成果",
            "創意與活力",
            "穩定與可靠",
            "品質與準確"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=78,
        text="你比較喜歡的成長方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "挑戰自我",
            "與他人交流",
            "穩步提升",
            "深入研究"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=79,
        text="你比較擅長的溝通技巧是？",
        category="DISC",
        test_type="DISC",
        options=[
            "說服他人",
            "活躍氣氛",
            "傾聽理解",
            "邏輯分析"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=80,
        text="你比較喜歡的成就感來源是？",
        category="DISC",
        test_type="DISC",
        options=[
            "達成目標",
            "獲得認可",
            "幫助他人",
            "專業精進"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=81,
        text="你比較喜歡的創新方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "大膽嘗試",
            "集思廣益",
            "漸進改善",
            "深入研究"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=82,
        text="你比較重視的個人特質是？",
        category="DISC",
        test_type="DISC",
        options=[
            "決斷力",
            "親和力",
            "耐心",
            "專業度"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=83,
        text="你比較喜歡的風險程度是？",
        category="DISC",
        test_type="DISC",
        options=[
            "高風險高回報",
            "適度冒險",
            "保守穩健",
            "精確計算"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=84,
        text="你比較擅長的時間管理是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速完成",
            "靈活調整",
            "穩定進行",
            "精確規劃"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=85,
        text="你比較喜歡的責任範圍是？",
        category="DISC",
        test_type="DISC",
        options=[
            "全面負責",
            "團隊合作",
            "專注本職",
            "專業領域"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=86,
        text="你比較重視的職業發展是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速晉升",
            "多元發展",
            "穩定成長",
            "專業精進"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=87,
        text="你比較喜歡的激勵方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "挑戰目標",
            "公開表揚",
            "溫馨鼓勵",
            "專業認可"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=88,
        text="你比較擅長的適應能力是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速調整",
            "靈活應變",
            "穩定適應",
            "深入理解"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=89,
        text="你比較重視的工作價值是？",
        category="DISC",
        test_type="DISC",
        options=[
            "成就與影響",
            "人際與認可",
            "和諧與支持",
            "品質與專業"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=90,
        text="你比較喜歡的領導方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接指揮",
            "激勵鼓舞",
            "關懷支持",
            "專業指導"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=91,
        text="你比較擅長的問題解決是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速決策",
            "集體討論",
            "耐心等待",
            "深入分析"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=92,
        text="你比較喜歡的團隊角色是？",
        category="DISC",
        test_type="DISC",
        options=[
            "領導者",
            "激勵者",
            "協調者",
            "專家"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=93,
        text="你比較重視的個人成長是？",
        category="DISC",
        test_type="DISC",
        options=[
            "能力提升",
            "人際拓展",
            "內心平靜",
            "專業精進"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=94,
        text="你比較喜歡的挑戰類型是？",
        category="DISC",
        test_type="DISC",
        options=[
            "高難度目標",
            "創新嘗試",
            "穩定發展",
            "精準執行"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=95,
        text="你比較擅長的溝通方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "直接明確",
            "生動有趣",
            "溫和友善",
            "詳細完整"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=96,
        text="你比較重視的工作環境是？",
        category="DISC",
        test_type="DISC",
        options=[
            "競爭激烈",
            "活潑熱鬧",
            "穩定和諧",
            "安靜有序"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=97,
        text="你比較喜歡的成就感是？",
        category="DISC",
        test_type="DISC",
        options=[
            "達成目標",
            "獲得認可",
            "幫助他人",
            "專業精進"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=98,
        text="你比較擅長的學習方式是？",
        category="DISC",
        test_type="DISC",
        options=[
            "快速上手",
            "互動學習",
            "按部就班"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=99,
        text="你比較重視的人際互動是？",
        category="DISC",
        test_type="DISC",
        options=[
            "互相尊重",
            "親密友誼",
            "和諧相處",
            "專業合作"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
    Question(
        id=100,
        text="你比較喜歡的個人特質是？",
        category="DISC",
        test_type="DISC",
        options=[
            "決斷力",
            "親和力",
            "耐心",
            "專業度"
        ],
        weight=[
            {"D": 1, "I": 0, "S": 0, "C": 0},
            {"D": 0, "I": 1, "S": 0, "C": 0},
            {"D": 0, "I": 0, "S": 1, "C": 0},
            {"D": 0, "I": 0, "S": 0, "C": 1}
        ]
    ),
]

big5_questions = [
    Question(
        id=101,
        text="我是一個外向的人。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=102,
        text="我容易感到焦慮。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=103,
        text="我喜歡與人交談。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=104,
        text="我是一個友善的人。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=105,
        text="我是一個負責任的人。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=106,
        text="我做事有條理。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=107,
        text="我情緒穩定。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [1, 2, 3, 4, 5]}
    ),
    Question(
        id=108,
        text="我喜歡嘗試新事物。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=109,
        text="我有豐富的想像力。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=110,
        text="我樂於幫助他人。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=111,
        text="我喜歡參加社交活動。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=112,
        text="我容易感到緊張。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=113,
        text="我喜歡藝術和文化活動。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=114,
        text="我信任他人。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=115,
        text="我做事很有效率。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=116,
        text="我喜歡獨處。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [1, 2, 3, 4, 5]}
    ),
    Question(
        id=117,
        text="我容易感到沮喪。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=118,
        text="我喜歡抽象思考。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=119,
        text="我對他人很寬容。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=120,
        text="我做事很仔細。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=121,
        text="我喜歡成為注意的焦點。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=122,
        text="我容易感到擔心。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=123,
        text="我喜歡探索新想法。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=124,
        text="我很少與他人爭吵。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=125,
        text="我做事很有計劃。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=126,
        text="我喜歡安靜的環境。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [1, 2, 3, 4, 5]}
    ),
    Question(
        id=127,
        text="我容易感到情緒波動。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=128,
        text="我喜歡複雜的問題。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=129,
        text="我對他人很友善。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=130,
        text="我做事很可靠。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=131,
        text="我喜歡與他人合作。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=132,
        text="我容易感到壓力。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=133,
        text="我喜歡創新的想法。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=134,
        text="我對他人很體貼。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=135,
        text="我做事很有條理。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=136,
        text="我喜歡熱鬧的場合。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=137,
        text="我容易感到不安。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=138,
        text="我喜歡哲學討論。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=139,
        text="我對他人很慷慨。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=140,
        text="我做事很認真。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=141,
        text="我喜歡認識新朋友。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=142,
        text="我容易感到緊張。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=143,
        text="我喜歡嘗試新體驗。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=144,
        text="我對他人很尊重。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=145,
        text="我做事很有目標。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=146,
        text="我喜歡成為領導者。",
        category="外向性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"外向性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=147,
        text="我容易感到情緒化。",
        category="神經質",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"神經質": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=148,
        text="我喜歡藝術作品。",
        category="開放性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"開放性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=149,
        text="我對他人很關心。",
        category="友善性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"友善性": [5, 4, 3, 2, 1]}
    ),
    Question(
        id=150,
        text="我做事很有紀律。",
        category="盡責性",
        test_type="BIG5",
        options=["非常同意", "同意", "中立", "不同意", "非常不同意"],
        weight={"盡責性": [5, 4, 3, 2, 1]}
    ),
]

enneagram_questions = [
    Question(
        id=151,
        text="我重視正確與完美。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=152,
        text="我喜歡被他人需要。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=153,
        text="我追求成功與成就。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=154,
        text="我是一個獨特的人。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=155,
        text="我偏好深入思考。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=156,
        text="我傾向於擔心未來。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=157,
        text="我喜歡新體驗。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=158,
        text="我是一個強勢的人。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=159,
        text="我重視內在平靜。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=160,
        text="我容易批評自己與他人。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=161,
        text="我傾向於照顧他人需求。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=162,
        text="我重視效率與結果。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=163,
        text="我容易被強烈情緒影響。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=164,
        text="我喜歡獨處學習。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=165,
        text="我重視安全與穩定。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=166,
        text="我傾向於樂觀積極。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=167,
        text="我喜歡掌控局面。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=168,
        text="我傾向於避免衝突。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=169,
        text="我認為規則很重要。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=170,
        text="我喜歡被他人讚美。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=171,
        text="我喜歡成為焦點。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=172,
        text="我喜歡藝術創作。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=173,
        text="我喜歡分析問題。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=174,
        text="我容易懷疑他人。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=175,
        text="我喜歡冒險。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=176,
        text="我喜歡保護弱者。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=177,
        text="我喜歡和諧的環境。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=178,
        text="我對錯誤很敏感。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=179,
        text="我容易感到被利用。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=180,
        text="我喜歡競爭。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=181,
        text="我喜歡深度對話。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=182,
        text="我喜歡收集資訊。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=183,
        text="我喜歡忠誠的朋友。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=184,
        text="我喜歡多樣化。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=185,
        text="我喜歡直接表達。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=186,
        text="我喜歡隨遇而安。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=187,
        text="我喜歡改善事物。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=188,
        text="我喜歡照顧他人。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=189,
        text="我喜歡設定目標。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=190,
        text="我喜歡獨特的事物。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=191,
        text="我喜歡深入研究。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=192,
        text="我喜歡準備充分。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=193,
        text="我喜歡有趣的事物。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=194,
        text="我喜歡挑戰權威。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=195,
        text="我喜歡平靜的生活。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=196,
        text="我喜歡公平正義。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=197,
        text="我喜歡被需要。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=198,
        text="我喜歡高效率。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=199,
        text="我喜歡表達情感。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=200,
        text="我喜歡獨立思考。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=201,
        text="我喜歡可靠的夥伴。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=202,
        text="我喜歡自由選擇。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=203,
        text="我喜歡保護他人。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=204,
        text="我喜歡包容他人。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=205,
        text="我喜歡改善自己。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=206,
        text="我喜歡幫助他人。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=207,
        text="我喜歡成功。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=208,
        text="我喜歡深度體驗。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=209,
        text="我喜歡知識。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=210,
        text="我喜歡安全感。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=211,
        text="我喜歡快樂。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=212,
        text="我喜歡力量。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=213,
        text="我喜歡和平。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=214,
        text="我喜歡正確。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=215,
        text="我喜歡愛。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=216,
        text="我喜歡成就。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=217,
        text="我喜歡美。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=218,
        text="我喜歡智慧。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=219,
        text="我喜歡忠誠。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=220,
        text="我喜歡自由。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=221,
        text="我喜歡正義。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=222,
        text="我喜歡和諧。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=223,
        text="我喜歡完美。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=224,
        text="我喜歡關懷。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=225,
        text="我喜歡效率。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=226,
        text="我喜歡獨特。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=227,
        text="我喜歡理解。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=228,
        text="我喜歡穩定。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=229,
        text="我喜歡冒險。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=230,
        text="我喜歡控制。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=231,
        text="我喜歡接納。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=232,
        text="我喜歡改進。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=233,
        text="我喜歡支持。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=234,
        text="我喜歡表現。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=235,
        text="我喜歡感受。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=236,
        text="我喜歡觀察。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=237,
        text="我喜歡準備。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=238,
        text="我喜歡探索。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=239,
        text="我喜歡保護。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=240,
        text="我喜歡調和。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=241,
        text="我喜歡標準。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
    Question(
        id=242,
        text="我喜歡給予。",
        category="類型2",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型2": 1}
    ),
    Question(
        id=243,
        text="我喜歡目標。",
        category="類型3",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型3": 1}
    ),
    Question(
        id=244,
        text="我喜歡深度。",
        category="類型4",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型4": 1}
    ),
    Question(
        id=245,
        text="我喜歡知識。",
        category="類型5",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型5": 1}
    ),
    Question(
        id=246,
        text="我喜歡安全。",
        category="類型6",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型6": 1}
    ),
    Question(
        id=247,
        text="我喜歡變化。",
        category="類型7",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型7": 1}
    ),
    Question(
        id=248,
        text="我喜歡力量。",
        category="類型8",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型8": 1}
    ),
    Question(
        id=249,
        text="我喜歡平靜。",
        category="類型9",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型9": 1}
    ),
    Question(
        id=250,
        text="我喜歡正確。",
        category="類型1",
        test_type="ENNEAGRAM",
        options=["是", "否"],
        weight={"類型1": 1}
    ),
]

# 查詢函數
all_questions = mbti_questions + disc_questions + big5_questions + enneagram_questions

def get_questions_by_type(test_type: str) -> List[Question]:
    return [q for q in all_questions if q.test_type == test_type]

def get_all_questions() -> List[Question]:
    return all_questions

def get_mbti_questions() -> List[Question]:
    return get_questions_by_type("MBTI")

def get_disc_questions() -> List[Question]:
    return get_questions_by_type("DISC")

def get_big5_questions() -> List[Question]:
    return get_questions_by_type("BIG5")

def get_enneagram_questions() -> List[Question]:
    return get_questions_by_type("ENNEAGRAM")

def get_question_count_by_type() -> dict:
    return {
        "MBTI": len(get_mbti_questions()),
        "DISC": len(get_disc_questions()),
        "BIG5": len(get_big5_questions()),
        "ENNEAGRAM": len(get_enneagram_questions()),
        "Total": len(all_questions)
    }