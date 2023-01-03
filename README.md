# Consumption_History

## Goal
- 고객이 본인의 소비내역을 기록/관리하고 싶습니다.
- 아래의 요구사항을 만족하는 DB 테이블과 REST API를 만들어주세요.

## Python

* Version required 3.8

## Installation

* Install library using pip command

```bash
pip install -r requirements.txt
```

## Environments

```bash
export MYSQL_HOST=database_ip
export MYSQL_NAME=database_name
export MYSQL_USER=username
export MYSQL_PWD=password
export MYSQL_PORT=port
```

## Database
- Docker container에 MYSQL 올려서 사용
```bash
# M1 mac의 경우 --platform amd64 옵션 추가
docker run -v {VOLUME PATH}:/var/lib/mysql -p {CONTAINER PORT}:3306 --name consumption_history -e MYSQL_ROOT_PASSWORD={PASSWORD} -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
- Database 생성
```sql
CREATE database consumption CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
