-- Add missing indices for better performance
ALTER TABLE users ADD INDEX idx_username (username);
ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE users ADD INDEX idx_user_type (user_type);

ALTER TABLE courses ADD INDEX idx_teacher (teacher_id);
ALTER TABLE courses ADD INDEX idx_language (language);
ALTER TABLE courses ADD INDEX idx_level (level);

ALTER TABLE student_courses ADD INDEX idx_student (student_id);
ALTER TABLE student_courses ADD INDEX idx_course (course_id);

ALTER TABLE lessons ADD INDEX idx_course (course_id);
ALTER TABLE exercises ADD INDEX idx_lesson (lesson_id);

ALTER TABLE student_exercise_submissions ADD INDEX idx_student (student_id);
ALTER TABLE student_exercise_submissions ADD INDEX idx_exercise (exercise_id);

ALTER TABLE attendance ADD INDEX idx_student_course (student_id, course_id);
ALTER TABLE payments ADD INDEX idx_student_course (student_id, course_id);
ALTER TABLE chat_messages ADD INDEX idx_chat (chat_id);
