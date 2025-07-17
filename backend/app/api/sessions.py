from fastapi import APIRouter, HTTPException
import sqlite3
import json
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter()

@router.post("/sessions/")
def start_session(data: Dict[str, Any]):
    """建立新的測驗 session"""
    try:
        user_id = data.get("user_id")
        test_type = data.get("test_type")
        question_ids = data.get("question_ids", [])
        
        if not user_id or not test_type or not question_ids:
            raise HTTPException(status_code=400, detail="缺少必要參數")
        
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 檢查題目是否存在
        cursor.execute("SELECT id FROM test_question WHERE test_type = ?", (test_type,))
        valid_question_ids = [row[0] for row in cursor.fetchall()]
        
        if not all(qid in valid_question_ids for qid in question_ids):
            raise HTTPException(status_code=400, detail="包含不存在的題目")
        
        # 建立 session
        session_id = int(datetime.now().timestamp() * 1000)  # 使用時間戳作為 session ID
        started_at = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO test_session (id, user_id, test_type, question_ids, started_at, status) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, user_id, test_type, json.dumps(question_ids), started_at, "in_progress")
        )
        
        conn.commit()
        conn.close()
        
        return {
            "id": session_id,
            "user_id": user_id,
            "test_type": test_type,
            "question_ids": question_ids,
            "started_at": started_at,
            "status": "in_progress"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"建立 session 失敗：{str(e)}")

@router.get("/sessions/{user_id}/{test_type}/last")
def get_last_session(user_id: str, test_type: str):
    """取得用戶最後一次的測驗 session"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 取得最後一次的 session
        cursor.execute(
            "SELECT id, question_ids, started_at, status FROM test_session WHERE user_id = ? AND test_type = ? ORDER BY started_at DESC LIMIT 1",
            (user_id, test_type)
        )
        session_row = cursor.fetchone()
        
        if not session_row:
            raise HTTPException(status_code=404, detail="找不到 session")
        
        session_id, question_ids_json, started_at, status = session_row
        question_ids = json.loads(question_ids_json)
        
        # 取得已回答的題目
        cursor.execute(
            "SELECT question_id FROM test_answer WHERE session_id = ?",
            (session_id,)
        )
        answered_questions = [row[0] for row in cursor.fetchall()]
        
        # 計算剩餘題目
        remaining_questions = [qid for qid in question_ids if qid not in answered_questions]
        
        conn.close()
        
        return {
            "session": {
                "id": session_id,
                "user_id": user_id,
                "test_type": test_type,
                "question_ids": question_ids,
                "started_at": started_at,
                "status": status
            },
            "answered_questions": answered_questions,
            "remaining_questions": remaining_questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢 session 失敗：{str(e)}") 