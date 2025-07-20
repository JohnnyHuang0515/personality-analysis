import sqlite3
import json
from typing import Dict, List, Any, Optional, Tuple
import os

class ComprehensivePersonalityAnalyzer:
    """綜合人格分析器 - 整合所有測驗類型的詳細分析"""
    
    def __init__(self):
        self.db_path = 'personality_test.db'
    
    def calculate_mbti_score(self, user_id: str) -> Dict[str, float]:
        """計算 MBTI 分數（處理反向計分）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.answer, tq.category, tq.weight, tq.options, tq.is_reverse
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = 'MBTI'
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        scores = {
            'E': {'total': 0, 'count': 0},
            'I': {'total': 0, 'count': 0},
            'S': {'total': 0, 'count': 0},
            'N': {'total': 0, 'count': 0},
            'T': {'total': 0, 'count': 0},
            'F': {'total': 0, 'count': 0},
            'J': {'total': 0, 'count': 0},
            'P': {'total': 0, 'count': 0}
        }
        
        for answer_data in answers_data:
            answer_text, category, weight_json, options_json, is_reverse = answer_data
            
            try:
                weight_data = json.loads(weight_json)
                options = json.loads(options_json)
                answer_index = options.index(answer_text)
                
                if isinstance(weight_data, list) and 0 <= answer_index < len(weight_data):
                    score = weight_data[answer_index]
                    
                    if is_reverse:
                        if category == 'E':
                            scores['I']['total'] += score
                            scores['I']['count'] += 1
                        elif category == 'S':
                            scores['N']['total'] += score
                            scores['N']['count'] += 1
                        elif category == 'T':
                            scores['F']['total'] += score
                            scores['F']['count'] += 1
                        elif category == 'J':
                            scores['P']['total'] += score
                            scores['P']['count'] += 1
                    else:
                        if category == 'E':
                            scores['E']['total'] += score
                            scores['E']['count'] += 1
                        elif category == 'S':
                            scores['S']['total'] += score
                            scores['S']['count'] += 1
                        elif category == 'T':
                            scores['T']['total'] += score
                            scores['T']['count'] += 1
                        elif category == 'J':
                            scores['J']['total'] += score
                            scores['J']['count'] += 1
                            
            except (ValueError, json.JSONDecodeError):
                continue
        
        final_scores = {}
        for trait, data in scores.items():
            if data['count'] > 0:
                final_scores[trait] = data['total'] / data['count']
            else:
                final_scores[trait] = 0
        
        return final_scores

    def calculate_disc_score(self, user_id: str) -> Dict[str, float]:
        """計算 DISC 分數（處理反向計分）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.answer, tq.category, tq.weight, tq.options, tq.is_reverse
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = 'DISC'
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        scores = {
            'D': {'total': 0, 'count': 0},
            'I': {'total': 0, 'count': 0},
            'S': {'total': 0, 'count': 0},
            'C': {'total': 0, 'count': 0}
        }
        
        for answer_data in answers_data:
            answer_text, category, weight_json, options_json, is_reverse = answer_data
            
            try:
                weight_data = json.loads(weight_json)
                options = json.loads(options_json)
                answer_index = options.index(answer_text)
                
                if isinstance(weight_data, list) and 0 <= answer_index < len(weight_data):
                    score = weight_data[answer_index]
                    scores[category]['total'] += score
                    scores[category]['count'] += 1
                            
            except (ValueError, json.JSONDecodeError):
                continue
        
        final_scores = {}
        for trait, data in scores.items():
            if data['count'] > 0:
                final_scores[trait] = data['total'] / data['count']
            else:
                final_scores[trait] = 0
        
        return final_scores

    def calculate_big5_score(self, user_id: str) -> Dict[str, float]:
        """計算 Big5 分數（處理反向計分）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.answer, tq.category, tq.weight, tq.options, tq.is_reverse
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = 'BIG5'
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        scores = {
            'O': {'total': 0, 'count': 0},
            'C': {'total': 0, 'count': 0},
            'E': {'total': 0, 'count': 0},
            'A': {'total': 0, 'count': 0},
            'N': {'total': 0, 'count': 0}
        }
        
        for answer_data in answers_data:
            answer_text, category, weight_json, options_json, is_reverse = answer_data
            
            try:
                weight_data = json.loads(weight_json)
                options = json.loads(options_json)
                answer_index = options.index(answer_text)
                
                if isinstance(weight_data, list) and 0 <= answer_index < len(weight_data):
                    score = weight_data[answer_index]
                    scores[category]['total'] += score
                    scores[category]['count'] += 1
                            
            except (ValueError, json.JSONDecodeError):
                continue
        
        final_scores = {}
        for trait, data in scores.items():
            if data['count'] > 0:
                final_scores[trait] = data['total'] / data['count']
            else:
                final_scores[trait] = 0
        
        return final_scores

    def calculate_enneagram_score(self, user_id: str) -> Dict[str, float]:
        """計算 Enneagram 分數（處理反向計分）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.answer, tq.category, tq.weight, tq.options, tq.is_reverse
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = 'enneagram'
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        scores = {
            '1': {'total': 0, 'count': 0},
            '2': {'total': 0, 'count': 0},
            '3': {'total': 0, 'count': 0},
            '4': {'total': 0, 'count': 0},
            '5': {'total': 0, 'count': 0},
            '6': {'total': 0, 'count': 0},
            '7': {'total': 0, 'count': 0},
            '8': {'total': 0, 'count': 0},
            '9': {'total': 0, 'count': 0}
        }
        
        for answer_data in answers_data:
            answer_text, category, weight_json, options_json, is_reverse = answer_data
            
            try:
                weight_data = json.loads(weight_json)
                options = json.loads(options_json)
                answer_index = options.index(answer_text)
                
                if isinstance(weight_data, list) and 0 <= answer_index < len(weight_data):
                    score = weight_data[answer_index]
                    scores[category]['total'] += score
                    scores[category]['count'] += 1
                            
            except (ValueError, json.JSONDecodeError):
                continue
        
        final_scores = {}
        for trait, data in scores.items():
            if data['count'] > 0:
                final_scores[trait] = data['total'] / data['count']
            else:
                final_scores[trait] = 0
        
        return final_scores

    def analyze_mbti_comprehensive(self, user_id: str) -> Dict[str, Any]:
        """MBTI 綜合分析"""
        scores = self.calculate_mbti_score(user_id)
        
        # 決定人格類型
        e_score = scores.get("E", 0)
        i_score = scores.get("I", 0)
        s_score = scores.get("S", 0)
        n_score = scores.get("N", 0)
        t_score = scores.get("T", 0)
        f_score = scores.get("F", 0)
        j_score = scores.get("J", 0)
        p_score = scores.get("P", 0)
        
        personality_type = ""
        personality_type += "E" if e_score > i_score else "I"
        personality_type += "S" if s_score > n_score else "N"
        personality_type += "T" if t_score > f_score else "F"
        personality_type += "J" if j_score > p_score else "P"
        
        # 計算偏好強度
        total_ei = e_score + i_score if (e_score + i_score) > 0 else 1
        total_sn = s_score + n_score if (s_score + n_score) > 0 else 1
        total_tf = t_score + f_score if (t_score + f_score) > 0 else 1
        total_jp = j_score + p_score if (j_score + p_score) > 0 else 1
        
        preference_strengths = {
            "E-I": (e_score / total_ei) * 100,
            "S-N": (s_score / total_sn) * 100,
            "T-F": (t_score / total_tf) * 100,
            "J-P": (j_score / total_jp) * 100
        }
        
        # MBTI 類型詳細描述
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
        
        # 組合分析
        combination_analysis = self._analyze_mbti_combination(scores)
        
        return {
            "user_id": user_id,
            "test_type": "MBTI",
            "scores": scores,
            "personality_type": personality_type,
            "description": mbti_descriptions.get(personality_type, "未知類型"),
            "preference_strengths": preference_strengths,
            "combination_analysis": combination_analysis,
            "strengths": self._get_mbti_strengths(personality_type),
            "weaknesses": self._get_mbti_weaknesses(personality_type),
            "career_suggestions": self._get_mbti_careers(personality_type),
            "communication_style": self._get_mbti_communication(personality_type),
            "work_style": self._get_mbti_work_style(personality_type),
            "development_suggestions": self._get_mbti_development(personality_type)
        }

    def analyze_disc_comprehensive(self, user_id: str) -> Dict[str, Any]:
        """DISC 綜合分析"""
        scores = self.calculate_disc_score(user_id)
        
        # 找出主要和次要風格
        disc_scores = {k: v for k, v in scores.items() if k in ['D', 'I', 'S', 'C']}
        sorted_scores = sorted(disc_scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_scores[0][0] if sorted_scores else None
        secondary_style = sorted_scores[1][0] if len(sorted_scores) > 1 else None
        
        # 風格強度分析
        total_score = sum(scores.values())
        style_intensities = {}
        for style, score in scores.items():
            style_intensities[style] = (score / total_score * 100) if total_score > 0 else 0
        
        # 組合分析
        combination_analysis = self._analyze_disc_combination(scores)
        
        disc_descriptions = {
            "D": "支配型 - 直接、果斷、結果導向",
            "I": "影響型 - 樂觀、社交、關係導向",
            "S": "穩健型 - 耐心、可靠、穩定導向",
            "C": "謹慎型 - 準確、分析、品質導向"
        }
        
        return {
            "user_id": user_id,
            "test_type": "DISC",
            "scores": scores,
            "primary_style": primary_style,
            "secondary_style": secondary_style,
            "style_intensities": style_intensities,
            "description": disc_descriptions.get(primary_style or "", "未知風格"),
            "combination_analysis": combination_analysis,
            "communication_style": self._get_disc_communication(primary_style or ""),
            "work_style": self._get_disc_work_style(primary_style or ""),
            "strengths": self._get_disc_strengths(primary_style or ""),
            "weaknesses": self._get_disc_weaknesses(primary_style or ""),
            "development_suggestions": self._get_disc_development(primary_style or "")
        }

    def analyze_big5_comprehensive(self, user_id: str) -> Dict[str, Any]:
        """Big5 綜合分析"""
        scores = self.calculate_big5_score(user_id)
        
        # 組合分析
        combination_analysis = self._analyze_big5_combination(scores)
        
        # 人格檔案
        personality_profile = self._get_big5_profile(scores)
        
        # 職業匹配
        career_matches = self._get_big5_careers(scores)
        
        return {
            "user_id": user_id,
            "test_type": "BIG5",
            "scores": scores,
            "combination_analysis": combination_analysis,
            "personality_profile": personality_profile,
            "career_matches": career_matches,
            "strengths": self._get_big5_strengths(scores),
            "weaknesses": self._get_big5_weaknesses(scores),
            "development_suggestions": self._get_big5_development(scores),
            "interpersonal_style": self._get_big5_interpersonal(scores)
        }

    def analyze_enneagram_comprehensive(self, user_id: str) -> Dict[str, Any]:
        """Enneagram 綜合分析"""
        scores = self.calculate_enneagram_score(user_id)
        
        # 找出主要類型
        primary_type = max(scores.items(), key=lambda x: x[1])[0] if scores else None
        
        # 翼型分析
        wing_analysis = self._get_enneagram_wing(primary_type or "", scores)
        
        # 三型組合
        tritype = self._get_enneagram_tritype(scores)
        
        # 健康程度評估
        health_level = self._assess_enneagram_health(scores)
        
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
            "test_type": "ENNEAGRAM",
            "scores": scores,
            "primary_type": primary_type,
            "description": enneagram_descriptions.get(primary_type or "", "未知類型"),
            "wing_analysis": wing_analysis,
            "tritype": tritype,
            "health_level": health_level,
            "fear": self._get_enneagram_fear(primary_type or ""),
            "desire": self._get_enneagram_desire(primary_type or ""),
            "growth": self._get_enneagram_growth(primary_type or ""),
            "stress": self._get_enneagram_stress(primary_type or ""),
            "strengths": self._get_enneagram_strengths(primary_type or ""),
            "weaknesses": self._get_enneagram_weaknesses(primary_type or ""),
            "development_suggestions": self._get_enneagram_development(primary_type or "")
        }

    # 輔助分析方法
    def _analyze_mbti_combination(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """分析 MBTI 組合特徵"""
        e_score = scores.get("E", 0)
        i_score = scores.get("I", 0)
        s_score = scores.get("S", 0)
        n_score = scores.get("N", 0)
        t_score = scores.get("T", 0)
        f_score = scores.get("F", 0)
        j_score = scores.get("J", 0)
        p_score = scores.get("P", 0)
        
        combinations = []
        
        # 分析各維度組合
        if e_score > i_score and s_score > n_score:
            combinations.append("外向感覺型 - 實際、社交、注重細節")
        elif e_score > i_score and n_score > s_score:
            combinations.append("外向直覺型 - 創新、社交、關注可能性")
        elif i_score > e_score and s_score > n_score:
            combinations.append("內向感覺型 - 實際、深思、注重細節")
        elif i_score > e_score and n_score > s_score:
            combinations.append("內向直覺型 - 創新、深思、關注可能性")
        
        if t_score > f_score and j_score > p_score:
            combinations.append("思考判斷型 - 邏輯、有條理、決策果斷")
        elif t_score > f_score and p_score > j_score:
            combinations.append("思考知覺型 - 邏輯、靈活、保持選項")
        elif f_score > t_score and j_score > p_score:
            combinations.append("情感判斷型 - 同理心、有條理、重視和諧")
        elif f_score > t_score and p_score > j_score:
            combinations.append("情感知覺型 - 同理心、靈活、適應性強")
        
        return {
            "combinations": combinations,
            "energy_style": "外向" if e_score > i_score else "內向",
            "information_style": "感覺" if s_score > n_score else "直覺",
            "decision_style": "思考" if t_score > f_score else "情感",
            "lifestyle_style": "判斷" if j_score > p_score else "知覺"
        }

    def _analyze_disc_combination(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """分析 DISC 組合特徵"""
        d_score = scores.get("D", 0)
        i_score = scores.get("I", 0)
        s_score = scores.get("S", 0)
        c_score = scores.get("C", 0)
        
        combinations = []
        
        # 雙風格組合分析
        if d_score > 3.5 and i_score > 3.5:
            combinations.append("D-I 組合：領導-影響型，強領導力、激勵能力")
        elif d_score > 3.5 and s_score > 3.5:
            combinations.append("D-S 組合：領導-穩健型，領導能力強、團隊合作")
        elif d_score > 3.5 and c_score > 3.5:
            combinations.append("D-C 組合：領導-謹慎型，戰略思維、品質導向")
        elif i_score > 3.5 and s_score > 3.5:
            combinations.append("I-S 組合：影響-穩健型，人際關係、團隊合作")
        elif i_score > 3.5 and c_score > 3.5:
            combinations.append("I-C 組合：影響-謹慎型，創意、品質導向")
        elif s_score > 3.5 and c_score > 3.5:
            combinations.append("S-C 組合：穩健-謹慎型，可靠執行、品質保證")
        
        return {
            "combinations": combinations,
            "leadership_style": "直接領導" if d_score > 3.5 else "支持領導" if s_score > 3.5 else "激勵領導" if i_score > 3.5 else "專業領導",
            "communication_style": "直接簡潔" if d_score > 3.5 else "熱情生動" if i_score > 3.5 else "溫和支持" if s_score > 3.5 else "精確邏輯",
            "work_style": "快速決策" if d_score > 3.5 else "創意合作" if i_score > 3.5 else "穩定可靠" if s_score > 3.5 else "系統分析"
        }

    def _analyze_big5_combination(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """分析 Big5 組合特徵"""
        o_score = scores.get("O", 0)
        c_score = scores.get("C", 0)
        e_score = scores.get("E", 0)
        a_score = scores.get("A", 0)
        n_score = scores.get("N", 0)
        
        combinations = []
        
        # 領導力組合
        if e_score > 3.5 and a_score > 3.5:
            combinations.append("高外向+高友善：社交領導者，善於激勵他人、建立團隊和諧")
        elif e_score > 3.5 and c_score > 3.5:
            combinations.append("高外向+高盡責：執行領導者，組織能力強、推動目標達成")
        
        # 創新組合
        if o_score > 3.5 and e_score > 3.5:
            combinations.append("高開放+高外向：創意領導者，創新思維、適應能力強、善於表達")
        elif o_score > 3.5 and a_score > 3.5:
            combinations.append("高開放+高友善：包容創新者，同理心強、創意思維、包容多元")
        
        # 執行組合
        if c_score > 3.5 and n_score < 2.5:
            combinations.append("高盡責+低神經質：可靠執行者，責任感強、情緒穩定、執行力高")
        elif a_score > 3.5 and c_score > 3.5:
            combinations.append("高友善+高盡責：可靠合作者，責任感強、團隊合作、支持他人")
        
        return {
            "combinations": combinations,
            "personality_type": self._get_big5_personality_type(scores),
            "work_style": self._get_big5_work_style(scores),
            "social_style": self._get_big5_social_style(scores)
        }

    # 其他輔助方法
    def _get_mbti_strengths(self, personality_type: str) -> List[str]:
        """取得 MBTI 優點"""
        strengths = {
            "INTJ": ["戰略思維", "獨立思考", "高標準", "創新能力"],
            "INTP": ["邏輯分析", "創意解決", "客觀理性", "深度思考"],
            "ENTJ": ["領導能力", "決策果斷", "組織能力", "效率導向"],
            "ENTP": ["創新思維", "適應能力", "辯論技巧", "多面性"],
            "INFJ": ["同理心", "洞察力", "理想主義", "創造力"],
            "INFP": ["創意表達", "同理心", "理想主義", "適應性"],
            "ENFJ": ["領導魅力", "同理心", "激勵能力", "組織能力"],
            "ENFP": ["熱情活力", "創意能力", "適應性", "同理心"],
            "ISTJ": ["可靠性", "組織能力", "實際性", "責任感"],
            "ISFJ": ["關懷他人", "可靠性", "實際性", "忠誠度"],
            "ESTJ": ["組織能力", "決策能力", "可靠性", "效率"],
            "ESFJ": ["社交能力", "關懷他人", "組織能力", "忠誠度"],
            "ISTP": ["解決問題", "適應能力", "實際性", "冷靜"],
            "ISFP": ["藝術感", "同理心", "適應性", "忠誠度"],
            "ESTP": ["行動力", "適應能力", "實際性", "冒險精神"],
            "ESFP": ["社交能力", "熱情活力", "適應性", "同理心"]
        }
        return strengths.get(personality_type, ["未知優點"])

    def _get_mbti_weaknesses(self, personality_type: str) -> List[str]:
        """取得 MBTI 缺點"""
        weaknesses = {
            "INTJ": ["過於完美主義", "缺乏耐心", "過於直接", "情感表達困難"],
            "INTP": ["缺乏組織", "過於理論化", "社交困難", "拖延傾向"],
            "ENTJ": ["過於專制", "缺乏耐心", "過於直接", "情感忽視"],
            "ENTP": ["缺乏耐心", "過於辯論", "缺乏組織", "承諾困難"],
            "INFJ": ["過於理想化", "過於敏感", "完美主義", "過度思考"],
            "INFP": ["過於理想化", "缺乏組織", "過於敏感", "決策困難"],
            "ENFJ": ["過於理想化", "過於敏感", "過度關懷", "完美主義"],
            "ENFP": ["缺乏組織", "過於理想化", "缺乏耐心", "過度熱情"],
            "ISTJ": ["缺乏彈性", "過於傳統", "缺乏創意", "過於嚴格"],
            "ISFJ": ["缺乏彈性", "過於傳統", "過度關懷", "缺乏自信"],
            "ESTJ": ["缺乏彈性", "過於專制", "缺乏同理心", "過於傳統"],
            "ESFJ": ["過於傳統", "過度關懷", "缺乏彈性", "過於依賴"],
            "ISTP": ["缺乏組織", "缺乏耐心", "過於獨立", "缺乏規劃"],
            "ISFP": ["缺乏組織", "缺乏自信", "過於敏感", "缺乏規劃"],
            "ESTP": ["缺乏組織", "缺乏耐心", "過於冒險", "缺乏規劃"],
            "ESFP": ["缺乏組織", "缺乏耐心", "過於依賴", "缺乏規劃"]
        }
        return weaknesses.get(personality_type, ["未知缺點"])

    def _get_mbti_careers(self, personality_type: str) -> List[str]:
        """取得 MBTI 職業建議"""
        careers = {
            "INTJ": ["科學家", "工程師", "律師", "企業家", "研究員"],
            "INTP": ["科學家", "工程師", "程式設計師", "研究員", "哲學家"],
            "ENTJ": ["企業家", "經理", "律師", "顧問", "政治家"],
            "ENTP": ["企業家", "顧問", "律師", "記者", "發明家"],
            "INFJ": ["心理學家", "作家", "教師", "社工", "藝術家"],
            "INFP": ["作家", "藝術家", "心理學家", "社工", "教師"],
            "ENFJ": ["教師", "經理", "社工", "顧問", "政治家"],
            "ENFP": ["記者", "藝術家", "教師", "顧問", "企業家"],
            "ISTJ": ["會計師", "工程師", "軍人", "警察", "經理"],
            "ISFJ": ["護士", "教師", "社工", "行政", "會計師"],
            "ESTJ": ["經理", "軍人", "警察", "會計師", "律師"],
            "ESFJ": ["教師", "護士", "社工", "經理", "行政"],
            "ISTP": ["工程師", "技師", "運動員", "警察", "軍人"],
            "ISFP": ["藝術家", "設計師", "護士", "社工", "技師"],
            "ESTP": ["企業家", "運動員", "警察", "軍人", "技師"],
            "ESFP": ["演員", "銷售員", "護士", "教師", "社工"]
        }
        return careers.get(personality_type, ["未知職業"])

    def _get_mbti_communication(self, personality_type: str) -> str:
        """取得 MBTI 溝通風格"""
        styles = {
            "INTJ": "直接、邏輯、戰略性溝通，重視效率和準確性",
            "INTP": "深度、分析、理論性溝通，喜歡探討概念和原理",
            "ENTJ": "直接、權威、效率導向溝通，善於組織和領導討論",
            "ENTP": "創意、辯論、多角度溝通，喜歡挑戰和創新思維",
            "INFJ": "深度、同理心、理想主義溝通，重視意義和價值",
            "INFP": "真誠、創意、價值導向溝通，善於表達情感和理想",
            "ENFJ": "激勵、同理心、領導性溝通，善於鼓舞和指導他人",
            "ENFP": "熱情、創意、激勵性溝通，善於激發靈感和可能性",
            "ISTJ": "實際、可靠、事實導向溝通，重視準確性和完整性",
            "ISFJ": "溫和、支持、關懷性溝通，重視和諧和實際幫助",
            "ESTJ": "直接、組織、效率導向溝通，善於管理和執行",
            "ESFJ": "熱情、支持、社交性溝通，重視關係和團隊合作",
            "ISTP": "實際、靈活、解決問題溝通，善於分析和實作",
            "ISFP": "溫和、藝術、和諧性溝通，重視美感和個人價值",
            "ESTP": "直接、行動、實用性溝通，善於快速決策和執行",
            "ESFP": "熱情、社交、娛樂性溝通，善於活躍氣氛和建立關係"
        }
        return styles.get(personality_type, "未知溝通風格")

    def _get_mbti_work_style(self, personality_type: str) -> str:
        """取得 MBTI 工作風格"""
        styles = {
            "INTJ": "戰略性、獨立、系統化工作，重視創新和效率",
            "INTP": "分析性、獨立、理論化工作，善於解決複雜問題",
            "ENTJ": "領導性、組織、效率導向工作，善於管理和決策",
            "ENTP": "創新性、適應、多樣化工作，善於創意和變革",
            "INFJ": "理想性、深度、意義導向工作，重視價值和影響",
            "INFP": "創意性、真實、價值導向工作，善於表達和創新",
            "ENFJ": "領導性、激勵、關係導向工作，善於指導和合作",
            "ENFP": "創意性、熱情、可能性導向工作，善於激勵和創新",
            "ISTJ": "實際性、可靠、系統化工作，重視品質和準確性",
            "ISFJ": "支持性、可靠、關懷導向工作，善於服務和合作",
            "ESTJ": "管理性、組織、效率導向工作，善於執行和管理",
            "ESFJ": "合作性、支持、關係導向工作，善於服務和領導",
            "ISTP": "實用性、靈活、解決問題工作，善於分析和實作",
            "ISFP": "藝術性、和諧、個人價值工作，重視美感和真實性",
            "ESTP": "行動性、靈活、實用導向工作，善於快速決策和執行",
            "ESFP": "社交性、熱情、娛樂導向工作，善於活躍氣氛和合作"
        }
        return styles.get(personality_type, "未知工作風格")

    def _get_mbti_development(self, personality_type: str) -> List[str]:
        """取得 MBTI 發展建議"""
        suggestions = {
            "INTJ": ["提升情感表達能力", "發展團隊合作技能", "改善人際關係", "接受不完美"],
            "INTP": ["提升組織能力", "改善時間管理", "發展社交技能", "增強執行力"],
            "ENTJ": ["提升同理心", "改善聆聽能力", "發展授權技能", "接受他人意見"],
            "ENTP": ["提升專注力", "改善承諾能力", "發展組織技能", "增強耐心"],
            "INFJ": ["提升現實感", "改善放鬆能力", "發展客觀性", "接受批評"],
            "INFP": ["提升組織能力", "改善決策能力", "發展現實感", "增強自信"],
            "ENFJ": ["提升客觀性", "改善邊界設定", "發展自我關懷", "接受不完美"],
            "ENFP": ["提升專注力", "改善組織能力", "發展執行力", "增強耐心"],
            "ISTJ": ["提升靈活性", "改善創新思維", "發展人際關係", "接受變化"],
            "ISFJ": ["提升自信", "改善創新思維", "發展領導技能", "增強獨立性"],
            "ESTJ": ["提升靈活性", "改善同理心", "發展創新思維", "接受差異"],
            "ESFJ": ["提升客觀性", "改善創新思維", "發展獨立性", "增強彈性"],
            "ISTP": ["提升組織能力", "改善規劃能力", "發展人際關係", "增強耐心"],
            "ISFP": ["提升組織能力", "改善自信", "發展規劃能力", "增強決策力"],
            "ESTP": ["提升組織能力", "改善規劃能力", "發展耐心", "增強深度"],
            "ESFP": ["提升組織能力", "改善規劃能力", "發展獨立性", "增強耐心"]
        }
        return suggestions.get(personality_type, ["未知發展建議"])

    def _get_disc_communication(self, primary_style: str) -> str:
        """取得 DISC 溝通風格"""
        styles = {
            "D": "直接、簡潔、命令式溝通，重視效率和結果",
            "I": "熱情、生動、故事性溝通，善於激勵和影響",
            "S": "溫和、支持、合作性溝通，重視和諧和關係",
            "C": "精確、邏輯、分析性溝通，重視準確性和品質"
        }
        return styles.get(primary_style, "未知溝通風格")

    def _get_disc_work_style(self, primary_style: str) -> str:
        """取得 DISC 工作風格"""
        styles = {
            "D": "快速、果斷、挑戰導向工作，善於領導和決策",
            "I": "創意、合作、激勵導向工作，善於創新和團隊建設",
            "S": "穩定、可靠、支持導向工作，善於合作和執行",
            "C": "精確、系統、品質導向工作，善於分析和規劃"
        }
        return styles.get(primary_style, "未知工作風格")

    def _get_disc_strengths(self, primary_style: str) -> List[str]:
        """取得 DISC 優點"""
        strengths = {
            "D": ["快速決策和行動", "強烈的領導能力", "結果導向和效率", "承擔風險的能力"],
            "I": ["強烈的人際關係能力", "激勵和鼓勵他人", "創意和創新思維", "樂觀和積極態度"],
            "S": ["強烈的團隊合作能力", "耐心和持久性", "可靠和忠誠", "和諧和穩定"],
            "C": ["強烈的分析能力", "品質導向和準確性", "系統思維和組織能力", "專業和知識"]
        }
        return strengths.get(primary_style, ["未知優點"])

    def _get_disc_weaknesses(self, primary_style: str) -> List[str]:
        """取得 DISC 缺點"""
        weaknesses = {
            "D": ["可能過於直接和強勢", "缺乏耐心和細節關注", "可能忽視他人感受", "可能過於控制"],
            "I": ["可能過於樂觀", "缺乏細節關注", "可能過於依賴他人", "可能缺乏組織能力"],
            "S": ["可能過於保守", "缺乏主動性和創新", "可能過於順從", "可能缺乏決策能力"],
            "C": ["可能過於完美主義", "缺乏靈活性和適應性", "可能過於保守", "可能缺乏人際關係技能"]
        }
        return weaknesses.get(primary_style, ["未知缺點"])

    def _get_disc_development(self, primary_style: str) -> List[str]:
        """取得 DISC 發展建議"""
        suggestions = {
            "D": ["提升耐心和聆聽能力", "發展同理心和團隊合作", "改善細節關注", "學習授權和信任他人"],
            "I": ["提升細節關注和組織能力", "發展獨立性和執行力", "改善時間管理", "學習客觀分析"],
            "S": ["提升主動性和創新思維", "發展決策能力和自信", "改善適應性和靈活性", "學習表達自己的需求"],
            "C": ["提升靈活性和適應性", "發展人際關係技能", "改善決策速度", "學習接受不完美"]
        }
        return suggestions.get(primary_style, ["未知發展建議"])

    def _get_big5_profile(self, scores: Dict[str, float]) -> str:
        """取得 Big5 人格檔案"""
        profile = "基於五因素人格模型，您的人格特質表現為：\n"
        
        trait_names = {"O": "開放性", "C": "盡責性", "E": "外向性", "A": "親和性", "N": "神經質"}
        for trait, score in scores.items():
            profile += f"- {trait_names.get(trait, trait)}: {score:.2f}/5.0\n"
        
        return profile

    def _get_big5_personality_type(self, scores: Dict[str, float]) -> str:
        """取得 Big5 人格類型"""
        o_score = scores.get("O", 0)
        c_score = scores.get("C", 0)
        e_score = scores.get("E", 0)
        a_score = scores.get("A", 0)
        n_score = scores.get("N", 0)
        
        if e_score > 3.5 and a_score > 3.5:
            return "社交領導型"
        elif o_score > 3.5 and e_score > 3.5:
            return "創意領導型"
        elif c_score > 3.5 and n_score < 2.5:
            return "可靠執行型"
        elif a_score > 3.5 and c_score > 3.5:
            return "可靠合作型"
        else:
            return "平衡發展型"

    def _get_big5_work_style(self, scores: Dict[str, float]) -> str:
        """取得 Big5 工作風格"""
        o_score = scores.get("O", 0)
        c_score = scores.get("C", 0)
        e_score = scores.get("E", 0)
        
        if e_score > 3.5 and c_score > 3.5:
            return "高效領導型工作風格，善於組織和推動團隊達成目標"
        elif o_score > 3.5 and e_score > 3.5:
            return "創意領導型工作風格，善於創新和激勵團隊"
        elif c_score > 3.5:
            return "可靠執行型工作風格，善於系統化完成任務"
        else:
            return "靈活適應型工作風格，善於應對變化和挑戰"

    def _get_big5_social_style(self, scores: Dict[str, float]) -> str:
        """取得 Big5 社交風格"""
        e_score = scores.get("E", 0)
        a_score = scores.get("A", 0)
        
        if e_score > 3.5 and a_score > 3.5:
            return "熱情友善型社交風格，善於建立和維護人際關係"
        elif e_score > 3.5:
            return "外向活躍型社交風格，善於社交和表達"
        elif a_score > 3.5:
            return "溫和合作型社交風格，善於和諧相處"
        else:
            return "獨立自主型社交風格，重視個人空間和自主性"

    def _get_big5_strengths(self, scores: Dict[str, float]) -> List[str]:
        """取得 Big5 優點"""
        strengths = []
        if scores.get("O", 0) > 3.5:
            strengths.append("開放性高，喜歡新事物和創意")
        if scores.get("C", 0) > 3.5:
            strengths.append("盡責性高，有組織和可靠")
        if scores.get("E", 0) > 3.5:
            strengths.append("外向性高，喜歡社交和刺激")
        if scores.get("A", 0) > 3.5:
            strengths.append("親和性高，友善和合作")
        if scores.get("N", 0) < 2.5:
            strengths.append("情緒穩定，不易焦慮")
        
        return strengths if strengths else ["人格特質平衡發展"]

    def _get_big5_weaknesses(self, scores: Dict[str, float]) -> List[str]:
        """取得 Big5 缺點"""
        weaknesses = []
        if scores.get("O", 0) < 2.5:
            weaknesses.append("開放性低，可能缺乏創新思維")
        if scores.get("C", 0) < 2.5:
            weaknesses.append("盡責性低，可能缺乏組織能力")
        if scores.get("E", 0) < 2.5:
            weaknesses.append("外向性低，可能缺乏社交技能")
        if scores.get("A", 0) < 2.5:
            weaknesses.append("親和性低，可能缺乏合作精神")
        if scores.get("N", 0) > 3.5:
            weaknesses.append("神經質高，可能容易焦慮")
        
        return weaknesses if weaknesses else ["人格特質發展均衡"]

    def _get_big5_development(self, scores: Dict[str, float]) -> List[str]:
        """取得 Big5 發展建議"""
        suggestions = []
        if scores.get("O", 0) < 2.5:
            suggestions.append("提升開放性：嘗試新事物、學習新技能、接受不同觀點")
        if scores.get("C", 0) < 2.5:
            suggestions.append("提升盡責性：制定計劃、改善時間管理、增強責任感")
        if scores.get("E", 0) < 2.5:
            suggestions.append("提升外向性：參與社交活動、改善溝通技能、增加人際互動")
        if scores.get("A", 0) < 2.5:
            suggestions.append("提升親和性：發展同理心、改善合作能力、增強包容性")
        if scores.get("N", 0) > 3.5:
            suggestions.append("改善情緒穩定性：學習壓力管理、發展放鬆技巧、尋求支持")
        
        return suggestions if suggestions else ["保持當前的人格特質平衡發展"]

    def _get_big5_careers(self, scores: Dict[str, float]) -> List[str]:
        """取得 Big5 職業建議"""
        careers = []
        o_score = scores.get("O", 0)
        c_score = scores.get("C", 0)
        e_score = scores.get("E", 0)
        a_score = scores.get("A", 0)
        
        if o_score > 3.5 and e_score > 3.5:
            careers.extend(["創意總監", "創業家", "研究員", "諮詢師"])
        elif e_score > 3.5 and a_score > 3.5:
            careers.extend(["教育工作者", "人力資源", "銷售經理", "公關專員"])
        elif c_score > 3.5:
            careers.extend(["會計師", "工程師", "專案經理", "品質控制"])
        elif a_score > 3.5:
            careers.extend(["護理師", "社工師", "客服專員", "輔導員"])
        else:
            careers.extend(["技術專家", "分析師", "研究員", "自由工作者"])
        
        return careers

    def _get_big5_interpersonal(self, scores: Dict[str, float]) -> str:
        """取得 Big5 人際關係風格"""
        e_score = scores.get("E", 0)
        a_score = scores.get("A", 0)
        
        if e_score > 3.5 and a_score > 3.5:
            return "熱情友善型：善於建立深度人際關係，樂於幫助他人，是團隊中的和諧因子"
        elif e_score > 3.5:
            return "外向活躍型：善於社交表達，樂於分享想法，是團體中的活力來源"
        elif a_score > 3.5:
            return "溫和合作型：善於傾聽理解，樂於支持他人，是值得信賴的朋友"
        else:
            return "獨立自主型：重視個人空間，善於獨立思考，是可靠的合作夥伴"

    def _get_enneagram_wing(self, primary_type: str, scores: Dict[str, float]) -> Optional[int]:
        """取得九型人格翼型"""
        if not primary_type:
            return None
        
        primary_num = int(primary_type)
        wing1 = primary_num - 1 if primary_num > 1 else 9
        wing2 = primary_num + 1 if primary_num < 9 else 1
        
        wing1_score = scores.get(str(wing1), 0)
        wing2_score = scores.get(str(wing2), 0)
        
        if wing1_score > wing2_score and wing1_score > 3.0:
            return wing1
        elif wing2_score > wing1_score and wing2_score > 3.0:
            return wing2
        
        return None

    def _get_enneagram_tritype(self, scores: Dict[str, float]) -> List[int]:
        """取得九型人格三型組合"""
        # 按中心分組
        head_center = {str(i): scores.get(str(i), 0) for i in [5, 6, 7]}
        heart_center = {str(i): scores.get(str(i), 0) for i in [2, 3, 4]}
        body_center = {str(i): scores.get(str(i), 0) for i in [8, 9, 1]}
        
        # 找出每個中心的最高分
        head_type = max(head_center.items(), key=lambda x: x[1])[0]
        heart_type = max(heart_center.items(), key=lambda x: x[1])[0]
        body_type = max(body_center.items(), key=lambda x: x[1])[0]
        
        return [int(head_type), int(heart_type), int(body_type)]

    def _assess_enneagram_health(self, scores: Dict[str, float]) -> str:
        """評估九型人格健康程度"""
        max_score = max(scores.values()) if scores else 0
        
        if max_score >= 4.5:
            return "健康水平：整合、成長、平衡"
        elif max_score >= 3.5:
            return "一般水平：正常、適應、功能"
        else:
            return "發展中：需要進一步成長和整合"

    def _get_enneagram_fear(self, primary_type: str) -> str:
        """取得九型人格核心恐懼"""
        fears = {
            "1": "害怕錯誤、不完美、批評",
            "2": "害怕不被愛、不被需要",
            "3": "害怕失敗、不被認可",
            "4": "害怕平凡、缺乏意義",
            "5": "害怕無能、無知",
            "6": "害怕不安全、缺乏支持",
            "7": "害怕痛苦、限制、無聊",
            "8": "害怕被控制、脆弱",
            "9": "害怕衝突、分離"
        }
        return fears.get(primary_type, "未知恐懼")

    def _get_enneagram_desire(self, primary_type: str) -> str:
        """取得九型人格基本慾望"""
        desires = {
            "1": "正直、平衡、改進",
            "2": "被愛、被認可",
            "3": "成功、被認可",
            "4": "獨特、真實",
            "5": "知識、理解",
            "6": "安全、支持",
            "7": "快樂、選擇",
            "8": "控制、保護",
            "9": "和平、和諧"
        }
        return desires.get(primary_type, "未知慾望")

    def _get_enneagram_growth(self, primary_type: str) -> str:
        """取得九型人格成長路徑"""
        growth_paths = {
            "1": "1 → 7：學習放鬆、享受、接受不完美",
            "2": "2 → 4：發展自我關懷、真實性、獨特",
            "3": "3 → 6：追求真實性、忠誠、合作",
            "4": "4 → 1：發展客觀性、原則性、改進",
            "5": "5 → 8：提升行動力、自信、保護",
            "6": "6 → 9：學習放鬆、和諧、接受",
            "7": "7 → 5：發展專注、深度、知識",
            "8": "8 → 2：發展關懷、支持、合作",
            "9": "9 → 3：提升主動性、成就、行動"
        }
        return growth_paths.get(primary_type, "未知成長路徑")

    def _get_enneagram_stress(self, primary_type: str) -> str:
        """取得九型人格壓力路徑"""
        stress_paths = {
            "1": "1 → 4：可能變得情緒化、自我中心",
            "2": "2 → 8：可能變得強勢、控制",
            "3": "3 → 9：可能變得被動、逃避",
            "4": "4 → 2：可能過度付出、依賴",
            "5": "5 → 7：可能變得分散、逃避",
            "6": "6 → 3：可能過度努力、競爭",
            "7": "7 → 1：可能變得批評、完美主義",
            "8": "8 → 5：可能變得孤立、分析",
            "9": "9 → 6：可能變得擔心、懷疑"
        }
        return stress_paths.get(primary_type, "未知壓力路徑")

    def _get_enneagram_strengths(self, primary_type: str) -> List[str]:
        """取得九型人格優點"""
        strengths = {
            "1": ["強烈的責任感和道德感", "追求完美和品質", "邏輯思維和分析能力", "改進和優化能力"],
            "2": ["強烈的人際關係能力", "同理心和關懷能力", "支持他人和團隊合作", "調解和安撫能力"],
            "3": ["強烈的成就動機和目標導向", "適應性和靈活性", "效率和實用性", "激勵和推銷能力"],
            "4": ["強烈的創意和藝術能力", "深度思考和感受能力", "獨特性和個性", "真實性和誠實"],
            "5": ["強烈的分析能力和邏輯思維", "知識豐富和專業能力", "獨立思考和行動", "觀察和分析能力"],
            "6": ["強烈的責任感和可靠性", "安全導向和警覺性", "忠誠和值得信賴", "謹慎和深思熟慮"],
            "7": ["強烈的創意和創新能力", "樂觀和積極態度", "適應性和靈活性", "激勵和啟發他人"],
            "8": ["強烈的領導能力和自信", "保護他人和正義感", "直接和坦率", "決斷和行動能力"],
            "9": ["強烈的調解和安撫能力", "包容和接受他人", "和平和和諧", "團隊合作和統一"]
        }
        return strengths.get(primary_type, ["未知優點"])

    def _get_enneagram_weaknesses(self, primary_type: str) -> List[str]:
        """取得九型人格缺點"""
        weaknesses = {
            "1": ["可能過於完美主義", "可能過於批評和嚴格", "可能缺乏靈活性", "可能忽視他人感受"],
            "2": ["可能過於依賴他人認可", "可能忽視自己的需求", "可能過於順從", "可能缺乏獨立性"],
            "3": ["可能過於注重形象", "可能忽視真實感受", "可能過於競爭", "可能缺乏深度"],
            "4": ["可能過於自我中心", "可能過於情緒化", "可能不切實際", "可能缺乏實用性"],
            "5": ["可能過於孤立", "可能缺乏實用性", "可能忽視人際關係", "可能過於理論化"],
            "6": ["可能過度擔心和焦慮", "可能過於依賴他人", "可能缺乏自信", "可能過於懷疑"],
            "7": ["可能過於分散注意力", "可能缺乏專注和深度", "可能逃避困難", "可能缺乏承諾"],
            "8": ["可能過於強勢和控制", "可能忽視他人感受", "可能過於直接", "可能缺乏耐心"],
            "9": ["可能過於被動和逃避", "可能缺乏主動性", "可能忽視自己的需求", "可能缺乏決策能力"]
        }
        return weaknesses.get(primary_type, ["未知缺點"])

    def _get_enneagram_development(self, primary_type: str) -> List[str]:
        """取得九型人格發展建議"""
        suggestions = {
            "1": ["提升靈活性和接受不完美", "發展同理心和寬容", "改善放鬆和享受能力", "學習接受批評和錯誤"],
            "2": ["提升獨立性和自我價值", "學會設定邊界和表達需求", "發展自信和決策能力", "重視自己的需求和感受"],
            "3": ["提升真實性和深度", "發展內在價值和感受", "改善放鬆和享受能力", "學習接受失敗和不完美"],
            "4": ["提升實用性和現實感", "發展客觀性和平衡", "改善情緒管理", "學習關注他人和現實"],
            "5": ["提升人際關係和溝通", "發展實用性和應用能力", "改善參與和合作", "學習表達和分享"],
            "6": ["提升自信和獨立性", "發展信任和放鬆能力", "改善決策和行動能力", "學習接受不確定性"],
            "7": ["提升專注和深度", "發展承諾和持久性", "改善面對困難的能力", "學習接受限制和痛苦"],
            "8": ["提升同理心和耐心", "發展合作和授權能力", "改善聆聽和溝通", "學習接受脆弱和依賴"],
            "9": ["提升主動性和決策能力", "發展表達自己需求的能力", "改善面對衝突的能力", "學習重視自己的需求"]
        }
        return suggestions.get(primary_type, ["未知發展建議"]) 