<?php
include '../inc/db.php';
session_start();
?>

<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Upload Bài Hát</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/cropperjs@1.5.13/dist/cropper.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/cropperjs@1.5.13/dist/cropper.min.js"></script>
  <style>
    body {
      background: linear-gradient(135deg, #f0f2f5, #ffffff);
    }
    .upload-container {
      max-width: 650px;
      margin: auto;
      margin-top: 40px;
      padding: 30px;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .form-label {
      font-weight: 600;
    }
    .preview-img {
      width: 100%;
      max-height: 300px;
      object-fit: cover;
      border-radius: 10px;
      margin-top: 10px;
    }
    #modalCropImage {
      max-width: 99%;
      max-height: 70vh;
      display: block;
      margin: auto;
      background: repeating-conic-gradient(#ccc 0% 25%, transparent 0% 50%) 50% / 20px 20px;
    }
    .cropper-bg {
      background-image: none !important;
      background-color: transparent !important;
    }
  </style>
</head>
<body>
  <div class="upload-container">
    <h3 class="text-center mb-4">🎶 Upload Bài Hát Mới</h3>
    <form method="post" action="../handler/upload_handler.php" enctype="multipart/form-data">
      
      <!-- Ảnh bìa -->
      <div class="mb-3">
        <label class="form-label">Ảnh bìa bài hát (upload hoặc link)</label>

        <div class="form-check mb-2">
          <input class="form-check-input" type="radio" name="cover_mode" id="coverUploadMode" value="upload" checked onchange="toggleCoverMode()">
          <label class="form-check-label" for="coverUploadMode">Tải ảnh từ thiết bị</label>
        </div>

        <div class="form-check mb-3">
          <input class="form-check-input" type="radio" name="cover_mode" id="coverLinkMode" value="url" onchange="toggleCoverMode()">
          <label class="form-check-label" for="coverLinkMode">Dán đường dẫn ảnh (Chỉ cho phép ảnh 1:1)</label>
        </div>

        <div id="coverUploadField">
          <input class="form-control" type="file" accept="image/*" id="coverInput" onchange="openCropModal(this.files[0])">
          <input type="hidden" name="cropped_image_data" id="croppedData">
        </div>

        <div id="coverLinkField" style="display: none;">
          <input type="url" class="form-control" name="cover_url" placeholder="https://example.com/image.jpg" oninput="previewCoverURL(this.value)">
        </div>

        <img id="coverPreview" class="preview-img" style="display:none;" alt="Preview ảnh bìa">
      </div>

      <!-- Tên bài hát -->
      <div class="mb-3">
        <label class="form-label">Tên bài hát</label>
        <input type="text" class="form-control" name="song_name" required>
      </div>

      <!-- Ca sĩ -->
      <div class="mb-3">
        <label class="form-label">Ca sĩ</label>
        <input type="text" class="form-control" name="artist_name" required>
      </div>

      <!-- Thể loại -->
      <div class="mb-3">
        <label class="form-label">Thể loại</label>
        <select class="form-select" name="genre" required>
          <option value="">-- Chọn thể loại --</option>
          <option>Official</option>
          <option>Lofi</option>
          <option>Hát Liver</option>
          <option>Cover</option>
          <option>Mashup</option>
          <option>Remix</option>
          <option>OST</option>
          <option>Nhạc Trung</option>
          <option>Nhạc nước ngoài</option>
        </select>
      </div>

      <!-- Nhạc -->
      <div class="mb-3">
        <label class="form-label">Nhạc bài hát (tải lên hoặc dán link)</label>

        <div class="form-check mb-2">
          <input class="form-check-input" type="radio" name="audio_mode" id="audioUploadMode" value="upload" checked onchange="toggleAudioMode()">
          <label class="form-check-label" for="audioUploadMode">Tải nhạc từ thiết bị</label>
        </div>

        <div class="form-check mb-3">
          <input class="form-check-input" type="radio" name="audio_mode" id="audioLinkMode" value="url" onchange="toggleAudioMode()">
          <label class="form-check-label" for="audioLinkMode">Dán đường dẫn .mp3</label>
        </div>

        <div id="audioUploadField">
          <input type="file" class="form-control" name="audio_file" accept=".mp3" onchange="checkFileSize(this)">
        </div>

        <div id="audioLinkField" style="display: none;">
          <input type="url" class="form-control" name="audio_url" placeholder="https://example.com/song.mp3">
        </div>
      </div>

      <!-- Submit -->
      <div class="text-center">
        <button type="submit" class="btn btn-primary px-4">Tải lên</button>
      </div>

    </form>
  </div>

  <!-- Modal crop ảnh -->
  <div class="modal fade" id="cropModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered" style="max-width: 90vw;">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Cắt ảnh bìa</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body text-center">
          <img id="modalCropImage" style="max-width:100%;">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Huỷ</button>
          <button type="button" class="btn btn-primary" onclick="cropImage()">Xong</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Scripts -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
  let cropper;
  const cropModal = new bootstrap.Modal(document.getElementById('cropModal'));

  function checkFileSize(input) {
    if (input.files[0].size > 50 * 1024 * 1024) {
      alert("⚠️ File quá lớn! Vui lòng chọn file dưới 50MB.");
      input.value = "";
    }
  }

  function openCropModal(file) {
    const image = document.getElementById('modalCropImage');
    const reader = new FileReader();

    reader.onload = function(e) {
      image.src = e.target.result;
      cropModal.show();

      setTimeout(() => {
        if (cropper) cropper.destroy();
        cropper = new Cropper(image, {
          aspectRatio: 1,
          viewMode: 1,
          autoCropArea: 1
        });
      }, 200);
    };

    if (file) reader.readAsDataURL(file);
  }

  function cropImage() {
    const canvas = cropper.getCroppedCanvas({
      width: 400,
      height: 400
    });
    const dataUrl = canvas.toDataURL('image/jpeg');

    document.getElementById('coverPreview').src = dataUrl;
    document.getElementById('coverPreview').style.display = 'block';
    document.getElementById('croppedData').value = dataUrl;

    cropModal.hide();
  }

  function toggleAudioMode() {
    const upload = document.getElementById('audioUploadMode').checked;
    document.getElementById('audioUploadField').style.display = upload ? 'block' : 'none';
    document.getElementById('audioLinkField').style.display = upload ? 'none' : 'block';
  }

  function toggleCoverMode() {
    const isUpload = document.getElementById('coverUploadMode').checked;
    document.getElementById('coverUploadField').style.display = isUpload ? 'block' : 'none';
    document.getElementById('coverLinkField').style.display = isUpload ? 'none' : 'block';
    document.getElementById('coverPreview').style.display = 'none';
    document.getElementById('croppedData').value = '';
  }

  function previewCoverURL(url) {
    const img = document.getElementById('coverPreview');
    if (!url) {
      img.style.display = 'none';
      return;
    }

    const testImg = new Image();
    testImg.onload = function() {
      img.src = url;
      img.style.display = 'block';
    };
    testImg.onerror = function() {
      img.style.display = 'none';
      alert('⚠️ Không thể tải ảnh từ đường dẫn đã nhập!');
    };
    testImg.src = url;
  }

  // 👇 Gọi toggle để đảm bảo trạng thái đúng khi load lại/trở lại trang
  window.addEventListener('DOMContentLoaded', () => {
    toggleCoverMode();
    toggleAudioMode();
  });
</script>
</body>
</html>