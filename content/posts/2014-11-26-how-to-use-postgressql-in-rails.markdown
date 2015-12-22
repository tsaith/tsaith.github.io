Title: 在 Rails 中使用 PostgresSQL
Date: 2014-11-26
Tags: rails
Category: Web


[PostgreSQL](http://www.postgresql.org/) 是目前相當受歡迎的一套開源資料庫，
下面將說明如何在 Rails 中使用它。

### 安裝套件

如若開發環境是 Mac 的話，請執行下列步驟

* 下載 [Postgres.app](http://postgresapp.com/) ，放到 /Applications/ 資料夾下
* 在 ~/.profile 加入
```
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin
export PGHOST=localhost
```
(假設版本號是 9.3)

### 設定 Rails 資料庫

* 編輯 config/database.yml 內容如下

```
development:
  adapter: postgresql
  encoding: unicode
  database: myflix_development
  pool: 5
  username: YOUR_USERNAME
  password: YOUR_PASSWORD

test:
  adapter: postgresql
  encoding: unicode
  database: myflix_test
  pool: 5
  username: YOUR_USERNAME
  password: YOUR_PASSWORD

production:
  adapter: postgresql
  encoding: unicode
  database: myflix_test
  pool: 5
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```

* 接著在 Gemfile 中加入 gem 'pg' 然後執行 `bundle`

完成上述步驟後，我們就可以在 Rails 中存取 PostgreSQL 資料庫。

### 常用指令

這裡列出一些 PostgreSQL 常用的指令

* 建立資料庫: `createdb db_name`

* 刪除資料庫: `dropdb db_name`


* 列出所有資料庫: `psql -l`


PostgreSQL 的內建命令:

* 列出所有資料庫: `\l`

* 連接資料庫: `\c db_name`

* 顯示所有 tables: `\d`

* 新增資料庫: `DROP DATABASE db_name;`

* 刪除資料庫: `DROP DATABASE db_name;`

* 建立 table: `CREATE TABLE db_table(id int, text VARCHAR(50));`

* 刪除 table: `DROP TABLE db_table;`

* 查詢記錄: `SELECT * FROM db_table WHERE id = 1;`

* 插入一筆記錄: `INSERT INTO db_table(id, text) VALUES(1, 'A new record');`

* 更新一筆記錄: `UPDATE db_table SET text = 'str' WHERE id = 1;`

* 刪除一筆記錄: `DELETE FROM test WHERE id = 1;`

