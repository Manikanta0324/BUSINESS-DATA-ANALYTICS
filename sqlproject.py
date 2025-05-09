-- Department Table
CREATE TABLE Department (
    department_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Faculty Table
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Project Table
CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2)
);

-- Research Grant Table
CREATE TABLE Research_Grant (
    grant_id INT PRIMARY KEY,
    source_name VARCHAR(150),
    total_amount DECIMAL(12, 2),
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES Project(project_id)
);

-- Project-Faculty Mapping Table
CREATE TABLE Project_Faculty (
    project_id INT,
    faculty_id INT,
    role VARCHAR(100),
    PRIMARY KEY (project_id, faculty_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

-- Grant Utilization Table
CREATE TABLE Grant_Utilization (
    utilization_id INT PRIMARY KEY,
    grant_id INT,
    amount_used DECIMAL(12,2),
    usage_date DATE,
    description VARCHAR(255),
    FOREIGN KEY (grant_id) REFERENCES Research_Grant(grant_id)
);
-- Insert Departments
INSERT INTO Department VALUES
(1, 'Computer Science'),
(2, 'Physics'),
(3, 'Biotechnology'),
(4, 'Mathematics');

-- Insert Faculty Members
INSERT INTO Faculty VALUES
(101, 'Dr. Alice', 1),
(102, 'Dr. Bob', 2),
(103, 'Dr. Clara', 1),
(104, 'Dr. David', 3),
(105, 'Dr. Eva', 4);

-- Insert Projects
INSERT INTO Project VALUES
(201, 'AI for Healthcare', '2024-01-01', '2025-01-01', 500000.00),
(202, 'Quantum Computing', '2023-06-01', '2025-06-01', 300000.00),
(203, 'Gene Editing Research', '2024-03-01', '2026-03-01', 450000.00);

-- Insert Research Grants
INSERT INTO Research_Grant VALUES
(301, 'National Science Foundation', 400000.00, 201),
(302, 'Tech Innovation Fund', 300000.00, 202),
(303, 'BioFuture Trust', 350000.00, 203);

-- Insert Project-Faculty Mappings
INSERT INTO Project_Faculty VALUES
(201, 101, 'Principal Investigator'),
(201, 104, 'Co-Investigator'),
(202, 102, 'Principal Investigator'),
(202, 105, 'Collaborator'),
(203, 103, 'Principal Investigator'),
(203, 104, 'Research Lead');

-- Insert Grant Utilizations
INSERT INTO Grant_Utilization VALUES
(401, 301, 150000.00, '2024-05-01', 'Initial AI research infrastructure'),
(402, 302, 50000.00, '2024-02-15', 'Quantum simulator setup'),
(403, 303, 100000.00, '2024-04-10', 'Lab equipment for gene editing');


SELECT p.title AS Project, f.name AS Faculty, pf.role AS Role
FROM Project p
JOIN Project_Faculty pf ON p.project_id = pf.project_id
JOIN Faculty f ON pf.faculty_id = f.faculty_id;


SELECT p.title AS Project, rg.source_name AS Grant_Source, rg.total_amount AS Grant_Amount
FROM Research_Grant rg
JOIN Project p ON rg.project_id = p.project_id;



SELECT p.title AS Project, p.budget AS Budget, 
       COALESCE(SUM(gu.amount_used), 0) AS Total_Utilized
FROM Project p
LEFT JOIN Research_Grant rg ON p.project_id = rg.project_id
LEFT JOIN Grant_Utilization gu ON rg.grant_id = gu.grant_id
GROUP BY p.title, p.budget;


SELECT f.name AS Faculty, d.name AS Department, p.title AS Project, pf.role AS Role
FROM Faculty f
JOIN Department d ON f.department_id = d.department_id
JOIN Project_Faculty pf ON f.faculty_id = pf.faculty_id
JOIN Project p ON pf.project_id = p.project_id;







SELECT pf1.project_id, p.title AS Project,
       f1.name AS Faculty1, d1.name AS Dept1,
       f2.name AS Faculty2, d2.name AS Dept2
FROM Project_Faculty pf1
JOIN Faculty f1 ON pf1.faculty_id = f1.faculty_id
JOIN Department d1 ON f1.department_id = d1.department_id
JOIN Project_Faculty pf2 ON pf1.project_id = pf2.project_id AND pf1.faculty_id < pf2.faculty_id
JOIN Faculty f2 ON pf2.faculty_id = f2.faculty_id
JOIN Department d2 ON f2.department_id = d2.department_id
JOIN Project p ON pf1.project_id = p.project_id
WHERE d1.department_id <> d2.department_id;



