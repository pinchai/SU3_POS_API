+++POS Project+++
------------------
+ API
	- Flask
	- Sqlite, Mysql, PostgreSQL (migration)
	- Auth (token base)
+ FrontEnd
	- Angular v20
------------------
+ Setting up
#### Create Virtual Environment
```
python -m venv venv
# ▶ Activate venv
```
#### ▶ Activate venv
```
source venv/bin/activate
```

#### ▶ Install project Package
```
pip install -r requirements.txt
```


#### ▶ Initialize migrations
```
flask db init

flask db migrate -m "fresh migrate"

flask db upgrade


```

