from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# データベースのパス
DB_PATH = 'todos.db'

def create_tasks_table(conn):
    """`tasks` テーブルを作成する（なければ作成）。

    カラム:
    - id: 自動採番
    - title: タスク名
    - done: 完了フラグ（初期値 0 = 未完了）
    - deadline: 締め切り日
    """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            memo TEXT,
            done INTEGER DEFAULT 0,
            deadline TEXT
        )
    ''')

    columns = [row[1] for row in conn.execute('PRAGMA table_info(tasks)').fetchall()]
    if 'memo' not in columns:
        conn.execute('ALTER TABLE tasks ADD COLUMN memo TEXT')
    if 'deadline' not in columns:
        conn.execute('ALTER TABLE tasks ADD COLUMN deadline TEXT')


def init_db():
    """データベースを初期化（必要なテーブルをすべて作成）。"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 既存の todos テーブルも確実に作成しておく（既存スキーマを維持）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # tasks テーブルを作成
    create_tasks_table(conn)

    conn.commit()
    conn.close()

def get_db_connection():
    """データベース接続を取得"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    """ホームダッシュボードを表示"""
    return render_template('home.html')

@app.route('/tasks')
def index():
    """タスク一覧を表示"""
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT * FROM tasks
        ORDER BY done ASC,
                 CASE WHEN deadline IS NULL OR deadline = '' THEN 1 ELSE 0 END,
                 deadline ASC,
                 id DESC
    ''').fetchall()
    conn.close()

    today = datetime.today().date()
    tasks = []
    for row in rows:
        task = dict(row)
        task['deadline_status'] = ''
        task['is_overdue'] = False
        task['is_today'] = False

        if task.get('deadline') and not task['done']:
            try:
                deadline_date = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
                if deadline_date < today:
                    task['deadline_status'] = '遅延'
                    task['is_overdue'] = True
                elif deadline_date == today:
                    task['deadline_status'] = '本日'
                    task['is_today'] = True
            except ValueError:
                pass

        tasks.append(task)

    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """新しいタスクを追加"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        memo = request.form.get('memo', '').strip() or None
        deadline = request.form.get('deadline', '').strip() or None
        
        if title:  # タイトルが空でない場合のみ追加
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO tasks (title, memo, deadline) VALUES (?, ?, ?)',
                (title, memo, deadline)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('add_edit.html', title='新しいタスク')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """タスクを編集"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if task is None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        memo = request.form.get('memo', '').strip() or None
        deadline = request.form.get('deadline', '').strip() or None
        
        if title:
            conn = get_db_connection()
            conn.execute(
                'UPDATE tasks SET title = ?, memo = ?, deadline = ? WHERE id = ?',
                (title, memo, deadline, id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('add_edit.html', title='タスク編集', todo=task)

@app.route('/toggle/<int:id>')
def toggle(id):
    """タスクの完了/未完了を切り替え"""
    conn = get_db_connection()
    task = conn.execute('SELECT done FROM tasks WHERE id = ?', (id,)).fetchone()
    
    if task:
        new_status = 1 - task['done']
        conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (new_status, id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('index'))

@app.route('/task/<int:id>')
def task_detail(id):
    """タスク詳細を表示"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    conn.close()
    if task is None:
        return redirect(url_for('index'))
    return render_template('task_detail.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    """タスクを削除"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/schedule')
def schedule():
    """スケジュールページを表示"""
    return render_template('schedule.html')

@app.route('/api/tasks')
def api_tasks():
    """タスク一覧を JSON で返す API"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT id, title, memo, done, deadline FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/simple')
def simple():
    """シンプルなタスク一覧 + 追加フォームページ"""
    return render_template('simple.html')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
