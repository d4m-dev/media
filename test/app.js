document.addEventListener('DOMContentLoaded', function() {
    const postFeed = document.getElementById('post-feed');

    // Sử dụng fetch API để thực hiện cuộc gọi AJAX
    fetch('posts.json')
        .then(response => {
            // Kiểm tra xem yêu cầu có thành công không
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Chuyển đổi phản hồi sang JSON
            return response.json();
        })
        .then(posts => {
            // Xóa nội dung mặc định (nếu có)
            postFeed.innerHTML = '';
            
            // Lặp qua mỗi bài đăng và tạo HTML tương ứng
            posts.forEach(post => {
                const postElement = document.createElement('article');
                postElement.classList.add('post');

                postElement.innerHTML = `
                    <div class="post-header">
                        <img class="avatar" src="${post.profilePic}" alt="${post.username}'s avatar">
                        <span class="username">${post.username}</span>
                    </div>
                    <div class="post-image">
                        <img src="${post.postImage}" alt="Post image">
                    </div>
                    <div class="post-footer">
                        <div class="post-actions">
                            <i class="far fa-heart"></i>
                            <i class="far fa-comment"></i>
                            <i class="far fa-paper-plane"></i>
                        </div>
                        <div class="post-info">
                            <div class="likes">${post.likes.toLocaleString()} lượt thích</div>
                            <div class="caption">
                                <span class="username">${post.username}</span>
                                <span>${post.caption}</span>
                            </div>
                        </div>
                    </div>
                `;
                
                // Thêm bài đăng đã tạo vào feed
                postFeed.appendChild(postElement);
            });
        })
        .catch(error => {
            console.error('Lỗi khi tải bài đăng:', error);
            postFeed.innerHTML = '<p>Không thể tải bài đăng. Vui lòng thử lại sau.</p>';
        });
});
