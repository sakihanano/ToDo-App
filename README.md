# シンプルな Todo アプリ（Flask + SQLite）

初心者向けの最小構成 Flask + SQLite による Todo アプリです。

## 📁 フォルダ構成

```
todo-app/
├── app.py                 # メインアプリケーション
├── requirements.txt       # Python 依存パッケージ
├── Procfile               # Heroku/Render の起動設定
├── runtime.txt            # 使用する Python ランタイム
├── templates/            # HTML テンプレート
│   ├── base.html        # ベーステンプレート
│   ├── index.html       # タスク一覧ページ
│   └── add_edit.html    # タスク追加・編集ページ
└── static/              # CSS・静的ファイル
    └── style.css        # スタイルシート
```

## 🚀 セットアップ手順

### 1. Python 環境の確認
```bash
python --version
# Python 3.7 以上が必要です
```

### 2. 仮想環境の作成（オプション だが推奨）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 4. アプリケーションの起動
```bash
python app.py
```

### 5. ブラウザでアクセス
ブラウザを開いて以下にアクセスします：
```
http://localhost:5000
```

### 6. デプロイ準備
Heroku や Render などの PaaS に公開する場合、以下のファイルが必要です。

- `requirements.txt` - Python 依存パッケージ
- `Procfile` - 起動コマンド
- `runtime.txt` - Python ランタイム

#### Heroku への手順例
```bash
cd todo-app
# Git リポジトリを作成してコミット
git init
git add .
git commit -m "Deploy todo app"

# Heroku にログインしてアプリを作成
heroku login
heroku create

git push heroku main
heroku open
```

> 注意: SQLite は Heroku の一時ファイルシステム上では永続化されません。データを保持したい場合は PostgreSQL などの外部 DB を検討してください。

#### Render への手順例
1. Render にログインして新しい Web Service を作成
2. GitHub または Git リポジトリを接続
3. Build Command に `pip install -r requirements.txt`
4. Start Command に `gunicorn app:app`
5. Python バージョンは `python-3.11.18` を使用

## 💡 主な機能

- ✅ **タスク一覧表示** - 作成したタスクを一覧で表示
- ✅ **タスク追加** - 新しいタスクをタイトルと説明付きで追加
- ✅ **タスク編集** - 既存のタスクを編集
- ✅ **完了/未完了の切り替え** - チェックボックスでタスクの完了状態を管理
- ✅ **タスク削除** - 不要なタスクを削除
- ✅ **永続化** - SQLite で自動保存

## 📝 コードの簡単な説明

### app.py の主要な部分

**データベース初期化**
```python
def init_db():
    # todos テーブルを作成
    # id, title, description, completed, created_at カラムを定義
```

**ルート定義**
```python
@app.route('/')                    # タスク一覧表示
@app.route('/add', methods=[...])  # タスク追加
@app.route('/edit/<id>', ...)      # タスク編集
@app.route('/toggle/<id>')         # 完了状態の切り替え
@app.route('/delete/<id>')         # タスク削除
```

### templates/ の役割

- `base.html` - 全ページの共通テンプレート
- `index.html` - タスク一覧ページ
- `add_edit.html` - タスク追加・編集フォーム

### static/style.css

レスポンシブデザインで PC/スマートフォンの両方に対応しています。

## 🔧 カスタマイズ例

### ポート番号を変更したい場合
`app.py` の最後を編集：
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=8000)  # 5000 → 8000 など
```

### デバッグモードを無効にする場合
本番環境では：
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📚 学べること

このプロジェクトを通じて以下が学べます：

- Flask の基本的な使い方（ルート、テンプレート）
- SQLite データベースの操作（Create, Read, Update, Delete）
- HTML フォームの処理
- HTML テンプレートと Jinja2
- CSS によるスタイリング
- HTTP リクエスト/レスポンスの流れ

## 🐛 トラブルシューティング

**ポート 5000 が既に使用中の場合**
```bash
# ポート 8000 で起動
# app.py の port を 8000 に変更して起動
```

**パッケージのインストールに失敗した場合**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**データベースが壊れた場合**
```bash
# todos.db を削除すれば、次回起動時に新規作成されます
rm todos.db  # または Manual で削除
python app.py
```

## 📖 次のステップ

このアプリをさらに拡張する案：
- [ ] ユーザー認証機能の追加
- [ ] タスクのカテゴリ分類
- [ ] 期限設定機能
- [ ] タスクの優先度設定
- [ ] API 化（REST API）
- [ ] テスト機能の追加

---

**作成日**: 2024年
**言語**: Python
**フレームワーク**: Flask
