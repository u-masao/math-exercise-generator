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

poetry を動かすために必要なライブラリなどをインストールします。

```
sudo apt update
sudo apt-get install pipx
pipx ensurepath
source ~/.bashrc
pipx install poetry
```

アプリを動作させるために必要なライブラリをインストールします。

```
sudo apt update
sudo apt-get install libjpeg-dev libpq-dev libfreetype6-dev
poetry install
```

### secret_key 設定

```
cd math_exercise
cp math_exercise/local_settings.py.example math_exercise/local_settings.py
poetry run python # secret_key 生成
> from django.core.management.utils import get_random_secret_key
> get_random_secret_key()
vi math_exercise/local_settings.py # secret_key 設定

```

### DB 設定

```
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

ブラウザで以下の URL に接続します。

http://127.0.0.1:8000/
