from collections.abc import Collection, Iterator, Mapping, Sequence
from typing import Any, NamedTuple

from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.utils import tree

class PathInfo(NamedTuple):
    from_opts: Any
    to_opts: Any
    target_fields: Any
    join_field: Any
    m2m: Any
    direct: Any
    filtered_relation: Any

class InvalidQuery(Exception): ...

def subclasses(
    cls: type[RegisterLookupMixin],
) -> Iterator[type[RegisterLookupMixin]]: ...

class QueryWrapper:
    contains_aggregate: bool = ...
    data: tuple[str, list[Any]] = ...
    def __init__(self, sql: str, params: list[Any]) -> None: ...
    def as_sql(self, compiler: SQLCompiler = ..., connection: Any = ...) -> Any: ...

class Q(tree.Node):
    AND: str = ...
    OR: str = ...
    conditional: bool = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __or__(self, other: Any) -> Q: ...
    def __and__(self, other: Any) -> Q: ...
    def __invert__(self) -> Q: ...
    def resolve_expression(
        self,
        query: Query = ...,
        allow_joins: bool = ...,
        reuse: set[str] | None = ...,
        summarize: bool = ...,
        for_save: bool = ...,
    ) -> WhereNode: ...
    def deconstruct(self) -> tuple[str, tuple[Any, ...], dict[str, str]]: ...

class DeferredAttribute:
    field_name: str = ...
    field: Field[Any, Any]
    def __init__(self, field_name: str) -> None: ...

class RegisterLookupMixin:
    lookup_name: str
    @classmethod
    def get_lookups(cls) -> dict[str, Any]: ...
    def get_lookup(self, lookup_name: str) -> Any | None: ...
    def get_transform(self, lookup_name: str) -> Any | None: ...
    @staticmethod
    def merge_dicts(dicts: list[dict[str, Any]]) -> dict[str, Any]: ...
    @classmethod
    def register_lookup(
        cls, lookup: Any, lookup_name: str | None = ...
    ) -> type[Any]: ...
    @classmethod
    def _unregister_lookup(cls, lookup: Any, lookup_name: str | None = ...) -> Any: ...

def select_related_descend(
    field: Field[Any, Any],
    restricted: bool,
    requested: Mapping[str, Any] | None,
    load_fields: Collection[str] | None,
    reverse: bool = ...,
) -> bool: ...
def refs_expression(
    lookup_parts: Sequence[str], annotations: Mapping[str, bool]
) -> tuple[bool, Sequence[str]]: ...
def check_rel_lookup_compatibility(
    model: type[Model], target_opts: Any, field: FieldCacheMixin
) -> bool: ...

class FilteredRelation:
    relation_name: str = ...
    alias: str | None = ...
    condition: Q = ...
    path: list[str] = ...
    def __init__(self, relation_name: str, *, condition: Any = ...) -> None: ...
    def clone(self) -> FilteredRelation: ...
    def resolve_expression(self, *args: Any, **kwargs: Any) -> None: ...
    def as_sql(self, compiler: SQLCompiler, connection: Any) -> Any: ...