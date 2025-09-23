-- Language School Management System Database Schema

-- Drop tables if they exist (for clean initialization)
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS test_results;
DROP TABLE IF EXISTS tests;
DROP TABLE IF EXISTS chat_messages;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS student_exercise_submissions;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS student_lesson_progress;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS student_courses;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_type ENUM('admin', 'teacher', 'student') NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create rooms table and populate ranges 101-150 and 201-250
CREATE TABLE IF NOT EXISTS rooms (
  room_number INT PRIMARY KEY
);

-- Populate 101..150
INSERT IGNORE INTO rooms (room_number)
VALUES
-- 101..150
(101),(102),(103),(104),(105),(106),(107),(108),(109),(110),
(111),(112),(113),(114),(115),(116),(117),(118),(119),(120),
(121),(122),(123),(124),(125),(126),(127),(128),(129),(130),
(131),(132),(133),(134),(135),(136),(137),(138),(139),(140),
(141),(142),(143),(144),(145),(146),(147),(148),(149),(150);

-- Populate 201..250
INSERT IGNORE INTO rooms (room_number)
VALUES
(201),(202),(203),(204),(205),(206),(207),(208),(209),(210),
(211),(212),(213),(214),(215),(216),(217),(218),(219),(220),
(221),(222),(223),(224),(225),(226),(227),(228),(229),(230),
(231),(232),(233),(234),(235),(236),(237),(238),(239),(240),
(241),(242),(243),(244),(245),(246),(247),(248),(249),(250);

-- Create courses table
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    language VARCHAR(50) NOT NULL,
    level VARCHAR(10) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    teacher_id INT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create schedules table (room now INT referencing rooms.room_number)
DROP TABLE IF EXISTS schedules;
CREATE TABLE schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room INT, -- changed to INT to reference rooms.room_number
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (room) REFERENCES rooms(room_number) ON DELETE SET NULL
);

-- Create student-course relationship table
CREATE TABLE student_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, course_id)
);

-- Create lessons table
CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    content TEXT,
    lesson_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Create student-lesson progress table
CREATE TABLE student_lesson_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    lesson_id INT NOT NULL,
    status ENUM('not_started', 'in_progress', 'completed') NOT NULL DEFAULT 'not_started',
    completion_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, lesson_id)
);

-- Create exercises table
CREATE TABLE exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lesson_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    content TEXT,
    due_date DATE,
    max_score INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
);

-- Create student-exercise submissions table
CREATE TABLE student_exercise_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    exercise_id INT NOT NULL,
    submission_text TEXT,
    submission_date DATETIME,
    score INT,
    feedback TEXT,
    status ENUM('not_submitted', 'submitted', 'graded') NOT NULL DEFAULT 'not_submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, exercise_id)
);

-- Create attendance table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('present', 'absent', 'late') NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, course_id, attendance_date)
);

-- Create payments table
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE,
    due_date DATE NOT NULL,
    status ENUM('pending', 'paid', 'overdue') NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Create chats table
CREATE TABLE chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY (user1_id, user2_id)
);

-- Create chat messages table (updated: support edit/delete metadata)
DROP TABLE IF EXISTS chat_messages;
CREATE TABLE chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    message TEXT,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    edited BOOLEAN NOT NULL DEFAULT FALSE,
    edited_at TIMESTAMP NULL DEFAULT NULL,
    read_status BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sender_id (sender_id),
    INDEX idx_chat_id (chat_id)
);

-- Create tests table
CREATE TABLE tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    content TEXT,
    test_date DATE,
    max_score INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Create test results table
CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    test_id INT NOT NULL,
    score INT,
    feedback TEXT,
    completion_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    UNIQUE KEY (student_id, test_id)
);

-- Create notifications table
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    read_status BOOLEAN NOT NULL DEFAULT FALSE,
    notification_type ENUM('info', 'warning', 'error', 'success') NOT NULL DEFAULT 'info',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create student dashboard stats table
