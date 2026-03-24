from fastapi import APIRouter, Depends
from src.router.auth import require_api_key
import pyaudio


router: APIRouter = APIRouter(prefix="/speakers", tags=["speakers"])


@router.get("/", dependencies=[Depends(require_api_key)])
def get_audio_devices():
    pa = pyaudio.PyAudio()
    device_names = [
        pa.get_device_info_by_index(i).get("name") for i in range(pa.get_device_count())
    ]
    pa.terminate()
    return device_names
