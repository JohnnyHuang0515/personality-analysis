from fastapi import APIRouter, HTTPException
import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()

@router.post("/sessions/create")
def create_session(data: Dict[str, Any]):
    """建立新的測驗 session"""
    try:
        user_id = data.get("user_id")
        test_type = data.get("test_type")
        question_ids = data.get("question_ids")  # 接受前端傳遞的題目ID列表
        
        if not user_id or not test_type:
            raise HTTPException(status_code=400, detail="缺少必要參數")
        
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 如果前端沒有傳遞題目ID，則隨機選擇30題
        if not question_ids:
            cursor.execute("SELECT id FROM test_question WHERE test_type = ? ORDER BY RANDOM() LIMIT 30", (test_type,))
            question_rows = cursor.fetchall()
            
            if not question_rows:
                raise HTTPException(status_code=404, detail=f"找不到 {test_type} 類型的題目")
            
            question_ids = [row[0] for row in question_rows]
        else:
            # 驗證前端傳遞的題目ID是否都屬於該測驗類型
            cursor.execute("SELECT id FROM test_question WHERE test_type = ?", (test_type,))
            valid_question_ids = {row[0] for row in cursor.fetchall()}
            
            if not all(qid in valid_question_ids for qid in question_ids):
                raise HTTPException(status_code=400, detail="包含不屬於該測驗類型的題目")
        
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
            "session_id": session_id,
            "user_id": user_id,
            "test_type": test_type,
            "total_questions": len(question_ids),
            "question_ids": question_ids,
            "started_at": started_at,
            "status": "in_progress",
            "message": "Session created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"建立 session 失敗：{str(e)}")

