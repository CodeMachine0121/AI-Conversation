import json
import os

USERS_FILE = "../users.json"

def create_user(username, password, is_admin=False):
    user = {
        "username": username,
        "password": password,
        "is_admin": is_admin
    }
    return user

def save_users(users, filename):
    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

def main():
    users = []
    users.append(create_user("normal_user", "normal_pass", False))
    users.append(create_user("admin_user", "admin_pass", True))
    save_users(users, USERS_FILE)
    print(f"Users created and saved to {USERS_FILE}")

if __name__ == "__main__":
    main()

