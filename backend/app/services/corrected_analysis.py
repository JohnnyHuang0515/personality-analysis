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
    
    def analyze_mbti_corrected(self, user_id: str) -> Dict[str, Any]:
        """
        修正後的 MBTI 分析
        根據計分修正報告：每個選項都代表一種偏好，都應該得1分
        計算相對偏好強度：E-I偏好 = (E選項數 / (E選項數 + I選項數)) × 100%
        """
        answers = self.get_user_answers(user_id, "MBTI")
        
        # 初始化選項計數
        option_counts = {
            "E": 0, "I": 0,  # Extraversion vs Introversion
            "S": 0, "N": 0,  # Sensing vs Intuition
            "T": 0, "F": 0,  # Thinking vs Feeling
            "J": 0, "P": 0   # Judging vs Perceiving
        }
        
        # 計算每個維度的選項數量
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for dimension, score in weight[answer_value].items():
                    # 每個選項都代表一種偏好，計數+1
                    option_counts[dimension] += 1
        
        # 計算相對偏好百分比
        preferences = {}
        dimension_pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
        
        for dim1, dim2 in dimension_pairs:
            total = option_counts[dim1] + option_counts[dim2]
            if total > 0:
                preferences[f"{dim1}_percentage"] = (option_counts[dim1] / total) * 100
                preferences[f"{dim2}_percentage"] = (option_counts[dim2] / total) * 100
            else:
                preferences[f"{dim1}_percentage"] = 50.0
                preferences[f"{dim2}_percentage"] = 50.0
        
        # 決定人格類型（50%以上表示偏好該方向）
        personality_type = ""
        personality_type += "E" if preferences["E_percentage"] >= 50 else "I"
        personality_type += "S" if preferences["S_percentage"] >= 50 else "N"
        personality_type += "T" if preferences["T_percentage"] >= 50 else "F"
        personality_type += "J" if preferences["J_percentage"] >= 50 else "P"
        
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
            "option_counts": option_counts,
            "preferences": preferences,
            "personality_type": personality_type,
            "description": mbti_descriptions.get(personality_type, "未知類型"),
            "strengths": self._get_mbti_strengths(personality_type),
            "weaknesses": self._get_mbti_weaknesses(personality_type),
            "career_suggestions": self._get_mbti_careers(personality_type),
            "analysis_method": "修正後計分方式：對立偏好百分比計算"
        }
    
    def analyze_disc_corrected(self, user_id: str) -> Dict[str, Any]:
        """
        修正後的 DISC 分析
        根據計分修正報告：四種風格是相互對立的行為模式
        計算相對強度：D風格強度 = (D選項數 / (D選項數 + I選項數 + S選項數 + C選項數)) × 100%
        """
        answers = self.get_user_answers(user_id, "DISC")
        
        # 初始化選項計數
        option_counts = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        # 計算每個風格的選項數量
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for style, score in weight[answer_value].items():
                    # 每個選項都代表一種風格偏好，計數+1
                    option_counts[style] += 1
        
        # 計算總選項數
        total_options = sum(option_counts.values())
        
        # 計算各風格強度百分比
        style_strengths = {}
        if total_options > 0:
            for style, count in option_counts.items():
                style_strengths[f"{style}_strength"] = (count / total_options) * 100
        else:
            # 如果沒有選項，平均分配
            for style in option_counts:
                style_strengths[f"{style}_strength"] = 25.0
        
        # 找出主要和次要風格
        sorted_strengths = sorted(style_strengths.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_strengths[0][0].split('_')[0]
        secondary_style = sorted_strengths[1][0].split('_')[0] if len(sorted_strengths) > 1 else None
        
        disc_descriptions = {
            "D": "支配型 - 直接、果斷、結果導向",
            "I": "影響型 - 樂觀、社交、關係導向",
            "S": "穩健型 - 耐心、可靠、穩定導向",
            "C": "謹慎型 - 準確、分析、品質導向"
        }
        
        return {
            "user_id": user_id,
            "test_type": "DISC",
            "option_counts": option_counts,
            "style_strengths": style_strengths,
            "primary_style": primary_style,
            "secondary_style": secondary_style,
            "description": disc_descriptions.get(primary_style, "未知風格"),
            "communication_style": self._get_disc_communication(primary_style),
            "work_style": self._get_disc_work_style(primary_style),
            "analysis_method": "修正後計分方式：四種風格相對強度計算"
        }
    
    def analyze_enneagram_corrected(self, user_id: str) -> Dict[str, Any]:
        """
        修正後的 ENNEAGRAM 分析
        根據計分修正報告：九種類型代表不同的核心動機和恐懼
        計算相對強度：類型1得分 = (類型1選項數 / (類型1選項數 + 類型2選項數 + ... + 類型9選項數)) × 100%
        """
        answers = self.get_user_answers(user_id, "ENNEAGRAM")
        
        # 初始化選項計數
        option_counts = {str(i): 0 for i in range(1, 10)}
        
        # 計算每個類型的選項數量
        for answer in answers:
            weight = answer["weight"]
            answer_value = answer["answer"]
            
            if answer_value in weight:
                for type_num, score in weight[answer_value].items():
                    # 每個選項都代表一種類型偏好，計數+1
                    option_counts[type_num] += 1
        
        # 計算總選項數
        total_options = sum(option_counts.values())
        
        # 計算各類型強度百分比
        type_strengths = {}
        if total_options > 0:
            for type_num, count in option_counts.items():
                type_strengths[f"type_{type_num}_strength"] = (count / total_options) * 100
        else:
            # 如果沒有選項，平均分配
            for type_num in option_counts:
                type_strengths[f"type_{type_num}_strength"] = 11.11  # 100/9
        
        # 找出主要類型
        primary_type = max(option_counts.items(), key=lambda x: x[1])[0]
        
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
            "option_counts": option_counts,
            "type_strengths": type_strengths,
            "primary_type": int(primary_type),
            "wing": self._get_enneagram_wing(primary_type, option_counts),
            "tritype": self._get_enneagram_tritype(option_counts),
            "description": enneagram_descriptions.get(primary_type, "未知類型"),
            "core_fear": self._get_enneagram_fear(primary_type),
            "core_desire": self._get_enneagram_desire(primary_type),
            "growth_direction": self._get_enneagram_growth(primary_type),
            "stress_direction": self._get_enneagram_stress(primary_type),
            "analysis_method": "修正後計分方式：九種類型相對強度計算"
        }
    
    def analyze_big5_corrected(self, user_id: str) -> Dict[str, Any]:
        """
        修正後的 BIG5 分析
        BIG5 的計分方式保持不變，因為它不是對立偏好，而是連續維度
        """
        answers = self.get_user_answers(user_id, "BIG5")
        
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
            "test_type": "BIG5",
            "openness": averages["O"],
            "conscientiousness": averages["C"],
            "extraversion": averages["E"],
            "agreeableness": averages["A"],
            "neuroticism": averages["N"],
            "description": self._get_big5_description(averages),
            "personality_profile": self._get_big5_profile(averages),
            "analysis_method": "BIG5計分方式：連續維度平均分數計算"
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
            "ESFJ": ["過於傳統", "缺乏彈性", "過於依賴他人"],
            "ISTP": ["缺乏耐心", "不穩定", "過於獨立"],
            "ISFP": ["缺乏規劃", "過於敏感", "不穩定"],
            "ESTP": ["缺乏耐心", "不穩定", "過於冒險"],
            "ESFP": ["缺乏規劃", "不穩定", "過於依賴他人"]
        }
        return weaknesses_map.get(personality_type, ["未知缺點"])
    
    def _get_mbti_careers(self, personality_type: str) -> List[str]:
        """取得 MBTI 職業建議"""
        careers_map = {
            "INTJ": ["科學家", "工程師", "戰略顧問", "投資分析師"],
            "INTP": ["研究員", "程式設計師", "哲學家", "建築師"],
            "ENTJ": ["企業家", "管理顧問", "律師", "執行長"],
            "ENTP": ["創業家", "銷售經理", "記者", "政治家"],
            "INFJ": ["心理學家", "作家", "教師", "社工"],
            "INFP": ["藝術家", "作家", "心理諮商師", "翻譯"],
            "ENFJ": ["教師", "人力資源經理", "公關", "非營利組織領導"],
            "ENFP": ["記者", "演員", "銷售員", "創業家"],
            "ISTJ": ["會計師", "軍人", "警察", "行政經理"],
            "ISFJ": ["護士", "社工", "行政助理", "圖書管理員"],
            "ESTJ": ["軍官", "警察", "法官", "專案經理"],
            "ESFJ": ["護士", "教師", "銷售員", "人力資源"],
            "ISTP": ["技師", "運動員", "警察", "飛行員"],
            "ISFP": ["藝術家", "設計師", "攝影師", "獸醫"],
            "ESTP": ["企業家", "運動員", "銷售員", "技師"],
            "ESFP": ["演員", "銷售員", "導遊", "活動策劃"]
        }
        return careers_map.get(personality_type, ["未知職業"])
    
    def _get_disc_communication(self, primary_style: str) -> str:
        """取得 DISC 溝通風格"""
        communication_styles = {
            "D": "直接、果斷、結果導向的溝通方式",
            "I": "熱情、樂觀、關係導向的溝通方式",
            "S": "耐心、穩定、和諧導向的溝通方式",
            "C": "準確、分析、品質導向的溝通方式"
        }
        return communication_styles.get(primary_style, "未知溝通風格")
    
    def _get_disc_work_style(self, primary_style: str) -> str:
        """取得 DISC 工作風格"""
        work_styles = {
            "D": "快速決策、直接行動、結果導向",
            "I": "創意豐富、團隊合作、激勵他人",
            "S": "穩定可靠、團隊合作、和諧工作環境",
            "C": "精確分析、品質控制、系統化工作"
        }
        return work_styles.get(primary_style, "未知工作風格")
    
    def _get_big5_description(self, averages: Dict[str, float]) -> str:
        """取得 BIG5 描述"""
        descriptions = []
        
        if averages["O"] > 3.5:
            descriptions.append("開放性高：喜歡新體驗、創意豐富")
        elif averages["O"] < 2.5:
            descriptions.append("開放性低：偏好傳統、實用")
        
        if averages["C"] > 3.5:
            descriptions.append("嚴謹性高：有組織、可靠、目標導向")
        elif averages["C"] < 2.5:
            descriptions.append("嚴謹性低：隨性、靈活、自發")
        
        if averages["E"] > 3.5:
            descriptions.append("外向性高：社交、活力充沛、積極")
        elif averages["E"] < 2.5:
            descriptions.append("外向性低：內向、安靜、深思熟慮")
        
        if averages["A"] > 3.5:
            descriptions.append("親和性高：合作、信任、同理心強")
        elif averages["A"] < 2.5:
            descriptions.append("親和性低：競爭、懷疑、直接")
        
        if averages["N"] > 3.5:
            descriptions.append("神經質高：情緒敏感、容易焦慮")
        elif averages["N"] < 2.5:
            descriptions.append("神經質低：情緒穩定、放鬆")
        
        return "；".join(descriptions) if descriptions else "人格特質平衡"
    
    def _get_big5_profile(self, averages: Dict[str, float]) -> str:
        """取得 BIG5 人格檔案"""
        profile = "五大人格特質檔案：\n"
        profile += f"開放性 (O): {averages['O']:.2f}/5.0\n"
        profile += f"嚴謹性 (C): {averages['C']:.2f}/5.0\n"
        profile += f"外向性 (E): {averages['E']:.2f}/5.0\n"
        profile += f"親和性 (A): {averages['A']:.2f}/5.0\n"
        profile += f"神經質 (N): {averages['N']:.2f}/5.0"
        return profile
    
    def _get_enneagram_wing(self, primary_type: str, option_counts: Dict[str, int]) -> Optional[int]:
        """取得 ENNEAGRAM 翼型"""
        primary_num = int(primary_type)
        
        # 翼型是相鄰的類型
        wing1 = primary_num - 1 if primary_num > 1 else 9
        wing2 = primary_num + 1 if primary_num < 9 else 1
        
        # 選擇計數較高的翼型
        if option_counts[str(wing1)] > option_counts[str(wing2)]:
            return wing1
        elif option_counts[str(wing2)] > option_counts[str(wing1)]:
            return wing2
        else:
            return None  # 沒有明顯的翼型
    
    def _get_enneagram_tritype(self, option_counts: Dict[str, int]) -> List[int]:
        """取得 ENNEAGRAM 三元型"""
        # 找出每個三元組中計數最高的類型
        centers = {
            "gut": [8, 9, 1],  # 腹中心
            "heart": [2, 3, 4],  # 心中心
            "head": [5, 6, 7]   # 腦中心
        }
        
        tritype = []
        for center_name, center_types in centers.items():
            center_scores = {str(t): option_counts[str(t)] for t in center_types}
            dominant_type = max(center_scores.items(), key=lambda x: x[1])[0]
            tritype.append(int(dominant_type))
        
        return tritype
    
    def _get_enneagram_fear(self, primary_type: str) -> str:
        """取得 ENNEAGRAM 核心恐懼"""
        fears = {
            "1": "害怕犯錯、不完美",
            "2": "害怕不被需要、不被愛",
            "3": "害怕失敗、無價值",
            "4": "害怕平凡、沒有身份",
            "5": "害怕無能、無助",
            "6": "害怕不安全、沒有支持",
            "7": "害怕痛苦、被限制",
            "8": "害怕被控制、軟弱",
            "9": "害怕衝突、失去和諧"
        }
        return fears.get(primary_type, "未知恐懼")
    
    def _get_enneagram_desire(self, primary_type: str) -> str:
        """取得 ENNEAGRAM 核心渴望"""
        desires = {
            "1": "渴望正確、完美",
            "2": "渴望被愛、被需要",
            "3": "渴望成功、被認可",
            "4": "渴望獨特、有意義",
            "5": "渴望知識、能力",
            "6": "渴望安全、支持",
            "7": "渴望快樂、自由",
            "8": "渴望控制、力量",
            "9": "渴望和平、和諧"
        }
        return desires.get(primary_type, "未知渴望")
    
    def _get_enneagram_growth(self, primary_type: str) -> str:
        """取得 ENNEAGRAM 成長方向"""
        growth = {
            "1": "朝向類型7：學習放鬆、享受生活",
            "2": "朝向類型4：學習真實表達自我",
            "3": "朝向類型6：學習真誠、忠誠",
            "4": "朝向類型1：學習紀律、客觀",
            "5": "朝向類型8：學習行動、自信",
            "6": "朝向類型9：學習放鬆、信任",
            "7": "朝向類型5：學習專注、深度",
            "8": "朝向類型2：學習關懷、同理心",
            "9": "朝向類型3：學習目標、行動"
        }
        return growth.get(primary_type, "未知成長方向")
    
    def _get_enneagram_stress(self, primary_type: str) -> str:
        """取得 ENNEAGRAM 壓力方向"""
        stress = {
            "1": "朝向類型4：變得情緒化、自我批評",
            "2": "朝向類型8：變得專制、控制",
            "3": "朝向類型9：變得被動、逃避",
            "4": "朝向類型2：變得討好、依賴",
            "5": "朝向類型7：變得分散、逃避",
            "6": "朝向類型3：變得過度競爭、焦慮",
            "7": "朝向類型1：變得完美主義、批評",
            "8": "朝向類型5：變得退縮、孤立",
            "9": "朝向類型6：變得焦慮、懷疑"
        }
        return stress.get(primary_type, "未知壓力方向")
    
    def generate_composite_report(self, user_id: str) -> Dict[str, Any]:
        """生成綜合分析報告"""
        # 獲取所有測驗的結果
        mbti_result = self.analyze_mbti_corrected(user_id)
        disc_result = self.analyze_disc_corrected(user_id)
        enneagram_result = self.analyze_enneagram_corrected(user_id)
        big5_result = self.analyze_big5_corrected(user_id)
        
        # 綜合分析
        composite_analysis = {
            "user_id": user_id,
            "test_type": "COMPOSITE",
            "individual_results": {
                "mbti": mbti_result,
                "disc": disc_result,
                "enneagram": enneagram_result,
                "big5": big5_result
            },
            "cross_analysis": self._perform_cross_analysis(mbti_result, disc_result, enneagram_result, big5_result),
            "personalized_suggestions": self._generate_personalized_suggestions(mbti_result, disc_result, enneagram_result, big5_result),
            "generated_at": datetime.now().isoformat()
        }
        
        return composite_analysis
    
    def _perform_cross_analysis(self, mbti: Dict, disc: Dict, enneagram: Dict, big5: Dict) -> Dict[str, Any]:
        """執行交叉分析"""
        analysis = {
            "leadership_style": self._analyze_leadership_style(mbti, disc),
            "communication_pattern": self._analyze_communication_pattern(mbti, disc),
            "work_preferences": self._analyze_work_preferences(mbti, disc, big5),
            "stress_management": self._analyze_stress_management(enneagram, big5),
            "growth_areas": self._analyze_growth_areas(mbti, disc, enneagram, big5)
        }
        return analysis
    
    def _generate_personalized_suggestions(self, mbti: Dict, disc: Dict, enneagram: Dict, big5: Dict) -> Dict[str, List[str]]:
        """生成個人化建議"""
        suggestions = {
            "career_development": [],
            "communication_improvement": [],
            "personal_growth": [],
            "team_work": [],
            "stress_management": []
        }
        
        # 根據各測驗結果生成建議
        # 這裡可以根據具體需求擴展
        
        return suggestions
    
    def _analyze_leadership_style(self, mbti: Dict, disc: Dict) -> str:
        """分析領導風格"""
        # 根據MBTI和DISC結果分析領導風格
        return "綜合領導風格分析"
    
    def _analyze_communication_pattern(self, mbti: Dict, disc: Dict) -> str:
        """分析溝通模式"""
        # 根據MBTI和DISC結果分析溝通模式
        return "綜合溝通模式分析"
    
    def _analyze_work_preferences(self, mbti: Dict, disc: Dict, big5: Dict) -> str:
        """分析工作偏好"""
        # 根據MBTI、DISC和BIG5結果分析工作偏好
        return "綜合工作偏好分析"
    
    def _analyze_stress_management(self, enneagram: Dict, big5: Dict) -> str:
        """分析壓力管理"""
        # 根據ENNEAGRAM和BIG5結果分析壓力管理
        return "綜合壓力管理分析"
    
    def _analyze_growth_areas(self, mbti: Dict, disc: Dict, enneagram: Dict, big5: Dict) -> List[str]:
        """分析成長領域"""
        # 根據所有測驗結果分析成長領域
        return ["個人成長領域分析"] 