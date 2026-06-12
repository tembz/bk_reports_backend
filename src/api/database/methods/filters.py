from api.database.models import Report, Credit

def apply_report_filters(stmt, filters: dict):
    if not filters:
        return stmt

    active_types = [t for t, is_active in filters.items() if is_active]

    if not active_types:
        return stmt

    stmt = stmt.where(Report.report_type.in_(active_types))

    return stmt


def apply_credit_filters(stmt, filters: dict):
    if not filters:
        return stmt

    if filters.get("only_transfer"):
        stmt = stmt.where(Credit.is_transfer == True)

    if filters.get("active") and not filters.get("inactive"):
        stmt = stmt.where(Credit.is_active == True)
    elif filters.get("inactive") and not filters.get("active"):
        stmt = stmt.where(Credit.is_active == False)

    return stmt