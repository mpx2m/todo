from enum import Enum


class TodoStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class TodoPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DependencyStatus(str, Enum):
    UNBLOCKED = "UNBLOCKED"
    BLOCKED = "BLOCKED"


class Recurrence(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    CUSTOM = "CUSTOM"


class RecurrenceUnit(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class TodoHistoryChangeBy(str, Enum):
    MANUAL = "MANUAL"
    RECURRENCE = "RECURRENCE"


class SortBy(str, Enum):
    DUE_DATE = "dueDate"
    PRIORITY = "priority"
    STATUS = "status"
    NAME = "name"


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"
