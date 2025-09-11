from typing import Optional, List, Text
import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.lib.database.utils import Utils as DataBaseUtils


# TODO: quando for validar dados com e-mail, passwords e afins usar o pydantic, que ja possui essas validações e são mais seguras


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime]

    updated_at: Mapped[Optional[datetime.datetime]]
    updated_by: Mapped[Optional[Optional[str]]]
    updated_log: Mapped[Optional[Optional[Text]]]

    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by: Mapped[Optional[Optional[str]]]
    deleted_log: Mapped[Optional[Optional[Text]]]
    deleted: Mapped[Optional[Optional[bool]]] = mapped_column(default=False)


class RUMEvent(Base):
    __tablename__ = 'rum_events'

    id: Mapped[str] = mapped_column(
        String(36),
        name='id',
        primary_key=True,
        default=DataBaseUtils.generate_uuid,
    )

    event_type: Mapped[str] = mapped_column()
    event_tumestamp: Mapped[str] = mapped_column()
    event_position_x: Mapped[int] = mapped_column()
    event_position_y: Mapped[int] = mapped_column()

    rum_elements: Mapped[RUMElement] = relationship(
        back_populates='rum_event', cascade='all, delete-orphan'
    )

    rum_pages: Mapped[RUMPage] = relationship(
        back_populates='rum_event', cascade='all, delete-orphan'
    )

    rum_users: Mapped[RUMUser] = relationship(
        back_populates='rum_event', cascade='all, delete-orphan'
    )

    rum_meta_data: Mapped[RUMetaData] = relationship(
        back_populates='rum_event', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'RUMEvent(id={self.id!r}, event_type={self.event_type!r}, event_timestamp={self.event_timestamp!r})'


class RUMElement(Base):
    __tablename__ = 'rum_elements'

    id: Mapped[str] = mapped_column(
        String(36),
        name='id',
        primary_key=True,
        default=DataBaseUtils.generate_uuid,
    )

    element_id: Mapped[str] = mapped_column()
    element_name: Mapped[str] = mapped_column()
    element_tag_name: Mapped[str] = mapped_column()
    element_text: Mapped[str] = mapped_column()

    rum_event: Mapped[RUMEvent] = relationship(
        back_populates='rum_elements', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'RUMElement(id={self.id!r}, element_id={self.element_id!r}, element_name={self.element_name!r}, element_tag_name={self.element_tag_name!r}, element_text={self.element_text!r})'


class RUMPage(Base):
    __tablename__ = 'rum_pages'

    id: Mapped[str] = mapped_column(
        String(36),
        name='id',
        primary_key=True,
        default=DataBaseUtils.generate_uuid,
    )

    referrer: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()

    rum_event: Mapped[RUMEvent] = relationship(
        back_populates='rum_pages', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'RUMPage(id={self.id!r}, referrer={self.referrer!r}, title={self.title!r}, url={self.url!r})'


class RUMUser(Base):
    __tablename__ = 'rum_users'

    id: Mapped[str] = mapped_column(
        String(36),
        name='id',
        primary_key=True,
        default=DataBaseUtils.generate_uuid,
    )

    agent: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column()
    timezone: Mapped[str] = mapped_column()

    rum_event: Mapped[RUMEvent] = relationship(
        back_populates='rum_users', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'RUMUser(id={self.id!r}, agent={self.agent!r}, language={self.language!r}, timezone={self.timezone!r})'


class RUMetaData(Base):
    __tablename__ = 'rum_meta_data'

    id: Mapped[str] = mapped_column(
        String(36),
        name='id',
        primary_key=True,
        default=DataBaseUtils.generate_uuid,
    )

    app_version: Mapped[str] = mapped_column()
    environment: Mapped[str] = mapped_column()

    rum_event: Mapped[RUMEvent] = relationship(
        back_populates='rum_meta_data', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'RUMetaData(id={self.id!r}, app_version={self.app_version!r}, environment={self.environment!r})'
