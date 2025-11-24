import strawberry

from schema.job.query import JobQuery

@strawberry.type
class Query(
        JobQuery
    ):
    pass
