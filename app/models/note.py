import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Note:
    @staticmethod
    def create(summary, extension=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            'INSERT INTO notes (summary, extension, next_review_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
            (summary, extension, today, now, now)
        )
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(note) for note in notes]

    @staticmethod
    def get_by_id(note_id):
        conn = get_db_connection()
        note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
        conn.close()
        return dict(note) if note else None

    @staticmethod
    def update(note_id, summary, extension, is_weakspot=0):
        conn = get_db_connection()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            'UPDATE notes SET summary = ?, extension = ?, is_weakspot = ?, updated_at = ? WHERE id = ?',
            (summary, extension, is_weakspot, now, note_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(note_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_due_for_review():
        conn = get_db_connection()
        today = datetime.now().strftime('%Y-%m-%d')
        notes = conn.execute('SELECT * FROM notes WHERE next_review_date <= ? ORDER BY next_review_date ASC', (today,)).fetchall()
        conn.close()
        return [dict(note) for note in notes]

    @staticmethod
    def update_review_schedule(note_id, familiarity):
        # 簡易的間隔重複演算法
        conn = get_db_connection()
        note = conn.execute('SELECT review_interval FROM notes WHERE id = ?', (note_id,)).fetchone()
        if not note:
            conn.close()
            return
            
        current_interval = note['review_interval']
        is_weakspot = 0
        
        if familiarity == 1: # 不熟/答錯
            new_interval = 1
            is_weakspot = 1
        elif familiarity == 2: # 普通
            new_interval = max(3, current_interval * 2) if current_interval > 0 else 3
        else: # 熟悉
            new_interval = max(7, current_interval * 3) if current_interval > 0 else 7
            
        next_review_date = (datetime.now() + timedelta(days=new_interval)).strftime('%Y-%m-%d')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 更新排程
        conn.execute(
            'UPDATE notes SET review_interval = ?, next_review_date = ?, is_weakspot = ?, updated_at = ? WHERE id = ?',
            (new_interval, next_review_date, is_weakspot, now, note_id)
        )
        
        # 記錄複習日誌
        conn.execute(
            'INSERT INTO review_logs (note_id, familiarity, reviewed_at) VALUES (?, ?, ?)',
            (note_id, familiarity, now)
        )
        
        conn.commit()
        conn.close()
