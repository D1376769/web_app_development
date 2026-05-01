from flask import Blueprint, render_template, request, redirect, url_for

note_bp = Blueprint('notes', __name__, url_prefix='/notes')

@note_bp.route('/')
def index():
    """
    筆記列表
    輸入: query 參數 tag (選填)
    處理邏輯: 呼叫 Note.get_all()，若有 tag 則過濾
    輸出: 渲染 notes/index.html
    """
    pass

@note_bp.route('/new', methods=['GET'])
def new_note():
    """
    新增筆記頁面
    輸入: 無
    處理邏輯: 無
    輸出: 渲染 notes/new.html
    """
    pass

@note_bp.route('/', methods=['POST'])
def create_note():
    """
    建立筆記
    輸入: form 欄位 summary, extension, tags
    處理邏輯: 驗證資料後呼叫 Note.create() 與 Tag.set_note_tags()
    輸出: 重導向至 /notes
    """
    pass

@note_bp.route('/<int:id>')
def detail(id):
    """
    筆記詳情
    輸入: path 參數 id
    處理邏輯: 呼叫 Note.get_by_id(id)
    輸出: 渲染 notes/detail.html，若找不到則回傳 404
    """
    pass

@note_bp.route('/<int:id>/edit', methods=['GET'])
def edit_note(id):
    """
    編輯筆記頁面
    輸入: path 參數 id
    處理邏輯: 呼叫 Note.get_by_id(id) 取得資料以填入表單
    輸出: 渲染 notes/edit.html
    """
    pass

@note_bp.route('/<int:id>/update', methods=['POST'])
def update_note(id):
    """
    更新筆記
    輸入: path 參數 id, form 欄位 summary, extension, tags, is_weakspot
    處理邏輯: 呼叫 Note.update() 與 Tag.set_note_tags()
    輸出: 重導向至 /notes/<id>
    """
    pass

@note_bp.route('/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    刪除筆記
    輸入: path 參數 id
    處理邏輯: 呼叫 Note.delete(id)
    輸出: 重導向至 /notes
    """
    pass
