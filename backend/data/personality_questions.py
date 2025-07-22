import json
import os
from typing import List, Any
from dataclasses import dataclass

@dataclass
class Question:
    id: int
    text: str
    category: str
    test_type: str
    options: List[str]
    weight: Any
    is_reverse: bool = False

def load_questions_from_json(filename: str) -> List[Question]:
    """從 JSON 檔案載入題目"""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = []
    for i, item in enumerate(data, 1):
        question = Question(
            id=i,
            text=item['text'],
            category=item['category'],
            test_type=item['test_type'],
            options=item['options'],
            weight=item['weight'],
            is_reverse=item.get('is_reverse', False)
        )
        questions.append(question)
    
    return questions

# 載入各測驗類型的題目
mbti_questions = load_questions_from_json('MBTI_questions_final.json')
disc_questions = load_questions_from_json('DISC_questions_final.json')
big5_questions = load_questions_from_json('BIG5_questions_final.json')
enneagram_questions = load_questions_from_json('enneagram_questions_final.json')

# 為每個題目分配唯一 ID
def assign_unique_ids(questions: List[Question], start_id: int) -> List[Question]:
    """為題目分配唯一 ID"""
    for i, question in enumerate(questions):
        question.id = start_id + i
    return questions

# 重新分配 ID，確保每個題目都有唯一 ID
mbti_questions = assign_unique_ids(mbti_questions, 1)
disc_questions = assign_unique_ids(disc_questions, len(mbti_questions) + 1)
big5_questions = assign_unique_ids(big5_questions, len(mbti_questions) + len(disc_questions) + 1)
enneagram_questions = assign_unique_ids(enneagram_questions, len(mbti_questions) + len(disc_questions) + len(big5_questions) + 1)

def get_questions_by_type(test_type: str) -> List[Question]:
    """根據測驗類型獲取題目"""
    type_map = {
        'MBTI': mbti_questions,
        'DISC': disc_questions,
        'BIG5': big5_questions,
        'enneagram': enneagram_questions
    }
    return type_map.get(test_type.upper(), [])

def get_all_questions() -> List[Question]:
    """獲取所有題目"""
    return mbti_questions + disc_questions + big5_questions + enneagram_questions

def get_mbti_questions() -> List[Question]:
    """獲取 MBTI 題目"""
    return mbti_questions

def get_disc_questions() -> List[Question]:
    """獲取 DISC 題目"""
    return disc_questions

def get_big5_questions() -> List[Question]:
    """獲取 Big5 題目"""
    return big5_questions

def get_enneagram_questions() -> List[Question]:
    """獲取 Enneagram 題目"""
    return enneagram_questions

def get_question_count_by_type() -> dict:
    """獲取各測驗類型的題目數量"""
    return {
        'MBTI': len(mbti_questions),
        'DISC': len(disc_questions),
        'BIG5': len(big5_questions),
        'enneagram': len(enneagram_questions)
    }

def print_question_stats(questions: List[Question], test_name: str):
    """統計並列印指定題庫各維度題數與正反向題比例"""
    from collections import defaultdict
    stats = defaultdict(lambda: {'total': 0, '正向': 0, '反向': 0})
    for q in questions:
        stats[q.category]['total'] += 1
        if q.is_reverse:
            stats[q.category]['反向'] += 1
        else:
            stats[q.category]['正向'] += 1
    print(f"\n【{test_name} 題庫分布統計】")
    print(f"{'維度':<8}{'總數':<6}{'正向':<6}{'反向':<6}")
    for cat, d in stats.items():
        print(f"{cat:<8}{d['total']:<6}{d['正向']:<6}{d['反向']:<6}")
    print()

if __name__ == "__main__":
    print_question_stats(mbti_questions, "MBTI")
    print_question_stats(big5_questions, "BIG5")
    print_question_stats(disc_questions, "DISC")
    print_question_stats(enneagram_questions, "Enneagram")