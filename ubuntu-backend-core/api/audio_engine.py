import os
import subprocess
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import aiofiles

from core.security import verify_token

router = APIRouter(
    prefix="/api/audio",
    tags=["Audio Engine"],
    dependencies=[Depends(verify_token)] 
)

AUDIO_WORKSPACE = "/storage/emulated/0/coder/media/ubuntu-backend-core/audio_workspace"
INPUT_DIR = os.path.join(AUDIO_WORKSPACE, "inputs")
OUTPUT_DIR = os.path.join(AUDIO_WORKSPACE, "outputs")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/extract-mp3")
async def extract_mp3_from_video(file: UploadFile = File(...)):
    """API Tách tiếng Video: Nhận MP4, trả về MP3 320kbps"""
    if not file.filename.endswith(('.mp4', '.mkv', '.mov')):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng video (.mp4, .mkv, .mov)")

    input_path = os.path.join(INPUT_DIR, file.filename)
    output_filename = f"{os.path.splitext(file.filename)[0]}.mp3"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        command = [
            "ffmpeg", "-y", "-i", input_path, 
            "-q:a", "0", "-map", "a", output_path
        ]
        
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise Exception("Lỗi FFmpeg khi bóc tách luồng âm thanh.")

        return {
            "status": "success",
            "message": "✅ Tách tiếng video thành công!",
            "file_name": output_filename,
            "download_url": f"/audio-files/{output_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

@router.post("/remove-vocal")
async def remove_vocal(file: UploadFile = File(...)):
    """API Tách Lời & Beat: Phân tách âm thanh đa tầng bằng Demucs AI"""
    if not file.filename.endswith(('.mp3', '.wav', '.flac', '.m4a')):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file âm thanh (.mp3, .wav, .flac, .m4a)")

    input_path = os.path.join(INPUT_DIR, file.filename)
    base_name = os.path.splitext(file.filename)[0]
    
    try:
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Sử dụng mô hình htdemucs chạy tác vụ trên nhân CPU cục bộ
        command = [
            "demucs", "--two-stems=vocals", 
            "-d", "cpu", 
            "-o", OUTPUT_DIR, 
            input_path
        ]
        
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise Exception("Lỗi Động cơ AI Demucs khi phân rã bài hát.")

        result_dir = os.path.join(OUTPUT_DIR, "htdemucs", base_name)
        vocal_path = os.path.join(result_dir, "vocals.wav")
        beat_path = os.path.join(result_dir, "no_vocals.wav")

        final_vocal = f"{base_name}_vocal.wav"
        final_beat = f"{base_name}_beat.wav"
        
        if os.path.exists(vocal_path) and os.path.exists(beat_path):
            shutil.move(vocal_path, os.path.join(OUTPUT_DIR, final_vocal))
            shutil.move(beat_path, os.path.join(OUTPUT_DIR, final_beat))
            shutil.rmtree(os.path.join(OUTPUT_DIR, "htdemucs")) 

        return {
            "status": "success",
            "message": "✅ Demucs AI bóc tách giọng hát hoàn tất!",
            "vocal_url": f"/audio-files/{final_vocal}",
            "beat_url": f"/audio-files/{final_beat}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)