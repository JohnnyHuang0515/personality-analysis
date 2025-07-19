import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.database import get_db
from app.models.question import TestQuestion

def insert_mbti_questions():
    db = next(get_db())
    questions = [
        # 情境題
        {
            "text": "在一個重要會議中，你的同事提出了一個你認為有問題的提案。你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "立即指出問題並提出反對意見",
                "私下與同事討論，了解他的想法",
                "先觀察其他人的反應",
                "提出建設性的改進建議"
            ]
        },
        {
            "text": "週末朋友突然邀請你參加一個即興的戶外活動，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "興奮地答應，喜歡這種驚喜",
                "詢問詳細計劃和安排",
                "考慮天氣和準備時間",
                "建議改期，需要更多準備"
            ]
        },
        {
            "text": "工作中遇到一個複雜的技術問題，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "立即開始嘗試各種解決方案",
                "先研究相關文檔和理論",
                "尋求同事的經驗和建議",
                "制定詳細的分析計劃"
            ]
        },
        {
            "text": "朋友向你傾訴感情問題，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "提供具體的建議和解決方案",
                "仔細聆聽，理解他的感受",
                "分享類似的經驗",
                "幫助他分析問題的根源"
            ]
        },
        {
            "text": "公司要舉辦年會，需要有人負責策劃，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "主動承擔，享受創意過程",
                "仔細評估自己的能力",
                "與團隊合作，分工負責",
                "制定詳細的執行計劃"
            ]
        },
        {
            "text": "在一個陌生的城市迷路，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "隨意探索，享受冒險",
                "查看地圖和導航",
                "詢問當地人",
                "回到熟悉的地方重新規劃"
            ]
        },
        {
            "text": "同事對你的工作提出批評，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "立即辯解和反駁",
                "認真聽取，分析是否有道理",
                "尋求更多人的意見",
                "制定改進計劃"
            ]
        },
        {
            "text": "面對一個重要的決策，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "相信直覺，快速決定",
                "收集所有相關資訊",
                "諮詢信任的人",
                "分析各種可能性"
            ]
        },
        {
            "text": "在社交場合遇到陌生人，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "主動介紹自己，開始聊天",
                "等待別人先開口",
                "觀察環境，尋找共同話題",
                "保持禮貌但保持距離"
            ]
        },
        {
            "text": "學習新技能時，你偏好：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "直接動手實踐",
                "先理解理論基礎",
                "與他人一起學習",
                "制定學習計劃"
            ]
        },
        {
            "text": "處理衝突時，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "直接面對，立即解決",
                "分析衝突的原因",
                "尋求調解和妥協",
                "制定解決方案"
            ]
        },
        {
            "text": "面對變化和不確定性，你會：",
            "category": "situation",
            "test_type": "MBTI",
            "options": [
                "感到興奮和期待",
                "仔細評估風險",
                "尋求他人的支持",
                "制定應對計劃"
            ]
        },
        # 理論題
        {
            "text": "你更喜歡的工作環境是：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "充滿創意和自由",
                "結構化和有條理",
                "團隊合作和互動",
                "安靜和專注"
            ]
        },
        {
            "text": "做決定時，你更依賴：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "直覺和感受",
                "邏輯和分析",
                "他人的意見",
                "事實和數據"
            ]
        },
        {
            "text": "你更喜歡的學習方式是：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "實踐和體驗",
                "閱讀和研究",
                "討論和交流",
                "觀察和思考"
            ]
        },
        {
            "text": "面對壓力時，你傾向於：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "尋求外部刺激",
                "獨自思考和分析",
                "與他人分享",
                "制定計劃和行動"
            ]
        },
        {
            "text": "你更重視：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "創新和可能性",
                "穩定和可靠性",
                "和諧和關係",
                "效率和結果"
            ]
        },
        {
            "text": "你更喜歡的溝通方式是：",
            "category": "theory",
            "test_type": "MBTI",
            "options": [
                "直接和坦率",
                "詳細和準確",
                "溫和和體貼",
                "簡潔和重點"
            ]
        },
    ]
    for q in questions:
        db.add(TestQuestion(
            text=q["text"],
            category=q["category"],
            test_type=q["test_type"],
            options=json.dumps(q["options"], ensure_ascii=False),
            weight=""
        ))
    db.commit()
    print(f"已插入 {len(questions)} 題 MBTI 補充題目")

