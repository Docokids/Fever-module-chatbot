import google.generativeai as genai
from typing import List, Dict, Any
from src.models.schemas import Message
from src.providers.interface import LLMClient
from src.core.config import get_settings, Settings
from src.core.prompts import MedicalPrompts, ConversationPhase
import logging
import re

logger = logging.getLogger(__name__)

class GeminiClient(LLMClient):
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        logger.info(f"Initializing GeminiClient with settings: {self.settings}")
        logger.info(f"Gemini API Key present: {'Yes' if self.settings.gemini_api_key else 'No'}")
        logger.info(f"API Key length: {len(self.settings.gemini_api_key) if self.settings.gemini_api_key else 0}")
        
        if not self.settings.gemini_api_key:
            logger.error("Gemini API key is missing")
            raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY environment variable or provide it in conversation settings.")
        
        try:
            genai.configure(api_key=self.settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            raise

    async def generate(self, context: List[Message]) -> Message:
        try:
            # Verificar si hay síntomas de emergencia en el último mensaje del usuario
            if context and context[-1].role == "user":
                safety_alert = MedicalPrompts.get_safety_check(context[-1].content)
                if safety_alert:
                    return Message(
                        role="assistant",
                        content=f"🚨 {safety_alert}\n\nPor favor, busca atención médica inmediata. Esta información no reemplaza la consulta médica profesional."
                    )

            # Generar el prompt contextual basado en el historial
            conversation_history = [
                {"role": msg.role, "content": msg.content} 
                for msg in context
            ]
            
            # Determinar la fase de la conversación
            phase = MedicalPrompts._determine_phase(conversation_history)
            logger.info(f"Conversation phase: {phase.value}")
            
            # Analizar el contexto para determinar qué información ya tenemos
            context_info = self._analyze_conversation_context(conversation_history)
            
            # Generar el prompt contextual con la fase específica
            system_prompt = MedicalPrompts.get_contextual_prompt(conversation_history, phase)
            
            # Agregar instrucciones específicas para control de preguntas
            if phase in [ConversationPhase.INITIAL, ConversationPhase.DISCOVERY]:
                system_prompt += "\n\nCONTROL DE PREGUNTAS:\n"
                system_prompt += "- DEBES hacer SOLO UNA pregunta en tu respuesta\n"
                system_prompt += "- NO hagas múltiples preguntas\n"
                system_prompt += "- NO hagas listas de preguntas\n"
                system_prompt += "- Tu respuesta debe terminar con una sola pregunta\n"
                
                # Agregar la pregunta específica que debe hacer
                specific_question = MedicalPrompts.get_specific_question_for_phase(phase, context_info)
                system_prompt += f"- DEBES hacer esta pregunta específica: '{specific_question}'\n"
                system_prompt += f"- Ejemplo de respuesta correcta: 'Hola, soy el pediatra de DocoKids. {specific_question}'\n"
            
            # Crear el mensaje del sistema
            system_message = {
                "role": "user",
                "parts": [system_prompt]
            }
            
            # Crear el historial de mensajes para Gemini
            messages = [system_message]
            
            # Agregar el historial de la conversación
            for msg in context:
                messages.append({
                    "role": msg.role,
                    "parts": [msg.content]
                })
            
            # Generar la respuesta usando el modelo
            response = self.model.generate_content(messages)
            
            # Extraer el texto de la respuesta
            response_text = response.text
            
            # Validar y corregir la respuesta para asegurar que tenga la pregunta correcta
            if phase in [ConversationPhase.INITIAL, ConversationPhase.DISCOVERY]:
                response_text = self._force_specific_question(response_text, phase, context_info)
            
            # Asegurar que la respuesta sea apropiada para el contexto médico
            if not response_text.strip():
                if phase == ConversationPhase.INITIAL:
                    response_text = "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?"
                else:
                    specific_question = MedicalPrompts.get_specific_question_for_phase(phase, context_info)
                    response_text = f"Entiendo tu preocupación. {specific_question}"
            
            logger.info(f"Generated response for phase {phase.value}: {response_text[:100]}...")
            
            return Message(
                role="assistant",
                content=response_text
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Respuesta de fallback
            return Message(
                role="assistant",
                content="Disculpa, estoy teniendo dificultades técnicas. Por favor, consulta directamente con un pediatra para obtener la mejor atención para tu hijo."
            )

    def _analyze_conversation_context(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza el historial de conversación para extraer información clave"""
        context_info = {
            'has_age': False,
            'has_symptom': False,
            'symptom': None,
            'age': None
        }
        
        user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
        
        for msg in user_messages:
            content = msg.get('content', '').lower()
            
            # Detectar edad
            age_patterns = [
                r'(\d+)\s*(años?|meses?|mes|año)',
                r'edad\s*(?:del\s*nino|es)\s*(\d+)',
                r'(\d+)\s*(?:años?|meses?)'
            ]
            
            for pattern in age_patterns:
                match = re.search(pattern, content)
                if match:
                    context_info['has_age'] = True
                    context_info['age'] = match.group(1)
                    break
            
            # Detectar síntomas
            symptoms = {
                'fiebre': ['fiebre', 'temperatura', 'caliente', 'febril'],
                'tos': ['tos', 'tose', 'tosiendo'],
                'dolor': ['dolor', 'duele', 'molestia'],
                'vómitos': ['vómito', 'vomita', 'vomitar'],
                'diarrea': ['diarrea', 'caca', 'heces'],
                'garganta': ['garganta', 'dolor de garganta'],
                'oído': ['oído', 'oreja', 'dolor de oído']
            }
            
            for symptom, keywords in symptoms.items():
                if any(keyword in content for keyword in keywords):
                    context_info['has_symptom'] = True
                    context_info['symptom'] = symptom
                    break
        
        return context_info

    def _force_specific_question(self, response_text: str, phase: ConversationPhase, context_info: Dict[str, Any]) -> str:
        """Fuerza que la respuesta contenga la pregunta específica correcta"""
        
        # Obtener la pregunta específica que debe hacer
        specific_question = MedicalPrompts.get_specific_question_for_phase(phase, context_info)
        
        # Si es la fase inicial, forzar la pregunta de edad
        if phase == ConversationPhase.INITIAL:
            if "edad" not in response_text.lower() or "?" not in response_text:
                return f"Hola, soy el pediatra de DocoKids. {specific_question}"
        
        # Verificar si la respuesta ya contiene la pregunta correcta
        if specific_question.lower() in response_text.lower():
            # La pregunta está presente, solo validar que sea una sola
            return self._validate_single_question(response_text, phase)
        
        # Si no contiene la pregunta correcta, reemplazar o agregar
        if phase == ConversationPhase.INITIAL:
            return f"Hola, soy el pediatra de DocoKids. {specific_question}"
        else:
            # Para otras fases, intentar mantener el contexto pero agregar la pregunta correcta
            lines = response_text.split('\n')
            # Eliminar líneas que contengan preguntas incorrectas
            cleaned_lines = []
            for line in lines:
                if '?' not in line or specific_question.lower() in line.lower():
                    cleaned_lines.append(line)
            
            # Agregar la pregunta correcta al final
            if not any('?' in line for line in cleaned_lines):
                cleaned_lines.append(specific_question)
            
            return '\n'.join(cleaned_lines)

    def _validate_single_question(self, response_text: str, phase: ConversationPhase) -> str:
        """Valida y corrige la respuesta para asegurar que tenga solo una pregunta"""
        
        # Contar signos de interrogación
        question_marks = response_text.count('?')
        
        if question_marks == 0:
            # No hay preguntas, agregar una
            if phase == ConversationPhase.INITIAL:
                return response_text + "\n\n¿Cuál es la edad del niño?"
            else:
                return response_text + "\n\n¿Podrías contarme más sobre los síntomas?"
        
        elif question_marks == 1:
            # Perfecto, una sola pregunta
            return response_text
        
        else:
            # Múltiples preguntas, simplificar
            logger.warning(f"Multiple questions detected in response: {response_text}")
            
            # Encontrar la primera pregunta y eliminar las demás
            lines = response_text.split('\n')
            cleaned_lines = []
            question_found = False
            
            for line in lines:
                if '?' in line and not question_found:
                    cleaned_lines.append(line)
                    question_found = True
                elif '?' not in line:
                    cleaned_lines.append(line)
            
            # Si no encontramos preguntas válidas, agregar una
            if not question_found:
                if phase == ConversationPhase.INITIAL:
                    cleaned_lines.append("¿Cuál es la edad del niño?")
                else:
                    cleaned_lines.append("¿Podrías contarme más sobre los síntomas?")
            
            return '\n'.join(cleaned_lines) 