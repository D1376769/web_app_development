import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'instance/database.db'

def get_db_connection():
    """
    建立與 SQLite 資料庫的連線
    回傳: sqlite3.Connection 物件
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Note:
    @staticmethod
    def create(summary, extension=""):
        """
        新增一筆筆記記錄
        參數:
            summary (str): 筆記核心摘要
            extension (str): 延伸思考 (預設為空字串)
        回傳:
            int: 新增的筆記 ID，若失敗則回傳 None
        """
        try:
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
            return note_id
        except Exception as e:
            print(f"Error creating note: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有筆記記錄
        回傳:
            list: 包含筆記字典的列表
        """
        try:
            conn = get_db_connection()
            notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
            return [dict(note) for note in notes]
        except Exception as e:
            print(f"Error getting notes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(note_id):
        """
        取得單筆筆記記錄
        參數:
            note_id (int): 筆記 ID
        回傳:
            dict: 筆記資料，若找不到或失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
            return dict(note) if note else None
        except Exception as e:
            print(f"Error getting note by id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(note_id, summary, extension, is_weakspot=0):
        """
        更新筆記記錄
        參數:
            note_id (int): 筆記 ID
            summary (str): 新的核心摘要
            extension (str): 新的延伸思考
            is_weakspot (int): 是否為盲點 (0或1)
        回傳:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute(
                'UPDATE notes SET summary = ?, extension = ?, is_weakspot = ?, updated_at = ? WHERE id = ?',
                (summary, extension, is_weakspot, now, note_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating note: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(note_id):
        """
        刪除筆記記錄
        參數:
            note_id (int): 筆記 ID
        回傳:
            bool: 是否刪除成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_due_for_review():
        """
        取得今日待複習的筆記
        回傳:
            list: 包含筆記字典的列表
        """
        try:
            conn = get_db_connection()
            today = datetime.now().strftime('%Y-%m-%d')
            notes = conn.execute('SELECT * FROM notes WHERE next_review_date <= ? ORDER BY next_review_date ASC', (today,)).fetchall()
            return [dict(note) for note in notes]
        except Exception as e:
            print(f"Error getting due notes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update_review_schedule(note_id, familiarity):
        """
        更新筆記的間隔重複排程
        參數:
            note_id (int): 筆記 ID
            familiarity (int): 熟悉度 (1=不熟, 2=普通, 3=熟悉)
        回傳:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            note = conn.execute('SELECT review_interval FROM notes WHERE id = ?', (note_id,)).fetchone()
            if not note:
                return False
                
            current_interval = note['review_interval']
            is_weakspot = 0
            
            if familiarity == 1:
                new_interval = 1
                is_weakspot = 1
            elif familiarity == 2:
                new_interval = max(3, current_interval * 2) if current_interval > 0 else 3
            else:
                new_interval = max(7, current_interval * 3) if current_interval > 0 else 7
                
            next_review_date = (datetime.now() + timedelta(days=new_interval)).strftime('%Y-%m-%d')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            conn.execute(
                'UPDATE notes SET review_interval = ?, next_review_date = ?, is_weakspot = ?, updated_at = ? WHERE id = ?',
                (new_interval, next_review_date, is_weakspot, now, note_id)
            )
            conn.execute(
                'INSERT INTO review_logs (note_id, familiarity, reviewed_at) VALUES (?, ?, ?)',
                (note_id, familiarity, now)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating review schedule: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
