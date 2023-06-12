from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
Java: LanguageId
Python: LanguageId
kotlin: LanguageId

class Code(_message.Message):
    __slots__ = ["languageId", "text"]
    LANGUAGEID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    languageId: LanguageId
    text: str
    def __init__(self, text: _Optional[str] = ..., languageId: _Optional[_Union[LanguageId, str]] = ...) -> None: ...

class InitResult(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class InspectionResult(_message.Message):
    __slots__ = ["problems"]
    PROBLEMS_FIELD_NUMBER: _ClassVar[int]
    problems: _containers.RepeatedCompositeFieldContainer[Problem]
    def __init__(self, problems: _Optional[_Iterable[_Union[Problem, _Mapping]]] = ...) -> None: ...

class Problem(_message.Message):
    __slots__ = ["inspector", "length", "lineNumber", "name", "offset"]
    INSPECTOR_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    LINENUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    inspector: str
    length: int
    lineNumber: int
    name: str
    offset: int
    def __init__(self, name: _Optional[str] = ..., inspector: _Optional[str] = ..., lineNumber: _Optional[int] = ..., offset: _Optional[int] = ..., length: _Optional[int] = ...) -> None: ...

class Service(_message.Message):
    __slots__ = ["languageId", "name"]
    LANGUAGEID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    languageId: LanguageId
    name: str
    def __init__(self, name: _Optional[str] = ..., languageId: _Optional[_Union[LanguageId, str]] = ...) -> None: ...

class LanguageId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