CREATE TABLE student_dashboard_stats (
    student_id INT PRIMARY KEY,
    enrolled_courses_count INT DEFAULT 0,
    upcoming_lessons_count INT DEFAULT 0,
    pending_exercises_count INT DEFAULT 0,
    unread_messages_count INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create triggers to prevent overlapping schedules for the same room or same teacher
DELIMITER $$
CREATE TRIGGER trg_prevent_room_overlap
BEFORE INSERT ON schedules
FOR EACH ROW
BEGIN
  DECLARE cnt INT DEFAULT 0;
  IF NEW.room IS NOT NULL THEN
    SELECT COUNT(*) INTO cnt
    FROM schedules
    WHERE LOWER(TRIM(day_of_week)) = LOWER(TRIM(NEW.day_of_week))
      AND room = NEW.room
      AND NOT (end_time <= NEW.start_time OR start_time >= NEW.end_time);
    IF cnt > 0 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Room conflict: another schedule uses this room at the same time.';
    END IF;
  END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_prevent_teacher_overlap
BEFORE INSERT ON schedules
FOR EACH ROW
BEGIN
  DECLARE cnt INT DEFAULT 0;
  SELECT COUNT(*) INTO cnt
  FROM schedules s
  JOIN courses c ON s.course_id = c.course_id
  WHERE LOWER(TRIM(s.day_of_week)) = LOWER(TRIM(NEW.day_of_week))
    AND c.teacher_id IS NOT NULL AND c.teacher_id = (
        SELECT teacher_id FROM courses WHERE course_id = NEW.course_id
    )
    AND NOT (s.end_time <= NEW.start_time OR s.start_time >= NEW.end_time);
  IF cnt > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Teacher conflict: teacher has another class at the same time.';
  END IF;
END$$
DELIMITER ;

-- Create triggers for dashboard stats
DELIMITER //

-- Update enrolled courses count
CREATE TRIGGER after_student_course_insert
AFTER INSERT ON student_courses
FOR EACH ROW
BEGIN
    INSERT INTO student_dashboard_stats (student_id, enrolled_courses_count)
    VALUES (NEW.student_id, 1)
    ON DUPLICATE KEY UPDATE
    enrolled_courses_count = enrolled_courses_count + 1;
END//

CREATE TRIGGER after_student_course_delete 
AFTER DELETE ON student_courses
FOR EACH ROW 
BEGIN
    UPDATE student_dashboard_stats
    SET enrolled_courses_count = enrolled_courses_count - 1
    WHERE student_id = OLD.student_id;
END//

-- Update unread messages count
CREATE TRIGGER after_message_insert
AFTER INSERT ON chat_messages
FOR EACH ROW
BEGIN
    UPDATE student_dashboard_stats s
    JOIN chats c ON (NEW.chat_id = c.id)
    SET s.unread_messages_count = s.unread_messages_count + 1
    WHERE s.student_id IN (c.user1_id, c.user2_id)
    AND s.student_id != NEW.sender_id;
END//

-- Update exercises count
CREATE TRIGGER after_exercise_submit
AFTER UPDATE ON student_exercise_submissions
FOR EACH ROW
BEGIN
    IF NEW.status = 'submitted' AND OLD.status = 'not_submitted' THEN
        UPDATE student_dashboard_stats
        SET pending_exercises_count = pending_exercises_count - 1
        WHERE student_id = NEW.student_id;
    END IF;
END//

DELIMITER //

-- Insert test data

-- Insert admin user
INSERT INTO users (username, password, first_name, last_name, email, user_type, active)
VALUES ('admin', '1', 'Admin', 'User', 'admin@example.com', 'admin', 1);

-- Insert teacher users
INSERT INTO users (username, password, first_name, last_name, email, user_type, active)
VALUES 
('teacher1', '1', 'John', 'Smith', 'john.smith@example.com', 'teacher', 1),
('teacher2', 'password123', 'Maria', 'Garcia', 'maria.garcia@example.com', 'teacher', 1),
('teacher3', 'password123', 'David', 'Johnson', 'david.johnson@example.com', 'teacher', 1);

-- Insert student users
INSERT INTO users (username, password, first_name, last_name, email, user_type, active)
VALUES 
('student1', '1', 'Alice', 'Johnson', 'alice.johnson@example.com', 'student', 1),
('student2', 'password123', 'Bob', 'Smith', 'bob.smith@example.com', 'student', 1),
('student3', 'password123', 'Charlie', 'Brown', 'charlie.brown@example.com', 'student', 1),
('student4', 'password123', 'Diana', 'Wilson', 'diana.wilson@example.com', 'student', 1),
('student5', 'password123', 'Edward', 'Davis', 'edward.davis@example.com', 'student', 1);

-- Insert courses
INSERT INTO courses (name, language, level, description, price, teacher_id, active)
VALUES 
('English for Beginners', 'English', 'A1', 'A comprehensive course for beginners to learn English.', 500.00, 2, 1),
('Intermediate Spanish', 'Spanish', 'B1', 'Take your Spanish to the next level with this intermediate course.', 550.00, 3, 1),
('Advanced French', 'French', 'C1', 'Perfect your French with this advanced course.', 600.00, 4, 1),
('German for Travelers', 'German', 'A2', 'Learn practical German for your travels.', 450.00, 2, 1),
('Business English', 'English', 'B2', 'English for professional settings and business communication.', 700.00, 3, 1);

-- Insert schedules (use numeric room values; ensure rooms are valid)
INSERT INTO schedules (course_id, day_of_week, start_time, end_time, room)
VALUES 
(1, 'Monday', '10:00:00', '11:30:00', 101),
(1, 'Wednesday', '10:00:00', '11:30:00', 101),
(1, 'Friday', '10:00:00', '11:30:00', 101),
(2, 'Tuesday', '14:00:00', '15:30:00', 203),
(2, 'Thursday', '14:00:00', '15:30:00', 203),
-- changed 305 -> 205 (305 was outside defined rooms)
(3, 'Monday', '16:00:00', '17:30:00', 205),
(3, 'Wednesday', '16:00:00', '17:30:00', 205),
(4, 'Tuesday', '10:00:00', '11:30:00', 102),
(4, 'Thursday', '10:00:00', '11:30:00', 102),
(5, 'Monday', '18:00:00', '19:30:00', 204),
(5, 'Wednesday', '18:00:00', '19:30:00', 204);

-- Insert student enrollments
INSERT INTO student_courses (student_id, course_id, enrollment_date, active)
VALUES 
(5, 1, '2023-01-15', 1),
(6, 1, '2023-01-20', 1),
(7, 2, '2023-02-01', 1),
(8, 2, '2023-02-05', 1),
(9, 3, '2023-01-10', 1),
(5, 4, '2023-03-01', 1),
(6, 5, '2023-02-15', 1),
(7, 3, '2023-01-25', 1),
(8, 4, '2023-03-10', 1),
(9, 5, '2023-02-20', 1);

-- Insert lessons
INSERT INTO lessons (course_id, title, description, content, lesson_date)
VALUES 
(1, 'Introduction to English', 'Basic introduction to English language.', 'Content for Lesson 1', '2023-01-16'),
(1, 'Basic Grammar', 'Introduction to basic English grammar.', 'Content for Lesson 2', '2023-01-18'),
(1, 'Simple Conversations', 'Practice simple conversations in English.', 'Content for Lesson 3', '2023-01-20'),
(2, 'Spanish Vocabulary', 'Expanding your Spanish vocabulary.', 'Content for Lesson 1', '2023-02-02'),
(2, 'Spanish Grammar', 'Intermediate Spanish grammar concepts.', 'Content for Lesson 2', '2023-02-04'),
(3, 'Advanced French Grammar', 'Complex grammar structures in French.', 'Content for Lesson 1', '2023-01-11'),
(3, 'French Literature', 'Introduction to French literature.', 'Content for Lesson 2', '2023-01-13'),
(4, 'German Basics', 'Basic German phrases for travelers.', 'Content for Lesson 1', '2023-03-02'),
(5, 'Business Communication', 'Effective communication in business settings.', 'Content for Lesson 1', '2023-02-16');

-- Insert exercises
INSERT INTO exercises (lesson_id, title, description, content, due_date, max_score)
VALUES 
(1, 'Basic Vocabulary Exercise', 'Practice basic English vocabulary.', 'Exercise content here', '2023-01-23', 100),
(1, 'Pronunciation Exercise', 'Practice English pronunciation.', 'Exercise content here', '2023-01-25', 100),
(2, 'Grammar Exercise 1', 'Practice basic English grammar.', 'Exercise content here', '2023-01-27', 100),
(3, 'Conversation Practice', 'Practice conversations with a partner.', 'Exercise content here', '2023-01-30', 100),
(4, 'Spanish Vocabulary Quiz', 'Test your Spanish vocabulary.', 'Exercise content here', '2023-02-09', 100),
(5, 'Spanish Grammar Exercise', 'Practice intermediate Spanish grammar.', 'Exercise content here', '2023-02-11', 100),
(6, 'French Grammar Exercise', 'Practice advanced French grammar.', 'Exercise content here', '2023-01-18', 100),
(7, 'French Literature Analysis', 'Analyze a French literary text.', 'Exercise content here', '2023-01-20', 100),
(8, 'German Phrases Exercise', 'Practice common German phrases.', 'Exercise content here', '2023-03-09', 100),
(9, 'Business Email Writing', 'Practice writing professional emails.', 'Exercise content here', '2023-02-23', 100);

-- Insert student exercise submissions
INSERT INTO student_exercise_submissions (student_id, exercise_id, submission_text, submission_date, score, feedback, status)
VALUES 
(5, 1, 'Submission content here', '2023-01-22 14:30:00', 85, 'Good work, but some vocabulary errors.', 'graded'),
(5, 2, 'Submission content here', '2023-01-24 15:45:00', 90, 'Excellent pronunciation!', 'graded'),
(6, 1, 'Submission content here', '2023-01-23 10:15:00', 78, 'Need to work on vocabulary.', 'graded'),
(6, 2, 'Submission content here', '2023-01-25 11:30:00', 82, 'Good effort, keep practicing.', 'graded'),
(7, 5, 'Submission content here', '2023-02-08 16:20:00', 92, 'Excellent vocabulary knowledge!', 'graded'),
(8, 5, 'Submission content here', '2023-02-09 09:45:00', 88, 'Very good work.', 'graded'),
(9, 7, 'Submission content here', '2023-01-17 14:00:00', 95, 'Outstanding grammar understanding!', 'graded');

-- Insert attendance records
INSERT INTO attendance (student_id, course_id, attendance_date, status, notes)
VALUES 
(5, 1, '2023-01-16', 'present', NULL),
(5, 1, '2023-01-18', 'present', NULL),
(5, 1, '2023-01-20', 'absent', 'Sick'),
(6, 1, '2023-01-16', 'present', NULL),
(6, 1, '2023-01-18', 'late', 'Arrived 15 minutes late'),
(6, 1, '2023-01-20', 'present', NULL),
(7, 2, '2023-02-02', 'present', NULL),
(7, 2, '2023-02-04', 'present', NULL),
(8, 2, '2023-02-02', 'absent', 'Family emergency'),
(8, 2, '2023-02-04', 'present', NULL),
(9, 3, '2023-01-11', 'present', NULL),
(9, 3, '2023-01-13', 'present', NULL);

-- Insert payments
INSERT INTO payments (student_id, course_id, amount, payment_date, due_date, status, payment_method, notes)
VALUES 
(5, 1, 500.00, '2023-01-15', '2023-01-15', 'paid', 'Credit Card', NULL),
(6, 1, 500.00, '2023-01-20', '2023-01-20', 'paid', 'Bank Transfer', NULL),
(7, 2, 550.00, '2023-02-01', '2023-02-01', 'paid', 'Credit Card', NULL),
(8, 2, 550.00, NULL, '2023-02-05', 'overdue', NULL, 'Payment reminder sent'),
(9, 3, 600.00, '2023-01-10', '2023-01-10', 'paid', 'PayPal', NULL),
(5, 4, 450.00, NULL, '2023-03-01', 'pending', NULL, NULL),
(6, 5, 700.00, '2023-02-15', '2023-02-15', 'paid', 'Credit Card', NULL),
(7, 3, 600.00, '2023-01-25', '2023-01-25', 'paid', 'Bank Transfer', NULL),
(8, 4, 450.00, NULL, '2023-03-10', 'pending', NULL, NULL),
(9, 5, 700.00, '2023-02-20', '2023-02-20', 'paid', 'Credit Card', NULL);

-- Insert chats
INSERT INTO chats (user1_id, user2_id)
VALUES 
(2, 5),  -- Teacher 1 and Student 1
(2, 6),  -- Teacher 1 and Student 2
(3, 7),  -- Teacher 2 and Student 3
(3, 8),  -- Teacher 2 and Student 4
(4, 9),  -- Teacher 3 and Student 5
(2, 3),  -- Teacher 1 and Teacher 2
(1, 2),  -- Admin and Teacher 1
(1, 5);  -- Admin and Student 1

-- Insert chat messages
INSERT INTO chat_messages (chat_id, sender_id, message, read_status, sent_at)
VALUES 
(1, 2, 'Hello Alice, how are you doing with the homework?', 1, '2023-01-17 10:00:00'),
(1, 5, 'Hi Mr. Smith, I\'m working on it. I have a question about exercise 2.', 1, '2023-01-17 10:05:00'),
(1, 2, 'Sure, what\'s your question?', 1, '2023-01-17 10:07:00'),
(1, 5, 'I\'m not sure how to approach the pronunciation part.', 1, '2023-01-17 10:10:00'),
(1, 2, 'Let me explain it in our next class. In the meantime, try watching the video I shared.', 1, '2023-01-17 10:15:00'),
(1, 5, 'Thank you, I\'ll do that!', 1, '2023-01-17 10:20:00'),
(2, 2, 'Bob, I noticed you were late to class today. Is everything okay?', 1, '2023-01-18 14:00:00'),
(2, 6, 'Sorry Mr. Smith, I had a transportation issue. It won\'t happen again.', 1, '2023-01-18 14:30:00'),
(2, 2, 'I understand. Please try to be on time for our next class.', 1, '2023-01-18 14:35:00'),
(2, 6, 'I will, thank you for understanding.', 1, '2023-01-18 14:40:00');

-- Insert tests
INSERT INTO tests (course_id, title, description, content, test_date, max_score)
VALUES 
(1, 'English Midterm Exam', 'Midterm examination for English course.', 'Test content here', '2023-02-15', 100),
(1, 'English Final Exam', 'Final examination for English course.', 'Test content here', '2023-03-15', 100),
(2, 'Spanish Midterm Exam', 'Midterm examination for Spanish course.', 'Test content here', '2023-03-01', 100),
(2, 'Spanish Final Exam', 'Final examination for Spanish course.', 'Test content here', '2023-04-01', 100),
(3, 'French Midterm Exam', 'Midterm examination for French course.', 'Test content here', '2023-02-10', 100),
(3, 'French Final Exam', 'Final examination for French course.', 'Test content here', '2023-03-10', 100);

-- Insert test results
INSERT INTO test_results (student_id, test_id, score, feedback, completion_date)
VALUES 
(5, 1, 88, 'Good understanding of basic concepts. Work on grammar.', '2023-02-15'),
(6, 1, 75, 'Need to improve vocabulary and grammar.', '2023-02-15'),
(7, 3, 92, 'Excellent work! Very good command of Spanish vocabulary.', '2023-03-01'),
(8, 3, 85, 'Good effort. Work on verb conjugations.', '2023-03-01'),
(9, 5, 95, 'Outstanding performance! Excellent command of French grammar.', '2023-02-10');

-- Insert notifications
INSERT INTO notifications (user_id, title, message, read_status, notification_type)
VALUES 
(5, 'New Lesson Available', 'A new lesson has been added to your English course.', 0, 'info'),
(5, 'Homework Due Soon', 'Your English homework is due in 2 days.', 0, 'warning'),
(6, 'Grade Posted', 'Your grade for the English midterm exam has been posted.', 1, 'success'),
(7, 'New Message', 'You have a new message from your Spanish teacher.', 0, 'info'),
(8, 'Payment Overdue', 'Your payment for the Spanish course is overdue.', 0, 'error'),
(9, 'Class Canceled', 'Your French class on Friday has been canceled.', 1, 'warning'),
(2, 'New Student Enrolled', 'A new student has enrolled in your English course.', 0, 'info'),
(3, 'Schedule Change', 'Your Spanish class schedule has been updated.', 1, 'info'),
(4, 'Admin Message', 'Please submit your course materials by Friday.', 0, 'info'),
(1, 'System Update', 'The system will be updated tonight at 10 PM.', 0, 'warning');

-- =========================
-- Migration / Cleanup Steps
-- (Run these on an existing database to enforce rooms & prevent invalid inserts)
-- =========================

-- 1) Set non-matching room values to NULL (handles varchar/old values)
UPDATE schedules s
LEFT JOIN rooms r ON CAST(s.room AS UNSIGNED) = r.room_number
SET s.room = NULL
WHERE r.room_number IS NULL;

