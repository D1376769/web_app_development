from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.note import Note

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/weakspots')
def weakspots():
    """
    錯題/盲點清單
    """
    all_notes = Note.get_all()
    weak_notes = [note for note in all_notes if note['is_weakspot'] == 1]
    return render_template('review/weakspots.html', notes=weak_notes)

@review_bp.route('/quiz')
def quiz():
    """
    測驗模式 (閃卡)
    """
    due_notes = Note.get_due_for_review()
    if not due_notes:
        flash('目前沒有需要複習的筆記！太棒了！', 'success')
        return redirect(url_for('main.index'))
        
    # 取第一筆需要複習的筆記作為題目
    current_note = due_notes[0]
    return render_template('review/quiz.html', note=current_note, remaining=len(due_notes))

@review_bp.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    提交測驗結果
    """
    note_id = request.form.get('note_id')
    familiarity = int(request.form.get('familiarity', 2))
    
    if note_id:
        success = Note.update_review_schedule(int(note_id), familiarity)
        if not success:
            flash('記錄複習結果時發生錯誤', 'error')
            
    return redirect(url_for('review.quiz'))
