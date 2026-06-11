<?php
class Database {
    private $host = 'sql309.infinityfree.com';
    private $db_name = 'if0_39253495_musicapp';
    private $username = 'if0_39253495';
    private $password = 'a9C42m6f5taEz';
    private $conn;

    public function connect() {
        $this->conn = null;

        try {
            $this->conn = new PDO(
                "mysql:host={$this->host};dbname={$this->db_name}", 
                $this->username, 
                $this->password
            );
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->conn->exec("SET NAMES utf8mb4");
        } catch(PDOException $e) {
            error_log("Connection error: " . $e->getMessage());
            die("Database connection failed. Please try again later.");
        }

        return $this->conn;
    }
}

// ⚠️ THÊM DÒNG NÀY để khởi tạo và cung cấp kết nối PDO cho $conn
$database = new Database();
$conn = $database->connect();