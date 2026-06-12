# MyHouse24 CRM

MyHouse24 is a comprehensive Customer Relationship Management (CRM) system tailored for property management and residential complex administration. It provides a centralized platform for managing residents, apartments, utility bills, maintenance requests, and communication.

## Key Features

*   **User Management:** Secure authentication and authorization, with specialized roles for administrators, staff, and residents.
*   **Property Management:** Structured organization of residential complexes, buildings, sections, floors, and individual apartments.
*   **Billing and Utilities:** Management of utility meters, tariff generation, and automated invoice processing.
*   **Service Requests:** A ticketing system for residents to submit maintenance requests and for staff to track their resolution.
*   **Communication:** Integrated email sending capabilities and rich text announcements for residents.
*   **Data Export & Reporting:** Automated generation of PDF documents and receipts, as well as data management with Excel spreadsheets.
*   **Security:** Integrated hCaptcha for spam prevention and administrative troubleshooting tools.

## Tech Stack

*   **Core:** Python 3.13, Django 5.1
*   **API:** Django Ninja, Django REST Framework (SimpleJWT)
*   **Database:** PostgreSQL
*   **Asynchronous Tasks:** Celery, Redis
*   **Tools & Utilities:** 
    *   **PDF Generation:** WeasyPrint
    *   **Email Services:** Django Anymail (Brevo)
    *   **Text Editing:** Django CKEditor
    *   **Data Processing:** Openpyxl (Excel), Pillow (Images)
    *   **Frontend Integration:** Django AJAX Datatable, Django Select2

## Development

The project utilizes `pre-commit` hooks alongside tools like `djlint` to ensure code quality and maintain formatting standards across the codebase.