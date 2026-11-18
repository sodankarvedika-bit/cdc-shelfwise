# CP-035 ShelfWise: Library Circulation and Reservation Management System

## Team
Vedika.P (1AT24AI113), Vanaparthi Sai Sri Nidhi (1AT24AI111), Python Track

## How to run
```bash
python main.py
```

## Features that work

1. Add books with book ID, title, author and number of copies.
2. Register library members with member ID, name and phone number.
3. Issue books to registered members only if copies are available and the member is within the borrowing limit (maximum 3 books).
4. Return books and automatically calculate fines based on overdue days (₹2 per day).
5. Search books by title or author.
6. Display overdue books with member details, due dates and estimated fines.
7. Reserve unavailable books and notify the first waiting member when a copy is returned.

## Library Rules

- Maximum borrowing limit: 3 books per member.
- Borrowing period: 14 days.
- Fine: ₹2 per overdue day.
- Reservations follow the first-come, first-served order.

## Sample run

```text
=================================================================
       CP-035 SHELFWISE: LIBRARY MANAGEMENT SYSTEM
=================================================================
 1. Add New Book
 2. Register Member
 3. Issue Book
 4. Return Book
 5. Search Books
 6. Overdue Book Report
 7. Reserve Book
 0. Exit Application
=================================================================
Select an option (0-7): 1

===== ADD NEW BOOK =====
Enter Book ID: B101
Enter Book Title: Python Programming
Enter Author Name: Mark Lutz
Enter Number of Copies: 5

[SUCCESS] Book added successfully!

Select an option (0-7): 2

===== REGISTER MEMBER =====
Enter Member ID: M101
Enter Member Name: Vedika
Enter Phone Number: 9876543210

[SUCCESS] Member registered successfully!

Select an option (0-7): 3

===== ISSUE BOOK =====
Enter Book ID: B101
Enter Member ID: M101

[SUCCESS] Book issued successfully!
Book Title: Python Programming
Member: Vedika
Issue Date: 2026-11-16
Due Date: 2026-11-30

Select an option (0-7): 5

===== SEARCH BOOKS =====
Enter Book Title or Author: Python

ID       TITLE                AUTHOR          AVAILABLE
B101     Python Programming   Mark Lutz       4

Select an option (0-7): 4

===== RETURN BOOK =====
Enter Issue ID: I101

[SUCCESS] Book returned successfully!
Overdue Days: 0
Fine Amount: Rs. 0

Select an option (0-7): 6

===== OVERDUE BOOK REPORT =====
No overdue books found.

Select an option (0-7): 7

===== RESERVE BOOK =====
Enter Book ID: B102
Enter Member ID: M101

[SUCCESS] Reservation added to waiting list.

Select an option (0-7): 0

Thank you for using ShelfWise!
```

**Note:** The sample run is illustrative. Actual dates and results depend on the system date and the records entered. The program currently uses in-memory Python lists, so records are not permanently saved after exiting.