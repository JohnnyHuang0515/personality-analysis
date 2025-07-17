from fastapi import FastAPI, HTTPException
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

app = FastAPI(
    title="綜合人格特質分析 API",
    description="提供 MBTI、DISC、Big5、Enneagram 四種人格測驗的完整 API 服務",
    version="1.0.0"
)

# ==================== 題庫查詢 API ====================

@app.get("/")
def read_root():
    return {"message": "綜合人格特質分析後端啟動成功"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "服務正常運行"}

@app.get("/api/v1/questions/{test_type}")
def get_questions_by_type(test_type: str):
    """根據測驗類型取得題庫"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, text, category, test_type, options, weight FROM test_question WHERE test_type = ?", (test_type,))
        questions = cursor.fetchall()
        
        if not questions:
            raise HTTPException(status_code=404, detail=f"找不到 {test_type} 類型的題目")
        
        question_list = []
        for q in questions:
            question_list.append({
                "id": q[0],
                "text": q[1],
                "category": q[2],
                "test_type": q[3],
                "options": json.loads(q[4]),
                "weight": json.loads(q[5])
            })
        
        conn.close()
        
        return {
            "questions": question_list,
            "total": len(question_list),
            "test_type": test_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}")

@app.get("/api/v1/questions/types")
def get_test_types():
    """取得所有可用的測驗類型"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type")
        type_counts = cursor.fetchall()
        
        test_types = []
        total_questions = {}
        
        for test_type, count in type_counts:
            test_types.append(test_type)
            total_questions[test_type] = count
        
        conn.close()
        
        return {
            "test_types": test_types,
            "total_questions": total_questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}")

# ==================== 答案提交 API ====================

@app.post("/api/v1/answers/submit")
def submit_test_answers(submission: Dict[str, Any]):
    """提交測驗答案"""
    try:
        user_id = submission.get("user_id")
        test_type = submission.get("test_type")
        answers = submission.get("answers", [])
        
        if not user_id or not test_type:
            raise HTTPException(status_code=400, detail="缺少必要參數")
        
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 檢查該測驗類型的總題目數
        cursor.execute("SELECT COUNT(*) FROM test_question WHERE test_type = ?", (test_type,))
        total_questions = cursor.fetchone()[0]
        
        if total_questions == 0:
            raise HTTPException(status_code=404, detail=f"找不到 {test_type} 類型的題目")
        
        # 插入答案
        answered_count = 0
        for answer_data in answers:
            question_id = answer_data.get("question_id")
            answer = answer_data.get("answer")
            
            if question_id and answer:
                cursor.execute("""
                    INSERT INTO test_answer (user_id, question_id, answer, created_at)
                    VALUES (?, ?, ?, ?)
                """, (user_id, question_id, answer, datetime.now()))
                answered_count += 1
        
        conn.commit()
        conn.close()
        
        completion_rate = (answered_count / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "user_id": user_id,
            "test_type": test_type,
            "total_questions": total_questions,
            "answered_questions": answered_count,
            "completion_rate": completion_rate,
            "message": f"成功提交 {answered_count} 題答案"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交失敗：{str(e)}")

@app.get("/api/v1/answers/{user_id}")
def get_user_answers(user_id: str):
    """取得用戶的所有答案"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, question_id, answer, created_at 
            FROM test_answer 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """, (user_id,))
        
        answers = cursor.fetchall()
        conn.close()
        
        answer_list = []
        for a in answers:
            answer_list.append({
                "id": a[0],
                "user_id": a[1],
                "question_id": a[2],
                "answer": a[3],
                "created_at": a[4]
            })
        
        return {
            "answers": answer_list,
            "total": len(answer_list),
            "user_id": user_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}")

# ==================== 報告生成 API ====================

@app.get("/api/v1/reports/{user_id}/{test_type}")
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
        
        # 簡化的報告生成邏輯
        report = {
            "user_id": user_id,
            "test_type": test_type,
            "analysis": f"這是 {test_type} 測驗的分析結果",
            "summary": f"用戶 {user_id} 完成了 {answer_count} 題 {test_type} 測驗",
            "recommendations": ["建議1", "建議2", "建議3"],
            "generated_at": datetime.now().isoformat()
        }
        
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

@app.get("/api/v1/reports/{user_id}")
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

@app.get("/api/v1/reports/{user_id}/composite")
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
        for test_type, answer_count in test_status:
            if answer_count > 0:
                completed_tests.append(test_type)
        
        if not completed_tests:
            raise HTTPException(status_code=404, detail=f"用戶 {user_id} 尚未完成任何測驗")
        
        # 生成綜合分析
        composite_report = {
            "user_id": user_id,
            "test_type": "Composite",
            "completed_tests": completed_tests,
            "overall_analysis": f"用戶已完成 {len(completed_tests)} 種測驗：{', '.join(completed_tests)}",
            "career_recommendations": ["綜合職業建議1", "綜合職業建議2"],
            "personal_development_suggestions": ["個人發展建議1", "個人發展建議2"],
            "compatibility_insights": {
                "overall_compatibility": "綜合相容性分析",
                "communication_style": "溝通風格建議"
            }
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 