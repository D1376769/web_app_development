from flask import Blueprint, render_template, request, redirect, url_for

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/weakspots')
def weakspots():
    """
    錯題/盲點清單
    輸入: 無
    處理邏輯: 從 DB 查詢 is_weakspot = 1 的所有筆記
    輸出: 渲染 review/weakspots.html
    """
    pass

@review_bp.route('/quiz')
def quiz():
    """
    測驗模式 (閃卡)
    輸入: 無
    處理邏輯: 呼叫 Note.get_due_for_review() 取出第一筆作為題目
    輸出: 渲染 review/quiz.html，若無題目則顯示完成提示
    """
    pass

@review_bp.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    提交測驗結果
    輸入: form 欄位 note_id, familiarity (熟悉度)
    處理邏輯: 呼叫 Note.update_review_schedule(note_id, familiarity) 更新間隔重複資料
    輸出: 重導向至 /review/quiz 取下一題
    """
    pass
