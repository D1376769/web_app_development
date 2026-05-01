import sqlite3

DB_PATH = 'instance/database.db'

def get_db_connection():
    """
    建立與 SQLite 資料庫的連線，並啟用 Foreign Keys
    回傳: sqlite3.Connection 物件
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn

class Tag:
    @staticmethod
    def create(name):
        """
        新增標籤 (若已存在則直接回傳既有 ID)
        參數:
            name (str): 標籤名稱
        回傳:
            int: 標籤 ID，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                tag_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                tag_id = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
            return tag_id
        except Exception as e:
            print(f"Error creating tag: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有標籤
        回傳:
            list: 標籤字典的列表
        """
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM tags ORDER BY name ASC').fetchall()
            return [dict(tag) for tag in tags]
        except Exception as e:
            print(f"Error getting all tags: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_note_tags(note_id):
        """
        取得指定筆記的所有標籤
        參數:
            note_id (int): 筆記 ID
        回傳:
            list: 標籤字典的列表
        """
        try:
            conn = get_db_connection()
            tags = conn.execute('''
                SELECT t.id, t.name 
                FROM tags t
                JOIN note_tags nt ON t.id = nt.tag_id
                WHERE nt.note_id = ?
            ''', (note_id,)).fetchall()
            return [dict(tag) for tag in tags]
        except Exception as e:
            print(f"Error getting note tags: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def set_note_tags(note_id, tag_names):
        """
        設定指定筆記的標籤 (會先清除舊關聯再建立新關聯)
        參數:
            note_id (int): 筆記 ID
            tag_names (list): 標籤名稱的列表
        回傳:
            bool: 是否設定成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM note_tags WHERE note_id = ?', (note_id,))
            
            for name in tag_names:
                name = name.strip()
                if not name:
                    continue
                    
                try:
                    cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                    tag_id = cursor.lastrowid
                except sqlite3.IntegrityError:
                    tag_id = cursor.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
                    
                cursor.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
                
            conn.commit()
            return True
        except Exception as e:
            print(f"Error setting note tags: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
