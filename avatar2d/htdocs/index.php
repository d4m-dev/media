<?php
require_once 'inc/db.php';

// Khởi tạo mảng kết quả
$check_result = [];
$success = 0;
$fail = 0;

// Truy vấn danh sách bảng trong cơ sở dữ liệu
$tables_query = $conn->query("SHOW TABLES FROM `$db_name`");

if ($tables_query) {
    while ($row = $tables_query->fetch_array()) {
        $table = $row[0];
        $count_query = $conn->query("SELECT COUNT(*) as total FROM `$table`");

        if ($count_query) {
            $count = $count_query->fetch_assoc();
            $check_result[] = "✅ [$table]: {$count['total']} dòng";
            $success++;
        } else {
            $check_result[] = "❌ [$table]: Không truy vấn được";
            $fail++;
        }
    }
} else {
    echo "❌ Không thể lấy danh sách bảng từ cơ sở dữ liệu.";
    exit;
}

// Hiển thị kết quả
echo "<h3>🔍 Kết quả kiểm tra kết nối với tất cả bảng SQL</h3>";
echo "<ul>";
foreach ($check_result as $line) {
    echo "<li>$line</li>";
}
echo "</ul>";
echo "<p>🟢 Thành công: <b>$success</b> | 🔴 Thất bại: <b>$fail</b></p>";

$conn->close();
?>