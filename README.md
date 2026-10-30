# Factory RAPID Application Documentation

## Overview

The Factory RAPID app is a modular, cross-platform application for managing, tracking, and printing production data for manufacturing parts, jobs, and stations. It is built using Python, wxPython for GUI, and integrates with both MSSQL and PostgreSQL databases. The app supports barcode generation, PDF printing, and flexible configuration.

***

## Table of Contents

1.  **Architecture & Components**
2.  **Configuration**
3.  **Core Modules**
    *   printLib.py
    *   rapidJob.py
    *   rapidSinglePart.py
    *   rapidModel.py / rapidModel2.py
    *   rapid-enter.py
    *   rapid-station.py
4.  **Database Integration**
5.  **GUI Features**
6.  **Printing & Barcode**
7.  **Requirements**
8.  **Extending & Customising**
9.  **Troubleshooting**

***

## 1. Architecture & Components

*   **Modular Design:** Each major workflow (job, part, station) is handled by a dedicated module.
*   **Database Layer:** Supports MSSQL (production/archive) and PostgreSQL (rapid).
*   **GUI Layer:** wxPython dialogs and frames for user interaction.
*   **Printing Layer:** PDF generation and barcode printing via ReportLab.
*   **Configuration:** Centralised via rapid.ini.

***

## 2. Configuration (`rapid.ini`)

*   **Delimiters:** Set for reading/writing CSV data.
*   **Database Settings:** Credentials and table names for MSSQL production/archive servers.
*   **Part Settings:** Enable/disable editing and creation of new parts.
*   **Visible Stations:** Toggle visibility of workflow stations (allocations, bay drops, purchasing, etc.).

***

## 3. Core Modules

### `printLib.py`

*   **Purpose:** Handles PDF generation, barcode creation, and printing utilities.
*   **Key Features:**
    *   Table and paragraph formatting for PDF output.
    *   Barcode support (Code128, Code39, etc.).
    *   Label printing for parts (includes part ID, job, material, dimensions, edge, comments).
    *   PDF preview via wxPython.

### `rapidJob.py`

*   **Purpose:** Manages job-level operations.
*   **Features:**
    *   Job part management dialog.
    *   Grid for displaying/editing job parts.
    *   Add, edit, print, and save job parts.
    *   Integration with rapidModel2 for database updates.

### `rapidSinglePart.py`

*   **Purpose:** Manages single part operations.
*   **Features:**
    *   Dialog for viewing/editing a single part.
    *   Add new part, edit, print label, save, and close.
    *   Station and tool selection.
    *   Integration with rapidModel2 for database updates.

### `rapidModel.py` / `rapidModel2.py`

*   **Purpose:** Database access and business logic.
*   **Features:**
    *   Connects to MSSQL (`rapidModel.py`) and PostgreSQL (`rapidModel2.py`).
    *   CRUD operations for parts and jobs.
    *   Move parts between stations, set reasons, update details.
    *   Retrieve job/part data for printing and display.

### `rapid-enter.py`

*   **Purpose:** Main entry point for RAPID defect entry and job printing.
*   **Features:**
    *   Frame for entering defects (missing, chipped, scratched, etc.).
    *   Combo boxes for selecting reasons and stations.
    *   Print job RAPIDs and workstation jobs.
    *   Integrates with rapidModel2 and printLib.

### `rapid-station.py`

*   **Purpose:** Main entry point for station-level management.
*   **Features:**
    *   Frame for managing parts across stations.
    *   Grid for job list and part details.
    *   Buttons for moving parts between stations.
    *   Print job RAPIDs and workstation jobs.
    *   Integrates with rapidModel2 and printLib.

***

## 4. Database Integration

*   **MSSQL:** Used for production and archive data (see rapidModel.py).
*   **PostgreSQL:** Used for rapid data (see rapidModel2.py).
*   **Configurable:** Database credentials and tables set in rapid.ini.
*   **Functions:** Connect, fetch, update, insert, and move parts/jobs.

***

## 5. GUI Features

*   **wxPython Dialogs/Frames:** For job, part, and station management.
*   **Grids:** Display part/job data with editable cells.
*   **Combo Boxes:** For selecting stations, tools, reasons.
*   **Buttons:** For actions (add, edit, print, save, move).
*   **Barcode Scanning:** Supports part ID entry via barcode.

***

## 6. Printing & Barcode

*   **PDF Generation:** Uses ReportLab for formatted output.
*   **Barcode Support:** Code128, Code39, and others for part IDs.
*   **Label Printing:** Customisable labels for parts/jobs.
*   **Preview:** PDF preview window before printing.

***

## 7. Requirements (`requirements.txt`)

*   **Python Packages:**
    *   wxPython (GUI)
    *   numpy (data handling)
    *   reportlab (PDF/barcode)
    *   pymssql, psycopg2 (database)
    *   Pillow, PyPDF2, PyMuPDF (PDF/image)
    *   Others for utility and compatibility

***

## 8. Extending & Customising

*   **Add Stations:** Update rapid.ini and relevant modules.
*   **Custom Labels:** Modify printLib.py for label layout.
*   **Database Schema:** Adjust rapidModel.py/rapidModel2.py for new fields.
*   **GUI Layout:** Use wxGlade or edit Python code for new dialogs/frames.
*   **Barcode Types:** Add new barcode formats in printLib.py.

***

## 9. Troubleshooting

*   **Database Connection Errors:** Check rapid.ini for correct credentials.
*   **Missing Packages:** Install all requirements via `pip install -r requirements.txt`.
*   **GUI Issues:** Ensure wxPython is installed and compatible with your OS.
*   **Printing Problems:** Verify ReportLab and Pillow installations.

***

## Example Workflow

1.  **Start Application:** Run rapid-enter.py or rapid-station.py.
2.  **Enter/Scan Part:** Use barcode or manual entry.
3.  **Edit/Move Part:** Use dialogs to update part/job details and move between stations.
4.  **Print Labels/Reports:** Generate and preview PDFs for jobs, parts, or stations.
5.  **Database Sync:** All changes are reflected in the configured database.

***

## File Summary

| File               | Purpose/Role                                 |
| ------------------ | -------------------------------------------- |
| printLib.py        | PDF/barcode printing utilities               |
| rapid.ini          | Configuration (database, stations, settings) |
| rapid-enter.py     | Main defect entry and job printing GUI       |
| rapidJob.py        | Job management dialog                        |
| rapidSinglePart.py | Single part management dialog                |
| rapidModel.py      | MSSQL database logic                         |
| rapidModel2.py     | PostgreSQL database logic                    |
| rapid-station.py   | Station management GUI                       |
| README.md          | (Empty/placeholder)                          |
| requirements.txt   | Python package dependencies                  |

***

## Getting Started

1.  **Install Python 3.7+**
2.  **Install dependencies:**  
    `pip install -r requirements.txt`
3.  **Configure rapid.ini:**  
    Set database credentials, stations, and settings.
4.  **Run the application:**  
    `python rapid-enter.py` or `python rapid-station.py`
5.  **Use the GUI:**  
    Manage jobs, parts, stations, and print labels/reports.

***

## Support & Maintenance

*   **Customisation:** Update configuration and Python modules as needed.
*   **Database:** Ensure backups and maintenance for MSSQL/PostgreSQL.
*   **Updates:** Regularly update Python packages for security and compatibility.

***