@router.get("/sessions/{user_id}/{test_type}/latest")
def get_latest_session(user_id: str, test_type: str):
    """取得用戶最新的測驗 session"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 取得最新的 session
        cursor.execute(
            "SELECT id, question_ids, started_at, status FROM test_session WHERE user_id = ? AND test_type = ? ORDER BY started_at DESC LIMIT 1",
            (user_id, test_type)
        )
        session_row = cursor.fetchone()
        
        if not session_row:
            return {
                "has_session": False,
                "message": "No session found"
            }
        
        session_id, question_ids_json, started_at, status = session_row
        question_ids = json.loads(question_ids_json)
        
        # 取得已回答的題目
        cursor.execute(
            "SELECT question_id, answer, created_at FROM test_answer WHERE session_id = ?",
            (session_id,)
        )
        answered_rows = cursor.fetchall()
        
        # 構建已回答題目的詳細信息
        answered_questions = {}
        for row in answered_rows:
            question_id, answer, created_at = row
            answered_questions[str(question_id)] = {
                "answer": answer,
                "answered_at": created_at
            }
        
        # 計算進度
        answered_count = len(answered_questions)
        total_questions = len(question_ids)
        progress_percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0
        
        # 找到下一個未答題目的索引
        next_question_index = None
        remaining_questions = []
        for i, qid in enumerate(question_ids):
            if str(qid) not in answered_questions:
                remaining_questions.append(qid)
                if next_question_index is None:
                    next_question_index = i
        
        # 計算已過時間（秒）
        started_datetime = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
        current_datetime = datetime.now()
        
        # 獲取總計時時間
        cursor.execute("SELECT total_time_seconds FROM test_session WHERE id = ?", (session_id,))
        total_time_row = cursor.fetchone()
        total_time_seconds = total_time_row[0] if total_time_row else 0
        
        # 修復：直接使用總時間，不再重複計算
        elapsed_seconds = total_time_seconds
        
        conn.close()
        
        return {
            "has_session": True,
            "session_id": session_id,
            "user_id": user_id,
            "test_type": test_type,
            "total_questions": total_questions,
            "answered_count": answered_count,
            "progress_percentage": progress_percentage,
            "next_question_index": next_question_index,
            "remaining_questions": remaining_questions,
            "status": status,
            "started_at": started_at,
            "elapsed_seconds": elapsed_seconds,
            "question_ids": question_ids,
            "answered_questions": answered_questions,
            "message": "Session found"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢 session 失敗：{str(e)}")

@router.get("/sessions/{user_id}/all")
def get_all_sessions(user_id: str):
    """取得用戶的所有測驗 session"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, test_type, question_ids, started_at, status FROM test_session WHERE user_id = ? ORDER BY started_at DESC",
            (user_id,)
        )
        sessions = cursor.fetchall()
        
        session_list = []
        for session in sessions:
            session_id, test_type, question_ids_json, started_at, status = session
            question_ids = json.loads(question_ids_json)
            
            session_list.append({
                "session_id": session_id,
                "test_type": test_type,
                "total_questions": len(question_ids),
                "started_at": started_at,
                "status": status
            })
        
        conn.close()
        
        return {
            "sessions": session_list,
            "total": len(session_list)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢 sessions 失敗：{str(e)}")

# 保留原有的路由以向後兼容
@router.post("/sessions/")
def start_session(data: Dict[str, Any]):
    """建立新的測驗 session (向後兼容)"""
    return create_session(data)

@router.get("/sessions/{user_id}/{test_type}/last")
def get_last_session(user_id: str, test_type: str):
    """取得用戶最後一次的測驗 session (向後兼容)"""
    return get_latest_session(user_id, test_type) 

@router.post("/sessions/{session_id}/pause")
def pause_session(session_id: int, data: Optional[Dict[str, Any]] = None):
    """暫停會話 - 簡化版本：直接記錄當前時間"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 檢查會話是否存在且狀態為 in_progress
        cursor.execute(
            "SELECT started_at, total_time_seconds FROM test_session WHERE id = ? AND status = 'in_progress'",
            (session_id,)
        )
        session_row = cursor.fetchone()
        
        if not session_row:
            raise HTTPException(status_code=404, detail="會話不存在或已暫停")
        
        started_at, total_time_seconds = session_row
        paused_at = datetime.now().isoformat()
        
        # 簡化：直接使用前端傳遞的時間，不再重新計算
        elapsed_seconds = data.get("elapsed_seconds", total_time_seconds) if data else total_time_seconds
        
        # 更新會話狀態和時間
        cursor.execute(
            "UPDATE test_session SET status = 'paused', paused_at = ?, total_time_seconds = ? WHERE id = ?",
            (paused_at, elapsed_seconds, session_id)
        )
        
        conn.commit()
        conn.close()
        
        return {
            "session_id": session_id,
            "status": "paused",
            "paused_at": paused_at,
            "total_time_seconds": elapsed_seconds,
            "message": "會話已暫停"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"暫停會話失敗：{str(e)}")

@router.post("/sessions/{session_id}/update-time")
def update_session_time(session_id: int, data: Dict[str, Any]):
    """更新會話時間"""
    try:
        elapsed_seconds = data.get("elapsed_seconds", 0)
        
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 檢查會話是否存在
        cursor.execute("SELECT status FROM test_session WHERE id = ?", (session_id,))
        session_row = cursor.fetchone()
        
        if not session_row:
            raise HTTPException(status_code=404, detail="會話不存在")
        
        status = session_row[0]
        
        if status == "in_progress":
            # 如果會話正在進行中，更新總時間
            cursor.execute(
                "UPDATE test_session SET total_time_seconds = ? WHERE id = ?",
                (elapsed_seconds, session_id)
            )
        else:
            # 如果會話已暫停，只更新總時間
            cursor.execute(
                "UPDATE test_session SET total_time_seconds = ? WHERE id = ?",
                (elapsed_seconds, session_id)
            )
        
        conn.commit()
        conn.close()
        
        return {
            "session_id": session_id,
            "elapsed_seconds": elapsed_seconds,
            "message": "時間已更新"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新時間失敗：{str(e)}")

@router.post("/sessions/{session_id}/resume")
def resume_session(session_id: int):
    """恢復會話"""
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 檢查會話是否存在且狀態為 paused
        cursor.execute(
            "SELECT total_time_seconds FROM test_session WHERE id = ? AND status = 'paused'",
            (session_id,)
        )
        session_row = cursor.fetchone()
        
        if not session_row:
            raise HTTPException(status_code=404, detail="會話不存在或未暫停")
        
        total_time_seconds = session_row[0]
        resumed_at = datetime.now().isoformat()
        
        # 更新會話狀態，重置開始時間為當前時間，保持總時間不變
        cursor.execute(
            "UPDATE test_session SET status = 'in_progress', started_at = ?, paused_at = NULL, total_time_seconds = ? WHERE id = ?",
            (resumed_at, total_time_seconds, session_id)
        )
        
        conn.commit()
        conn.close()
        
        return {
            "session_id": session_id,
            "status": "in_progress",
            "resumed_at": resumed_at,
            "total_time_seconds": total_time_seconds,
            "message": "會話已恢復"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"恢復會話失敗：{str(e)}") 