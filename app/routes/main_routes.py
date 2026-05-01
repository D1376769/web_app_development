from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁/儀表板
    輸入: 無
    處理邏輯: 呼叫 Note.get_due_for_review() 取得今日待複習筆記
    輸出: 渲染 index.html
    """
    pass
