const zoneData = {
  "zone-home": {
    text: "🏠 Đây là khu nhà ở – nơi bạn sinh sống, trang trí và gặp gỡ bạn bè.",
    image: "../assets/images/khunhao.png"
  },
  "zone-park": {
    text: "🌳 Công viên để thư giãn, gặp NPC và khám phá sự kiện đặc biệt.",
    image: "../assets/images/congvien.png"
  },
  "zone-fun": {
    text: "🎮 Khu giải trí đầy mini game hấp dẫn!",
    image: "../assets/images/khugiaitri.png"
  },
  "zone-suburb": {
    text: "🏡 Khu ngoại ô – nơi yên bình, phù hợp với du lịch hoặc thử thách cộng đồng.",
    image: "../assets/images/ngoaio.png"
  },
  "zone-farm": {
    text: "🚜 Nông trại – trồng trọt, chăn nuôi và thu hoạch.",
    image: "../assets/images/nongtrai.png"
  },
  "zone-fishing": {
    text: "🎣 Khu câu cá – kiếm phần thưởng và thư giãn cuối ngày.",
    image: "../assets/images/cauca.png"
  },
  "zone-airport": {
    text: "✈️ Sân bay – nơi di chuyển tới các thành phố khác hoặc nhận quà từ sự kiện!",
    image: "../assets/images/sanbay.png" // Đây là ảnh bạn vừa gửi!
  },
  "zone-shop": {
    text: "🛍️ Khu mua sắm – thời trang, phụ kiện và vật phẩm siêu xịn.",
    image: "../assets/images/khumuasam.png"
  }
};

document.querySelectorAll(".map-zone").forEach(zone => {
  zone.addEventListener("click", () => {
    const zoneId = zone.getAttribute("id");
    const content = zoneData[zoneId];
    const popup = document.getElementById("zone-content");
    const imageEl = document.getElementById("zone-image");

    if (content) {
      popup.querySelector("p").innerText = content.text;
      imageEl.src = "assets/images/" + content.image;
      imageEl.style.display = "block";
      imageEl.alt = zoneId;
    } else {
      popup.querySelector("p").innerText = "📦 Nội dung đang được cập nhật!";
      imageEl.style.display = "none";
    }
  });
});