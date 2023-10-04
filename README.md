
# Employee Expense Portal

## About the Project

The Employee Expense Portal is a web application built using Flask, designed to simplify and automate the process of tracking and managing employee expenses within an organization. It provides an intuitive interface for employees to submit expense claims and for managers to review and approve or reject them.

## Problem Statement

Many businesses face challenges in efficiently managing employee expenses. Traditional methods like paper receipts and manual spreadsheets can be time-consuming and error-prone. This often leads to delays in reimbursement and frustration among employees. The Employee Expense Portal aims to address these issues by providing a digital platform for managing expenses.

## How the Project Works

The Employee Expense Portal consists of three main components:

1. **Employee Dashboard**: Employees can log in to the portal, enter details of their expenses, and submit them for approval. They can also track the status of their claims.

2. **Manager Dashboard**: Managers have access to a dashboard where they can review expense claims submitted by employees. They can then either approve or reject the claims. Managers can also generate reports related to expenses.

3. **Admin Panel**: The admin panel allows administrators to manage user accounts, assign roles and permissions, and oversee the overall functioning of the portal.

## Features

- User authentication and authorization
- The portal is equipped with the ability to send email notifications. When an employee submits an expense, they receive a confirmation email. Furthermore, they are promptly notified via email when their expense request is either approved or rejected. This feature ensures timely and transparent communication between employees and the management.
- User-friendly interfaces for employees and managers
- Secure submission and storage of expense data
- Notification system for status updates on expense claims
- Reporting functionality for managers and administrators
- Role-based access control

## Getting Started

### Prerequisites

- Python 3.x installed
- pip package manager
- MongoDB database set up

### Installation

1. Clone the repository:

```bash
git clone https://github.com/loki4514/Employee-Expense-Portal.git
```

### Navigate to the project directory and Install the required packages:

```bash
pip install -r requirements.txt
```

### Start the Flask application:
```bash
python run.py
```




