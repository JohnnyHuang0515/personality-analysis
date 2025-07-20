import sys
import os
import requests
import json

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.comprehensive_analysis import ComprehensivePersonalityAnalyzer

def test_comprehensive_analysis():
    """測試綜合分析器"""
    print("=== 測試綜合人格分析器 ===")
    
    # 創建分析器實例
    analyzer = ComprehensivePersonalityAnalyzer()
    
    # 測試用戶 ID
    test_user_id = "test_user_complete"
    
    print("\n=== 測試 MBTI 綜合分析 ===")
    try:
        mbti_result = analyzer.analyze_mbti_comprehensive(test_user_id)
        print(f"人格類型: {mbti_result['personality_type']}")
        print(f"描述: {mbti_result['description']}")
        print(f"得分: {mbti_result['scores']}")
        print(f"組合分析: {mbti_result['combination_analysis']}")
        print(f"優點: {mbti_result['strengths']}")
        print(f"缺點: {mbti_result['weaknesses']}")
        print(f"職業建議: {mbti_result['career_suggestions']}")
        print(f"溝通風格: {mbti_result['communication_style']}")
        print(f"工作風格: {mbti_result['work_style']}")
        print(f"發展建議: {mbti_result['development_suggestions']}")
    except Exception as e:
        print(f"MBTI 分析失敗: {e}")
    
    print("\n=== 測試 DISC 綜合分析 ===")
    try:
        disc_result = analyzer.analyze_disc_comprehensive(test_user_id)
        print(f"主要風格: {disc_result['primary_style']}")
        print(f"次要風格: {disc_result['secondary_style']}")
        print(f"描述: {disc_result['description']}")
        print(f"得分: {disc_result['scores']}")
        print(f"風格強度: {disc_result['style_intensities']}")
        print(f"組合分析: {disc_result['combination_analysis']}")
        print(f"優點: {disc_result['strengths']}")
        print(f"缺點: {disc_result['weaknesses']}")
        print(f"溝通風格: {disc_result['communication_style']}")
        print(f"工作風格: {disc_result['work_style']}")
        print(f"發展建議: {disc_result['development_suggestions']}")
    except Exception as e:
        print(f"DISC 分析失敗: {e}")
    
    print("\n=== 測試 Big5 綜合分析 ===")
    try:
        big5_result = analyzer.analyze_big5_comprehensive(test_user_id)
        print(f"人格檔案: {big5_result['personality_profile']}")
        print(f"得分: {big5_result['scores']}")
        print(f"組合分析: {big5_result['combination_analysis']}")
        print(f"優點: {big5_result['strengths']}")
        print(f"缺點: {big5_result['weaknesses']}")
        print(f"職業匹配: {big5_result['career_matches']}")
        print(f"人際關係風格: {big5_result['interpersonal_style']}")
        print(f"發展建議: {big5_result['development_suggestions']}")
    except Exception as e:
        print(f"Big5 分析失敗: {e}")
    
    print("\n=== 測試 Enneagram 綜合分析 ===")
    try:
        enneagram_result = analyzer.analyze_enneagram_comprehensive(test_user_id)
        print(f"主要類型: {enneagram_result['primary_type']}")
        print(f"描述: {enneagram_result['description']}")
        print(f"得分: {enneagram_result['scores']}")
        print(f"翼型分析: {enneagram_result['wing_analysis']}")
        print(f"三型組合: {enneagram_result['tritype']}")
        print(f"健康程度: {enneagram_result['health_level']}")
        print(f"核心恐懼: {enneagram_result['fear']}")
        print(f"基本慾望: {enneagram_result['desire']}")
        print(f"成長路徑: {enneagram_result['growth']}")
        print(f"壓力路徑: {enneagram_result['stress']}")
        print(f"優點: {enneagram_result['strengths']}")
        print(f"缺點: {enneagram_result['weaknesses']}")
        print(f"發展建議: {enneagram_result['development_suggestions']}")
    except Exception as e:
        print(f"Enneagram 分析失敗: {e}")

if __name__ == "__main__":
    test_comprehensive_analysis() 