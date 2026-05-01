import sqlite3

DB_PATH = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign keys for cascade delete
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn

class Tag:
    @staticmethod
    def create(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
            tag_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            # 已經存在
            tag_id = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
        conn.close()
        return tag_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        tags = conn.execute('SELECT * FROM tags ORDER BY name ASC').fetchall()
        conn.close()
        return [dict(tag) for tag in tags]

    @staticmethod
    def get_note_tags(note_id):
        conn = get_db_connection()
        tags = conn.execute('''
            SELECT t.id, t.name 
            FROM tags t
            JOIN note_tags nt ON t.id = nt.tag_id
            WHERE nt.note_id = ?
        ''', (note_id,)).fetchall()
        conn.close()
        return [dict(tag) for tag in tags]

    @staticmethod
    def set_note_tags(note_id, tag_names):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 刪除現有關聯
        cursor.execute('DELETE FROM note_tags WHERE note_id = ?', (note_id,))
        
        for name in tag_names:
            name = name.strip()
            if not name:
                continue
                
            # 確保標籤存在
            try:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                tag_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                tag_id = cursor.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()['id']
                
            # 建立關聯
            cursor.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
            
        conn.commit()
        conn.close()
