from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.note import Note
from app.models.tag import Tag

note_bp = Blueprint('notes', __name__, url_prefix='/notes')

@note_bp.route('/')
def index():
    """
    筆記列表
    """
    tag_filter = request.args.get('tag')
    notes = Note.get_all()
    
    if tag_filter:
        # 過濾包含此標籤的筆記
        filtered_notes = []
        for note in notes:
            note_tags = [t['name'] for t in Tag.get_note_tags(note['id'])]
            if tag_filter in note_tags:
                filtered_notes.append(note)
        notes = filtered_notes

    # 取得所有筆記的標籤
    for note in notes:
        note['tags'] = Tag.get_note_tags(note['id'])

    all_tags = Tag.get_all()
    return render_template('notes/index.html', notes=notes, all_tags=all_tags, current_tag=tag_filter)

@note_bp.route('/new', methods=['GET'])
def new_note():
    """
    新增筆記頁面
    """
    return render_template('notes/new.html')

@note_bp.route('/', methods=['POST'])
def create_note():
    """
    建立筆記
    """
    summary = request.form.get('summary', '').strip()
    extension = request.form.get('extension', '').strip()
    tags_input = request.form.get('tags', '')
    
    if not summary:
        flash('核心摘要為必填欄位！', 'error')
        return render_template('notes/new.html', extension=extension, tags=tags_input)
        
    note_id = Note.create(summary, extension)
    if note_id:
        # 處理標籤 (假設以逗號分隔)
        tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
        if tag_names:
            Tag.set_note_tags(note_id, tag_names)
        flash('筆記新增成功！', 'success')
        return redirect(url_for('notes.index'))
    else:
        flash('筆記新增失敗，請稍後再試。', 'error')
        return render_template('notes/new.html', summary=summary, extension=extension, tags=tags_input)

@note_bp.route('/<int:id>')
def detail(id):
    """
    筆記詳情
    """
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該筆記', 'error')
        return redirect(url_for('notes.index'))
        
    tags = Tag.get_note_tags(id)
    return render_template('notes/detail.html', note=note, tags=tags)

@note_bp.route('/<int:id>/edit', methods=['GET'])
def edit_note(id):
    """
    編輯筆記頁面
    """
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該筆記', 'error')
        return redirect(url_for('notes.index'))
        
    tags = Tag.get_note_tags(id)
    tag_names = ', '.join([t['name'] for t in tags])
    return render_template('notes/edit.html', note=note, tags_string=tag_names)

@note_bp.route('/<int:id>/update', methods=['POST'])
def update_note(id):
    """
    更新筆記
    """
    summary = request.form.get('summary', '').strip()
    extension = request.form.get('extension', '').strip()
    tags_input = request.form.get('tags', '')
    is_weakspot = 1 if request.form.get('is_weakspot') else 0
    
    if not summary:
        flash('核心摘要為必填欄位！', 'error')
        note = Note.get_by_id(id)
        return render_template('notes/edit.html', note=note, tags_string=tags_input)
        
    success = Note.update(id, summary, extension, is_weakspot)
    if success:
        tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
        Tag.set_note_tags(id, tag_names)
        flash('筆記更新成功！', 'success')
    else:
        flash('更新失敗，請稍後再試。', 'error')
        
    return redirect(url_for('notes.detail', id=id))

@note_bp.route('/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    刪除筆記
    """
    success = Note.delete(id)
    if success:
        flash('筆記已刪除', 'success')
    else:
        flash('刪除失敗', 'error')
    return redirect(url_for('notes.index'))
