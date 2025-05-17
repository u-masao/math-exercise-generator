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

### secret_key 設定

```
cd math_exercise
cp math_exercise/local_settings.py.example math_exercise/localsettings.py
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

ブラウザで、以下の URL に接続

http://127.0.0.1:8000/



## heroku deploy


```
sudo snap install --classic heroku
heroku login
heroku create # app name を確認
heroku config:set SECRET_KEY="your_secret_key"
git remote remove heroku
git remote add heroku https://git.heroku.com/< app name >.git
git push heroku <branch name>:main
heroku run 'cd math_exercise ; python manage.py migrate'
heroku run 'cd math_exercise ; python manage.py createsuperuser'
heroku ps:scale web=1
heroku open
heroku logs --tail
```
