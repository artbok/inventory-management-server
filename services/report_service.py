from peewee import *
from models.report import Report


def createReport(text) -> None:
    Report.create(text = text)


def getReports(page) -> list[Report]:
    reports = []
    for report in Report.select().paginate(page, 10):
        reports.append({
            'text': report.text,
            'date': str(report.date)
        })
    return reports


if not Report.table_exists():
    Report.create_table()
    print("Table 'Report' created")