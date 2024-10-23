INSERT INTO students (student_name, image_path) VALUES ('Vedesh', 'B:/STUDY_VEDESH_laptop/coding_new/college/mpi_mini_project/known_face1.jpg');
INSERT INTO students (student_name, image_path) VALUES ('Tom', 'B:/STUDY_VEDESH_laptop/coding_new/college/mpi_mini_project/tom.jpeg');
INSERT INTO students (student_name, image_path) VALUES ('Jackie', 'B:/STUDY_VEDESH_laptop/coding_new/college/mpi_mini_project/jackie.jpeg');



-- Insert 5 sample classes
INSERT INTO classes (class_name) VALUES ('MPI');
INSERT INTO classes (class_name) VALUES ('Data Structures');
INSERT INTO classes (class_name) VALUES ('Java');
INSERT INTO classes (class_name) VALUES ('DMS');
INSERT INTO classes (class_name) VALUES ('DECO');

-- Register students for classes
-- Student 1 is registered for Mathematics and Physics
INSERT INTO registrations (student_id, class_id) VALUES (1, 1);
INSERT INTO registrations (student_id, class_id) VALUES (1, 2);

-- Student 2 is registered for Mathematics, Chemistry, and Computer Science
INSERT INTO registrations (student_id, class_id) VALUES (2, 1);
INSERT INTO registrations (student_id, class_id) VALUES (2, 3);
INSERT INTO registrations (student_id, class_id) VALUES (2, 5);

-- Student 3 is registered for Biology and Physics
INSERT INTO registrations (student_id, class_id) VALUES (3, 2);
INSERT INTO registrations (student_id, class_id) VALUES (3, 4);



-- Insert some sample attendance records
-- Student 1 is present in Mathematics on 2024-10-23
INSERT INTO attendance (student_id, class_id, attendance_date, is_present) VALUES (1, 1, '2024-10-23', 1);

-- Student 2 is present in Computer Science on 2024-10-23
INSERT INTO attendance (student_id, class_id, attendance_date, is_present) VALUES (2, 5, '2024-10-23', 1);

-- Student 3 is present in Physics on 2024-10-23
INSERT INTO attendance (student_id, class_id, attendance_date, is_present) VALUES (3, 2, '2024-10-23', 1);