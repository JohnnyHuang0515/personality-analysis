#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查題目品質：重複性、相似性、規範遵守
"""

import sqlite3
import json
import re
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher

def get_all_questions():
    """獲取所有題目"""
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, text, category, test_type, options, weight 
        FROM test_question 
        ORDER BY test_type, category, id
    """)
    
    questions = []
    for row in cursor.fetchall():
        questions.append({
            'id': row[0],
            'text': row[1],
            'category': row[2],
            'test_type': row[3],
            'options': json.loads(row[4]),
            'weight': json.loads(row[5])
        })
    
    conn.close()
    return questions

def check_duplicates(questions: List[Dict[str, Any]]) -> List[Tuple[int, int, str]]:
    """檢查完全重複的題目"""
    print("🔍 檢查完全重複題目...")
    
    duplicates = []
    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            q1, q2 = questions[i], questions[j]
            
            # 檢查題目文字是否完全相同
            if q1['text'] == q2['text']:
                duplicates.append((q1['id'], q2['id'], f"完全重複: {q1['text'][:50]}..."))
            
            # 檢查選項是否完全相同
            elif (q1['options'] == q2['options'] and 
                  q1['test_type'] == q2['test_type'] and
                  q1['category'] == q2['category']):
                duplicates.append((q1['id'], q2['id'], f"選項重複: {q1['text'][:50]}..."))
    
    return duplicates

def calculate_similarity(text1: str, text2: str) -> float:
    """計算兩個文字的相似度"""
    return SequenceMatcher(None, text1, text2).ratio()

def check_similarity(questions: List[Dict[str, Any]], threshold: float = 0.8) -> List[Tuple[int, int, float, str]]:
    """檢查相似題目"""
    print("🔍 檢查相似題目...")
    
    similar_questions = []
    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            q1, q2 = questions[i], questions[j]
            
            # 只檢查同類型同分類的題目
            if q1['test_type'] == q2['test_type'] and q1['category'] == q2['category']:
                similarity = calculate_similarity(q1['text'], q2['text'])
                if similarity >= threshold:
                    similar_questions.append((
                        q1['id'], q2['id'], similarity,
                        f"相似度 {similarity:.2f}: {q1['text'][:50]}... vs {q2['text'][:50]}..."
                    ))
    
    return similar_questions

