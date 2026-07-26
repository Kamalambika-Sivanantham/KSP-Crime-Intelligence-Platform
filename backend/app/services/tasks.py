"""
Background tasks. These run in the celery_worker container.
Notification delivery (email/SMS/push) and report generation are wired here
so the API can enqueue work instead of blocking the request thread.
"""
from app.services.celery_app import celery_app


@celery_app.task(name="tasks.send_high_risk_alert")
def send_high_risk_alert(district_name: str, risk_score: float, recipient_emails: list[str]):
    # Wire to an actual SMTP/SNS provider in production; logs for now so the
    # pipeline is observable end-to-end during development.
    print(f"[ALERT] High risk score {risk_score} detected in {district_name}. "
          f"Notifying: {recipient_emails}")
    return {"status": "sent", "recipients": len(recipient_emails)}


@celery_app.task(name="tasks.generate_daily_report")
def generate_daily_report(district_id: str | None = None):
    print(f"[REPORT] Generating daily crime report for district={district_id or 'ALL'}")
    return {"status": "queued", "district_id": district_id}