def insert_disc_questions():
    db = next(get_db())
    questions = [
        # 情境題
        {"text": "團隊中有人不配合工作，你會：", "category": "situation", "test_type": "DISC", "options": ["直接指出問題，要求改正", "分析原因，制定解決方案", "耐心溝通，了解困難", "避免衝突，自己承擔"]},
        {"text": "面對緊急任務，你會：", "category": "situation", "test_type": "DISC", "options": ["立即行動，快速完成", "制定計劃，有序執行", "尋求幫助，協調資源", "仔細評估，確保品質"]},
        {"text": "同事對你的想法提出質疑，你會：", "category": "situation", "test_type": "DISC", "options": ["堅持己見，據理力爭", "提供更多證據支持", "聆聽意見，尋求共識", "接受批評，調整想法"]},
        {"text": "需要說服他人接受你的建議，你會：", "category": "situation", "test_type": "DISC", "options": ["展現自信，強調優勢", "提供詳細的分析報告", "建立關係，獲得信任", "等待時機，慢慢推進"]},
        {"text": "面對失敗，你會：", "category": "situation", "test_type": "DISC", "options": ["立即重新開始，不氣餒", "分析原因，改進方法", "尋求支持，調整心態", "反思過程，吸取教訓"]},
        {"text": "在會議中，你更傾向於：", "category": "situation", "test_type": "DISC", "options": ["主導討論，表達觀點", "提供數據，分析問題", "協調各方，促進合作", "聆聽他人，記錄重點"]},
        {"text": "處理客戶投訴，你會：", "category": "situation", "test_type": "DISC", "options": ["立即回應，快速解決", "調查原因，制定方案", "耐心聆聽，安撫情緒", "記錄問題，轉交處理"]},
        {"text": "面對競爭，你會：", "category": "situation", "test_type": "DISC", "options": ["積極應對，爭取勝利", "分析對手，制定策略", "尋求合作，共創雙贏", "專注自己，提升能力"]},
        {"text": "需要創新解決方案，你會：", "category": "situation", "test_type": "DISC", "options": ["大膽嘗試，突破常規", "系統分析，邏輯推理", "集思廣益，團隊合作", "深入研究，謹慎評估"]},
        {"text": "面對變化，你會：", "category": "situation", "test_type": "DISC", "options": ["積極適應，把握機會", "仔細評估，制定計劃", "尋求支持，共同面對", "觀察趨勢，穩步調整"]},
        {"text": "領導團隊時，你更注重：", "category": "situation", "test_type": "DISC", "options": ["設定目標，激勵行動", "制定流程，確保效率", "關懷成員，建立關係", "提供指導，培養能力"]},
        {"text": "面對衝突，你會：", "category": "situation", "test_type": "DISC", "options": ["直接面對，快速解決", "分析根源，制定方案", "調解各方，促進和解", "避免對立，尋求妥協"]},
        {"text": "需要做出重要決策，你會：", "category": "situation", "test_type": "DISC", "options": ["相信直覺，快速決定", "收集資訊，分析利弊", "諮詢他人，尋求共識", "仔細考慮，謹慎選擇"]},
        {"text": "面對挑戰，你會：", "category": "situation", "test_type": "DISC", "options": ["迎難而上，克服困難", "制定計劃，逐步解決", "尋求幫助，共同面對", "評估風險，選擇時機"]},
        {"text": "與他人合作時，你更重視：", "category": "situation", "test_type": "DISC", "options": ["達成目標，取得成果", "明確分工，提高效率", "建立關係，促進和諧", "互相學習，共同成長"]},
        {"text": "面對批評，你會：", "category": "situation", "test_type": "DISC", "options": ["立即回應，捍衛立場", "分析內容，改進不足", "虛心接受，調整態度", "反思自己，吸取教訓"]},
        {"text": "需要影響他人，你會：", "category": "situation", "test_type": "DISC", "options": ["展現魅力，激發熱情", "提供證據，邏輯說服", "建立信任，情感共鳴", "耐心等待，適時推進"]},
        {"text": "面對壓力，你會：", "category": "situation", "test_type": "DISC", "options": ["積極應對，化壓力為動力", "制定計劃，有序處理", "尋求支持，分擔壓力", "調整心態，保持平靜"]},
        {"text": "需要創新，你會：", "category": "situation", "test_type": "DISC", "options": ["大膽嘗試，突破限制", "系統思考，邏輯創新", "集思廣益，團隊創新", "深入研究，穩健創新"]},
        {"text": "面對機會，你會：", "category": "situation", "test_type": "DISC", "options": ["立即把握，快速行動", "仔細評估，制定策略", "與人分享，共同把握", "謹慎考慮，穩步推進"]},
        # 理論題
        {"text": "你更喜歡的工作節奏是：", "category": "theory", "test_type": "DISC", "options": ["快速和刺激", "有序和穩定", "溫和和協調", "謹慎和深思"]},
        {"text": "與他人互動時，你更注重：", "category": "theory", "test_type": "DISC", "options": ["達成目標", "提高效率", "建立關係", "互相理解"]},
        {"text": "面對問題，你更傾向於：", "category": "theory", "test_type": "DISC", "options": ["直接解決", "分析原因", "尋求共識", "謹慎評估"]},
        {"text": "你更重視的價值是：", "category": "theory", "test_type": "DISC", "options": ["成就和成功", "準確和可靠", "和諧和合作", "品質和完美"]},
        {"text": "做決定時，你更依賴：", "category": "theory", "test_type": "DISC", "options": ["直覺和勇氣", "邏輯和分析", "感受和關係", "事實和證據"]},
        {"text": "你更喜歡的溝通風格是：", "category": "theory", "test_type": "DISC", "options": ["直接和有力", "詳細和準確", "溫和和體貼", "謹慎和深思"]},
        {"text": "面對變化，你更傾向於：", "category": "theory", "test_type": "DISC", "options": ["積極適應", "仔細評估", "尋求支持", "穩步調整"]},
        {"text": "你更重視的結果是：", "category": "theory", "test_type": "DISC", "options": ["快速達成", "準確完成", "和諧共贏", "品質卓越"]},
    ]
    for q in questions:
        db.add(TestQuestion(
            text=q["text"],
            category=q["category"],
            test_type=q["test_type"],
            options=json.dumps(q["options"], ensure_ascii=False),
            weight=""
        ))
    db.commit()
    print(f"已插入 {len(questions)} 題 DISC 補充題目")

