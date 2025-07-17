from fastapi import APIRouter, HTTPException
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from app.services.analysis import PersonalityAnalyzer

router = APIRouter()
analyzer = PersonalityAnalyzer()

@router.get("/reports/{user_id}/{test_type}")
def generate_report(user_id: str, test_type: str):
    """生成特定測驗類型的報告"""
    try:
        # 檢查用戶是否有該測驗的答案
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM test_answer ta
            JOIN test_question tq ON ta.question_id = tq.id
            WHERE ta.user_id = ? AND tq.test_type = ?
        """, (user_id, test_type))
        
        answer_count = cursor.fetchone()[0]
        conn.close()
        
        if answer_count == 0:
            raise HTTPException(status_code=404, detail=f"找不到用戶 {user_id} 的 {test_type} 測驗答案")
        
        # 根據測驗類型生成報告
        if test_type == "MBTI":
            report = analyzer.analyze_mbti(user_id)
        elif test_type == "DISC":
            report = analyzer.analyze_disc(user_id)
        elif test_type == "Big5":
            report = analyzer.analyze_big5(user_id)
        elif test_type == "Enneagram":
            report = analyzer.analyze_enneagram(user_id)
        else:
            raise HTTPException(status_code=400, detail=f"不支援的測驗類型：{test_type}")
        
        # 儲存報告到資料庫
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO test_report (user_id, test_type, result, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, test_type, json.dumps(report), datetime.now()))
        
        conn.commit()
        conn.close()
        
        return {
            "user_id": user_id,
            "test_type": test_type,
            "report": report,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成報告失敗：{str(e)}")

@router.get("/reports/{user_id}")
def get_user_reports(user_id: str):
    """取得用戶的所有報告"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT test_type, result, created_at
            FROM test_report
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        
        reports = cursor.fetchall()
        conn.close()
        
        report_list = []
        for r in reports:
            report_list.append({
                "test_type": r[0],
                "result": json.loads(r[1]),
                "created_at": r[2]
            })
        
        return {
            "user_id": user_id,
            "reports": report_list,
            "total": len(report_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢報告失敗：{str(e)}")

@router.get("/reports/{user_id}/composite")
def generate_composite_report(user_id: str):
    """生成綜合分析報告"""
    try:
        # 檢查用戶完成哪些測驗
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT tq.test_type, COUNT(ta.id) as answer_count
            FROM test_question tq
            LEFT JOIN test_answer ta ON tq.id = ta.question_id AND ta.user_id = ?
            GROUP BY tq.test_type
        """, (user_id,))
        
        test_status = cursor.fetchall()
        conn.close()
        
        completed_tests = []
        individual_reports = {}
        
        for test_type, answer_count in test_status:
            if answer_count > 0:
                completed_tests.append(test_type)
                # 生成個別報告
                if test_type == "MBTI":
                    individual_reports["mbti_result"] = analyzer.analyze_mbti(user_id)
                elif test_type == "DISC":
                    individual_reports["disc_result"] = analyzer.analyze_disc(user_id)
                elif test_type == "Big5":
                    individual_reports["big5_result"] = analyzer.analyze_big5(user_id)
                elif test_type == "Enneagram":
                    individual_reports["enneagram_result"] = analyzer.analyze_enneagram(user_id)
        
        if not completed_tests:
            raise HTTPException(status_code=404, detail=f"用戶 {user_id} 尚未完成任何測驗")
        
        # 生成綜合分析
        overall_analysis = _generate_overall_analysis(individual_reports)
        career_recommendations = _generate_career_recommendations(individual_reports)
        personal_development = _generate_personal_development(individual_reports)
        compatibility_insights = _generate_compatibility_insights(individual_reports)
        
        composite_report = {
            "user_id": user_id,
            "test_type": "Composite",
            "completed_tests": completed_tests,
            "overall_analysis": overall_analysis,
            "career_recommendations": career_recommendations,
            "personal_development_suggestions": personal_development,
            "compatibility_insights": compatibility_insights,
            **individual_reports
        }
        
        # 儲存綜合報告
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO test_report (user_id, test_type, result, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, "Composite", json.dumps(composite_report), datetime.now()))
        
        conn.commit()
        conn.close()
        
        return composite_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成綜合報告失敗：{str(e)}")

def _generate_overall_analysis(reports: Dict[str, Any]) -> str:
    """生成整體分析"""
    analysis_parts = []
    
    if "mbti_result" in reports:
        mbti = reports["mbti_result"]
        analysis_parts.append(f"根據 MBTI 測驗，您是 {mbti['personality_type']} 類型：{mbti['description']}")
    
    if "disc_result" in reports:
        disc = reports["disc_result"]
        analysis_parts.append(f"DISC 測驗顯示您的主要風格是 {disc['primary_style']}：{disc['description']}")
    
    if "big5_result" in reports:
        big5 = reports["big5_result"]
        analysis_parts.append(f"五大人格特質測驗顯示：{big5['description']}")
    
    if "enneagram_result" in reports:
        enneagram = reports["enneagram_result"]
        analysis_parts.append(f"九型人格測驗顯示您是第 {enneagram['primary_type']} 型：{enneagram['description']}")
    
    return "。".join(analysis_parts) + "。"

def _generate_career_recommendations(reports: Dict[str, Any]) -> List[str]:
    """生成職業建議"""
    recommendations = []
    
    if "mbti_result" in reports:
        mbti = reports["mbti_result"]
        recommendations.extend(mbti.get("career_suggestions", []))
    
    # 根據 DISC 風格添加建議
    if "disc_result" in reports:
        disc = reports["disc_result"]
        disc_careers = {
            "D": ["企業主管", "銷售經理", "創業家"],
            "I": ["公關", "行銷", "培訓師"],
            "S": ["人力資源", "客服", "行政"],
            "C": ["會計師", "分析師", "研究員"]
        }
        recommendations.extend(disc_careers.get(disc["primary_style"], []))
    
    # 去重並限制數量
    unique_recommendations = list(set(recommendations))
    return unique_recommendations[:8]  # 最多8個建議

def _generate_personal_development(reports: Dict[str, Any]) -> List[str]:
    """生成個人發展建議"""
    suggestions = []
    
    if "mbti_result" in reports:
        mbti = reports["mbti_result"]
        suggestions.append(f"發展您的優勢：{', '.join(mbti.get('strengths', [])[:3])}")
        suggestions.append(f"改善您的弱點：{', '.join(mbti.get('weaknesses', [])[:2])}")
    
    if "enneagram_result" in reports:
        enneagram = reports["enneagram_result"]
        suggestions.append(f"成長方向：{enneagram.get('growth_direction', '')}")
    
    return suggestions

def _generate_compatibility_insights(reports: Dict[str, Any]) -> Dict[str, Any]:
    """生成相容性洞察"""
    insights = {}
    
    if "mbti_result" in reports:
        mbti = reports["mbti_result"]
        insights["mbti_type"] = mbti["personality_type"]
        insights["mbti_compatibility"] = _get_mbti_compatibility(mbti["personality_type"])
    
    if "disc_result" in reports:
        disc = reports["disc_result"]
        insights["disc_style"] = disc["primary_style"]
        insights["communication_preference"] = disc["communication_style"]
    
    return insights

def _get_mbti_compatibility(personality_type: str) -> List[str]:
    """取得 MBTI 相容性建議"""
    compatibility_map = {
        "INTJ": ["ENFP", "ENTP"],
        "INTP": ["ENFJ", "ENTJ"],
        "ENTJ": ["INFP", "INTP"],
        "ENTP": ["INFJ", "INTJ"],
        "INFJ": ["ENTP", "ENFP"],
        "INFP": ["ENTJ", "ENFJ"],
        "ENFJ": ["INTP", "INFP"],
        "ENFP": ["INTJ", "INFJ"],
        "ISTJ": ["ESFP", "ENFP"],
        "ISFJ": ["ESFP", "ENFP"],
        "ESTJ": ["ISFP", "INFP"],
        "ESFJ": ["ISFP", "INFP"],
        "ISTP": ["ESFJ", "ENFJ"],
        "ISFP": ["ESTJ", "ESFJ"],
        "ESTP": ["ISFJ", "INFJ"],
        "ESFP": ["ISTJ", "ISFJ"]
    }
    return compatibility_map.get(personality_type, ["未知相容性"]) 