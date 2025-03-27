import datetime
import logging
import os
from typing import Any

from password_generator.generator import PasswordGenerator
from password_generator.utils import (
    Defaults,
    Envars,
    Keys,
    load_password_database,
    save_password_database,
)


class PasswordAdministrator:
    def __init__(self) -> None:
        self.root_dir: str = os.environ.get(Envars.root_dir, os.getcwd())
        self.db_name: str = os.environ.get(Envars.db_name, Defaults.db_name)
        self._pre_setup()
        self.pass_db: dict[str, dict[str, Any]] = load_password_database(
            root_dir=self.root_dir, db_name=self.db_name
        )

    def _pre_setup(self) -> None:
        path = os.path.join(self.root_dir, self.db_name)
        if not os.path.exists(path):
            save_password_database(self.root_dir, self.db_name, {})

    def add(
        self, service: str, user: str, method: str, length: int, use_symbols: bool
    ) -> None:
        generator = PasswordGenerator(method, length, use_symbols)
        if service in self.pass_db and user in self.pass_db[service]:
            logging.warning(
                f"There is already an account for service {service}. It would be overwritten."
            )
            self.pass_db[service][user][Keys.password] = generator.generate()
            self.pass_db[service][user][Keys.creation] = (
                datetime.datetime.now().isoformat()
            )

        else:
            self.pass_db[service][user] = {
                Keys.password: generator.generate(),
                Keys.creation: datetime.datetime.now().isoformat(),
            }
            logging.info(f"New account added to service {service} for user {user}")
        self.save()

    def delete(self, service: str, user: str) -> None:
        if service not in self.pass_db:
            logging.info(f"The service {service} doesn't exist!")

        if self.pass_db[service].pop(user, False):
            logging.info(f"Account for user {user} in service {service} was deleted!")
            self.save()
        else:
            logging.info(f"The user {user} doesn't exist for service {service}!")

    def search(self, service: str, user: str) -> None:
        if service in self.pass_db and user in self.pass_db[service]:
            password = self.pass_db[service][user][Keys.password]
            logging.info(
                f"Password for service: {service}, and user: {user} is {password}"
            )
        else:
            logging.info("Account not found!")

    def save(self) -> None:
        path = os.path.join(self.root_dir, self.db_name)
        save_password_database(self.root_dir, self.db_name, self.pass_db)
        logging.info(f"Database saved at {path}")