def insert_big5_questions():
    db = next(get_db())
    questions = [
        # 情境題
        {"text": "在一個陌生的社交場合，你會：", "category": "situation", "test_type": "Big5", "options": ["主動與陌生人交談", "等待別人先開口", "尋找熟悉的人", "保持安靜觀察"]},
        {"text": "面對新的挑戰，你會：", "category": "situation", "test_type": "Big5", "options": ["感到興奮和期待", "仔細評估風險", "尋求他人建議", "保持謹慎態度"]},
        {"text": "工作中遇到困難，你會：", "category": "situation", "test_type": "Big5", "options": ["積極尋找解決方案", "系統分析問題", "與同事討論", "尋求上級指導"]},
        {"text": "面對批評，你會：", "category": "situation", "test_type": "Big5", "options": ["虛心接受並改進", "分析批評的合理性", "尋求更多意見", "反思自己的不足"]},
        {"text": "需要做出重要決定，你會：", "category": "situation", "test_type": "Big5", "options": ["相信直覺快速決定", "收集所有相關資訊", "諮詢信任的人", "仔細考慮各種可能"]},
        {"text": "面對壓力時，你會：", "category": "situation", "test_type": "Big5", "options": ["積極應對化壓力為動力", "制定計劃有序處理", "尋求他人支持", "調整心態保持冷靜"]},
        {"text": "學習新技能時，你偏好：", "category": "situation", "test_type": "Big5", "options": ["直接動手實踐", "先理解理論基礎", "與他人一起學習", "制定詳細計劃"]},
        {"text": "處理衝突時，你會：", "category": "situation", "test_type": "Big5", "options": ["直接面對解決問題", "分析衝突的原因", "尋求調解和妥協", "避免正面衝突"]},
        {"text": "面對變化，你會：", "category": "situation", "test_type": "Big5", "options": ["感到興奮和期待", "仔細評估影響", "尋求他人意見", "保持謹慎態度"]},
        {"text": "與他人合作時，你更重視：", "category": "situation", "test_type": "Big5", "options": ["達成共同目標", "明確分工和責任", "建立良好關係", "確保工作品質"]},
        {"text": "面對失敗，你會：", "category": "situation", "test_type": "Big5", "options": ["立即重新開始", "分析失敗原因", "尋求他人安慰", "反思學習經驗"]},
        {"text": "需要創新解決方案，你會：", "category": "situation", "test_type": "Big5", "options": ["大膽嘗試新方法", "系統分析問題", "集思廣益討論", "深入研究可行性"]},
        {"text": "面對競爭，你會：", "category": "situation", "test_type": "Big5", "options": ["積極參與爭取勝利", "制定策略提高競爭力", "尋求合作共創雙贏", "專注提升自己能力"]},
        {"text": "處理緊急情況，你會：", "category": "situation", "test_type": "Big5", "options": ["立即行動快速反應", "冷靜分析制定方案", "尋求他人協助", "謹慎評估風險"]},
        {"text": "面對不確定性，你會：", "category": "situation", "test_type": "Big5", "options": ["感到興奮和期待", "仔細評估各種可能", "尋求他人意見", "保持謹慎態度"]},
        {"text": "需要影響他人，你會：", "category": "situation", "test_type": "Big5", "options": ["展現自信和魅力", "提供邏輯和證據", "建立信任和關係", "耐心等待時機"]},
        {"text": "面對批評，你會：", "category": "situation", "test_type": "Big5", "options": ["立即回應和辯解", "分析批評的內容", "尋求更多意見", "反思自己的不足"]},
        {"text": "學習新知識時，你偏好：", "category": "situation", "test_type": "Big5", "options": ["直接實踐和體驗", "系統學習和思考", "與他人討論交流", "制定學習計劃"]},
        {"text": "面對挑戰，你會：", "category": "situation", "test_type": "Big5", "options": ["迎難而上克服困難", "制定計劃逐步解決", "尋求他人幫助", "評估風險選擇時機"]},
        {"text": "處理複雜問題，你會：", "category": "situation", "test_type": "Big5", "options": ["大膽嘗試各種方法", "系統分析問題結構", "與他人合作解決", "深入研究問題本質"]},
        # 理論題
        {"text": "你更喜歡的工作環境是：", "category": "theory", "test_type": "Big5", "options": ["充滿挑戰和變化", "結構化和有序", "團隊合作和互動", "安靜和專注"]},
        {"text": "做決定時，你更依賴：", "category": "theory", "test_type": "Big5", "options": ["直覺和感受", "邏輯和分析", "他人的意見", "事實和數據"]},
        {"text": "你更重視的價值是：", "category": "theory", "test_type": "Big5", "options": ["創新和冒險", "穩定和可靠", "和諧和合作", "品質和完美"]},
        {"text": "面對壓力，你傾向於：", "category": "theory", "test_type": "Big5", "options": ["積極應對", "系統處理", "尋求支持", "調整心態"]},
        {"text": "你更喜歡的溝通方式是：", "category": "theory", "test_type": "Big5", "options": ["直接和坦率", "詳細和準確", "溫和和體貼", "謹慎和深思"]},
        {"text": "你更重視的結果是：", "category": "theory", "test_type": "Big5", "options": ["快速達成", "準確完成", "和諧共贏", "品質卓越"]},
        {"text": "面對變化，你更傾向於：", "category": "theory", "test_type": "Big5", "options": ["積極適應", "仔細評估", "尋求支持", "穩步調整"]},
        {"text": "你更喜歡的學習方式是：", "category": "theory", "test_type": "Big5", "options": ["實踐和體驗", "閱讀和思考", "討論和交流", "觀察和反思"]},
        {"text": "你更重視的關係是：", "category": "theory", "test_type": "Big5", "options": ["深度和真誠", "穩定和可靠", "和諧和溫暖", "尊重和獨立"]},
        {"text": "你更喜歡的領導風格是：", "category": "theory", "test_type": "Big5", "options": ["激勵和創新", "系統和效率", "關懷和支持", "專業和權威"]},
    ]
    for q in questions:
        db.add(TestQuestion(
            text=q["text"],
            category=q["category"],
            test_type=q["test_type"],
            options=json.dumps(q["options"], ensure_ascii=False),
            weight=""
        ))
    db.commit()
    print(f"已插入 {len(questions)} 題 Big5 補充題目")

