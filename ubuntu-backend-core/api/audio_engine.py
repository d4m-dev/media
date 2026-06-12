import os
import re
import shutil
import subprocess
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/audio",
    tags=["Audio Engine"]
)

# Định nghĩa hệ thống đường dẫn động
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "audio_workspace")
INPUT_DIR = os.path.join(WORKSPACE_DIR, "inputs")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "outputs")

# Đảm bảo các thư mục lõi luôn tồn tại
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_folder_name(filename: str) -> tuple:
    """Làm sạch tên file, loại bỏ ký tự lạ để tạo thư mục không bị lỗi Linux"""
    name, ext = os.path.splitext(filename)
    clean_name = re.sub(r'[^\w\-_]', '_', name)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    return clean_name, ext

def process_audio_pipeline(file_path: str, clean_name: str, ext: str, separate_beat: bool, extract_lyrics: bool):
    """Luồng xử lý ngầm: Tách nền âm thanh (MP4 -> MP3), bóc Beat và tìm Lời hát"""
    
    print(f"✅ [Audio Engine] Hoàn thành trọn vẹn Pipeline cho dự án: {clean_name}")
    # 🚀 THÊM 2 DÒNG NÀY ĐỂ BÁO HIỆU CHO FRONTEND BIẾT LÀ ĐÃ XONG:
    with open(os.path.join(project_dir, "completed.txt"), "w") as f:
        f.write("DONE")
    # Tạo thư mục định danh riêng cho bài hát để gom nhóm tệp
    project_dir = os.path.join(OUTPUT_DIR, clean_name)
    os.makedirs(project_dir, exist_ok=True)
    
    # Đường dẫn xuất file tường minh
    vocal_output = os.path.join(project_dir, f"{clean_name}_vocal.mp3")
    beat_output = os.path.join(project_dir, f"{clean_name}_beat.mp3")
    lyrics_output = os.path.join(project_dir, f"{clean_name}_lyrics.txt")
    
    # ------------------------------------------------------------
    # 🛠️ GIAI ĐOẠN 0: TRÍCH XUẤT ÂM THANH TỪ VIDEO (MP4 -> MP3)
    # ------------------------------------------------------------
    video_extensions = ['.mp4', '.mov', '.mkv', '.avi', '.flv', '.webm']
    if ext.lower() in video_extensions:
        print(f"🎬 [Audio Engine] Phát hiện định dạng Video ({ext}). Đang trích xuất MP3...")
        mp3_converted_path = os.path.join(INPUT_DIR, f"{clean_name}_converted.mp3")
        try:
            # Lấy nguyên vẹn luồng âm thanh không làm giảm chất lượng (-q:a 0)
            cmd_convert = f"ffmpeg -y -i '{file_path}' -q:a 0 -map a '{mp3_converted_path}'"
            subprocess.run(cmd_convert, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Gán lại đường dẫn file để các AI bên dưới xử lý bản MP3
            file_path = mp3_converted_path
            ext = '.mp3'
            print("✅ Đã trích xuất MP3 thành công!")
        except Exception as e:
            print(f"❌ Lỗi chuyển đổi Video sang MP3: {str(e)}")

    # ------------------------------------------------------------
    # 🛠️ GIAI ĐOẠN 1: TÁCH BEAT & VOCAL (Bằng Meta Demucs AI)
    # ------------------------------------------------------------
    if separate_beat:
        print(f"🎵 [Audio Engine] Đang bóc tách Beat/Vocal bằng Demucs AI cho: {clean_name}")
        temp_demucs_dir = os.path.join(WORKSPACE_DIR, f"temp_demucs_{clean_name}")
        os.makedirs(temp_demucs_dir, exist_ok=True)
        
        try:
            cmd_demucs = f"~/myenv/bin/demucs --two-stems=vocals -o '{temp_demucs_dir}' '{file_path}'"
            subprocess.run(cmd_demucs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Quét vào thư mục nội bộ của Demucs để bốc tệp ra
            raw_out_dir = os.path.join(temp_demucs_dir, "htdemucs", os.path.basename(file_path).replace(ext, ""))
            if not os.path.exists(raw_out_dir):
                raw_out_dir = os.path.join(temp_demucs_dir, "htdemucs", clean_name)
                
            if os.path.exists(raw_out_dir):
                vocal_wav = os.path.join(raw_out_dir, "vocals.wav")
                beat_wav = os.path.join(raw_out_dir, "no_vocals.wav")
                
                # Nén từ file WAV nặng nề sang MP3 192kbps
                if os.path.exists(vocal_wav):
                    subprocess.run(f"ffmpeg -y -i '{vocal_wav}' -b:a 192k '{vocal_output}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if os.path.exists(beat_wav):
                    subprocess.run(f"ffmpeg -y -i '{beat_wav}' -b:a 192k '{beat_output}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
        except Exception as e:
            print(f"❌ Lỗi cục bộ tại công cụ Demucs: {str(e)}")
        finally:
            if os.path.exists(temp_demucs_dir):
                shutil.rmtree(temp_demucs_dir)

    # ------------------------------------------------------------
    # 🛠️ GIAI ĐOẠN 2: TRÍCH XUẤT LỜI BÀI HÁT (Dùng Whisper STT)
    # ------------------------------------------------------------
    if extract_lyrics:
        print(f"📝 [Audio Engine] Đang quét tìm lời bài hát cho: {clean_name}")
        temp_whisper_dir = os.path.join(WORKSPACE_DIR, f"temp_whisper_{clean_name}")
        os.makedirs(temp_whisper_dir, exist_ok=True)
        
        # Lấy file Vocal ưu tiên trước để AI nghe rõ tiếng người nhất
        audio_target_for_stt = vocal_output if os.path.exists(vocal_output) else file_path
        
        try:
            cmd_whisper = f"~/myenv/bin/whisper '{audio_target_for_stt}' --model base --language vi --output_dir '{temp_whisper_dir}'"
            subprocess.run(cmd_whisper, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            whisper_file_base = os.path.basename(audio_target_for_stt).replace(".mp3", "").replace(ext, "")
            generated_txt = os.path.join(temp_whisper_dir, f"{whisper_file_base}.txt")
            
            if os.path.exists(generated_txt):
                shutil.move(generated_txt, lyrics_output)
                
        except Exception as e:
            print(f"❌ Lỗi cục bộ tại công cụ Whisper STT: {str(e)}")
        finally:
            if os.path.exists(temp_whisper_dir):
                shutil.rmtree(temp_whisper_dir)

    print(f"✅ [Audio Engine] Hoàn thành trọn vẹn Pipeline cho dự án: {clean_name}")


@router.post("/extract")
async def extract_audio_features(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    custom_name: str = Form(None), 
    separate_beat: bool = Form(True),
    extract_lyrics: bool = Form(True)
):
    """Endpoint tiếp nhận file từ Frontend Audio Studio"""
    try:
        original_clean, ext = sanitize_folder_name(file.filename)
        
        # Nếu giao diện có gửi kèm tên mới, lấy tên đó làm chuẩn
        final_name = custom_name.strip() if custom_name and custom_name.strip() else original_clean
        clean_name, _ = sanitize_folder_name(final_name)
        
        saved_input_path = os.path.join(INPUT_DIR, f"{clean_name}{ext}")
        with open(saved_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        background_tasks.add_task(
            process_audio_pipeline, 
            saved_input_path, 
            clean_name, 
            ext, 
            separate_beat, 
            extract_lyrics
        )
        
        return JSONResponse(status_code=202, content={
            "status": "processing",
            "message": f"Hệ thống đã tiếp nhận. Đang xử lý ngầm thành dự án: '{clean_name}'...",
            "project_folder": clean_name,
            "expected_outputs": {
                "vocal": f"/audio-files/{clean_name}/{clean_name}_vocal.mp3" if separate_beat else None,
                "beat": f"/audio-files/{clean_name}/{clean_name}_beat.mp3" if separate_beat else None,
                "lyrics": f"/audio-files/{clean_name}/{clean_name}_lyrics.txt" if extract_lyrics else None
            }
        })
        
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Lỗi phân rã hạ tầng âm thanh: {str(error)}")

@router.get("/status/{project_name}")
async def check_audio_status(project_name: str):
    """API để Frontend liên tục gọi vào hỏi xem AI đã chạy xong chưa"""
    flag_path = os.path.join(OUTPUT_DIR, project_name, "completed.txt")
    if os.path.exists(flag_path):
        return {"status": "completed"}
    return {"status": "processing"}