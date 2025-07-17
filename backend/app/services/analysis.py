import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime

class PersonalityAnalyzer:
    def __init__(self):
        self.db_path = 'personality_test.db'
    
    def get_user_answers(self, user_id: str, test_type: str) -> List[Dict[str, Any]]:
        """取得用戶特定測驗類型的答案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = ?
        """, (user_id, test_type))
        
        answers = cursor.fetchall()
        conn.close()
        
        return [
            {
                "question_id": a[0],
                "answer": a[1],
                "category": a[2],
                "weight": json.loads(a[3])
            }
            for a in answers
        ]
    
    def analyze_mbti(self, user_id: str) -> Dict[str, Any]:
        """分析 MBTI 測驗結果"""
        answers = self.get_user_answers(user_id, "MBTI")
        
        # 初始化分數
        scores = {
            "E": 0, "I": 0,  # Extraversion vs Introversion
            "S": 0, "N": 0,  # Sensing vs Intuition
            "T": 0, "F": 0,  # Thinking vs Feeling
            "J": 0, "P": 0   # Judging vs Perceiving
        }
        
        # 計算分數
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for dimension, score in weight[answer_value].items():
                    scores[dimension] += score
        
        # 決定人格類型
        personality_type = ""
        personality_type += "E" if scores["E"] >= scores["I"] else "I"
        personality_type += "S" if scores["S"] >= scores["N"] else "N"
        personality_type += "T" if scores["T"] >= scores["F"] else "F"
        personality_type += "J" if scores["J"] >= scores["P"] else "P"
        
        # MBTI 類型描述
        mbti_descriptions = {
            "INTJ": "建築師 - 富有想像力和戰略性的思考者",
            "INTP": "邏輯學家 - 創新的發明家",
            "ENTJ": "指揮官 - 大膽、富有想像力的強領導者",
            "ENTP": "辯論家 - 聰明好奇的思想家",
            "INFJ": "提倡者 - 安靜而神秘",
            "INFP": "調停者 - 詩意、善良的利他主義者",
            "ENFJ": "主人公 - 富有魅力和鼓舞人心的領導者",
            "ENFP": "競選者 - 熱情、有創意、社交能力強",
            "ISTJ": "物流師 - 實際和注重事實的個人",
            "ISFJ": "守衛者 - 非常專注和溫暖的守護者",
            "ESTJ": "總經理 - 優秀的管理者",
            "ESFJ": "執政官 - 非常關心和受歡迎",
            "ISTP": "鑑賞家 - 大膽而實用的實驗者",
            "ISFP": "探險家 - 靈活和有魅力的藝術家",
            "ESTP": "企業家 - 聰明、精力充沛、非常善於感知的人",
            "ESFP": "娛樂家 - 自發、精力充沛、熱情的表演者"
        }
        
        return {
            "user_id": user_id,
            "test_type": "MBTI",
            "e_i_score": scores["E"] - scores["I"],
            "s_n_score": scores["S"] - scores["N"],
            "t_f_score": scores["T"] - scores["F"],
            "j_p_score": scores["J"] - scores["P"],
            "personality_type": personality_type,
            "description": mbti_descriptions.get(personality_type, "未知類型"),
            "strengths": self._get_mbti_strengths(personality_type),
            "weaknesses": self._get_mbti_weaknesses(personality_type),
            "career_suggestions": self._get_mbti_careers(personality_type)
        }
    
    def analyze_disc(self, user_id: str) -> Dict[str, Any]:
        """分析 DISC 測驗結果"""
        answers = self.get_user_answers(user_id, "DISC")
        
        scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for dimension, score in weight[answer_value].items():
                    scores[dimension] += score
        
        # 找出主要和次要風格
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_scores[0][0]
        secondary_style = sorted_scores[1][0] if sorted_scores[1][1] > 0 else None
        
        disc_descriptions = {
            "D": "支配型 - 直接、果斷、結果導向",
            "I": "影響型 - 樂觀、社交、關係導向",
            "S": "穩健型 - 耐心、可靠、穩定導向",
            "C": "謹慎型 - 準確、分析、品質導向"
        }
        
        return {
            "user_id": user_id,
            "test_type": "DISC",
            "d_score": scores["D"],
            "i_score": scores["I"],
            "s_score": scores["S"],
            "c_score": scores["C"],
            "primary_style": primary_style,
            "secondary_style": secondary_style,
            "description": disc_descriptions.get(primary_style, "未知風格"),
            "communication_style": self._get_disc_communication(primary_style),
            "work_style": self._get_disc_work_style(primary_style)
        }
    
    def analyze_big5(self, user_id: str) -> Dict[str, Any]:
        """分析 Big5 測驗結果"""
        answers = self.get_user_answers(user_id, "Big5")
        
        scores = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        total_questions = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for dimension, score in weight[answer_value].items():
                    scores[dimension] += score
                    total_questions[dimension] += 1
        
        # 計算平均分數
        averages = {}
        for dimension in scores:
            if total_questions[dimension] > 0:
                averages[dimension] = scores[dimension] / total_questions[dimension]
            else:
                averages[dimension] = 0
        
        return {
            "user_id": user_id,
            "test_type": "Big5",
            "openness": averages["O"],
            "conscientiousness": averages["C"],
            "extraversion": averages["E"],
            "agreeableness": averages["A"],
            "neuroticism": averages["N"],
            "description": self._get_big5_description(averages),
            "personality_profile": self._get_big5_profile(averages)
        }
    
    def analyze_enneagram(self, user_id: str) -> Dict[str, Any]:
        """分析 Enneagram 測驗結果"""
        answers = self.get_user_answers(user_id, "Enneagram")
        
        scores = {str(i): 0 for i in range(1, 10)}
        
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for type_num, score in weight[answer_value].items():
                    scores[type_num] += score
        
        # 找出主要類型
        primary_type = max(scores.items(), key=lambda x: x[1])[0]
        
        enneagram_descriptions = {
            "1": "完美主義者 - 理性、理想主義、有原則",
            "2": "助人者 - 關心他人、慷慨、討人喜歡",
            "3": "成就者 - 適應性強、雄心勃勃、形象導向",
            "4": "個人主義者 - 浪漫、自我表達、戲劇性",
            "5": "調查者 - 好奇、獨立、分析性",
            "6": "忠誠者 - 負責任、焦慮、懷疑",
            "7": "冒險家 - 忙碌、有趣、分散注意力",
            "8": "挑戰者 - 強大、自信、對抗性",
            "9": "調停者 - 接受、信任、穩定"
        }
        
        return {
            "user_id": user_id,
            "test_type": "Enneagram",
            "primary_type": int(primary_type),
            "wing": self._get_enneagram_wing(primary_type, scores),
            "tritype": self._get_enneagram_tritype(scores),
            "description": enneagram_descriptions.get(primary_type, "未知類型"),
            "core_fear": self._get_enneagram_fear(primary_type),
            "core_desire": self._get_enneagram_desire(primary_type),
            "growth_direction": self._get_enneagram_growth(primary_type),
            "stress_direction": self._get_enneagram_stress(primary_type)
        }
    
    def _get_mbti_strengths(self, personality_type: str) -> List[str]:
        """取得 MBTI 優點"""
        strengths_map = {
            "INTJ": ["戰略思維", "獨立", "分析能力強"],
            "INTP": ["邏輯思維", "創新", "客觀"],
            "ENTJ": ["領導能力", "決策果斷", "組織能力強"],
            "ENTP": ["適應性強", "創意豐富", "辯論能力"],
            "INFJ": ["洞察力強", "同理心", "理想主義"],
            "INFP": ["創造力", "同理心", "忠誠"],
            "ENFJ": ["領導魅力", "同理心", "激勵他人"],
            "ENFP": ["熱情", "創意", "適應性強"],
            "ISTJ": ["可靠", "務實", "組織能力"],
            "ISFJ": ["忠誠", "實用", "關懷他人"],
            "ESTJ": ["組織能力", "決策能力", "可靠"],
            "ESFJ": ["合作", "關懷", "實用"],
            "ISTP": ["靈活", "實用", "冷靜"],
            "ISFP": ["藝術感", "同理心", "靈活"],
            "ESTP": ["行動力", "實用", "適應性強"],
            "ESFP": ["熱情", "實用", "社交能力"]
        }
        return strengths_map.get(personality_type, ["未知優點"])
    
    def _get_mbti_weaknesses(self, personality_type: str) -> List[str]:
        """取得 MBTI 缺點"""
        weaknesses_map = {
            "INTJ": ["過於完美主義", "不擅社交", "固執"],
            "INTP": ["拖延", "不切實際", "社交困難"],
            "ENTJ": ["專制", "不耐煩", "過於直接"],
            "ENTP": ["不專注", "好辯", "不穩定"],
            "INFJ": ["過於理想化", "敏感", "完美主義"],
            "INFP": ["過於理想化", "情緒化", "不切實際"],
            "ENFJ": ["過於理想化", "控制欲強", "情緒化"],
            "ENFP": ["不專注", "情緒化", "不切實際"],
            "ISTJ": ["固執", "缺乏彈性", "過於傳統"],
            "ISFJ": ["過於傳統", "缺乏自信", "過於順從"],
            "ESTJ": ["專制", "缺乏彈性", "過於直接"],
            "ESFJ": ["過於傳統", "依賴他人認同", "缺乏彈性"],
            "ISTP": ["缺乏耐心", "不擅規劃", "冷漠"],
            "ISFP": ["缺乏規劃", "過於敏感", "缺乏自信"],
            "ESTP": ["缺乏耐心", "不擅規劃", "衝動"],
            "ESFP": ["缺乏規劃", "過於依賴他人", "衝動"]
        }
        return weaknesses_map.get(personality_type, ["未知缺點"])
    
    def _get_mbti_careers(self, personality_type: str) -> List[str]:
        """取得 MBTI 職業建議"""
        careers_map = {
            "INTJ": ["科學家", "工程師", "策略顧問", "投資分析師"],
            "INTP": ["研究員", "程式設計師", "哲學家", "建築師"],
            "ENTJ": ["企業主管", "律師", "管理顧問", "政治家"],
            "ENTP": ["企業家", "律師", "記者", "行銷專家"],
            "INFJ": ["心理學家", "作家", "教師", "社工"],
            "INFP": ["作家", "藝術家", "心理學家", "社工"],
            "ENFJ": ["教師", "人力資源", "公關", "非營利組織主管"],
            "ENFP": ["記者", "演員", "教師", "行銷專家"],
            "ISTJ": ["會計師", "軍人", "警察", "行政主管"],
            "ISFJ": ["護士", "教師", "社工", "行政助理"],
            "ESTJ": ["軍官", "警察", "企業主管", "會計師"],
            "ESFJ": ["護士", "教師", "社工", "銷售員"],
            "ISTP": ["技師", "運動員", "警察", "工程師"],
            "ISFP": ["藝術家", "設計師", "護士", "技師"],
            "ESTP": ["企業家", "運動員", "銷售員", "技師"],
            "ESFP": ["演員", "銷售員", "護士", "導遊"]
        }
        return careers_map.get(personality_type, ["未知職業建議"])
    
    def _get_disc_communication(self, primary_style: str) -> str:
        """取得 DISC 溝通風格"""
        styles = {
            "D": "直接、簡潔、結果導向",
            "I": "熱情、故事性、關係導向",
            "S": "耐心、詳細、支持性",
            "C": "準確、邏輯、數據導向"
        }
        return styles.get(primary_style, "未知溝通風格")
    
    def _get_disc_work_style(self, primary_style: str) -> str:
        """取得 DISC 工作風格"""
        styles = {
            "D": "快速決策、獨立工作、挑戰導向",
            "I": "團隊合作、創意發想、激勵他人",
            "S": "穩定可靠、團隊合作、支持他人",
            "C": "精確分析、獨立工作、品質導向"
        }
        return styles.get(primary_style, "未知工作風格")
    
    def _get_big5_description(self, averages: Dict[str, float]) -> str:
        """取得 Big5 描述"""
        descriptions = []
        if averages["O"] > 0.6:
            descriptions.append("開放性高")
        elif averages["O"] < 0.4:
            descriptions.append("開放性低")
        
        if averages["C"] > 0.6:
            descriptions.append("盡責性高")
        elif averages["C"] < 0.4:
            descriptions.append("盡責性低")
        
        if averages["E"] > 0.6:
            descriptions.append("外向性高")
        elif averages["E"] < 0.4:
            descriptions.append("外向性低")
        
        if averages["A"] > 0.6:
            descriptions.append("親和性高")
        elif averages["A"] < 0.4:
            descriptions.append("親和性低")
        
        if averages["N"] > 0.6:
            descriptions.append("神經質高")
        elif averages["N"] < 0.4:
            descriptions.append("神經質低")
        
        return "、".join(descriptions) if descriptions else "各項特質均衡"
    
    def _get_big5_profile(self, averages: Dict[str, float]) -> str:
        """取得 Big5 人格檔案"""
        profile = []
        if averages["O"] > 0.7:
            profile.append("富有創意和想像力")
        if averages["C"] > 0.7:
            profile.append("可靠且有組織")
        if averages["E"] > 0.7:
            profile.append("社交且精力充沛")
        if averages["A"] > 0.7:
            profile.append("友善且合作")
        if averages["N"] < 0.3:
            profile.append("情緒穩定")
        
        return "、".join(profile) if profile else "人格特質均衡"
    
    def _get_enneagram_wing(self, primary_type: str, scores: Dict[str, int]) -> Optional[int]:
        """取得 Enneagram 翼型"""
        if primary_type == "1":
            return 2 if scores["2"] > scores["9"] else 9
        elif primary_type == "2":
            return 1 if scores["1"] > scores["3"] else 3
        elif primary_type == "3":
            return 2 if scores["2"] > scores["4"] else 4
        elif primary_type == "4":
            return 3 if scores["3"] > scores["5"] else 5
        elif primary_type == "5":
            return 4 if scores["4"] > scores["6"] else 6
        elif primary_type == "6":
            return 5 if scores["5"] > scores["7"] else 7
        elif primary_type == "7":
            return 6 if scores["6"] > scores["8"] else 8
        elif primary_type == "8":
            return 7 if scores["7"] > scores["9"] else 9
        elif primary_type == "9":
            return 8 if scores["8"] > scores["1"] else 1
        return None
    
    def _get_enneagram_tritype(self, scores: Dict[str, int]) -> List[int]:
        """取得 Enneagram 三元組"""
        # 簡化版本，取前三高分
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [int(t[0]) for t in sorted_types[:3]]
    
    def _get_enneagram_fear(self, primary_type: str) -> str:
        """取得 Enneagram 核心恐懼"""
        fears = {
            "1": "害怕犯錯、不完美",
            "2": "害怕不被需要、不被愛",
            "3": "害怕失敗、不被認可",
            "4": "害怕平凡、沒有身份",
            "5": "害怕無能、被入侵",
            "6": "害怕不安全、沒有支持",
            "7": "害怕痛苦、被限制",
            "8": "害怕被控制、軟弱",
            "9": "害怕衝突、失去和諧"
        }
        return fears.get(primary_type, "未知恐懼")
    
    def _get_enneagram_desire(self, primary_type: str) -> str:
        """取得 Enneagram 核心渴望"""
        desires = {
            "1": "渴望正確、完美",
            "2": "渴望被愛、被需要",
            "3": "渴望成功、被認可",
            "4": "渴望獨特、真實",
            "5": "渴望知識、能力",
            "6": "渴望安全、支持",
            "7": "渴望快樂、自由",
            "8": "渴望控制、力量",
            "9": "渴望和平、和諧"
        }
        return desires.get(primary_type, "未知渴望")
    
    def _get_enneagram_growth(self, primary_type: str) -> str:
        """取得 Enneagram 成長方向"""
        growth = {
            "1": "朝向類型7：放鬆、享受",
            "2": "朝向類型4：自我關懷",
            "3": "朝向類型6：真實、合作",
            "4": "朝向類型1：自律、客觀",
            "5": "朝向類型8：行動、自信",
            "6": "朝向類型9：放鬆、信任",
            "7": "朝向類型5：專注、深度",
            "8": "朝向類型2：關懷、柔軟",
            "9": "朝向類型3：行動、目標"
        }
        return growth.get(primary_type, "未知成長方向")
    
    def _get_enneagram_stress(self, primary_type: str) -> str:
        """取得 Enneagram 壓力方向"""
        stress = {
            "1": "朝向類型4：情緒化、自我批評",
            "2": "朝向類型8：控制、憤怒",
            "3": "朝向類型9：退縮、拖延",
            "4": "朝向類型2：討好、依賴",
            "5": "朝向類型7：分散、逃避",
            "6": "朝向類型3：過度工作、焦慮",
            "7": "朝向類型1：完美主義、批評",
            "8": "朝向類型5：退縮、分析",
            "9": "朝向類型6：焦慮、懷疑"
        }
        return stress.get(primary_type, "未知壓力方向") 