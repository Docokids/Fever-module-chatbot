# src/providers/adapters/local_adapter.py
from typing import List, Any, Dict, Optional
from src.models.schemas import Message
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.core.config import get_settings, Settings
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class LocalAdapter(BaseLLMAdapter):
    """
    Adapter para modelos locales usando transformers.
    Soporta modelos como OLMo, Llama, etc. que se ejecutan localmente.
    """
    
    def __init__(self, settings: Settings | None = None):
        super().__init__(settings or get_settings())
        self._initialize_local_model()
        self._executor = ThreadPoolExecutor(max_workers=1)  # Para ejecutar en thread separado
    
    def _initialize_local_model(self):
        """Inicializa el modelo local."""
        self.logger.info(f"Initializing LocalAdapter with settings: {self.settings}")
        
        try:
            # Configurar dispositivo
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.logger.info(f"Using device: {self.device}")
            
            # Modelo por defecto si no se especifica
            model_name = self.settings.llm_model or "allenai/OLMo-2-1124-13B-Instruct"
            
            self.logger.info(f"Loading model: {model_name}")
            
            # Cargar tokenizer y modelo
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
                device_map=None  # Usamos to(device) en lugar de device_map
            ).to(self.device)
            
            self.model.eval()
            self.logger.info("Local model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing local model: {str(e)}")
            raise
    
    def _format_messages_for_provider(self, context: List[Message], system_prompt: str) -> str:
        """
        Formatea los mensajes para el formato específico del modelo local.
        
        Args:
            context: Lista de mensajes de la conversación
            system_prompt: Prompt del sistema
            
        Returns:
            Prompt formateado como string
        """
        # Construir prompt en formato de texto plano
        prompt = system_prompt.strip() + "\n\n"
        
        # Agregar historial de conversación
        for msg in context:
            if msg.role == "user":
                prompt += f"Usuario: {msg.content}\n"
            elif msg.role == "assistant":
                prompt += f"Asistente: {msg.content}\n"
        
        # Agregar prompt para la respuesta del asistente
        prompt += "Asistente: "
        
        return prompt
    
    async def _call_provider(self, formatted_prompt: str) -> str:
        """
        Llama al modelo local para generar la respuesta.
        
        Args:
            formatted_prompt: Prompt formateado
            
        Returns:
            Texto de la respuesta generada
        """
        try:
            # Ejecutar en thread separado para no bloquear el event loop
            loop = asyncio.get_event_loop()
            response_text = await loop.run_in_executor(
                self._executor,
                self._generate_text,
                formatted_prompt
            )
            
            self.logger.info(f"Local model response generated: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error calling local model: {str(e)}")
            raise
    
    def _generate_text(self, prompt: str) -> str:
        """
        Genera texto usando el modelo local (ejecutado en thread separado).
        
        Args:
            prompt: Prompt completo
            
        Returns:
            Texto generado
        """
        try:
            # Tokenizar el prompt
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            # Generar respuesta
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=300,
                    do_sample=True,
                    temperature=self.settings.llm_temperature,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.eos_token_id,
                    early_stopping=True
                )
            
            # Decodificar la respuesta
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            return generated_text.strip()
            
        except Exception as e:
            self.logger.error(f"Error in text generation: {str(e)}")
            raise
    
    def __del__(self):
        """Cleanup del executor al destruir el objeto."""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False) 