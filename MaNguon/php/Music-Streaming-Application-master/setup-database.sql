-- MySQL User Configuration for Music Streaming Application
-- Execute these commands in MySQL to set up user access

-- Option 1: Configure root user with password
ALTER USER 'root'@'localhost' IDENTIFIED BY 'mat_khau_cua_an';
FLUSH PRIVILEGES;

-- Option 2: Create a dedicated admin user (Recommended)
CREATE USER 'an_admin'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'an_admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Option 3: Configure d4m_admin (if using this user)
ALTER USER 'd4m_admin'@'localhost' IDENTIFIED BY 'admin';
FLUSH PRIVILEGES;

-- Exit
EXIT;
