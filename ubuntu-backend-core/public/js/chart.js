let trafficChartInstance = null;

// Hàm khởi tạo biểu đồ rỗng (Style Glassmorphism)
function initChart() {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    
    // Tạo gradient đổ màu siêu đẹp dưới đường Line
    let gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)'); // Xanh dương trong suốt
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)'); 

    trafficChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Giờ/Phút
            datasets: [{
                label: ' Số Lượng Request',
                data: [], // Số liệu request
                borderColor: '#3b82f6', // Neon Blue
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4, // Tạo đường cong mềm mại
                pointBackgroundColor: '#fff',
                pointBorderColor: '#3b82f6',
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#3b82f6',
                    padding: 10,
                    cornerRadius: 8,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#9ca3af',
                        stepSize: 1, // Để đồ thị hiện số nguyên (1, 2, 3...)
                        font: { family: 'sans-serif' }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#9ca3af',
                        font: { family: 'sans-serif' }
                    }
                }
            }
        }
    });
}

// Hàm fetch dữ liệu và update biểu đồ
async function fetchChartData() {
    if (!authToken) return; // Không có token thì không fetch
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/dashboard/analytics`);
        const data = await response.json();
        
        // Trích xuất mảng thời gian và dữ liệu
        const labels = data.timeline.map(item => item.time);
        const counts = data.timeline.map(item => item.count);

        // Đổ dữ liệu mới vào biểu đồ và cập nhật hiệu ứng mượt
        trafficChartInstance.data.labels = labels;
        trafficChartInstance.data.datasets[0].data = counts;
        trafficChartInstance.update('none'); // Update không có animation lag

    } catch (error) {
        console.error("Lỗi cập nhật biểu đồ:", error);
    }
}

// Khởi chạy biểu đồ khi DOM tải xong
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    
    // Cập nhật biểu đồ mỗi 5 giây cho hiệu ứng Real-time
    setInterval(fetchChartData, 5000);
});