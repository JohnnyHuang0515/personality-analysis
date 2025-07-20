import requests
import json

def test_comprehensive_report_api():
    """測試新的綜合報告 API"""
    print("=== 測試新的綜合報告 API ===")
    
    # API 端點
    base_url = "http://localhost:8000"
    user_id = "test_user_complete"
    
    try:
        # 測試綜合報告 API
        response = requests.get(f"{base_url}/api/v1/reports/{user_id}")
        
        if response.status_code == 200:
            report = response.json()
            print("✅ 綜合報告 API 測試成功！")
            print(f"用戶 ID: {report['user_id']}")
            print(f"報告生成時間: {report['report_generated_at']}")
            
            # 顯示摘要
            summary = report['summary']
            print(f"\n📊 人格摘要:")
            print(f"  MBTI 類型: {summary['mbti_type']}")
            print(f"  DISC 主要風格: {summary['disc_primary']}")
            print(f"  Big5 類型: {summary['big5_type']}")
            print(f"  Enneagram 類型: {summary['enneagram_type']}")
            
            # 顯示詳細分析
            detailed = report['detailed_analysis']
            
            print(f"\n🔍 MBTI 詳細分析:")
            mbti = detailed['mbti']
            print(f"  人格類型: {mbti['personality_type']}")
            print(f"  描述: {mbti['description']}")
            print(f"  優點: {', '.join(mbti['strengths'][:3])}")
            print(f"  職業建議: {', '.join(mbti['career_suggestions'][:3])}")
            
            print(f"\n🔍 DISC 詳細分析:")
            disc = detailed['disc']
            print(f"  主要風格: {disc['primary_style']}")
            print(f"  描述: {disc['description']}")
            print(f"  優點: {', '.join(disc['strengths'][:3])}")
            print(f"  溝通風格: {disc['communication_style']}")
            
            print(f"\n🔍 Big5 詳細分析:")
            big5 = detailed['big5']
            print(f"  人格檔案: {big5['personality_profile'].split('：')[1].strip()}")
            print(f"  優點: {', '.join(big5['strengths'][:3])}")
            print(f"  職業匹配: {', '.join(big5['career_matches'][:3])}")
            
            print(f"\n🔍 Enneagram 詳細分析:")
            enneagram = detailed['enneagram']
            print(f"  主要類型: {enneagram['primary_type']}")
            print(f"  描述: {enneagram['description']}")
            print(f"  核心恐懼: {enneagram['fear']}")
            print(f"  基本慾望: {enneagram['desire']}")
            print(f"  成長路徑: {enneagram['growth']}")
            
            # 顯示整合洞察
            insights = report['integrated_insights']
            print(f"\n🎯 整合洞察:")
            
            leadership = insights['leadership_style']
            print(f"  領導風格: {leadership['primary_style']}")
            print(f"  領導優點: {', '.join(leadership['strengths'][:2])}")
            
            communication = insights['communication_preferences']
            print(f"  溝通方式: {communication['primary_approach']}")
            
            work_env = insights['work_environment_fit']
            print(f"  理想工作環境: {work_env['ideal_environment']}")
            
            development = insights['personal_development_priorities']
            print(f"  高優先級發展: {', '.join(development['high_priority'][:2])}")
            
        else:
            print(f"❌ API 測試失敗，狀態碼: {response.status_code}")
            print(f"錯誤信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 API 服務器，請確保服務器正在運行")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_comprehensive_report_api() 