import React, { useState, useEffect } from 'react';
import { ChevronDown, X, Loader2, Zap, Shield, Maximize, Coins, ArrowRight } from 'lucide-react';

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [ideaInput, setIdeaInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resultText, setResultText] = useState('');
  const [isScrolled, setIsScrolled] = useState(false);

  // Hiệu ứng thay đổi Navbar khi cuộn trang
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const generatePitch = async () => {
    if (!ideaInput.trim()) return;
    setIsLoading(true);
    setResultText('');

    const apiKey = ""; // API key is provided by the execution environment

    const fetchWithRetry = async (url, options, retries = 5) => {
      const delays = [1000, 2000, 4000, 8000, 16000];
      for (let i = 0; i < retries; i++) {
        try {
          const res = await fetch(url, options);
          if (res.ok) return res;
          if (i === retries - 1) throw new Error('Max retries reached');
        } catch (err) {
          if (i === retries - 1) throw err;
          await new Promise(resolve => setTimeout(resolve, delays[i]));
        }
      }
    };

    const systemPrompt = "Bạn là một chuyên gia kiến trúc Web3 và nhà đầu tư mạo hiểm (VC). Người dùng sẽ cung cấp một ý tưởng ứng dụng truyền thống. Nhiệm vụ của bạn là nâng cấp nó thành một bản thuyết trình DApp Web3 xuất sắc. Bao gồm 3 phần ngắn gọn bằng TIẾNG VIỆT: 1. Ý tưởng cốt lõi (Elevator Pitch), 2. Tại sao lại là Web3? (Lợi thế phi tập trung), 3. Các tính năng chính. Viết súc tích, mang tính tầm nhìn và dưới 200 từ.";

    try {
      const response = await fetchWithRetry(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: ideaInput }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] }
          })
        }
      );

      const data = await response.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      setResultText(text || "Không thể tạo bản đánh giá. Vui lòng thử lại.");
    } catch (error) {
      setResultText("Có lỗi xảy ra khi kết nối với hệ thống AI. Vui lòng thử lại sau.");
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    { icon: <Zap size={24} />, title: "Tốc độ chớp nhoáng", desc: "Giao dịch được xử lý và xác nhận tính bằng mili giây, mang lại trải nghiệm không độ trễ." },
    { icon: <Shield size={24} />, title: "Bảo mật tuyệt đối", desc: "Mã hóa đa lớp và hợp đồng thông minh đã được kiểm toán đảm bảo an toàn cho mọi tài sản số." },
    { icon: <Maximize size={24} />, title: "Mở rộng không giới hạn", desc: "Cấu trúc mạng lưới được thiết kế để chịu tải cho hàng triệu người dùng cùng lúc mà không bị nghẽn." },
    { icon: <Coins size={24} />, title: "Chi phí cực thấp", desc: "Phí gas được tối ưu hóa đến mức gần như bằng không, giúp tối đa hóa lợi nhuận cho người dùng." },
  ];

  const stats = [
    { value: "10M+", label: "Giao dịch mỗi ngày" },
    { value: "500K+", label: "Người dùng tích cực" },
    { value: "$2B+", label: "Tổng giá trị khóa (TVL)" },
    { value: "99.9%", label: "Thời gian hoạt động (Uptime)" },
  ];

  return (
    <>
      <style dangerouslySetInnerHTML={{
        __html: `
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        .font-jakarta {
          font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.2);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.3);
        }
        html { scroll-behavior: smooth; }
      `}} />

      <div className="bg-black min-h-screen font-jakarta text-white selection:bg-white/30">
        
        {/* ================= NAVBAR ================= */}
        <nav className={`fixed top-0 left-0 w-full flex items-center justify-between px-6 md:px-[120px] py-4 md:py-[20px] z-50 transition-all duration-300 ${isScrolled ? 'bg-black/80 backdrop-blur-lg border-b border-white/10' : 'bg-transparent'}`}>
          <div className="flex items-center gap-[60px]">
            {/* Logo */}
            <div className="w-[187px] h-[25px] flex items-center shrink-0">
              <svg viewBox="0 0 187 25" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-full w-auto">
                <text x="0" y="20" fill="white" className="font-bold text-xl tracking-widest uppercase">LOGOIPSUM</text>
              </svg>
            </div>

            {/* Nav Links */}
            <div className="hidden md:flex items-center gap-[30px]">
              {['Bắt đầu', 'Lập trình viên', 'Tính năng', 'Tài nguyên'].map((link) => (
                <a key={link} href={`#${link.toLowerCase()}`} className="flex items-center gap-[14px] text-white text-[14px] font-medium hover:text-white/70 transition-colors">
                  {link}
                  <ChevronDown size={14} strokeWidth={2.5} />
                </a>
              ))}
            </div>
          </div>

          <button className="relative group hidden sm:inline-flex p-[0.6px] rounded-full overflow-hidden shrink-0 transition-transform hover:scale-105 duration-300">
            <div className="absolute inset-0 bg-white"></div>
            <div className="absolute -top-[6px] left-1/2 -translate-x-1/2 w-[70%] h-[14px] bg-white blur-[6px] opacity-80 z-[1]"></div>
            <div className="relative z-10 flex items-center justify-center bg-black text-white px-[29px] py-[11px] rounded-full text-[14px] font-medium w-full h-full">
              Tham gia danh sách chờ
            </div>
          </button>
        </nav>

        {/* ================= HERO SECTION ================= */}
        <section className="relative h-screen w-full flex flex-col items-center justify-center overflow-hidden pt-[80px]">
          {/* Background Video */}
          <video autoPlay loop muted playsInline className="absolute inset-0 w-full h-full object-cover z-0">
            <source src="./assets/background.mp4" type="video/mp4" />
          </video>
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black z-[1]"></div>

          <main className="relative z-20 flex flex-col items-center justify-center text-center w-full px-4">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 rounded-[20px] bg-white/10 border border-white/20 px-3 py-1.5 backdrop-blur-sm mb-[40px] animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="w-1 h-1 rounded-full bg-white shrink-0 shadow-[0_0_8px_2px_rgba(255,255,255,0.8)]"></div>
              <p className="text-[13px] font-medium tracking-wide">
                <span className="text-white/70">Mở truy cập sớm từ</span>
                <span className="text-white ml-1 font-semibold">1 tháng 5, 2026</span>
              </p>
            </div>

            {/* Heading */}
            <h1 className="text-[40px] md:text-[64px] font-medium leading-[1.15] max-w-[700px] mb-[24px] tracking-tight animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100"
                style={{ 
                  backgroundImage: 'linear-gradient(144.5deg, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 0.4) 115%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent'
                }}>
              Web3 với Tốc độ của Trải nghiệm
            </h1>

            {/* Subtitle */}
            <p className="text-[16px] md:text-[18px] font-normal text-white/70 max-w-[680px] leading-relaxed mb-[48px] animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
              Thúc đẩy những trải nghiệm liền mạch và kết nối thời gian thực. Nền tảng hoàn hảo cho các nhà sáng tạo hành động có mục đích, tận dụng tính bền bỉ, tốc độ và quy mô để định hình tương lai.
            </p>

            {/* Buttons */}
            <div className="flex flex-col sm:flex-row items-center gap-5 animate-in fade-in slide-in-from-bottom-10 duration-700 delay-300">
              <button className="relative group inline-flex p-[0.6px] rounded-full overflow-hidden shrink-0 transition-transform hover:scale-105 duration-300">
                <div className="absolute inset-0 bg-white"></div>
                <div className="absolute -top-[8px] left-1/2 -translate-x-1/2 w-[80%] h-[18px] bg-white shadow-[0_0_15px_5px_rgba(255,255,255,0.7)] blur-[8px] opacity-100 z-[1]"></div>
                <div className="relative z-10 flex items-center justify-center bg-white text-black px-[32px] py-[14px] rounded-full text-[15px] font-semibold w-full h-full">
                  Bắt đầu ngay
                </div>
              </button>

              <button 
                onClick={() => setIsModalOpen(true)}
                className="relative group inline-flex p-[1px] rounded-full overflow-hidden shrink-0 transition-all hover:scale-105 duration-300"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/50 via-purple-500/50 to-blue-500/50 opacity-70 group-hover:opacity-100 transition-opacity"></div>
                <div className="relative z-10 flex items-center justify-center gap-2 bg-black/50 backdrop-blur-md text-white px-[32px] py-[13px] rounded-full text-[15px] font-medium w-full h-full border border-white/10 hover:bg-black/40 transition-colors">
                  ✨ Đánh giá Ý tưởng DApp
                </div>
              </button>
            </div>
          </main>
          
          {/* Scroll Indicator */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-50 z-20">
            <ChevronDown size={24} />
          </div>
        </section>

        {/* ================= STATS SECTION ================= */}
        <section className="py-20 bg-[#020202] border-b border-white/5 relative z-10">
          <div className="max-w-[1200px] mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4 divide-x-0 md:divide-x divide-white/10">
            {stats.map((stat, idx) => (
              <div key={idx} className="flex flex-col items-center justify-center text-center">
                <h3 className="text-4xl md:text-5xl font-semibold mb-2 bg-gradient-to-br from-white to-white/40 bg-clip-text text-transparent">{stat.value}</h3>
                <p className="text-white/50 text-sm font-medium uppercase tracking-wider">{stat.label}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ================= FEATURES SECTION ================= */}
        <section id="tính năng" className="py-24 md:py-32 bg-black relative z-10">
          <div className="max-w-[1200px] mx-auto px-6">
            <div className="text-center mb-16 md:mb-24">
              <h2 className="text-3xl md:text-5xl font-medium mb-6">Định nghĩa lại giới hạn</h2>
              <p className="text-white/60 text-lg max-w-2xl mx-auto">Kiến trúc của chúng tôi được thiết kế để vượt qua những rào cản của blockchain truyền thống, mang lại trải nghiệm ưu việt cho cả lập trình viên và người dùng.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10">
              {features.map((feature, idx) => (
                <div key={idx} className="group p-8 md:p-10 rounded-[32px] bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-colors duration-300">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-white/10 to-transparent border border-white/10 flex items-center justify-center mb-6 text-white group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-medium mb-4">{feature.title}</h3>
                  <p className="text-white/60 leading-relaxed">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ================= CTA SECTION ================= */}
        <section className="py-24 relative z-10 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-black to-[#050505] z-0"></div>
          {/* Subtle glow effect in background */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-blue-600/20 blur-[120px] rounded-full z-0 pointer-events-none"></div>
          
          <div className="relative z-10 max-w-[800px] mx-auto px-6 text-center">
            <h2 className="text-4xl md:text-5xl font-medium mb-6">Sẵn sàng để xây dựng tương lai?</h2>
            <p className="text-white/60 text-lg mb-10">Gia nhập cùng hàng ngàn nhà phát triển đang kiến tạo thế hệ ứng dụng phi tập trung tiếp theo trên nền tảng của chúng tôi.</p>
            <button className="relative group inline-flex p-[0.6px] rounded-full overflow-hidden shrink-0 transition-transform hover:scale-105 duration-300">
              <div className="absolute inset-0 bg-white"></div>
              <div className="absolute -top-[8px] left-1/2 -translate-x-1/2 w-[80%] h-[18px] bg-white shadow-[0_0_15px_5px_rgba(255,255,255,0.7)] blur-[8px] opacity-100 z-[1]"></div>
              <div className="relative z-10 flex items-center justify-center gap-2 bg-white text-black px-[36px] py-[16px] rounded-full text-[15px] font-semibold w-full h-full">
                Tham gia Discord cộng đồng <ArrowRight size={18} />
              </div>
            </button>
          </div>
        </section>

        {/* ================= FOOTER ================= */}
        <footer className="bg-[#020202] pt-20 pb-10 border-t border-white/10 relative z-10">
          <div className="max-w-[1200px] mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-16">
              <div className="col-span-1 md:col-span-2">
                <div className="w-[150px] h-[20px] flex items-center mb-6">
                  <svg viewBox="0 0 187 25" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-full w-auto">
                    <text x="0" y="20" fill="white" className="font-bold text-xl tracking-widest uppercase opacity-50">LOGOIPSUM</text>
                  </svg>
                </div>
                <p className="text-white/50 max-w-sm mb-6 text-sm">Hạ tầng Web3 ưu việt dành cho thế hệ nhà phát triển sáng tạo tương lai.</p>
                <div className="flex items-center gap-4 text-white/50">
                  <a href="#" className="hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/></svg>
                  </a>
                  <a href="#" className="hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                  </a>
                  <a href="#" className="hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="2"/></svg>
                  </a>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-white mb-6">Sản phẩm</h4>
                <ul className="space-y-4 text-sm text-white/50">
                  <li><a href="#" className="hover:text-white transition-colors">Tính năng chính</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Bảo mật</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Mở rộng</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Bảng giá phí</a></li>
                </ul>
              </div>

              <div>
                <h4 className="font-medium text-white mb-6">Tài nguyên</h4>
                <ul className="space-y-4 text-sm text-white/50">
                  <li><a href="#" className="hover:text-white transition-colors">Tài liệu API</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Sách trắng (Whitepaper)</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Hỗ trợ</a></li>
                </ul>
              </div>
            </div>
            
            <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-white/40">
              <p>© 2026 LogoIpsum. Đã đăng ký bản quyền.</p>
              <div className="flex gap-6">
                <a href="#" className="hover:text-white">Điều khoản sử dụng</a>
                <a href="#" className="hover:text-white">Chính sách bảo mật</a>
              </div>
            </div>
          </div>
        </footer>

        {/* ================= MODAL AI PITCH ================= */}
        {isModalOpen && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center px-4">
            <div className="absolute inset-0 bg-black/80 backdrop-blur-md" onClick={() => setIsModalOpen(false)}></div>
            <div className="relative w-full max-w-lg bg-[#0a0a0a] border border-white/10 rounded-[24px] p-6 shadow-2xl flex flex-col gap-5 animate-in fade-in zoom-in-95 duration-200">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-medium flex items-center gap-2">
                  <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">✨ Trình tạo Pitch AI</span>
                </h3>
                <button onClick={() => setIsModalOpen(false)} className="text-white/40 hover:text-white hover:bg-white/10 p-2 rounded-full transition-all">
                  <X size={20} />
                </button>
              </div>
              
              <p className="text-[14px] text-white/60 leading-relaxed">
                Mô tả ý tưởng ứng dụng Web2 truyền thống của bạn, AI Architect của chúng tôi sẽ chuyển đổi nó thành một bản thuyết trình Web3 đầy sức mạnh.
              </p>

              <textarea 
                className="w-full bg-white/[0.03] border border-white/10 rounded-xl p-4 text-white placeholder:text-white/30 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 resize-none h-32 text-[14px] transition-all"
                placeholder="VD: Một nền tảng đặt vé xem phim và đánh giá phim..."
                value={ideaInput}
                onChange={(e) => setIdeaInput(e.target.value)}
              />

              <button 
                onClick={generatePitch}
                disabled={isLoading || !ideaInput.trim()}
                className="relative overflow-hidden rounded-xl bg-white text-black font-semibold py-3.5 text-[14px] flex items-center justify-center gap-2 hover:bg-white/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                {isLoading ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <>✨ Phân tích Ý tưởng <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" /></>
                )}
              </button>

              {resultText && (
                <div className="mt-2 p-5 bg-gradient-to-b from-white/5 to-transparent border border-white/10 rounded-xl max-h-[250px] overflow-y-auto custom-scrollbar">
                  <div className="text-[14px] text-white/80 whitespace-pre-wrap leading-relaxed">
                    {resultText}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

      </div>
    </>
  );
}