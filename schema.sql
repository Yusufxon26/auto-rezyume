CREATE DATABASE IF NOT EXISTS auto_rezyume CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE auto_rezyume;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(150),
    profession VARCHAR(150),
    about TEXT,
    education TEXT,
    experience TEXT,
    skills TEXT,
    template_name VARCHAR(50),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
