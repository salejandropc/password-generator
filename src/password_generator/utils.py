import dataclasses
import json
import logging
import os
from typing import Any


@dataclasses.dataclass
class Defaults:
    db_name: str = ".db.json"


@dataclasses.dataclass(frozen=True)
class Envars:
    root_dir: str = "GENPASS_ROOT_DIR"
    db_name: str = "GENPASS_DB_NAME"


@dataclasses.dataclass
class Keys:
    user: str = "user"
    password: str = "pass"
    creation: str = "creation_date"


def load_password_database(root_dir: str, db_name: str) -> dict[str, dict[str, Any]]:
    path = os.path.join(root_dir, db_name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Export your variables {Envars.root_dir} and {Envars.db_name}"
        )

    with open(path, encoding="utf-8") as pass_db:
        saved_pass = json.load(pass_db)

    if not saved_pass:
        logging.warning("The database is empty!")

    return saved_pass


def save_password_database(
    root_dir: str, db_name: str, db_obj: dict[str, dict[str, Any]]
) -> None:
    path = os.path.join(root_dir, db_name)
    with open(path, encoding="utf-8") as pass_db:
        json.dump(db_obj, pass_db)
