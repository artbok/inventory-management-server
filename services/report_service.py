from peewee import *
from models.report import Report


def createReport(text) -> None:
    Report.create(text = text)


def getReports(page) -> list[Report]:
    reports = []
    for report in Report.select().order_by(Report.id.desc()).paginate(page, 10):
        reports.append({
            'text': report.text,
            'date': str(report.date.strftime('%d-%m-%Y %H:%M'))
        })
    return reports


if not Report.table_exists():
    Report.create_table()
    print("Table 'Report' created")