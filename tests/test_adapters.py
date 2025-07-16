# tests/test_adapters.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.providers.adapters.gemini_adapter import GeminiAdapter
from src.providers.adapters.openai_adapter import OpenAIAdapter
from src.providers.adapters.deepseek_adapter import DeepSeekAdapter
from src.providers.adapters.local_adapter import LocalAdapter
from src.models.schemas import Message
from src.core.config import Settings

class TestBaseAdapter:
    """Tests para el BaseLLMAdapter."""
    
    def test_base_adapter_initialization(self):
        """Test que el base adapter se inicializa correctamente."""
        settings = Settings()
        adapter = BaseLLMAdapter(settings)
        assert adapter.settings == settings
    
    def test_analyze_context(self):
        """Test del análisis de contexto."""
        settings = Settings()
        adapter = BaseLLMAdapter(settings)
        
        # Crear contexto de prueba
        context = [
            Message(role="user", content="Mi hijo tiene 2 años y tiene fiebre"),
            Message(role="assistant", content="¿Cuál es la temperatura?"),
            Message(role="user", content="39 grados")
        ]
        
        context_info = adapter._analyze_context(context)
        
        assert context_info['has_age'] == True
        assert context_info['age'] == "2"
        assert context_info['has_symptom'] == True
        assert context_info['symptom'] == "fiebre"
        assert context_info['message_count'] == 3

class TestGeminiAdapter:
    """Tests para el GeminiAdapter."""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_gemini_adapter_initialization(self, mock_model, mock_configure):
        """Test que el GeminiAdapter se inicializa correctamente."""
        settings = Settings(gemini_api_key="test_key")
        adapter = GeminiAdapter(settings)
        
        assert adapter.settings == settings
        mock_configure.assert_called_once_with(api_key="test_key")
        mock_model.assert_called_once_with('gemini-2.0-flash')
    
    def test_gemini_adapter_missing_api_key(self):
        """Test que falla cuando falta la API key."""
        settings = Settings(gemini_api_key=None)
        
        with pytest.raises(ValueError, match="Gemini API key is required"):
            GeminiAdapter(settings)

class TestOpenAIAdapter:
    """Tests para el OpenAIAdapter."""
    
    @patch('openai.api_key')
    def test_openai_adapter_initialization(self, mock_api_key):
        """Test que el OpenAIAdapter se inicializa correctamente."""
        settings = Settings(openai_api_key="test_key")
        adapter = OpenAIAdapter(settings)
        
        assert adapter.settings == settings
        assert adapter.model == "gpt-4o-mini"
    
    def test_openai_adapter_missing_api_key(self):
        """Test que falla cuando falta la API key."""
        settings = Settings(openai_api_key=None)
        
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OpenAIAdapter(settings)

class TestDeepSeekAdapter:
    """Tests para el DeepSeekAdapter."""
    
    def test_deepseek_adapter_initialization(self):
        """Test que el DeepSeekAdapter se inicializa correctamente."""
        settings = Settings(deepseek_api_key="test_key")
        adapter = DeepSeekAdapter(settings)
        
        assert adapter.settings == settings
        assert adapter.model == "deepseek-chat"
        assert adapter.api_key == "test_key"
    
    def test_deepseek_adapter_missing_api_key(self):
        """Test que falla cuando falta la API key."""
        settings = Settings(deepseek_api_key=None)
        
        with pytest.raises(ValueError, match="DeepSeek API key is required"):
            DeepSeekAdapter(settings)

class TestLocalAdapter:
    """Tests para el LocalAdapter."""
    
    @patch('torch.device')
    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('transformers.AutoModelForCausalLM.from_pretrained')
    def test_local_adapter_initialization(self, mock_model, mock_tokenizer, mock_device):
        """Test que el LocalAdapter se inicializa correctamente."""
        settings = Settings(llm_model="test-model")
        
        # Mock del dispositivo
        mock_device.return_value = "cpu"
        
        # Mock del tokenizer y modelo
        mock_tokenizer.return_value = Mock()
        mock_model.return_value = Mock()
        
        adapter = LocalAdapter(settings)
        
        assert adapter.settings == settings
        assert adapter.model_name == "test-model"

class TestFactory:
    """Tests para el factory de LLM."""
    
    def test_get_available_providers(self):
        """Test que retorna los proveedores disponibles."""
        from src.providers.factory import get_available_providers
        
        providers = get_available_providers()
        expected_providers = ["gemini", "openai", "deepseek", "local"]
        
        for provider in expected_providers:
            assert provider in providers
    
    def test_register_provider(self):
        """Test que se puede registrar un nuevo proveedor."""
        from src.providers.factory import register_provider, get_available_providers
        
        # Crear un adapter de prueba
        class TestAdapter(BaseLLMAdapter):
            def _format_messages_for_provider(self, context, system_prompt):
                return []
            
            async def _call_provider(self, formatted_messages):
                return "test response"
        
        # Registrar el adapter de prueba
        register_provider("test", TestAdapter)
        
        providers = get_available_providers()
        assert "test" in providers 