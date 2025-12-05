from config import client

sample_task_list = tasks = [
    {
        "title": "Prepare Monthly Sales Report",
        "description": "Compile sales data from CRM and generate the monthly performance report.",
        "note": "Include charts and year-to-date comparison."
    },
    {
        "title": "Design Landing Page Mockup",
        "description": "Create a UI/UX mockup for the new marketing landing page.",
        "note": "Use the updated brand color palette."
    },
    {
        "title": "Team Standup Meeting",
        "description": "Attend the daily standup meeting to discuss progress and blockers.",
        "note": "Keep updates under 2 minutes."
    },
    {
        "title": "Customer Onboarding Call",
        "description": "Guide the client through initial setup and platform features.",
        "note": "Record pain points for follow-up."
    },
    {
        "title": "Database Backup Verification",
        "description": "Verify that automated backups are running correctly and test restore.",
        "note": "Perform restore on staging DB only."
    },
    {
        "title": "Write API Documentation",
        "description": "Document the new endpoints added for the user authentication module.",
        "note": "Follow the OpenAPI documentation format."
    },
    {
        "title": "Update Product Pricing",
        "description": "Modify pricing plans on the website and admin dashboard.",
        "note": "Publish changes after legal team approval."
    },
    {
        "title": "Bug Fix: Login Timeout Issue",
        "description": "Investigate and resolve the issue causing user sessions to expire prematurely.",
        "note": "Reproduce issue using QA test accounts."
    },
    {
        "title": "Conduct Code Review",
        "description": "Review pull request #148 for code quality, performance, and security issues.",
        "note": "Pay attention to new dependency additions."
    },
    {
        "title": "Employee Training Session",
        "description": "Provide onboarding training to the new intern joining the tech team.",
        "note": "Prepare slides before the meeting."
    },
    {
        "title": "Inventory Stock Check",
        "description": "Check warehouse stock levels and update the inventory management system.",
        "note": "Notify procurement if any items fall below threshold."
    },
    {
        "title": "Email Marketing Campaign Setup",
        "description": "Set up and schedule the promotional email campaign for next week.",
        "note": "Include A/B subject line testing."
    },
    {
        "title": "Optimize Database Queries",
        "description": "Identify slow SQL queries and optimize them for better performance.",
        "note": "Start with user and order tables."
    },
    {
        "title": "Website Security Audit",
        "description": "Run a security scan and review potential vulnerabilities.",
        "note": "Focus on outdated dependencies."
    },
    {
        "title": "Prepare Presentation Slides",
        "description": "Create slides for the quarterly review meeting with stakeholders.",
        "note": "Use the corporate slide template."
    },
    {
        "title": "Update User Permissions",
        "description": "Adjust user roles and permissions based on the latest policy changes.",
        "note": "Double-check admin privileges."
    },
    {
        "title": "Social Media Content Plan",
        "description": "Prepare a weekly content schedule for all social media platforms.",
        "note": "Include visuals and caption drafts."
    },
    {
        "title": "Server Maintenance Cleanup",
        "description": "Remove unused logs, rotate old files, and free up server disk space.",
        "note": "Perform cleanup during low-traffic hours."
    }
]

TOKEN_ODD = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY1NzI2NjEwfQ.N1y_Fj2Wh-wqwpEpakAlV8cQLPku4LMYli4Za8iBeRI"
TOKEN_EVEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzY1NzI2NjEwfQ.6yNlN5CRWzC1uNoTOwdqHW_ZclFlpR50HLyg-2Mj9Ps"


def create_task(payload: dict, token: str):
    response = client.post(
        "/task/create",
        json=payload,
        headers={"x-api-token": token},
    )

    response.raise_for_status()
    return response.json()


def main():
    for index, task in enumerate(tasks, start=1):
        token = TOKEN_ODD if index % 2 == 1 else TOKEN_EVEN

        print(f"➡️ Creating Task #{index} using {'ODD token' if index % 2 == 1 else 'EVEN token'}...")

        result = create_task(task, token)

        print("✅ Created:", result)
        print("--------------------------------------------------")


if __name__ == '__main__':
    main()

"""

curl -X 'POST' \
  'http://127.0.0.1:8181/task/create' \
  -H 'accept: application/json' \
  -H 'x-api-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzY1NzI2NjEwfQ.N1y_Fj2Wh-wqwpEpakAlV8cQLPku4LMYli4Za8iBeRI' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Conduct User Feedback Survey",
    "description": "Prepare and distribute a survey to collect user feedback on the new features.",
    "note": "Analyze responses and summarize insights."
}'


curl -X 'POST' \
  'http://127.0.0.1:8181/task/create' \
  -H 'accept: application/json' \
  -H 'x-api-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzY1NzI2NjEwfQ.6yNlN5CRWzC1uNoTOwdqHW_ZclFlpR50HLyg-2Mj9Ps' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Configure CI/CD Pipeline",
    "description": "Set up automated build, test, and deployment workflow for the application.",
    "note": "Integrate with GitLab CI and add environment-specific variables."
}'

"""
