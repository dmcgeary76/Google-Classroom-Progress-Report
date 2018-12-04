# Google-Classroom-Progress-Report
Python script to pull a user's name, assignment grades, and course progress status.  Eventually automated to send via email to each student enrolled in the course.

# What you will need
python 3+
Google API Account with credentials
MySQL database with the following tables created

+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int(20)     | NO   | PRI | NULL    | auto_increment |
| assignid | varchar(50) | YES  |     | NULL    |                |
| name     | varchar(50) | YES  |     | NULL    |                |
| courseid | varchar(50) | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+

