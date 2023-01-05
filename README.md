# Consumption_History

## Implemented functions(구현 기능)
- 유저 회원가입/로그인/로그아웃 기능 (JWT 토큰 인증 방식 사용)
- 유저의 가계부 등록/수정/삭제/조회(전체 + 상세) 기능
- 가계부 특정 세부 내역 단축 URL 생성 가능

### * 미구현
- 가계부 세부 내역 복제(무슨 말인지 모르겠습니다)
- 테스트 케이스 작성

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

