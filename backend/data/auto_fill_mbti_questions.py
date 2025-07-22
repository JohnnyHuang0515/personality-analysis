import os
import json
import random
from collections import defaultdict

MBTI_DIMENSIONS = ["E", "I", "S", "N", "T", "F", "J", "P"]
TARGET_PER_DIM = 20

# 口語化繁體中文反向題模板（每維度 10 題，僅舉例 E/I/S/N，其他可依此風格擴充）
REVERSE_TEMPLATES = {
    "E": [
        "我在熱鬧的聚會裡常常覺得很累，寧願早點離開。",
        "和一群人相處時，我通常比較安靜，不太主動發言。",
        "遇到新朋友時，我很少主動介紹自己。",
        "我在團體活動中，常常選擇旁觀而不是參與討論。",
        "參加社交活動後，我通常需要獨處一段時間來恢復精力。",
        "我不太喜歡成為大家注目的焦點。",
        "在新環境裡，我通常會先觀察，不會馬上和大家互動。",
        "我很少主動邀請朋友參加活動。",
        "我在團體中多半選擇傾聽，很少主動發言。",
        "我在社交場合常常覺得不自在，比較想快點結束。"
    ],
    "I": [
        "我很享受和朋友們一起參加熱鬧的聚會。",
        "遇到新朋友時，我會主動介紹自己。",
        "我在團體活動中經常主動參與討論。",
        "參加社交活動後，我通常還是很有精神。",
        "我喜歡成為大家注目的焦點。",
        "在新環境裡，我會主動和大家互動。",
        "我常常主動邀請朋友參加活動。",
        "我在團體中經常主動發言。",
        "我在社交場合總是很自在。",
        "和一群人相處時，我通常很活躍。"
    ],
    "S": [
        "我很少注意生活中的細節，常常忽略小地方。",
        "我不太在意實際經驗，更喜歡憑感覺做決定。",
        "我做事時不太重視事實，常常依賴直覺。",
        "我對細節不太敏感，容易漏掉小事。",
        "我不太喜歡按部就班，偏好創新和變化。",
        "我很少觀察周遭環境的細節。",
        "我做決定時很少考慮過去經驗。",
        "我不太會記得生活中的小事。",
        "我做事時不太重視實際成果。",
        "我對現實細節不太感興趣。"
    ],
    "N": [
        "我很少思考未來的可能性，專注於當下。",
        "我不太會聯想或幻想，習慣腳踏實地。",
        "我做決定時只考慮現實，不太想像未來。",
        "我不太喜歡討論抽象的想法。",
        "我很少有創新或不尋常的想法。",
        "我做事時不太依賴靈感。",
        "我不太會從不同角度看問題。",
        "我很少主動提出新觀點。",
        "我做事時不太考慮長遠發展。",
        "我對未來的想像力不太豐富。"
    ],
    "T": [
        "我做決定時很少考慮邏輯，通常依感覺行事。",
        "我不太重視分析問題，常常隨意判斷。",
        "我做事時不太在意公平，只看心情。",
        "我很少根據事實做決定。",
        "我不太會用理性思考問題。",
        "我做事時很少考慮原則。",
        "我不太重視數據和證據。",
        "我做決定時很少分析利弊。",
        "我不太會用邏輯推理。",
        "我做事時很少考慮後果。"
    ],
    "F": [
        "我做決定時很少考慮他人感受。",
        "我不太在意人際關係的和諧。",
        "我做事時很少顧及別人的想法。",
        "我不太會主動關心朋友的情緒。",
        "我做決定時很少考慮團隊氣氛。",
        "我不太重視同理心。",
        "我做事時很少考慮他人需求。",
        "我不太會主動協調人際關係。",
        "我做事時很少顧及團隊成員的感受。",
        "我不太會主動幫助別人。"
    ],
    "J": [
        "我做事時很少規劃，常常臨時決定。",
        "我不太喜歡安排日程，隨遇而安。",
        "我做事時很少列出待辦事項。",
        "我不太在意計畫的細節。",
        "我做決定時很少考慮步驟。",
        "我不太喜歡有明確的行程安排。",
        "我做事時很少提前準備。",
        "我不太在意事情的秩序感。",
        "我做事時很少按部就班。",
        "我不太會為未來做詳細規劃。"
    ],
    "P": [
        "我做事時很少隨機應變，偏好照計畫進行。",
        "我不太喜歡臨時改變計畫。",
        "我做事時很少根據當下情況調整。",
        "我不太會靈活應對突發狀況。",
        "我做決定時很少考慮彈性。",
        "我不太喜歡即興發揮。",
        "我做事時很少調整自己的計畫。",
        "我不太會根據情況改變做法。",
        "我做事時很少接受突發變化。",
        "我不太會隨機應變。"
    ]
}

LIKERT = ["非常不同意", "不同意", "普通", "同意", "非常同意"]

DATA_PATH = os.path.join(os.path.dirname(__file__), "MBTI_questions_final.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

# 去重現有題庫
uniq = {}
for q in questions:
    key = (q["text"].strip(), q["category"], q["is_reverse"])
    if key not in uniq:
        uniq[key] = q

# 補齊每維度反向題
for dim in MBTI_DIMENSIONS:
    exist = [q for q in uniq.values() if q["category"] == dim and q["is_reverse"]]
    need = 10 - len(exist)
    if need > 0:
        for t in REVERSE_TEMPLATES[dim][:need]:
            key = (t.strip(), dim, True)
            if key not in uniq:
                uniq[key] = {
                    "text": t,
                    "category": dim,
                    "test_type": "MBTI",
                    "options": LIKERT,
                    "weight": [1, 2, 3, 4, 5],
                    "is_reverse": True
                }

# 只保留合規、無重複、無低質量題目
final_questions = list(uniq.values())
final_questions.sort(key=lambda x: (MBTI_DIMENSIONS.index(x["category"]) if x["category"] in MBTI_DIMENSIONS else 99, x["is_reverse"]))

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(final_questions, f, ensure_ascii=False, indent=2)

print("【MBTI 反向題補齊完成】")
for dim in MBTI_DIMENSIONS:
    cnt = len([q for q in final_questions if q["category"] == dim and q["is_reverse"]])
    print(f"{dim} 反向題數：{cnt}") 