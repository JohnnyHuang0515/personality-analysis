from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
import logging

from ..core.database import get_db
from ..services.comprehensive_analysis import ComprehensivePersonalityAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/reports/{user_id}")
async def get_personality_report(user_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """獲取綜合人格分析報告"""
    try:
        logger.info(f"開始為用戶 {user_id} 生成綜合人格分析報告")
        
        # 創建綜合分析器
        analyzer = ComprehensivePersonalityAnalyzer()
        
        # 執行所有測驗的綜合分析
        mbti_result = analyzer.analyze_mbti_comprehensive(user_id)
        disc_result = analyzer.analyze_disc_comprehensive(user_id)
        big5_result = analyzer.analyze_big5_comprehensive(user_id)
        enneagram_result = analyzer.analyze_enneagram_comprehensive(user_id)
        
        # 整合所有結果
        comprehensive_report = {
            "user_id": user_id,
            "report_generated_at": "2024-01-01T00:00:00Z",  # 可以改為實際時間
            "summary": {
                "mbti_type": mbti_result["personality_type"],
                "disc_primary": disc_result["primary_style"],
                "big5_type": big5_result["combination_analysis"]["personality_type"],
                "enneagram_type": enneagram_result["primary_type"]
            },
            "detailed_analysis": {
                "mbti": {
                    "test_type": "MBTI",
                    "personality_type": mbti_result["personality_type"],
                    "description": mbti_result["description"],
                    "scores": mbti_result["scores"],
                    "preference_strengths": mbti_result["preference_strengths"],
                    "combination_analysis": mbti_result["combination_analysis"],
                    "strengths": mbti_result["strengths"],
                    "weaknesses": mbti_result["weaknesses"],
                    "career_suggestions": mbti_result["career_suggestions"],
                    "communication_style": mbti_result["communication_style"],
                    "work_style": mbti_result["work_style"],
                    "development_suggestions": mbti_result["development_suggestions"]
                },
                "disc": {
                    "test_type": "DISC",
                    "primary_style": disc_result["primary_style"],
                    "secondary_style": disc_result["secondary_style"],
                    "description": disc_result["description"],
                    "scores": disc_result["scores"],
                    "style_intensities": disc_result["style_intensities"],
                    "combination_analysis": disc_result["combination_analysis"],
                    "strengths": disc_result["strengths"],
                    "weaknesses": disc_result["weaknesses"],
                    "communication_style": disc_result["communication_style"],
                    "work_style": disc_result["work_style"],
                    "development_suggestions": disc_result["development_suggestions"]
                },
                "big5": {
                    "test_type": "BIG5",
                    "personality_profile": big5_result["personality_profile"],
                    "scores": big5_result["scores"],
                    "combination_analysis": big5_result["combination_analysis"],
                    "strengths": big5_result["strengths"],
                    "weaknesses": big5_result["weaknesses"],
                    "career_matches": big5_result["career_matches"],
                    "interpersonal_style": big5_result["interpersonal_style"],
                    "development_suggestions": big5_result["development_suggestions"]
                },
                "enneagram": {
                    "test_type": "ENNEAGRAM",
                    "primary_type": enneagram_result["primary_type"],
                    "description": enneagram_result["description"],
                    "scores": enneagram_result["scores"],
                    "wing_analysis": enneagram_result["wing_analysis"],
                    "tritype": enneagram_result["tritype"],
                    "health_level": enneagram_result["health_level"],
                    "fear": enneagram_result["fear"],
                    "desire": enneagram_result["desire"],
                    "growth": enneagram_result["growth"],
                    "stress": enneagram_result["stress"],
                    "strengths": enneagram_result["strengths"],
                    "weaknesses": enneagram_result["weaknesses"],
                    "development_suggestions": enneagram_result["development_suggestions"]
                }
            },
            "integrated_insights": {
                "leadership_style": _get_integrated_leadership_style(mbti_result, disc_result, big5_result, enneagram_result),
                "communication_preferences": _get_integrated_communication_style(mbti_result, disc_result, big5_result, enneagram_result),
                "work_environment_fit": _get_integrated_work_environment(mbti_result, disc_result, big5_result, enneagram_result),
                "personal_development_priorities": _get_integrated_development_priorities(mbti_result, disc_result, big5_result, enneagram_result)
            }
        }
        
        logger.info(f"成功為用戶 {user_id} 生成綜合人格分析報告")
        return comprehensive_report
        
    except Exception as e:
        logger.error(f"生成綜合人格分析報告時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成報告失敗: {str(e)}")

def _get_integrated_leadership_style(mbti_result: Dict, disc_result: Dict, big5_result: Dict, enneagram_result: Dict) -> Dict[str, Any]:
    """整合領導風格分析"""
    mbti_type = mbti_result.get("personality_type", "")
    disc_primary = disc_result.get("primary_style", "")
    big5_type = big5_result.get("combination_analysis", {}).get("personality_type", "")
    enneagram_type = enneagram_result.get("primary_type", "")
    
    # 分析領導傾向
    leadership_traits = []
    
    # MBTI 領導分析
    if mbti_type.startswith("E"):
        leadership_traits.append("外向領導：善於激勵和影響他人")
    if mbti_type.endswith("J"):
        leadership_traits.append("結構化領導：重視組織和規劃")
    if "T" in mbti_type:
        leadership_traits.append("邏輯領導：基於分析和理性決策")
    
    # DISC 領導分析
    if disc_primary == "D":
        leadership_traits.append("直接領導：快速決策和行動導向")
    elif disc_primary == "I":
        leadership_traits.append("激勵領導：善於鼓舞和團隊建設")
    elif disc_primary == "S":
        leadership_traits.append("支持領導：重視和諧和團隊合作")
    elif disc_primary == "C":
        leadership_traits.append("專業領導：重視品質和系統化")
    
    # Enneagram 領導分析
    if enneagram_type in ["3", "8"]:
        leadership_traits.append("成就導向：目標明確和結果驅動")
    elif enneagram_type in ["2", "9"]:
        leadership_traits.append("服務導向：重視他人需求和團隊和諧")
    
    return {
        "primary_style": _determine_primary_leadership_style(leadership_traits),
        "strengths": leadership_traits,
        "development_areas": _get_leadership_development_areas(leadership_traits)
    }

def _get_integrated_communication_style(mbti_result: Dict, disc_result: Dict, big5_result: Dict, enneagram_result: Dict) -> Dict[str, Any]:
    """整合溝通風格分析"""
    communication_traits = []
    
    # 整合各測驗的溝通特徵
    communication_traits.append(mbti_result.get("communication_style", ""))
    communication_traits.append(disc_result.get("communication_style", ""))
    communication_traits.append(big5_result.get("interpersonal_style", ""))
    
    return {
        "primary_approach": _determine_primary_communication_approach(communication_traits),
        "strengths": [trait for trait in communication_traits if trait],
        "adaptation_suggestions": _get_communication_adaptation_suggestions(communication_traits)
    }

def _get_integrated_work_environment(mbti_result: Dict, disc_result: Dict, big5_result: Dict, enneagram_result: Dict) -> Dict[str, Any]:
    """整合工作環境適應性分析"""
    work_preferences = []
    
    # 整合工作風格偏好
    work_preferences.append(mbti_result.get("work_style", ""))
    work_preferences.append(disc_result.get("work_style", ""))
    work_preferences.append(big5_result.get("combination_analysis", {}).get("work_style", ""))
    
    return {
        "ideal_environment": _determine_ideal_work_environment(work_preferences),
        "team_dynamics": _get_team_dynamics_preferences(work_preferences),
        "stress_factors": _get_work_stress_factors(mbti_result, disc_result, big5_result, enneagram_result)
    }

def _get_integrated_development_priorities(mbti_result: Dict, disc_result: Dict, big5_result: Dict, enneagram_result: Dict) -> Dict[str, Any]:
    """整合個人發展優先級"""
    all_suggestions = []
    
    # 收集所有發展建議
    all_suggestions.extend(mbti_result.get("development_suggestions", []))
    all_suggestions.extend(disc_result.get("development_suggestions", []))
    all_suggestions.extend(big5_result.get("development_suggestions", []))
    all_suggestions.extend(enneagram_result.get("development_suggestions", []))
    
    return {
        "high_priority": _get_high_priority_development_areas(all_suggestions),
        "medium_priority": _get_medium_priority_development_areas(all_suggestions),
        "long_term_goals": _get_long_term_development_goals(all_suggestions)
    }

# 輔助函數
def _determine_primary_leadership_style(traits: List[str]) -> str:
    """確定主要領導風格"""
    if any("直接" in trait for trait in traits):
        return "直接領導型"
    elif any("激勵" in trait for trait in traits):
        return "激勵領導型"
    elif any("支持" in trait for trait in traits):
        return "支持領導型"
    elif any("專業" in trait for trait in traits):
        return "專業領導型"
    else:
        return "平衡領導型"

def _get_leadership_development_areas(traits: List[str]) -> List[str]:
    """獲取領導發展領域"""
    development_areas = []
    if not any("外向" in trait for trait in traits):
        development_areas.append("提升外向溝通和激勵能力")
    if not any("結構" in trait for trait in traits):
        development_areas.append("發展組織和規劃能力")
    if not any("邏輯" in trait for trait in traits):
        development_areas.append("增強分析和決策能力")
    return development_areas

def _determine_primary_communication_approach(traits: List[str]) -> str:
    """確定主要溝通方式"""
    if any("直接" in trait for trait in traits):
        return "直接簡潔型"
    elif any("熱情" in trait for trait in traits):
        return "熱情生動型"
    elif any("溫和" in trait for trait in traits):
        return "溫和支持型"
    elif any("精確" in trait for trait in traits):
        return "精確邏輯型"
    else:
        return "平衡適應型"

def _get_communication_adaptation_suggestions(traits: List[str]) -> List[str]:
    """獲取溝通適應建議"""
    suggestions = []
    if any("直接" in trait for trait in traits):
        suggestions.append("在需要和諧的場合，增加同理心和耐心")
    if any("熱情" in trait for trait in traits):
        suggestions.append("在正式場合，增加結構化和準確性")
    if any("溫和" in trait for trait in traits):
        suggestions.append("在需要決策的場合，增加直接性和果斷性")
    if any("精確" in trait for trait in traits):
        suggestions.append("在社交場合，增加熱情和靈活性")
    return suggestions

def _determine_ideal_work_environment(traits: List[str]) -> str:
    """確定理想工作環境"""
    if any("創新" in trait for trait in traits):
        return "創意導向環境"
    elif any("系統" in trait for trait in traits):
        return "結構化環境"
    elif any("合作" in trait for trait in traits):
        return "團隊合作環境"
    elif any("獨立" in trait for trait in traits):
        return "自主工作環境"
    else:
        return "平衡多元環境"

def _get_team_dynamics_preferences(traits: List[str]) -> List[str]:
    """獲取團隊動態偏好"""
    preferences = []
    if any("合作" in trait for trait in traits):
        preferences.append("重視團隊合作和和諧")
    if any("領導" in trait for trait in traits):
        preferences.append("傾向擔任領導角色")
    if any("支持" in trait for trait in traits):
        preferences.append("善於支持他人和調解")
    if any("專業" in trait for trait in traits):
        preferences.append("重視專業能力和品質")
    return preferences

def _get_work_stress_factors(mbti_result: Dict, disc_result: Dict, big5_result: Dict, enneagram_result: Dict) -> List[str]:
    """獲取工作壓力因素"""
    stress_factors = []
    
    # 基於各測驗結果分析壓力因素
    if mbti_result.get("personality_type", "").endswith("J"):
        stress_factors.append("缺乏結構和計劃")
    if disc_result.get("primary_style") == "D":
        stress_factors.append("缺乏控制權和決策權")
    if big5_result.get("scores", {}).get("N", 0) > 3.5:
        stress_factors.append("高壓力和不確定性環境")
    if enneagram_result.get("primary_type") == "6":
        stress_factors.append("缺乏安全感和支持")
    
    return stress_factors

def _get_high_priority_development_areas(suggestions: List[str]) -> List[str]:
    """獲取高優先級發展領域"""
    # 這裡可以根據建議的內容和頻率來確定優先級
    return suggestions[:3] if suggestions else ["持續自我反思和學習"]

def _get_medium_priority_development_areas(suggestions: List[str]) -> List[str]:
    """獲取中等優先級發展領域"""
    return suggestions[3:6] if len(suggestions) > 3 else []

def _get_long_term_development_goals(suggestions: List[str]) -> List[str]:
    """獲取長期發展目標"""
    return [
        "建立持續學習和成長的習慣",
        "發展跨文化溝通能力",
        "提升領導力和影響力",
        "建立專業網絡和關係"
    ] 