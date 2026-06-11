<!DOCTYPE HTML>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
  />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    body {
      font-family: 'Inter', sans-serif;
      padding-bottom: 80px; /* Để tránh content bị che bởi bottom nav */
    }
    
    .nav-item {
      transition: all 0.2s ease-in-out;
      position: relative;
    }
    
    .nav-item:hover {
      transform: translateY(-2px);
    }
    
    .nav-item.active {
      color: #1db954 !important;
    }
    
    .nav-item.active::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 50%;
      transform: translateX(-50%);
      width: 4px;
      height: 4px;
      background-color: #1db954;
      border-radius: 50%;
      display: none;
    }
    
    .nav-item:active {
      transform: scale(0.95);
    }
    
    .bottom-nav {
      backdrop-filter: blur(20px);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
      z-index: 997;
      transition: transform 0.4s ease-in-out;
    }
    
    @media (prefers-color-scheme: dark) {
      .bottom-nav {
        background: rgba(18, 18, 18, 0.95);
        border-color: rgba(255, 255, 255, 0.1);
      }
    }
  </style>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'spotify-green': '#1db954',
            'spotify-black': '#191414',
            'spotify-gray': '#535353'
          }
        }
      }
    }
  </script>
</head>

<body>
  <!-- Bottom Navigation -->
  <nav id="sticky-menu" class="bottom-nav fixed bottom-0 left-0 right-0 w-full border-t border-gray-200 dark:border-gray-700">
    <ul class="flex justify-around items-center py-3 px-2 max-w-md mx-auto">
      
      <!-- Home -->
      <li>
        <a href="../index.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-home text-xl mb-1"></i>
          <span class="text-xs font-medium">Home</span>
        </a>
      </li>
      
      <!-- Search -->
      <li>
        <a href="../pages/search.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-search text-xl mb-1"></i>
          <span class="text-xs font-medium">Search</span>
        </a>
      </li>
      
      <!-- Your Library -->
      <li>
        <a href="../pages/library.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-book text-xl mb-1"></i>
          <span class="text-xs font-medium">Library</span>
        </a>
      </li>
      
      <!-- Premium -->
      <li>
        <a href="../pages/subscription.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-crown text-xl mb-1"></i>
          <span class="text-xs font-medium">Premium</span>
        </a>
      </li>
      
      <!-- Profile -->
      <li>
        <a href="../private/profile.php" class="nav-item flex flex-col items-center text-spotify-gray hover:text-gray-900 dark:hover:text-white cursor-pointer p-2 rounded-lg">
          <i class="fas fa-user text-xl mb-1"></i>
          <span class="text-xs font-medium">Profile</span>
        </a>
      </li>
      
    </ul>
  </nav>
  <script>
    // JavaScript để ẩn/hiện thanh menu khi người dùng vuốt lên/xuống
    let lastScrollTop = 0;
    const menu = document.getElementById('sticky-menu');

    window.addEventListener('scroll', function() {
        let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > lastScrollTop) {
            // Vuốt xuống, ẩn menu
            menu.style.transform = 'translateY(100%)';
        } else {
            // Vuốt lên, hiện menu
            menu.style.transform = 'translateY(0)';
        }
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Đảm bảo không bị lỗi khi ở đầu trang
    });
  
    // JavaScript để xử lý navigation
    document.addEventListener('DOMContentLoaded', function() {
      const navItems = document.querySelectorAll('.nav-item');
      
      navItems.forEach(item => {
        item.addEventListener('click', function(e) {
          e.preventDefault();
          
          // Remove active class from all items
          navItems.forEach(nav => nav.classList.remove('active'));
          
          // Add active class to clicked item
          this.classList.add('active');
          
          // Get the href attribute
          const href = this.getAttribute('href');
          
          // Simulate navigation (replace with actual routing logic)
          console.log(`Navigating to: ${href}`);
          
          // For demo purposes, we'll just update the URL without actually navigating
          if (href !== '#') {
            // For actual navigation:
            window.location.href = href;
          }
        });
      });
    });
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', function(event) {
      updateActiveNavItem();
    });
    
    function updateActiveNavItem() {
      const currentPath = window.location.pathname;
      const navItems = document.querySelectorAll('.nav-item');
      
      navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === currentPath) {
          item.classList.add('active');
        }
      });
    }
    
    // Smooth scroll behavior when clicking navigation
    document.documentElement.style.scrollBehavior = 'smooth';
  </script>
</body>
</html>