def insert_enneagram_questions():
    db = next(get_db())
    questions = [
        # 情境題
        {"text": "面對不公平的對待，你會：", "category": "situation", "test_type": "Enneagram", "options": ["立即抗議，爭取正義", "分析情況，制定策略", "尋求調解，促進和諧", "反思自己，改進不足"]},
        {"text": "在團隊中，你更傾向於：", "category": "situation", "test_type": "Enneagram", "options": ["承擔領導責任", "提供專業建議", "協調各方關係", "專注完成任務"]},
        {"text": "面對衝突，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接面對，快速解決", "分析根源，制定方案", "調解各方，促進和解", "避免對立，尋求妥協"]},
        {"text": "需要做出重要決策，你會：", "category": "situation", "test_type": "Enneagram", "options": ["相信直覺，快速決定", "收集資訊，分析利弊", "諮詢他人，尋求共識", "仔細考慮，謹慎選擇"]},
        {"text": "面對批評，你會：", "category": "situation", "test_type": "Enneagram", "options": ["立即回應，捍衛立場", "分析內容，改進不足", "虛心接受，調整態度", "反思自己，吸取教訓"]},
        {"text": "工作中遇到困難，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極尋找解決方案", "系統分析問題", "與同事合作", "尋求上級指導"]},
        {"text": "面對變化，你會：", "category": "situation", "test_type": "Enneagram", "options": ["感到興奮和期待", "仔細評估影響", "尋求他人支持", "保持謹慎態度"]},
        {"text": "與他人合作時，你更重視：", "category": "situation", "test_type": "Enneagram", "options": ["達成共同目標", "明確分工責任", "建立良好關係", "確保工作品質"]},
        {"text": "面對失敗，你會：", "category": "situation", "test_type": "Enneagram", "options": ["立即重新開始", "分析失敗原因", "尋求他人安慰", "反思學習經驗"]},
        {"text": "需要創新解決方案，你會：", "category": "situation", "test_type": "Enneagram", "options": ["大膽嘗試新方法", "系統分析問題", "集思廣益討論", "深入研究可行性"]},
        {"text": "面對競爭，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極參與爭取勝利", "制定策略提高競爭力", "尋求合作共創雙贏", "專注提升自己能力"]},
        {"text": "處理緊急情況，你會：", "category": "situation", "test_type": "Enneagram", "options": ["立即行動快速反應", "冷靜分析制定方案", "尋求他人協助", "謹慎評估風險"]},
        {"text": "面對不確定性，你會：", "category": "situation", "test_type": "Enneagram", "options": ["感到興奮和期待", "仔細評估各種可能", "尋求他人意見", "保持謹慎態度"]},
        {"text": "需要影響他人，你會：", "category": "situation", "test_type": "Enneagram", "options": ["展現自信和魅力", "提供邏輯和證據", "建立信任和關係", "耐心等待時機"]},
        {"text": "面對批評，你會：", "category": "situation", "test_type": "Enneagram", "options": ["立即回應和辯解", "分析批評的內容", "尋求更多意見", "反思自己的不足"]},
        {"text": "學習新知識時，你偏好：", "category": "situation", "test_type": "Enneagram", "options": ["直接實踐和體驗", "系統學習和思考", "與他人討論交流", "制定學習計劃"]},
        {"text": "面對變化，你會：", "category": "situation", "test_type": "Enneagram", "options": ["感到興奮和期待", "仔細評估影響", "尋求他人支持", "保持謹慎態度"]},
        {"text": "與他人合作時，你更重視：", "category": "situation", "test_type": "Enneagram", "options": ["達成共同目標", "明確分工責任", "建立良好關係", "確保工作品質"]},
        # 理論題
        {"text": "你更喜歡的工作環境是：", "category": "theory", "test_type": "Enneagram", "options": ["充滿挑戰和變化", "結構化和有序", "和諧和溫暖", "安靜和專注"]},
        {"text": "做決定時，你更依賴：", "category": "theory", "test_type": "Enneagram", "options": ["直覺和感受", "邏輯和分析", "他人的意見", "事實和數據"]},
        {"text": "你更重視的價值是：", "category": "theory", "test_type": "Enneagram", "options": ["成就和成功", "準確和可靠", "和諧和愛", "品質和完美"]},
        {"text": "面對壓力，你傾向於：", "category": "theory", "test_type": "Enneagram", "options": ["積極應對", "系統處理", "尋求支持", "調整心態"]},
        {"text": "你更喜歡的溝通方式是：", "category": "theory", "test_type": "Enneagram", "options": ["直接和有力", "詳細和準確", "溫和和體貼", "謹慎和深思"]},
        {"text": "你更重視的結果是：", "category": "theory", "test_type": "Enneagram", "options": ["快速達成", "準確完成", "和諧共贏", "品質卓越"]},
        {"text": "面對變化，你更傾向於：", "category": "theory", "test_type": "Enneagram", "options": ["積極適應", "仔細評估", "尋求支持", "穩步調整"]},
        {"text": "你更喜歡的學習方式是：", "category": "theory", "test_type": "Enneagram", "options": ["實踐和體驗", "閱讀和思考", "討論和交流", "觀察和反思"]},
        {"text": "你更重視的關係是：", "category": "theory", "test_type": "Enneagram", "options": ["深度和真誠", "穩定和可靠", "和諧和溫暖", "尊重和獨立"]},
        {"text": "你更喜歡的領導風格是：", "category": "theory", "test_type": "Enneagram", "options": ["激勵和創新", "系統和效率", "關懷和支持", "專業和權威"]},
        {"text": "你更重視的品質是：", "category": "theory", "test_type": "Enneagram", "options": ["勇氣和決心", "智慧和理性", "愛心和同情", "完美和卓越"]},
        {"text": "面對挑戰，你更傾向於：", "category": "theory", "test_type": "Enneagram", "options": ["迎難而上", "制定計劃", "尋求幫助", "評估風險"]},
        {"text": "你更喜歡的社交方式是：", "category": "theory", "test_type": "Enneagram", "options": ["主動參與", "保持距離", "深度交流", "適度參與"]},
    ]
    for q in questions:
        db.add(TestQuestion(
            text=q["text"],
            category=q["category"],
            test_type=q["test_type"],
            options=json.dumps(q["options"], ensure_ascii=False),
            weight=""
        ))
    db.commit()
    print(f"已插入 {len(questions)} 題 Enneagram 補充題目")

