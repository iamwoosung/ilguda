import strawberry

from schema.job_query import JobQuery

@strawberry.type
class Query(
        JobQuery
    ):
    pass