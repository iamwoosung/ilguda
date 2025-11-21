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


CREATE TABLE job_classify (
    jpc_no INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '직무별 장애 조건 분류 고유번호',
    jpc_physical_disability BOOL NOT NULL COMMENT '지체장애 수행 가능 여부',
    jpc_brain_lesion BOOL NOT NULL COMMENT '뇌병변장애 수행 가능 여부',
    jpc_visual_impairment BOOL NOT NULL COMMENT '시각장애 수행 가능 여부',
    jpc_hearing_impairment BOOL NOT NULL COMMENT '청각장애 수행 가능 여부',
    jpc_speech_disorder BOOL NOT NULL COMMENT '언어장애 수행 가능 여부',
    jpc_facial_deformity BOOL NOT NULL COMMENT '안면장애 수행 가능 여부',
    jpc_kidney_disorder BOOL NOT NULL COMMENT '신장장애 수행 가능 여부',
    jpc_cardiac_disorder BOOL NOT NULL COMMENT '심장장애 수행 가능 여부',
    jpc_liver_disorder BOOL NOT NULL COMMENT '간장애 수행 가능 여부',
    jpc_respiratory_disorder BOOL NOT NULL COMMENT '호흡기장애 수행 가능 여부',
    jpc_urinary_diversion BOOL NOT NULL COMMENT '장루, 요루 장애 수행 가능 여부',
    jpc_epilepsy BOOL NOT NULL COMMENT '간질장애 수행 가능 여부',
    jpc_intellectual_disability BOOL NOT NULL COMMENT '지적장애 수행 가능 여부',
    jpc_autism BOOL NOT NULL COMMENT '자폐성장애 수행 가능 여부',
    jpc_mental_illness BOOL NOT NULL COMMENT '정신장애 수행 가능 여부',
    jpc_job_no INT NOT NULL COMMENT '채용 공고 고유번호 (FK)',
    
    FOREIGN KEY (jpc_job_no) REFERENCES job (job_no)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
COMMENT '채용 공고의 장애 유형별 업무 가능 여부 분류 테이블`';


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

CREATE DEFINER=`root`@`localhost` PROCEDURE `AGENT_JOB_CLASSIFIED_SET`(
    IN p_jpc_job_no INT,
    IN p_jpc_physical_disability BOOL,
    IN p_jpc_brain_lesion BOOL,
    IN p_jpc_visual_impairment BOOL,
    IN p_jpc_hearing_impairment BOOL,
    IN p_jpc_speech_disorder BOOL,
    IN p_jpc_facial_deformity BOOL,
    IN p_jpc_kidney_disorder BOOL,
    IN p_jpc_cardiac_disorder BOOL,
    IN p_jpc_liver_disorder BOOL,
    IN p_jpc_respiratory_disorder BOOL,
    IN p_jpc_urinary_diversion BOOL,
    IN p_jpc_epilepsy BOOL,
    IN p_jpc_intellectual_disability BOOL,
    IN p_jpc_autism BOOL,
    IN p_jpc_mental_illness BOOL
)
BEGIN

	IF (SELECT job_is_classified FROM JOB WHERE job_no = p_jpc_job_no) = 1 THEN
		SELECT p_jpc_job_no AS job_no, 'ALREADY_EXISTS' AS status; 
	ELSE 
		INSERT INTO job_physical_condition (
			jpc_job_no,
			jpc_physical_disability,
			jpc_brain_lesion,
			jpc_visual_impairment,
			jpc_hearing_impairment,
			jpc_speech_disorder,
			jpc_facial_deformity,
			jpc_kidney_disorder,
			jpc_cardiac_disorder,
			jpc_liver_disorder,
			jpc_respiratory_disorder,
			jpc_urinary_diversion,
			jpc_epilepsy,
			jpc_intellectual_disability,
			jpc_autism,
			jpc_mental_illness
		)
		VALUES (
			p_jpc_job_no,
			p_jpc_physical_disability,
			p_jpc_brain_lesion,
			p_jpc_visual_impairment,
			p_jpc_hearing_impairment,
			p_jpc_speech_disorder,
			p_jpc_facial_deformity,
			p_jpc_kidney_disorder,
			p_jpc_cardiac_disorder,
			p_jpc_liver_disorder,
			p_jpc_respiratory_disorder,
			p_jpc_urinary_diversion,
			p_jpc_epilepsy,
			p_jpc_intellectual_disability,
			p_jpc_autism,
			p_jpc_mental_illness
		);
        UPDATE job SET job_is_classified = 1 WHERE job_no = p_jpc_job_no;
		SELECT p_jpc_job_no AS job_no, 'INSERTED' AS status; 
    END IF;

END //

DELIMITER ;

DELIMITER //

CREATE DEFINER=`root`@`localhost` PROCEDURE `SERVER_JOB_LIST_GET`(
    IN p_jobBusplaName VARCHAR(50),
    IN p_jobCompAddr VARCHAR(150),
    IN p_jobRecruitStartDate DATETIME,
    IN p_jobRecruitEndDate DATETIME,
    IN p_jobEmpType VARCHAR(50),
    IN p_jobEnterType VARCHAR(50),
    IN p_jobReqCareer VARCHAR(50),
    IN p_jobReqEduc VARCHAR(50),
    IN p_jobSalaryType VARCHAR(50)
)
BEGIN
    -- 결과를 저장할 변수
    SET @sql = '
        SELECT
			job_no,
			job_hash,
			job_recruit_start_date,
			job_recruit_end_date,
			job_buspla_name,
			job_cntct_no,
			job_comp_addr,
			job_emp_type,
			job_enter_type,
			job_job_nm,
			job_offer_reg_date,
			job_reg_date,
			job_regagn_name,
			job_req_career,
			job_req_educ,
			job_rno,
			job_rnum,
			job_salary,
			job_salary_type,
			job_env_both_hands,
			job_env_eyesight,
			job_env_handwork,
			job_env_lift_power,
			job_env_lstn_talk,
			job_env_stnd_walk
		FROM Job
		WHERE 1=1';

    -- 1. LIKE 검색 조건 추가 (사업장명)
    IF p_jobBusplaName IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_buspla_name LIKE ''%', p_jobBusplaName, '%''');
    END IF;

    -- 2. LIKE 검색 조건 추가 (사업장 주소)
    IF p_jobCompAddr IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_comp_addr LIKE ''%', p_jobCompAddr, '%''');
    END IF;
    
    -- 3. 날짜 범위 검색 조건 추가 (시작일)
    -- job_recruit_start_date가 파라미터보다 크거나 같아야 함
    IF p_jobRecruitStartDate IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_recruit_start_date >= ''', DATE_FORMAT(p_jobRecruitStartDate, '%Y-%m-%d %H:%i:%s'), '''');
    END IF;

    -- 4. 날짜 범위 검색 조건 추가 (종료일)
    -- job_recruit_end_date가 파라미터보다 작거나 같아야 함
    IF p_jobRecruitEndDate IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_recruit_end_date <= ''', DATE_FORMAT(p_jobRecruitEndDate, '%Y-%m-%d %H:%i:%s'), '''');
    END IF;

    -- 5. Equals 검색 조건 추가 (고용 형태)
    IF p_jobEmpType IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_emp_type = ''', p_jobEmpType, '''');
    END IF;
    
    -- 6. Equals 검색 조건 추가 (입사 형태)
    IF p_jobEnterType IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_enter_type = ''', p_jobEnterType, '''');
    END IF;
    
    -- 7. Equals 검색 조건 추가 (요구 경력)
    IF p_jobReqCareer IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_req_career = ''', p_jobReqCareer, '''');
    END IF;
    
    -- 8. Equals 검색 조건 추가 (요구 학력)
    IF p_jobReqEduc IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_req_educ = ''', p_jobReqEduc, '''');
    END IF;
    
    -- 9. Equals 검색 조건 추가 (임금 형태)
    IF p_jobSalaryType IS NOT NULL THEN
        SET @sql = CONCAT(@sql, ' AND job_salary_type = ''', p_jobSalaryType, '''');
    END IF;

    -- 최종 SQL 쿼리 실행
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

END //

DELIMITER ;