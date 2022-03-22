"""
Injected database interface dependencies
"""
import inspect
from contextlib import ExitStack, contextmanager
from functools import wraps
from typing import Callable

from prefect.orion.database.configurations import (
    AioSqliteConfiguration,
    AsyncPostgresConfiguration,
    BaseDatabaseConfiguration,
)
from prefect.orion.database.interface import OrionDBInterface
from prefect.orion.database.orm_models import (
    AioSqliteORMConfiguration,
    AsyncPostgresORMConfiguration,
    BaseORMConfiguration,
)
from prefect.orion.database.query_components import (
    AioSqliteQueryComponents,
    AsyncPostgresQueryComponents,
    BaseQueryComponents,
)
from prefect.orion.utilities.database import get_dialect
from prefect.settings import PREFECT_ORION_DATABASE_CONNECTION_URL

MODELS_DEPENDENCIES = {
    "database_config": None,
    "query_components": None,
    "orm": None,
}


def provide_database_interface() -> OrionDBInterface:
    """
    Get the current orion database interface.

    If components of the interface are not set, defaults will be inferred
    based on the dialect of the connection url.
    """
    connection_url = PREFECT_ORION_DATABASE_CONNECTION_URL.value()

    database_config = MODELS_DEPENDENCIES.get("database_config")
    query_components = MODELS_DEPENDENCIES.get("query_components")
    orm = MODELS_DEPENDENCIES.get("orm")
    dialect = get_dialect(connection_url)

    if database_config is None:

        if dialect.name == "postgresql":
            database_config = AsyncPostgresConfiguration(connection_url=connection_url)
        elif dialect.name == "sqlite":
            database_config = AioSqliteConfiguration(connection_url=connection_url)
        else:
            raise ValueError(
                f"Unable to infer database configuration from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["database_config"] = database_config

    if query_components is None:
        if dialect.name == "postgresql":
            query_components = AsyncPostgresQueryComponents()
        elif dialect.name == "sqlite":
            query_components = AioSqliteQueryComponents()
        else:
            raise ValueError(
                f"Unable to infer query components from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["query_components"] = query_components

    if orm is None:
        if dialect.name == "postgresql":
            orm = AsyncPostgresORMConfiguration()
        elif dialect.name == "sqlite":
            orm = AioSqliteORMConfiguration()
        else:
            raise ValueError(
                f"Unable to infer orm configuration from provided dialect. Got dialect name {dialect.name!r}"
            )

        MODELS_DEPENDENCIES["orm"] = orm

    return OrionDBInterface(
        database_config=database_config,
        query_components=query_components,
        orm=orm,
    )


def inject_db(fn: Callable) -> Callable:
    """
    Decorator that provides a database interface to a function.

    The decorated function _must_ take a `db` kwarg and if a db is passed
    when called it will be used instead of creating a new one.

    If the function is a coroutine function, the wrapper will await the
    function's result. Otherwise, the wrapper will call the function
    normally.
    """

    def inject(kwargs):
        if "db" not in kwargs or kwargs["db"] is None:
            kwargs["db"] = provide_database_interface()

    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        inject(kwargs)
        return await fn(*args, **kwargs)

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        inject(kwargs)
        return fn(*args, **kwargs)

    if inspect.iscoroutinefunction(fn):
        return async_wrapper
    return sync_wrapper


@contextmanager
def temporary_database_config(tmp_database_config: BaseDatabaseConfiguration):
    """
    Temporarily override the Orion database configuration.
    When the context is closed, the existing database configuration will
    be restored.

    Args:
        tmp_database_config: Orion database configuration to inject.

    """
    starting_config = MODELS_DEPENDENCIES["database_config"]
    try:
        MODELS_DEPENDENCIES["database_config"] = tmp_database_config
        yield
    finally:
        MODELS_DEPENDENCIES["database_config"] = starting_config


@contextmanager
def temporary_query_components(tmp_queries: BaseQueryComponents):
    """
    Temporarily override the Orion database query components.
    When the context is closed, the existing query components will
    be restored.

    Args:
        tmp_queries: Orion query components to inject.

    """
    starting_queries = MODELS_DEPENDENCIES["query_components"]
    try:
        MODELS_DEPENDENCIES["query_components"] = tmp_queries
        yield
    finally:
        MODELS_DEPENDENCIES["query_components"] = starting_queries


@contextmanager
def temporary_orm_config(tmp_orm_config: BaseORMConfiguration):
    """
    Temporarily override the Orion orm configuration.
    When the context is closed, the existing orm configuration will
    be restored.

    Args:
        tmp_orm_config: Orion orm configuration to inject.

    """
    starting_orm_config = MODELS_DEPENDENCIES["orm"]
    try:
        MODELS_DEPENDENCIES["orm"] = tmp_orm_config
        yield
    finally:
        MODELS_DEPENDENCIES["orm"] = starting_orm_config


@contextmanager
def temporary_database_interface(
    tmp_database_config: BaseDatabaseConfiguration = None,
    tmp_queries: BaseQueryComponents = None,
    tmp_orm_config: BaseORMConfiguration = None,
):
    """
    Temporarily override the Orion database interface.

    Any interface components that are not explicitly provided will be
    cleared and inferred from the Orion database connection string
    dialect.

    When the context is closed, the existing database interface will
    be restored.

    Args:
        tmp_database_config: An optional Orion database configuration to inject.
        tmp_orm_config: An optional Orion orm configuration to inject.
        tmp_queries: Optional Orion query components to inject.

    """
    with ExitStack() as stack:
        stack.enter_context(
            temporary_database_config(tmp_database_config=tmp_database_config)
        )
        stack.enter_context(temporary_query_components(tmp_queries=tmp_queries))
        stack.enter_context(temporary_orm_config(tmp_orm_config=tmp_orm_config))
        yield


def set_database_config(database_config: BaseDatabaseConfiguration):
    """Set Orion database configuration."""
    MODELS_DEPENDENCIES["database_config"] = database_config


def set_query_components(query_components: BaseQueryComponents):
    """Set Orion query components."""
    MODELS_DEPENDENCIES["query_components"] = query_components


def set_orm_config(orm_config: BaseORMConfiguration):
    """Set Orion orm configuration."""
    MODELS_DEPENDENCIES["orm"] = orm_config
