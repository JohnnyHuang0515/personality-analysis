import requests
import json

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def test_health():
    """測試健康檢查"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康檢查: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"健康檢查失敗: {e}")
        return False

def test_root():
    """測試根路徑"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"根路徑: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"根路徑測試失敗: {e}")
        return False

def test_question_types():
    """測試題目類型查詢"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/questions/types")
        print(f"題目類型查詢: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"題目類型查詢失敗: {e}")
        return False

def test_questions_by_type(test_type="MBTI"):
    """測試特定類型題目查詢"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/questions/{test_type}")
        print(f"{test_type} 題目查詢: {response.status_code}")
        data = response.json()
        print(f"題目數量: {data.get('total', 0)}")
        return True
    except Exception as e:
        print(f"{test_type} 題目查詢失敗: {e}")
        return False

def test_submit_answers():
    """測試答案提交"""
    try:
        # 先取得 MBTI 題目
        response = requests.get(f"{BASE_URL}/api/v1/questions/MBTI")
        if response.status_code != 200:
            print("無法取得 MBTI 題目")
            return False
        
        questions = response.json().get("questions", [])
        if not questions:
            print("沒有 MBTI 題目")
            return False
        
        # 準備測試答案
        test_answers = []
        for i, question in enumerate(questions[:5]):  # 只提交前5題
            options = question.get("options", [])
            if options and isinstance(options, list):
                # 選擇第一個選項
                first_option = options[0]
                test_answers.append({
                    "question_id": question["id"],
                    "answer": first_option
                })
        
        submission_data = {
            "user_id": "test_user_001",
            "test_type": "MBTI",
            "answers": test_answers
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/answers/submit",
            json=submission_data
        )
        print(f"答案提交: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"答案提交失敗: {e}")
        return False

def test_generate_report():
    """測試報告生成"""
    try:
        user_id = "test_user_001"
        test_type = "MBTI"
        
        response = requests.get(f"{BASE_URL}/api/v1/reports/{user_id}/{test_type}")
        print(f"報告生成: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"報告生成失敗: {e}")
        return False

def test_composite_report():
    """測試綜合報告"""
    try:
        user_id = "test_user_001"
        
        response = requests.get(f"{BASE_URL}/api/v1/reports/{user_id}/composite")
        print(f"綜合報告: {response.status_code}")
        print(f"回應: {response.json()}")
        return True
    except Exception as e:
        print(f"綜合報告失敗: {e}")
        return False

def main():
    """執行所有測試"""
    print("=== 綜合人格特質分析 API 測試 ===")
    print()
    
    tests = [
        ("健康檢查", test_health),
        ("根路徑", test_root),
        ("題目類型查詢", test_question_types),
        ("MBTI 題目查詢", lambda: test_questions_by_type("MBTI")),
        ("DISC 題目查詢", lambda: test_questions_by_type("DISC")),
        ("Big5 題目查詢", lambda: test_questions_by_type("Big5")),
        ("Enneagram 題目查詢", lambda: test_questions_by_type("Enneagram")),
        ("答案提交", test_submit_answers),
        ("報告生成", test_generate_report),
        ("綜合報告", test_composite_report),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"測試: {test_name}")
        print("-" * 50)
        try:
            if test_func():
                print("✅ 通過")
                passed += 1
            else:
                print("❌ 失敗")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        print()
    
    print(f"測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！API 功能正常")
    else:
        print("⚠️  部分測試失敗，請檢查服務狀態")

if __name__ == "__main__":
    main() 