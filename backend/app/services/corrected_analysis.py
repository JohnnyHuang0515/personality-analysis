#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正後的計分分析服務
根據計分修正報告更新計分邏輯
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime

class CorrectedPersonalityAnalyzer:
    def __init__(self):
        self.db_path = 'personality_test.db'
    
    def get_user_answers(self, user_id: str, test_type: str) -> List[Dict[str, Any]]:
        """取得用戶特定測驗類型的答案"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight, tq.options
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
                "weight": json.loads(a[3]),
                "options": json.loads(a[4])
            }
            for a in answers
        ]
    
    def calculate_score(self, answers: List[Dict[str, Any]]) -> Dict[str, float]:
        """計算測驗分數（支援新的 JSON 格式）"""
        scores = {}
        
        for answer in answers:
            category = answer["category"]
            answer_text = answer["answer"]
            options = answer["options"]
            weight_data = answer["weight"]
            
            # 找到答案在選項中的索引
            try:
                answer_index = options.index(answer_text)
            except ValueError:
                continue
            
            # 獲取該類別的權重陣列
            if category in weight_data:
                weights = weight_data[category]
                
                # 根據答案索引獲得分數
                if 0 <= answer_index < len(weights):
                    score = weights[answer_index]
                    
                    # 累積分數
                    if category not in scores:
                        scores[category] = {'total': 0, 'count': 0}
                    
                    scores[category]['total'] += score
                    scores[category]['count'] += 1
        
        # 計算平均分
        for category in scores:
            if scores[category]['count'] > 0:
                scores[category] = scores[category]['total'] / scores[category]['count']
            else:
                scores[category] = 0
        
        return scores
    
    def analyze_mbti(self, user_id: str) -> Dict[str, Any]:
        """分析 MBTI 測驗結果"""
        # 獲取所有答案，然後過濾出 MBTI 相關的類別
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight, tq.options
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.category IN ('E', 'I', 'S', 'N', 'T', 'F', 'J', 'P')
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        answers = [
            {
                "question_id": a[0],
                "answer": a[1],
                "category": a[2],
                "weight": json.loads(a[3]),
                "options": json.loads(a[4])
            }
            for a in answers_data
        ]
        
        scores = self.calculate_score(answers)
        
        # 計算偏好強度
        e_score = scores.get("E", 0)
        i_score = scores.get("I", 0)
        s_score = scores.get("S", 0)
        n_score = scores.get("N", 0)
        t_score = scores.get("T", 0)
        f_score = scores.get("F", 0)
        j_score = scores.get("J", 0)
        p_score = scores.get("P", 0)
        
        # 決定人格類型
        personality_type = ""
        personality_type += "E" if e_score > i_score else "I"
        personality_type += "S" if s_score > n_score else "N"
        personality_type += "T" if t_score > f_score else "F"
        personality_type += "J" if j_score > p_score else "P"
        
        # 計算偏好強度百分比
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
        
        return {
            "user_id": user_id,
            "test_type": "MBTI",
            "scores": scores,
            "personality_type": personality_type,
            "description": mbti_descriptions.get(personality_type, "未知類型"),
            "preference_strengths": preference_strengths,
            "strengths": self._get_mbti_strengths(personality_type),
            "weaknesses": self._get_mbti_weaknesses(personality_type),
            "career_suggestions": self._get_mbti_careers(personality_type),
            "communication_style": self._get_mbti_communication(personality_type),
            "work_style": self._get_mbti_work_style(personality_type),
            "development_suggestions": self._get_mbti_development(personality_type)
        }
    
    def analyze_disc(self, user_id: str) -> Dict[str, Any]:
        """分析 DISC 測驗結果"""
        # 獲取所有答案，然後過濾出 DISC 相關的類別
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight, tq.options
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.category IN ('D', 'I', 'S', 'C')
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        answers = [
            {
                "question_id": a[0],
                "answer": a[1],
                "category": a[2],
                "weight": json.loads(a[3]),
                "options": json.loads(a[4])
            }
            for a in answers_data
        ]
        
        scores = self.calculate_score(answers)
        
        # 找出主要和次要風格
        disc_scores = {k: v for k, v in scores.items() if k in ['D', 'I', 'S', 'C']}
        sorted_scores = sorted(disc_scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_scores[0][0] if sorted_scores else None
        secondary_style = sorted_scores[1][0] if len(sorted_scores) > 1 else None
        
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
            "description": disc_descriptions.get(primary_style or "", "未知風格"),
            "communication_style": self._get_disc_communication(primary_style or ""),
            "work_style": self._get_disc_work_style(primary_style or "")
        }
    
    def analyze_big5(self, user_id: str) -> Dict[str, Any]:
        """分析 Big5 測驗結果"""
        # 獲取所有答案，然後過濾出 BIG5 相關的類別
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight, tq.options
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.category IN ('O', 'C', 'E', 'A', 'N')
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        answers = [
            {
                "question_id": a[0],
                "answer": a[1],
                "category": a[2],
                "weight": json.loads(a[3]),
                "options": json.loads(a[4])
            }
            for a in answers_data
        ]
        
        scores = self.calculate_score(answers)
        
        # 只保留 BIG5 相關分數
        big5_scores = {k: v for k, v in scores.items() if k in ['O', 'C', 'E', 'A', 'N']}
        
        return {
            "user_id": user_id,
            "test_type": "BIG5",
            "scores": big5_scores,
            "description": self._get_big5_description(big5_scores),
            "personality_profile": self._get_big5_profile(big5_scores)
        }
    
    def analyze_enneagram(self, user_id: str) -> Dict[str, Any]:
        """分析 Enneagram 測驗結果"""
        # 獲取所有答案，然後過濾出九型人格相關的類別
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ta.question_id, ta.answer, tq.category, tq.weight, tq.options
            FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.category IN ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        """, (user_id,))
        
        answers_data = cursor.fetchall()
        conn.close()
        
        answers = [
            {
                "question_id": a[0],
                "answer": a[1],
                "category": a[2],
                "weight": json.loads(a[3]),
                "options": json.loads(a[4])
            }
            for a in answers_data
        ]
        
        scores = self.calculate_score(answers)
        
        # 只保留九型人格相關分數
        enneagram_scores = {k: v for k, v in scores.items() if k in [str(i) for i in range(1, 10)]}
        
        # 找出主要類型
        primary_type = max(enneagram_scores.items(), key=lambda x: x[1])[0] if enneagram_scores else None
        
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
            "scores": enneagram_scores,
            "primary_type": primary_type,
            "description": enneagram_descriptions.get(primary_type or "", "未知類型"),
            "wing": self._get_enneagram_wing(primary_type or "", enneagram_scores),
            "tritype": self._get_enneagram_tritype(enneagram_scores),
            "fear": self._get_enneagram_fear(primary_type or ""),
            "desire": self._get_enneagram_desire(primary_type or ""),
            "growth": self._get_enneagram_growth(primary_type or ""),
            "stress": self._get_enneagram_stress(primary_type or "")
        }
    
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
    
    def _get_disc_communication(self, primary_style: str) -> str:
        """取得 DISC 溝通風格"""
        styles = {
            "D": "直接、簡潔、結果導向的溝通方式",
            "I": "熱情、樂觀、關係導向的溝通方式",
            "S": "耐心、支持、和諧導向的溝通方式",
            "C": "準確、詳細、品質導向的溝通方式"
        }
        return styles.get(primary_style, "未知溝通風格")
    
    def _get_disc_work_style(self, primary_style: str) -> str:
        """取得 DISC 工作風格"""
        styles = {
            "D": "快速、果斷、挑戰導向的工作方式",
            "I": "創意、合作、激勵導向的工作方式",
            "S": "穩定、可靠、支持導向的工作方式",
            "C": "精確、系統、品質導向的工作方式"
        }
        return styles.get(primary_style, "未知工作風格")
    
    def _get_big5_description(self, scores: Dict[str, float]) -> str:
        """取得 BIG5 描述"""
        descriptions = []
        
        if scores.get("O", 0) > 3.5:
            descriptions.append("開放性高，喜歡新事物和創意")
        elif scores.get("O", 0) < 2.5:
            descriptions.append("開放性低，偏好傳統和穩定")
        
        if scores.get("C", 0) > 3.5:
            descriptions.append("盡責性高，有組織和可靠")
        elif scores.get("C", 0) < 2.5:
            descriptions.append("盡責性低，較為隨性和靈活")
        
        if scores.get("E", 0) > 3.5:
            descriptions.append("外向性高，喜歡社交和刺激")
        elif scores.get("E", 0) < 2.5:
            descriptions.append("外向性低，偏好獨處和安靜")
        
        if scores.get("A", 0) > 3.5:
            descriptions.append("親和性高，友善和合作")
        elif scores.get("A", 0) < 2.5:
            descriptions.append("親和性低，較為直接和競爭")
        
        if scores.get("N", 0) > 3.5:
            descriptions.append("神經質高，容易焦慮和情緒化")
        elif scores.get("N", 0) < 2.5:
            descriptions.append("神經質低，情緒穩定和放鬆")
        
        return "；".join(descriptions) if descriptions else "人格特質平衡"
    
    def _get_big5_profile(self, scores: Dict[str, float]) -> str:
        """取得 BIG5 人格檔案"""
        profile = "基於五因素人格模型，您的人格特質表現為："
        
        for trait, score in scores.items():
            trait_names = {"O": "開放性", "C": "盡責性", "E": "外向性", "A": "親和性", "N": "神經質"}
            profile += f"\n- {trait_names.get(trait, trait)}: {score:.2f}/5.0"
        
        return profile
    
    def _get_enneagram_wing(self, primary_type: str, scores: Dict[str, float]) -> Optional[int]:
        """取得九型人格翼型"""
        if not primary_type:
            return None
        
        primary_num = int(primary_type)
        wing1 = primary_num - 1 if primary_num > 1 else 9
        wing2 = primary_num + 1 if primary_num < 9 else 1
        
        wing1_score = scores.get(str(wing1), 0)
        wing2_score = scores.get(str(wing2), 0)
        
        if wing1_score > wing2_score:
            return wing1
        elif wing2_score > wing1_score:
            return wing2
        else:
            return None
    
    def _get_enneagram_tritype(self, scores: Dict[str, float]) -> List[int]:
        """取得九型人格三元型"""
        # 心中心 (2, 3, 4)
        heart_scores = {k: v for k, v in scores.items() if k in ['2', '3', '4']}
        heart_type = max(heart_scores.items(), key=lambda x: x[1])[0] if heart_scores else None
        
        # 腦中心 (5, 6, 7)
        head_scores = {k: v for k, v in scores.items() if k in ['5', '6', '7']}
        head_type = max(head_scores.items(), key=lambda x: x[1])[0] if head_scores else None
        
        # 腹中心 (8, 9, 1)
        gut_scores = {k: v for k, v in scores.items() if k in ['8', '9', '1']}
        gut_type = max(gut_scores.items(), key=lambda x: x[1])[0] if gut_scores else None
        
        tritype = []
        if heart_type:
            tritype.append(int(heart_type))
        if head_type:
            tritype.append(int(head_type))
        if gut_type:
            tritype.append(int(gut_type))
        
        return tritype
    
    def _get_enneagram_fear(self, primary_type: str) -> str:
        """取得九型人格恐懼"""
        fears = {
            "1": "害怕犯錯和不完美",
            "2": "害怕不被需要和愛",
            "3": "害怕失敗和無價值",
            "4": "害怕平凡和缺乏身份",
            "5": "害怕無能和無知",
            "6": "害怕不安全和不確定",
            "7": "害怕痛苦和限制",
            "8": "害怕被控制和軟弱",
            "9": "害怕衝突和失去和諧"
        }
        return fears.get(primary_type, "未知恐懼")
    
    def _get_enneagram_desire(self, primary_type: str) -> str:
        """取得九型人格渴望"""
        desires = {
            "1": "渴望正確和完美",
            "2": "渴望被愛和需要",
            "3": "渴望成功和認可",
            "4": "渴望獨特和深度",
            "5": "渴望知識和理解",
            "6": "渴望安全和指導",
            "7": "渴望快樂和自由",
            "8": "渴望控制和力量",
            "9": "渴望和平和和諧"
        }
        return desires.get(primary_type, "未知渴望")
    
    def _get_enneagram_growth(self, primary_type: str) -> str:
        """取得九型人格成長方向"""
        growth = {
            "1": "向類型7發展：放鬆、享受、接受不完美",
            "2": "向類型4發展：關注自我、表達真實感受",
            "3": "向類型6發展：放慢腳步、建立深度關係",
            "4": "向類型1發展：行動、紀律、客觀",
            "5": "向類型8發展：行動、自信、與他人連結",
            "6": "向類型9發展：放鬆、信任、接受",
            "7": "向類型5發展：深度、專注、內省",
            "8": "向類型2發展：關懷、同理心、服務他人",
            "9": "向類型3發展：行動、目標、自我實現"
        }
        return growth.get(primary_type, "未知成長方向")
    
    def _get_enneagram_stress(self, primary_type: str) -> str:
        """取得九型人格壓力方向"""
        stress = {
            "1": "向類型4發展：情緒化、自我批評、退縮",
            "2": "向類型8發展：控制、憤怒、專制",
            "3": "向類型9發展：拖延、逃避、缺乏動力",
            "4": "向類型2發展：過度關懷、依賴、討好",
            "5": "向類型7發展：分散注意力、逃避、過度活動",
            "6": "向類型3發展：過度工作、競爭、焦慮",
            "7": "向類型1發展：完美主義、批評、固執",
            "8": "向類型5發展：退縮、分析、孤立",
            "9": "向類型6發展：焦慮、懷疑、過度思考"
        }
        return stress.get(primary_type, "未知壓力方向")
    
    def _get_mbti_communication(self, personality_type: str) -> str:
        """獲取 MBTI 類型的溝通風格"""
        communication_styles = {
            "INTJ": "直接、邏輯、分析性，善於戰略思考",
            "INTP": "精確、邏輯、深度分析，喜歡理論討論",
            "ENTJ": "直接、權威、效率導向，善於領導討論",
            "ENTP": "創意、辯論性、靈活，善於激發新想法",
            "INFJ": "深度、關懷、理想主義，善於理解他人",
            "INFP": "溫暖、支持性、創意，重視個人價值",
            "ENFJ": "熱情、激勵性、關懷，善於鼓舞他人",
            "ENFP": "熱情、創意、靈活，善於激勵和啟發",
            "ISTJ": "直接、事實導向、可靠，重視準確性",
            "ISFJ": "溫和、支持性、關懷，重視和諧",
            "ESTJ": "直接、組織性、效率導向，善於管理",
            "ESFJ": "溫暖、支持性、組織性，重視團隊合作",
            "ISTP": "直接、實用、靈活，善於解決問題",
            "ISFP": "溫和、支持性、實用，重視個人空間",
            "ESTP": "直接、實用、靈活，善於快速決策",
            "ESFP": "熱情、實用、支持性，善於活躍氣氛"
        }
        return communication_styles.get(personality_type, "一般溝通風格")
    
    def _get_mbti_work_style(self, personality_type: str) -> str:
        """獲取 MBTI 類型的工作風格"""
        work_styles = {
            "INTJ": "獨立、戰略性、系統性，善於長期規劃",
            "INTP": "獨立、創新、分析性，善於理論研究",
            "ENTJ": "領導性、效率導向、決策性，善於組織管理",
            "ENTP": "創新、適應性、靈活，善於創意解決問題",
            "INFJ": "理想主義、關懷、深度，善於理解他人需求",
            "INFP": "創意、支持性、價值導向，善於激勵他人",
            "ENFJ": "領導性、關懷、激勵性，善於團隊建設",
            "ENFP": "創意、適應性、激勵性，善於創新和啟發",
            "ISTJ": "可靠、組織性、效率導向，善於執行任務",
            "ISFJ": "支持性、可靠、關懷，善於團隊合作",
            "ESTJ": "組織性、效率導向、決策性，善於管理執行",
            "ESFJ": "支持性、組織性、關懷，善於團隊協調",
            "ISTP": "實用、靈活、獨立，善於技術問題解決",
            "ISFP": "支持性、實用、關懷，善於細節處理",
            "ESTP": "實用、靈活、決策性，善於快速行動",
            "ESFP": "支持性、實用、適應性，善於人際協調"
        }
        return work_styles.get(personality_type, "一般工作風格")
    
    def _get_mbti_development(self, personality_type: str) -> List[str]:
        """獲取 MBTI 類型的發展建議"""
        development_suggestions = {
            "INTJ": [
                "提升人際關係技能和團隊合作能力",
                "發展同理心和情感表達能力",
                "改善靈活性和適應性",
                "學習接受不完美和錯誤"
            ],
            "INTP": [
                "提升人際關係和溝通技能",
                "發展實用性和執行能力",
                "改善組織和時間管理",
                "學習表達情感和關懷他人"
            ],
            "ENTJ": [
                "提升聆聽和同理心能力",
                "發展耐心和細節關注",
                "改善授權和信任他人",
                "學習接受批評和不同意見"
            ],
            "ENTP": [
                "提升執行力和專注度",
                "發展耐心和細節關注",
                "改善組織和時間管理",
                "學習完成任務和承諾"
            ],
            "INFJ": [
                "提升客觀性和現實感",
                "發展決策能力和自信",
                "改善邊界設定和自我關懷",
                "學習接受批評和不同意見"
            ],
            "INFP": [
                "提升組織和執行能力",
                "發展決策能力和自信",
                "改善現實感和實用性",
                "學習設定目標和完成任務"
            ],
            "ENFJ": [
                "提升客觀性和決策能力",
                "發展邊界設定和自我關懷",
                "改善接受批評的能力",
                "學習平衡他人需求和自我需求"
            ],
            "ENFP": [
                "提升組織和執行能力",
                "發展專注度和完成能力",
                "改善時間管理和細節關注",
                "學習設定優先級和堅持到底"
            ],
            "ISTJ": [
                "提升靈活性和適應性",
                "發展創新思維和創意",
                "改善人際關係技能",
                "學習接受變化和不確定性"
            ],
            "ISFJ": [
                "提升自信和獨立性",
                "發展決策能力和領導技能",
                "改善創新思維和適應性",
                "學習表達自己的需求和想法"
            ],
            "ESTJ": [
                "提升靈活性和同理心",
                "發展創新思維和創意",
                "改善聆聽和授權能力",
                "學習接受變化和不同意見"
            ],
            "ESFJ": [
                "提升客觀性和決策能力",
                "發展創新思維和適應性",
                "改善邊界設定和自我關懷",
                "學習接受批評和不同意見"
            ],
            "ISTP": [
                "提升人際關係和溝通技能",
                "發展長期規劃和承諾能力",
                "改善組織和時間管理",
                "學習表達情感和關懷他人"
            ],
            "ISFP": [
                "提升自信和決策能力",
                "發展組織和規劃能力",
                "改善創新思維和適應性",
                "學習表達自己的需求和想法"
            ],
            "ESTP": [
                "提升耐心和細節關注",
                "發展長期規劃和承諾能力",
                "改善組織和時間管理",
                "學習聆聽和同理心"
            ],
            "ESFP": [
                "提升組織和規劃能力",
                "發展專注度和完成能力",
                "改善時間管理和細節關注",
                "學習設定優先級和堅持到底"
            ]
        }
        return development_suggestions.get(personality_type, ["持續學習和成長"]) 