def check_format_compliance(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """檢查格式規範遵守"""
    print("🔍 檢查格式規範遵守...")
    
    issues = []
    
    for q in questions:
        # 檢查題目文字格式
        if not q['text'].endswith('：') and not q['text'].endswith('?'):
            issues.append({
                'id': q['id'],
                'type': 'format',
                'issue': '題目文字應以冒號或問號結尾',
                'text': q['text'][:50] + '...'
            })
        
        # 檢查選項數量
        if len(q['options']) != 2:
            issues.append({
                'id': q['id'],
                'type': 'format',
                'issue': f'選項數量應為2個，實際為{len(q["options"])}個',
                'text': q['text'][:50] + '...'
            })
        
        # 檢查選項長度
        for i, option in enumerate(q['options']):
            if len(option) < 3 or len(option) > 50:
                issues.append({
                    'id': q['id'],
                    'type': 'format',
                    'issue': f'選項{i+1}長度不當: {len(option)}字元',
                    'text': q['text'][:50] + '...'
                })
        
        # 檢查權重格式
        if not isinstance(q['weight'], dict):
            issues.append({
                'id': q['id'],
                'type': 'format',
                'issue': '權重應為字典格式',
                'text': q['text'][:50] + '...'
            })
        
        # 檢查權重值
        for key, value in q['weight'].items():
            if not isinstance(value, (int, float)) or value <= 0:
                issues.append({
                    'id': q['id'],
                    'type': 'format',
                    'issue': f'權重值不當: {key}={value}',
                    'text': q['text'][:50] + '...'
                })
    
    return issues

def check_theory_compliance(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """檢查理論規範遵守"""
    print("🔍 檢查理論規範遵守...")
    
    # 理論規範定義
    theory_rules = {
        'MBTI': {
            'categories': ['E-I', 'S-N', 'T-F', 'J-P', 'situation'],
            'weight_keys': ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P']
        },
        'DISC': {
            'categories': ['DISC', 'situation'],
            'weight_keys': ['D', 'I', 'S', 'C']
        },
        'BIG5': {
            'categories': ['外向性', '友善性', '盡責性', '神經質', '開放性', 'situation'],
            'weight_keys': ['外向性', '內向性', '友善性', '對抗性', '盡責性', '隨性', '情緒穩定', '神經質', '開放性', '保守性']
        },
        'ENNEAGRAM': {
            'categories': ['類型1', '類型2', '類型3', '類型4', '類型5', '類型6', '類型7', '類型8', '類型9', 'situation'],
            'weight_keys': ['類型1', '類型2', '類型3', '類型4', '類型5', '類型6', '類型7', '類型8', '類型9']
        }
    }
    
    issues = []
    
    for q in questions:
        test_type = q['test_type']
        if test_type not in theory_rules:
            issues.append({
                'id': q['id'],
                'type': 'theory',
                'issue': f'未知測驗類型: {test_type}',
                'text': q['text'][:50] + '...'
            })
            continue
        
        rules = theory_rules[test_type]
        
        # 檢查分類是否合規
        if q['category'] not in rules['categories']:
            issues.append({
                'id': q['id'],
                'type': 'theory',
                'issue': f'分類不當: {q["category"]} (應為: {rules["categories"]})',
                'text': q['text'][:50] + '...'
            })
        
        # 檢查權重鍵是否合規
        weight_keys = list(q['weight'].keys())
        for key in weight_keys:
            if key not in rules['weight_keys']:
                issues.append({
                    'id': q['id'],
                    'type': 'theory',
                    'issue': f'權重鍵不當: {key} (應為: {rules["weight_keys"]})',
                    'text': q['text'][:50] + '...'
                })
    
    return issues

def check_balance_distribution(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """檢查分類分布平衡性"""
    print("🔍 檢查分類分布平衡性...")
    
    distribution = {}
    balance_issues = []
    
    for q in questions:
        test_type = q['test_type']
        category = q['category']
        
        if test_type not in distribution:
            distribution[test_type] = {}
        
        if category not in distribution[test_type]:
            distribution[test_type][category] = 0
        
        distribution[test_type][category] += 1
    
    # 檢查各分類的分布是否平衡
    for test_type, categories in distribution.items():
        total = sum(categories.values())
        avg = total / len(categories)
        
        for category, count in categories.items():
            ratio = count / avg
            if ratio < 0.5 or ratio > 2.0:  # 允許50%的偏差
                balance_issues.append({
                    'test_type': test_type,
                    'category': category,
                    'count': count,
                    'average': avg,
                    'ratio': ratio,
                    'issue': f'{category}題目數量不平衡 (平均{avg:.1f}題，實際{count}題)'
                })
    
    return {
        'distribution': distribution,
        'balance_issues': balance_issues
    }

def check_content_quality(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """檢查內容品質"""
    print("🔍 檢查內容品質...")
    
    quality_issues = []
    
    for q in questions:
        # 檢查題目長度
        if len(q['text']) < 5 or len(q['text']) > 100:
            quality_issues.append({
                'id': q['id'],
                'type': 'quality',
                'issue': f'題目長度不當: {len(q["text"])}字元',
                'text': q['text'][:50] + '...'
            })
        
        # 檢查是否包含敏感詞彙
        sensitive_words = ['歧視', '偏見', '攻擊', '侮辱', '貶低']
        for word in sensitive_words:
            if word in q['text']:
                quality_issues.append({
                    'id': q['id'],
                    'type': 'quality',
                    'issue': f'包含敏感詞彙: {word}',
                    'text': q['text'][:50] + '...'
                })
        
        # 檢查選項對立性
        if len(q['options']) == 2:
            option1, option2 = q['options']
            # 檢查選項是否過於相似
            similarity = calculate_similarity(option1, option2)
            if similarity > 0.7:
                quality_issues.append({
                    'id': q['id'],
                    'type': 'quality',
                    'issue': f'選項相似度過高: {similarity:.2f}',
                    'text': q['text'][:50] + '...'
                })
        
        # 檢查權重平衡性
        if len(q['weight']) == 2:
            values = list(q['weight'].values())
            if abs(values[0] - values[1]) > 1:
                quality_issues.append({
                    'id': q['id'],
                    'type': 'quality',
                    'issue': f'權重不平衡: {values[0]} vs {values[1]}',
                    'text': q['text'][:50] + '...'
                })
    
    return quality_issues

def generate_report(questions: List[Dict[str, Any]]):
    """生成檢查報告"""
    print("📊 生成品質檢查報告...")
    
    # 執行各項檢查
    duplicates = check_duplicates(questions)
    similar_questions = check_similarity(questions)
    format_issues = check_format_compliance(questions)
    theory_issues = check_theory_compliance(questions)
    balance_result = check_balance_distribution(questions)
    quality_issues = check_content_quality(questions)
    
    # 生成報告
    report = {
        'summary': {
            'total_questions': len(questions),
            'duplicates': len(duplicates),
            'similar_questions': len(similar_questions),
            'format_issues': len(format_issues),
            'theory_issues': len(theory_issues),
            'balance_issues': len(balance_result['balance_issues']),
            'quality_issues': len(quality_issues)
        },
        'details': {
            'duplicates': duplicates,
            'similar_questions': similar_questions,
            'format_issues': format_issues,
            'theory_issues': theory_issues,
            'balance_result': balance_result,
            'quality_issues': quality_issues
        }
    }
    
    return report

def print_report(report: Dict[str, Any]):
    """打印檢查報告"""
    print("\n" + "=" * 80)
    print("📋 題目品質檢查報告")
    print("=" * 80)
    
    summary = report['summary']
    print(f"\n📊 檢查摘要:")
    print(f"  總題目數: {summary['total_questions']}")
    print(f"  重複題目: {summary['duplicates']}")
    print(f"  相似題目: {summary['similar_questions']}")
    print(f"  格式問題: {summary['format_issues']}")
    print(f"  理論問題: {summary['theory_issues']}")
    print(f"  平衡問題: {summary['balance_issues']}")
    print(f"  品質問題: {summary['quality_issues']}")
    
    # 檢查結果評估
    total_issues = (summary['duplicates'] + summary['similar_questions'] + 
                   summary['format_issues'] + summary['theory_issues'] + 
                   summary['balance_issues'] + summary['quality_issues'])
    
    if total_issues == 0:
        print(f"\n🎉 檢查結果: ✅ 完美通過")
    elif total_issues <= 10:
        print(f"\n✅ 檢查結果: 良好 (問題數: {total_issues})")
    elif total_issues <= 30:
        print(f"\n⚠️ 檢查結果: 需要改進 (問題數: {total_issues})")
    else:
        print(f"\n❌ 檢查結果: 需要大幅改進 (問題數: {total_issues})")
    
    # 詳細問題報告
    if summary['duplicates'] > 0:
        print(f"\n🔍 重複題目 ({summary['duplicates']}個):")
        for dup in report['details']['duplicates'][:5]:  # 只顯示前5個
            print(f"  - {dup[2]}")
    
    if summary['similar_questions'] > 0:
        print(f"\n🔍 相似題目 ({summary['similar_questions']}個):")
        for sim in report['details']['similar_questions'][:5]:  # 只顯示前5個
            print(f"  - {sim[3]}")
    
    if summary['format_issues'] > 0:
        print(f"\n🔍 格式問題 ({summary['format_issues']}個):")
        for fmt in report['details']['format_issues'][:5]:  # 只顯示前5個
            print(f"  - ID {fmt['id']}: {fmt['issue']}")
    
    if summary['theory_issues'] > 0:
        print(f"\n🔍 理論問題 ({summary['theory_issues']}個):")
        for theory in report['details']['theory_issues'][:5]:  # 只顯示前5個
            print(f"  - ID {theory['id']}: {theory['issue']}")
    
    if summary['balance_issues'] > 0:
        print(f"\n🔍 平衡問題 ({summary['balance_issues']}個):")
        for balance in report['details']['balance_result']['balance_issues'][:5]:  # 只顯示前5個
            print(f"  - {balance['issue']}")
    
    if summary['quality_issues'] > 0:
        print(f"\n🔍 品質問題 ({summary['quality_issues']}個):")
        for quality in report['details']['quality_issues'][:5]:  # 只顯示前5個
            print(f"  - ID {quality['id']}: {quality['issue']}")
    
    # 分布統計
    print(f"\n📊 分類分布:")
    for test_type, categories in report['details']['balance_result']['distribution'].items():
        print(f"  {test_type}:")
        for category, count in categories.items():
            print(f"    {category}: {count}題")
    
    print("\n" + "=" * 80)

def main():
    """主函數"""
    print("🧪 開始題目品質檢查...")
    
    # 獲取所有題目
    questions = get_all_questions()
    print(f"📝 獲取到 {len(questions)} 個題目")
    
    # 生成檢查報告
    report = generate_report(questions)
    
    # 打印報告
    print_report(report)
    
    # 保存報告
    with open('docs/question_quality_report.md', 'w', encoding='utf-8') as f:
        f.write("# 題目品質檢查報告\n\n")
        f.write(f"## 檢查摘要\n\n")
        f.write(f"- 總題目數: {report['summary']['total_questions']}\n")
        f.write(f"- 重複題目: {report['summary']['duplicates']}\n")
        f.write(f"- 相似題目: {report['summary']['similar_questions']}\n")
        f.write(f"- 格式問題: {report['summary']['format_issues']}\n")
        f.write(f"- 理論問題: {report['summary']['theory_issues']}\n")
        f.write(f"- 平衡問題: {report['summary']['balance_issues']}\n")
        f.write(f"- 品質問題: {report['summary']['quality_issues']}\n\n")
        
        f.write("## 詳細問題\n\n")
        for issue_type, issues in report['details'].items():
            if issues and isinstance(issues, list) and len(issues) > 0:
                f.write(f"### {issue_type}\n\n")
                for issue in issues[:10]:  # 只保存前10個問題
                    if isinstance(issue, dict):
                        f.write(f"- ID {issue.get('id', 'N/A')}: {issue.get('issue', 'N/A')}\n")
                    else:
                        f.write(f"- {str(issue)}\n")
                f.write("\n")
    
    print("✅ 品質檢查完成！報告已保存到 docs/question_quality_report.md")

if __name__ == "__main__":
    main() 