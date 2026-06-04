from datetime import datetime, timezone

fake_db: list[dict] = []
_id_counter: int = 1


def get_all_users() -> list[dict]:
    return fake_db


def get_user_by_id(user_id: int) -> dict | None:
    for user in fake_db:
        if user["id"] == user_id:
            return user
    return None


def get_user_by_email(email: str) -> dict | None:
    for user in fake_db:
        if user["email"] == email:
            return user
    return None


def create_user(user_data: dict) -> dict:
    global _id_counter
    user_data["id"] = _id_counter
    user_data["created_at"] = datetime.now(timezone.utc)
    user_data.pop("password", None)
    fake_db.append(user_data)
    _id_counter += 1
    return user_data


def update_user(user_id: int, update_data: dict) -> dict | None:
    for idx, user in enumerate(fake_db):
        if user["id"] == user_id:
            fake_db[idx].update(update_data)
            return fake_db[idx]
    return None


def delete_user(user_id: int) -> bool:
    for idx, user in enumerate(fake_db):
        if user["id"] == user_id:
            fake_db.pop(idx)
            return True
    return False
