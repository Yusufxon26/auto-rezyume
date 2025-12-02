-- Database optimization for large text fields
-- Hajm muammosini hal qilish uchun TEXT ustunlarni MEDIUMTEXT ga oshirish

USE auto_rezyume;

ALTER TABLE resumes 
    MODIFY COLUMN career_objective MEDIUMTEXT,
    MODIFY COLUMN education_details MEDIUMTEXT,
    MODIFY COLUMN work_duties MEDIUMTEXT,
    MODIFY COLUMN technical_skills MEDIUMTEXT,
    MODIFY COLUMN soft_skills MEDIUMTEXT,
    MODIFY COLUMN languages MEDIUMTEXT,
    MODIFY COLUMN certificates MEDIUMTEXT,
    MODIFY COLUMN projects MEDIUMTEXT,
    MODIFY COLUMN achievements MEDIUMTEXT,
    MODIFY COLUMN interests MEDIUMTEXT;
