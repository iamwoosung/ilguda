DROP DATABASE IF EXISTS ILGUDA; 
CREATE DATABASE ILGUDA DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE ILGUDA;

CREATE USER 'user'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON ILGUDA.* TO 'user'@'%';
FLUSH PRIVILEGES;

CREATE TABLE Job (
    job_no INT AUTO_INCREMENT PRIMARY KEY COMMENT '순번 (Primary Key)',
    job_hash VARCHAR(64) NOT NULL UNIQUE COMMENT '공고 고유 해시값 (SHA256)',
    job_recruit_start_date DATETIME COMMENT '모집 시작일 (term_date 분리)',
    job_recruit_end_date DATETIME COMMENT '모집 마감일 (term_date 분리)',
    job_buspla_name VARCHAR(50) COMMENT '사업장명',
    job_cntct_no VARCHAR(50) COMMENT '연락처',
    job_comp_addr VARCHAR(150) COMMENT '사업장 주소',
    job_emp_type VARCHAR(50) COMMENT '고용형태',
    job_enter_type VARCHAR(50) COMMENT '입사형태',
    job_job_nm VARCHAR(50) COMMENT '모집직종',
    job_offer_reg_date DATETIME COMMENT '구인신청일자 (offerreg_dt)',
    job_reg_date DATETIME COMMENT '등록일 (reg_dt)',
    job_regagn_name VARCHAR(50) COMMENT '담당기관 (regagn_name)',
    job_req_career VARCHAR(50) COMMENT '요구경력',
    job_req_educ VARCHAR(50) COMMENT '요구학력',
    job_rno VARCHAR(20) COMMENT '순번 (rno)',
    job_rnum VARCHAR(20) COMMENT '순번 (rnum)',
    job_salary VARCHAR(50) COMMENT '임금',
    job_salary_type VARCHAR(50) COMMENT '임금형태',
    job_env_both_hands VARCHAR(100) COMMENT '작업환경_양손사용',
    job_env_eyesight VARCHAR(100) COMMENT '작업환경_시력',
    job_env_handwork VARCHAR(100) COMMENT '작업환경_손작업',
    job_env_lift_power VARCHAR(100) COMMENT '작업환경_드는힘',
    job_env_lstn_talk VARCHAR(100) COMMENT '작업환경_듣고 말하기',
    job_env_stnd_walk VARCHAR(100) COMMENT '작업환경_서거나 걷기',
    job_is_classified BOOL NOT NULL DEFAULT FALSE COMMENT '분류 여부', 
    job_created_subject INTEGER NOT NULL DEFAULT 1 COMMENT '생성 주체 (1: 배치, 2: APP, 3: 관리자)', 
    job_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 일시',
    job_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 일시' 
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
COMMENT '채용 공고 정보 테이블`';


DELIMITER //

CREATE PROCEDURE BATCH_JOB_SET(
    IN p_job_hash VARCHAR(64), 
    IN p_job_recruit_start_date DATETIME, 
    IN p_job_recruit_end_date DATETIME,   
    IN p_job_buspla_name VARCHAR(50),     
    IN p_job_cntct_no VARCHAR(50),        
    IN p_job_comp_addr VARCHAR(150),      
    IN p_job_emp_type VARCHAR(50),        
    IN p_job_enter_type VARCHAR(50),      
    IN p_job_job_nm VARCHAR(50),          
    IN p_job_offer_reg_date DATETIME,     
    IN p_job_reg_date DATETIME,           
    IN p_job_regagn_name VARCHAR(50),     
    IN p_job_req_career VARCHAR(50),      
    IN p_job_req_educ VARCHAR(50),        
    IN p_job_rno VARCHAR(20),             
    IN p_job_rnum VARCHAR(20),            
    IN p_job_salary VARCHAR(50),          
    IN p_job_salary_type VARCHAR(50),
    IN p_job_env_both_hands VARCHAR(100),
    IN p_job_env_eyesight VARCHAR(100),
    IN p_job_env_handwork VARCHAR(100),
    IN p_job_env_lift_power VARCHAR(100),
    IN p_job_env_lstn_talk VARCHAR(100),
    IN p_job_env_stnd_walk VARCHAR(100), 
    IN p_job_created_subject INTEGER 
)
BEGIN
    DECLARE v_IsValidHash INT;
    SELECT job_no INTO v_IsValidHash FROM Job WHERE job_hash = p_job_hash LIMIT 1;

    IF v_IsValidHash IS NOT NULL THEN
        SELECT v_IsValidHash AS job_no, 'ALREADY_EXISTS' AS status, p_job_hash AS job_hash; 
    ELSE
        INSERT INTO Job (
            job_hash, 
            job_recruit_start_date, job_recruit_end_date, job_buspla_name, job_cntct_no, 
            job_comp_addr, job_emp_type, job_enter_type, job_job_nm, job_offer_reg_date, 
            job_reg_date, job_regagn_name, job_req_career, job_req_educ, job_rno, 
            job_rnum, job_salary, job_salary_type, 
            job_env_both_hands, job_env_eyesight, job_env_handwork, 
            job_env_lift_power, job_env_lstn_talk, job_env_stnd_walk, 
            job_created_subject
        )
        VALUES (
            p_job_hash, 
            p_job_recruit_start_date, p_job_recruit_end_date, p_job_buspla_name, p_job_cntct_no, 
            p_job_comp_addr, p_job_emp_type, p_job_enter_type, p_job_job_nm, p_job_offer_reg_date, 
            p_job_reg_date, p_job_regagn_name, p_job_req_career, p_job_req_educ, p_job_rno, 
            p_job_rnum, p_job_salary, p_job_salary_type, 
            p_job_env_both_hands, p_job_env_eyesight, p_job_env_handwork, 
            p_job_env_lift_power, p_job_env_lstn_talk, p_job_env_stnd_walk, 
            p_job_created_subject
        );
        SELECT LAST_INSERT_ID() AS job_no, 'INSERTED' AS status, p_job_hash AS job_hash; 
    END IF;

END //
DELIMITER ;


DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `AGENT_JOB_CLASSIFIED_GET`(
    
)
BEGIN
    SELECT * FROM JOB WHERE job_is_classified = 0;
    
END //
DELIMITER ;