def insert_missing_questions():
    db = next(get_db())
    
    # DISC 補充1題
    disc_questions = [
        {"text": "面對新的工作環境，你會：", "category": "situation", "test_type": "DISC", "options": ["主動適應，快速融入", "觀察環境，制定策略", "尋求同事幫助", "保持原有工作方式"]},
    ]
    
    # Big5 補充18題
    big5_questions = [
        {"text": "面對陌生環境，你會：", "category": "situation", "test_type": "Big5", "options": ["主動探索，結識新朋友", "觀察環境，了解規則", "尋找熟悉的人", "保持低調，慢慢適應"]},
        {"text": "需要表達不同意見時，你會：", "category": "situation", "test_type": "Big5", "options": ["直接表達，據理力爭", "委婉提出，尋求共識", "私下溝通，避免衝突", "保持沉默，順從多數"]},
        {"text": "面對時間壓力，你會：", "category": "situation", "test_type": "Big5", "options": ["加快速度，提高效率", "重新規劃，優化流程", "尋求協助，分工合作", "延長工作時間"]},
        {"text": "需要學習新技術，你會：", "category": "situation", "test_type": "Big5", "options": ["立即開始，邊學邊做", "系統學習，掌握理論", "參加培訓，與人交流", "觀摩他人，模仿學習"]},
        {"text": "面對團隊分歧，你會：", "category": "situation", "test_type": "Big5", "options": ["積極調解，促進和諧", "分析原因，提出方案", "保持中立，避免選邊", "支持多數，維護團結"]},
        {"text": "需要承擔責任時，你會：", "category": "situation", "test_type": "Big5", "options": ["主動承擔，迎接挑戰", "仔細評估，確保能力", "尋求支持，共同承擔", "謹慎考慮，避免風險"]},
        {"text": "面對批評意見，你會：", "category": "situation", "test_type": "Big5", "options": ["認真聽取，積極改進", "分析內容，理性回應", "尋求更多意見", "反思自己，吸取教訓"]},
        {"text": "需要創新思維時，你會：", "category": "situation", "test_type": "Big5", "options": ["大膽想像，突破常規", "系統思考，邏輯創新", "集思廣益，團隊創新", "深入研究，穩健創新"]},
        {"text": "面對人際衝突，你會：", "category": "situation", "test_type": "Big5", "options": ["直接面對，快速解決", "分析根源，制定方案", "尋求調解，促進和解", "避免對立，尋求妥協"]},
        {"text": "需要做出選擇時，你會：", "category": "situation", "test_type": "Big5", "options": ["相信直覺，快速決定", "收集資訊，分析利弊", "諮詢他人，尋求建議", "仔細考慮，謹慎選擇"]},
        {"text": "面對工作挑戰，你會：", "category": "situation", "test_type": "Big5", "options": ["迎難而上，克服困難", "制定計劃，逐步解決", "尋求幫助，共同面對", "評估風險，選擇時機"]},
        {"text": "需要表達情感時，你會：", "category": "situation", "test_type": "Big5", "options": ["直接表達，真誠溝通", "理性分析，客觀表達", "尋求理解，情感共鳴", "保持克制，適度表達"]},
        {"text": "面對規則限制，你會：", "category": "situation", "test_type": "Big5", "options": ["尋求突破，創新方法", "遵守規則，確保合規", "協商調整，尋求平衡", "適應規則，靈活運用"]},
        {"text": "需要建立關係時，你會：", "category": "situation", "test_type": "Big5", "options": ["主動接觸，建立聯繫", "保持距離，專業交往", "深度交流，建立信任", "自然發展，順其自然"]},
        {"text": "面對資訊不足，你會：", "category": "situation", "test_type": "Big5", "options": ["大膽假設，快速行動", "收集資訊，充分準備", "尋求建議，集思廣益", "謹慎評估，等待時機"]},
        {"text": "需要解決問題時，你會：", "category": "situation", "test_type": "Big5", "options": ["立即行動，快速解決", "系統分析，制定方案", "團隊合作，共同解決", "深入研究，徹底解決"]},
        {"text": "面對個人目標，你會：", "category": "situation", "test_type": "Big5", "options": ["積極追求，全力以赴", "制定計劃，穩步推進", "尋求支持，共同實現", "調整目標，務實可行"]},
        {"text": "需要承擔風險時，你會：", "category": "situation", "test_type": "Big5", "options": ["大膽嘗試，接受挑戰", "評估風險，制定對策", "尋求保障，降低風險", "避免風險，選擇安全"]},
    ]
    
    # Enneagram 補充31題
    enneagram_questions = [
        {"text": "面對個人成長，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極追求，不斷突破", "系統規劃，穩步提升", "尋求指導，接受幫助", "自我反思，內在成長"]},
        {"text": "需要表達觀點時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接表達，堅持立場", "理性分析，客觀表達", "溫和表達，尋求理解", "謹慎表達，避免衝突"]},
        {"text": "面對個人價值，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極展現，追求認可", "默默實踐，用行動證明", "與人分享，共同成長", "保持謙遜，專注內在"]},
        {"text": "需要做出貢獻時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動承擔，發揮影響", "專業服務，提供價值", "關懷他人，促進和諧", "默默付出，不求回報"]},
        {"text": "面對個人需求，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極爭取，滿足需求", "理性分析，合理表達", "尋求平衡，兼顧他人", "自我調節，適應環境"]},
        {"text": "需要建立信任時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["展現能力，贏得信任", "真誠溝通，建立關係", "關懷他人，獲得信任", "保持誠信，用時間證明"]},
        {"text": "面對個人界限，你會：", "category": "situation", "test_type": "Enneagram", "options": ["明確設定，堅決維護", "靈活調整，適應情況", "尋求共識，建立平衡", "保持開放，接納變化"]},
        {"text": "需要解決衝突時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接面對，快速解決", "分析原因，制定方案", "調解各方，促進和解", "避免對立，尋求妥協"]},
        {"text": "面對個人責任，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動承擔，全力以赴", "仔細評估，確保能力", "尋求支持，共同承擔", "謹慎考慮，避免風險"]},
        {"text": "需要表達情感時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接表達，真誠溝通", "理性分析，客觀表達", "溫和表達，尋求理解", "保持克制，適度表達"]},
        {"text": "面對個人目標，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極追求，全力以赴", "制定計劃，穩步推進", "尋求支持，共同實現", "調整目標，務實可行"]},
        {"text": "需要建立關係時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動接觸，建立聯繫", "保持距離，專業交往", "深度交流，建立信任", "自然發展，順其自然"]},
        {"text": "面對個人價值觀，你會：", "category": "situation", "test_type": "Enneagram", "options": ["堅持原則，捍衛價值", "理性思考，客觀評估", "尋求共識，促進理解", "保持開放，接納多元"]},
        {"text": "需要做出選擇時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["相信直覺，快速決定", "收集資訊，分析利弊", "諮詢他人，尋求建議", "仔細考慮，謹慎選擇"]},
        {"text": "面對個人成長，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極追求，不斷突破", "系統規劃，穩步提升", "尋求指導，接受幫助", "自我反思，內在成長"]},
        {"text": "需要表達觀點時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接表達，堅持立場", "理性分析，客觀表達", "溫和表達，尋求理解", "謹慎表達，避免衝突"]},
        {"text": "面對個人價值，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極展現，追求認可", "默默實踐，用行動證明", "與人分享，共同成長", "保持謙遜，專注內在"]},
        {"text": "需要做出貢獻時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動承擔，發揮影響", "專業服務，提供價值", "關懷他人，促進和諧", "默默付出，不求回報"]},
        {"text": "面對個人需求，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極爭取，滿足需求", "理性分析，合理表達", "尋求平衡，兼顧他人", "自我調節，適應環境"]},
        {"text": "需要建立信任時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["展現能力，贏得信任", "真誠溝通，建立關係", "關懷他人，獲得信任", "保持誠信，用時間證明"]},
        {"text": "面對個人界限，你會：", "category": "situation", "test_type": "Enneagram", "options": ["明確設定，堅決維護", "靈活調整，適應情況", "尋求共識，建立平衡", "保持開放，接納變化"]},
        {"text": "需要解決衝突時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接面對，快速解決", "分析原因，制定方案", "調解各方，促進和解", "避免對立，尋求妥協"]},
        {"text": "面對個人責任，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動承擔，全力以赴", "仔細評估，確保能力", "尋求支持，共同承擔", "謹慎考慮，避免風險"]},
        {"text": "需要表達情感時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接表達，真誠溝通", "理性分析，客觀表達", "溫和表達，尋求理解", "保持克制，適度表達"]},
        {"text": "面對個人目標，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極追求，全力以赴", "制定計劃，穩步推進", "尋求支持，共同實現", "調整目標，務實可行"]},
        {"text": "需要建立關係時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["主動接觸，建立聯繫", "保持距離，專業交往", "深度交流，建立信任", "自然發展，順其自然"]},
        {"text": "面對個人價值觀，你會：", "category": "situation", "test_type": "Enneagram", "options": ["堅持原則，捍衛價值", "理性思考，客觀評估", "尋求共識，促進理解", "保持開放，接納多元"]},
        {"text": "需要做出選擇時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["相信直覺，快速決定", "收集資訊，分析利弊", "諮詢他人，尋求建議", "仔細考慮，謹慎選擇"]},
        {"text": "面對個人成長，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極追求，不斷突破", "系統規劃，穩步提升", "尋求指導，接受幫助", "自我反思，內在成長"]},
        {"text": "需要表達觀點時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["直接表達，堅持立場", "理性分析，客觀表達", "溫和表達，尋求理解", "謹慎表達，避免衝突"]},
        {"text": "面對個人價值，你會：", "category": "situation", "test_type": "Enneagram", "options": ["積極展現，追求認可", "默默實踐，用行動證明", "與人分享，共同成長", "保持謙遜，專注內在"]},
        {"text": "面對內在恐懼時，你會：", "category": "situation", "test_type": "Enneagram", "options": ["勇敢面對，克服恐懼", "理性分析，制定策略", "尋求支持，共同面對", "接納恐懼，與之共處"]},
    ]
    
    all_questions = disc_questions + big5_questions + enneagram_questions
    
    for q in all_questions:
        db.add(TestQuestion(
            text=q["text"],
            category=q["category"],
            test_type=q["test_type"],
            options=json.dumps(q["options"], ensure_ascii=False),
            weight=""
        ))
    db.commit()
    print(f"已插入 {len(disc_questions)} 題 DISC 補充題目")
    print(f"已插入 {len(big5_questions)} 題 Big5 補充題目")
    print(f"已插入 {len(enneagram_questions)} 題 Enneagram 補充題目")
    print(f"總共插入 {len(all_questions)} 題補充題目")

if __name__ == "__main__":
    # insert_mbti_questions()
    # insert_disc_questions()
    # insert_big5_questions()
    # insert_enneagram_questions()
    insert_missing_questions() 