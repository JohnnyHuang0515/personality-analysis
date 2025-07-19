from fastapi import APIRouter, HTTPException
import sqlite3
import json
from typing import List, Dict, Any

router = APIRouter()

@router.get("/questions/types")
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

@router.get("/questions/{test_type}")
def get_questions_by_type(test_type: str):
    """根據測驗類型取得題庫（隨機選取30題）"""
    try:
        # 轉換為大寫以匹配資料庫中的格式
        test_type_upper = test_type.upper()
        
        # 直接使用 SQLite 查詢，隨機選取30題
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, text, category, test_type, options, weight FROM test_question WHERE test_type = ? ORDER BY RANDOM() LIMIT 30", (test_type_upper,))
        questions = cursor.fetchall()
        
        if not questions:
            raise HTTPException(status_code=404, detail=f"找不到 {test_type_upper} 類型的題目")
        
        # 轉換為 response 格式
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
            "test_type": test_type_upper
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}")



@router.get("/questions/{test_type}/random")
def get_random_question(test_type: str):
    """取得指定類型的隨機題目"""
    try:
        # 轉換為大寫以匹配資料庫中的格式
        test_type_upper = test_type.upper()
        
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, text, category, test_type, options, weight FROM test_question WHERE test_type = ? ORDER BY RANDOM() LIMIT 1", (test_type_upper,))
        question = cursor.fetchone()
        
        if not question:
            raise HTTPException(status_code=404, detail=f"找不到 {test_type_upper} 類型的題目")
        
        conn.close()
        
        return {
            "id": question[0],
            "text": question[1],
            "category": question[2],
            "test_type": question[3],
            "options": json.loads(question[4]),
            "weight": json.loads(question[5])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗：{str(e)}") 