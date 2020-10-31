# math-exercise-generator

## 使い方

### インストール

```
mkdir ~/work
cd ~/work
git clone https://github.com/u-masao/math-exercise-generator.git
cd math-exercise-generator
```

### poetry コマンドインストール、環境構築

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
```

### DB 設定

```
cd math_execrcise
make migrate
```

### ログイン ID 設定

```
make createsuperuser
```

### サーバー起動

```
make runserver
```

### 利用

ブラウザで、以下の URL に接続

http://127.0.0.1:8000/sheets/

