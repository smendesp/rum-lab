from datetime import datetime

from app.lib.database.session import session
from app.lib.database.utils import Utils as DatabaseUtils
from app.services.utils import Utils

from app.models.entities import Address, UserAccount
from app.lib.logger import Logger

# from opentelemetry.trace import get_tracer


class UserAccountService:

    def __init__(self):
        self.log = Logger()
        self.database_utils = DatabaseUtils()
        self.utils = Utils()
        # self.tracer = get_tracer()

    def add(self, data=None):
        try:
            if data is None:
                raise ValueError("Data is required for update")

            data = dict(data)

            # with self.tracer.start_as_current_span("Add User"):

            session.add(
                UserAccount(
                    name=data["name"],
                    fullname=data["fullname"],
                    created_at=self.database_utils.default_format_date(datetime.now()),
                )
            )
            session.commit()

        except (ValueError, KeyError) as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except Exception as error:
            session.rollback()
            self.log.logger.error(error)
            raise error

        finally:
            session.close()

    def select_by_id(self, user_id=None):

        try:
            if user_id is None:
                raise ValueError("User ID is required for deletion")

            user_account = (
                session.query(UserAccount).filter(UserAccount.id == user_id).first()
            )

            if user_account is None:
                raise ValueError(f"User account with ID {user_id} not found")

            session.commit()

            # Return the updated user account as dict
            return self.database_utils.object_as_dict(user_account)

        except (ValueError, KeyError) as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except Exception as error:
            self.log.logger.error(f"Error restoring user account: {error}")
            raise error

        finally:
            session.close()

    def select_all(self):

        try:
            user_account_list: list[UserAccount] = []
            for user_account in (
                session.query(UserAccount).filter((UserAccount.deleted == False)).all()
            ):
                user_account_list.append(
                    self.database_utils.object_as_dict(user_account)
                )

            return user_account_list

        except IndentationError as error:
            self.log.logger.error(error)
            raise error

        except Exception as error:
            self.log.logger.error(error)
            raise error

    def hard_delete(self, user_id=None):
        try:
            if user_id is None:
                raise ValueError("User ID is required for deletion")

            user_account = (
                session.query(UserAccount).filter(UserAccount.id == user_id).first()
            )

            if user_account is None:
                raise ValueError(f"User account with ID {user_id} not found")

            session.delete(user_account)
            session.commit()

            self.log.logger.info(f"User account with ID {user_id} deleted successfully")
            return True

        except ValueError as error:
            self.log.logger.error(f"Validation error: {error}")
            raise error

        except Exception as error:
            session.rollback()
            self.log.logger.error(f"Error deleting user account: {error}")
            raise error

        finally:
            session.close()

    # TODO: Criar o soft delete cascade
    def delete(self, user_id=None):
        try:
            if user_id is None:
                raise ValueError("User ID is required for update")

            user_account = (
                session.query(UserAccount).filter(UserAccount.id == user_id).first()
            )

            if user_account is None:
                raise ValueError(f"User account with ID {user_id} not found")

            if user_account.deleted:
                raise KeyError(
                    f"User account with ID {user_id} is deleted in {user_account.deleted_at} by {user_account.deleted_by}"
                )

            user_account.deleted_at = self.database_utils.default_format_date(
                datetime.now()
            )

            pyproject = self.utils.get_pyproject()
            deleted_log = ""

            if user_account.deleted_log is not None:
                deleted_log = f"{user_account.deleted_log}:"

            # TODO: Pegar os dados do usuário para gravar no soft delete
            user_account.deleted_log = f"{deleted_log}{pyproject["project"]["name"]};{pyproject["project"]["version"]};MEUNOME"
            user_account.deleted_by = "dfsadfsadfsd"
            user_account.deleted = True

            session.commit()

            self.log.logger.info(f"User account with ID {user_id} deleted successfully")

            # Return the updated user account as dict
            return self.database_utils.object_as_dict(user_account)

        except (ValueError, KeyError) as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except Exception as error:
            session.rollback()
            self.log.logger.error(f"Error deteting user account: {error}")
            raise error

        finally:
            session.close()

    # TODO: Criar o soft delete cascade
    def restore(self, user_id=None):
        try:
            if user_id is None:
                raise ValueError("User ID is required for update")

            user_account = (
                session.query(UserAccount).filter(UserAccount.id == user_id).first()
            )

            if user_account is None:
                raise ValueError(f"User account with ID {user_id} not found")

            if not user_account.deleted:
                raise KeyError(f"User account with ID {user_id} is active")

            restored_at = self.database_utils.default_format_date(datetime.now())

            pyproject = self.utils.get_pyproject()
            restored_log = ""

            if user_account.deleted_log is not None:
                restored_log = f"{user_account.deleted_log}:"

            # TODO: Pegar os dados do usuário para gravar no soft delete
            user_account.deleted_at = restored_at
            user_account.deleted_log = f"{restored_log}restored_at={restored_at};{pyproject["project"]["name"]};{pyproject["project"]["version"]};MEUNOME"
            user_account.deleted_by = "dfsadfsadfsd"
            user_account.deleted = False

            session.commit()

            self.log.logger.info(
                f"User account with ID {user_id} restored successfully"
            )

            # Return the updated user account as dict
            return self.database_utils.object_as_dict(user_account)

        except KeyError as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except (ValueError, KeyError) as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except Exception as error:
            session.rollback()
            self.log.logger.error(f"Error restoring user account: {error}")
            raise error

        finally:
            session.close()

    def update(self, user_id=None, data=None):
        try:
            if user_id is None:
                raise ValueError("User ID is required for update")

            if data is None:
                raise ValueError("Data is required for update")

            data = dict(data)

            user_account = (
                session.query(UserAccount).filter(UserAccount.id == user_id).first()
            )

            if user_account is None:
                raise ValueError(f"User account with ID {user_id} not found")

            if "name" in data:
                user_account.name = data["name"]

            if "fullname" in data:
                user_account.fullname = data["fullname"]

            pyproject = self.utils.get_pyproject()
            updated_log = ""

            if user_account.updated_log is not None:
                updated_log = f"{user_account.updated_log}:"

            # TODO: Pegar os dados do usuário para gravar no update
            user_account.updated_log = f"{updated_log}{pyproject["project"]["name"]};{pyproject["project"]["version"]};MEUNOME"
            user_account.updated_by = "dfsadfsadfsd"

            user_account.updated_at = self.database_utils.default_format_date(
                datetime.now()
            )

            session.commit()

            self.log.logger.info(f"User account with ID {user_id} updated successfully")

            # Return the updated user account as dict
            return self.database_utils.object_as_dict(user_account)

        except (ValueError, KeyError) as error:
            self.log.logger.error(f"Data validation error: {error}")
            raise error

        except Exception as error:
            session.rollback()
            self.log.logger.error(f"Error updating user account: {error}")
            raise error

        finally:
            session.close()
