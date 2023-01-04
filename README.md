# Consumption_History

## Goal
- 유저가 본인의 소비내역을 기록/관리

## Python

* Version required 3.8

## Installation

* Install library using pip command

```bash
pip install -r requirements.txt
```

## Environments

```bash
# .env 파일 참조
export MYSQL_HOST={database_ip}
export MYSQL_NAME={database_name}
export MYSQL_USER={username}
export MYSQL_PWD={password}
export MYSQL_PORT={port}
export SECRET_KEY={secret_key}
export JWT_ALGORITHM={jwt_algorithm}
export REDIS_HOST={redis_host}
export REDIS_PORT={redis_port}
```

## Database
- Docker container에 MYSQL 올려서 사용
- MYSQL version 5.7
```bash
# M1 mac의 경우 --platform linux/amd64 옵션 추가
docker run -v {VOLUME PATH}:/var/lib/mysql -p {CONTAINER PORT}:3306 --name consumption_history -e MYSQL_ROOT_PASSWORD={PASSWORD} -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
- Database 생성
```sql
CREATE database consumption CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
