from flask import Blueprint, render_template
from app.models.note import Note

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁/儀表板
    """
    due_notes = Note.get_due_for_review()
    return render_template('index.html', due_notes=due_notes)
