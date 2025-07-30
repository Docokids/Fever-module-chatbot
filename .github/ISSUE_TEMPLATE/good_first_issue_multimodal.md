---
name: Good First Issue - Multi-modal Support
about: Implement support for image and voice inputs
labels: ["good first issue", "enhancement", "multimodal", "ai"]
assignees: []
---

## 🎯 Multi-modal Support Implementation

**Difficulty**: Advanced  
**Estimated Time**: 5-7 days  
**Area**: Multi-modal AI, Image Processing, Voice Recognition

### 📋 Description

Implement multi-modal capabilities to support image and voice inputs, allowing users to send photos of symptoms (like rashes, thermometers) and voice messages, making the chatbot more accessible and comprehensive for pediatric fever assessment.

### 🎯 Goals

- [ ] Create image processing service for symptom photos
- [ ] Implement voice-to-text conversion for voice messages
- [ ] Add multi-modal input handling to conversation flow
- [ ] Integrate with existing LLM providers that support multi-modal
- [ ] Add file upload and processing endpoints

### 🔧 Technical Details

**Files to modify/create:**
- `src/services/image_processor.py` (new)
- `src/services/voice_processor.py` (new)
- `src/services/multimodal_service.py` (new)
- `src/api/v1/multimodal.py` (new)
- `src/models/multimodal.py` (new)
- `src/core/config.py` (add multimodal settings)
- `tests/test_multimodal.py` (new)

**Key components:**
- Image processing and analysis
- Voice-to-text conversion
- Multi-modal message formatting
- File upload handling
- Integration with conversation system

### 🚀 Getting Started

1. **Familiarize yourself with the codebase:**
   - Review `src/api/v1/conversations.py` for endpoint patterns
   - Check `src/services/` for service patterns
   - Look at existing file handling in the project

2. **Study multi-modal concepts:**
   - Image processing and analysis
   - Voice recognition and transcription
   - Multi-modal AI models
   - File upload and storage patterns

3. **Implementation approach:**
   - Start with image upload and processing
   - Add voice-to-text conversion
   - Integrate with multi-modal LLM providers
   - Add comprehensive error handling

### 📚 Resources

- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/file-uploading/)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- [Pillow for image processing](https://pillow.readthedocs.io/)
- [Multi-modal AI concepts](https://en.wikipedia.org/wiki/Multimodal_learning)

### ✅ Acceptance Criteria

- [ ] Image upload and processing endpoints work
- [ ] Voice-to-text conversion is functional
- [ ] Multi-modal inputs are integrated with conversation flow
- [ ] Support for at least one multi-modal LLM provider
- [ ] File validation and security measures
- [ ] Tests cover multi-modal functionality
- [ ] Documentation includes multi-modal usage examples

### 💡 Tips

- Start with image processing as it's more straightforward
- Use cloud services for voice-to-text to avoid complexity
- Implement proper file validation and security
- Consider image compression and optimization
- Add support for multiple image formats

### 🔍 Example Implementation

```python
from fastapi import UploadFile, File
from PIL import Image
import io
import speech_recognition as sr
from typing import Dict, Any

class MultimodalService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.voice_processor = VoiceProcessor()
    
    async def process_image(self, image_file: UploadFile) -> Dict[str, Any]:
        """Process uploaded image for symptom analysis"""
        try:
            # Read and validate image
            image_data = await image_file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Process image for medical analysis
            analysis = await self.image_processor.analyze_symptoms(image)
            
            return {
                "type": "image",
                "content": analysis,
                "filename": image_file.filename,
                "size": len(image_data)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")
    
    async def process_voice(self, audio_file: UploadFile) -> Dict[str, Any]:
        """Convert voice message to text"""
        try:
            # Read audio file
            audio_data = await audio_file.read()
            
            # Convert to text
            text = await self.voice_processor.speech_to_text(audio_data)
            
            return {
                "type": "voice",
                "content": text,
                "filename": audio_file.filename,
                "duration": len(audio_data)  # Approximate duration
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Voice processing failed: {str(e)}")

class ImageProcessor:
    async def analyze_symptoms(self, image: Image) -> str:
        """Analyze image for medical symptoms"""
        # Resize image for processing
        image = image.resize((224, 224))
        
        # Convert to base64 for API calls
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Call multi-modal LLM for analysis
        analysis = await self._call_vision_model(image_base64)
        
        return analysis
    
    async def _call_vision_model(self, image_base64: str) -> str:
        """Call vision-capable LLM for image analysis"""
        # Implementation depends on chosen LLM provider
        # Example with OpenAI Vision API
        pass

class VoiceProcessor:
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert audio to text using speech recognition"""
        # Implementation using speech recognition library
        # or cloud service like Google Speech-to-Text
        pass
```

### 📱 API Endpoints

```python
@router.post("/conversations/{conversation_id}/image")
async def upload_image(
    conversation_id: str,
    image: UploadFile = File(...)
):
    """Upload and process image for conversation"""
    result = await multimodal_service.process_image(image)
    return await conversation_service.add_multimodal_message(
        conversation_id, result
    )

@router.post("/conversations/{conversation_id}/voice")
async def upload_voice(
    conversation_id: str,
    audio: UploadFile = File(...)
):
    """Upload and process voice message"""
    result = await multimodal_service.process_voice(audio)
    return await conversation_service.add_multimodal_message(
        conversation_id, result
    )
```

### 🎯 Supported Formats

**Images:**
- JPEG, PNG, WebP
- Maximum size: 10MB
- Recommended resolution: 224x224 or higher

**Voice:**
- MP3, WAV, M4A
- Maximum duration: 60 seconds
- Supported languages: Spanish (primary), English

### 🔒 Security Considerations

- File type validation
- File size limits
- Virus scanning for uploaded files
- Secure file storage and cleanup
- Privacy protection for medical images

---

**Ready to start?** Comment below to claim this issue and let us know your approach! 