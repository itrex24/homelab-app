import argparse
from sqlalchemy import select
from .db import SessionLocal
from .models.user import User
from .auth.passwords import hash_password

def create_user(username: str, password: str) -> None:
    db = SessionLocal()
    try:
        existing = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if existing:
            raise SystemExit(f"User already exists: {username}")
        user = User(username=username, password_hash=hash_password(password), is_active=True)
        db.add(user)
        db.commit()
        print(f"Created user: {username}")
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(prog="homelab-app-cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    cu = sub.add_parser("create-user", help="Create a local user")
    cu.add_argument("--username", required=True)
    cu.add_argument("--password", required=True)

    args = parser.parse_args()
    if args.cmd == "create-user":
        create_user(args.username, args.password)

if __name__ == "__main__":
    main()
