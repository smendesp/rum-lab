from sqlalchemy import inspect
from sqlalchemy import types
import uuid

from app.config.settings import settings


class Utils:
    def object_as_dict(self, obj):
        return {
            c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    def default_format_date(self, date_time: types.DateTime):
        return date_time.strftime(settings.DB_DEFAULT_FORMAT_DATE)

    def generate_uuid(self):
        return str(uuid.uuid4())