-- 2) Convert schedules.room to INT (safe if values now numeric or NULL)
ALTER TABLE schedules
  MODIFY COLUMN room INT NULL;

-- 3) Add foreign key constraint to enforce valid rooms (will fail if already exists)
-- If running on an existing DB and a FK already exists, drop it first or run this only once.
ALTER TABLE schedules
  ADD CONSTRAINT fk_schedules_room
  FOREIGN KEY (room) REFERENCES rooms(room_number)
  ON DELETE SET NULL;

-- 4) (Optional) As an extra safeguard, add triggers to block room/time overlaps in DB
DELIMITER $$
CREATE TRIGGER IF NOT EXISTS trg_prevent_room_overlap
BEFORE INSERT ON schedules
FOR EACH ROW
BEGIN
  DECLARE cnt INT DEFAULT 0;
  IF NEW.room IS NOT NULL THEN
    SELECT COUNT(*) INTO cnt
    FROM schedules
    WHERE LOWER(TRIM(day_of_week)) = LOWER(TRIM(NEW.day_of_week))
      AND room = NEW.room
      AND NOT (end_time <= NEW.start_time OR start_time >= NEW.end_time);
    IF cnt > 0 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Room conflict: another schedule uses this room at the same time.';
    END IF;
  END IF;
END$$
DELIMITER ;

-- Note: MySQL 8.0 does not support CREATE TRIGGER IF NOT EXISTS; if your server errors,
-- create the trigger only once (or check information_schema.TRIGGERS before creating).

-- End of migration block