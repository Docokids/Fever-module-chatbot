# src/providers/adapters/base_adapter.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.models.schemas import Message
from src.core.prompts import MedicalPrompts, ConversationPhase
import logging

logger = logging.getLogger(__name__)

class BaseLLMAdapter(ABC):
    """
    Base adapter que proporciona funcionalidad común para todos los LLM providers.
    Implementa el patrón Template Method para estandarizar el flujo de generación.
    """
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def generate(self, context: List[Message]) -> Message:
        """
        Template method que define el flujo estándar de generación de respuestas.
        """
        try:
            # 1. Safety check
            safety_response = self._check_safety(context)
            if safety_response:
                return safety_response
            
            # 2. Analyze context
            context_info = self._analyze_context(context)
            
            # 3. Determine conversation phase
            phase = self._determine_phase(context)
            self.logger.info(f"Conversation phase: {phase.value}")
            
            # 4. Generate system prompt
            system_prompt = self._generate_system_prompt(context, phase, context_info)
            
            # 5. Format messages for provider
            formatted_messages = self._format_messages_for_provider(context, system_prompt)
            
            # 6. Call provider-specific generation
            raw_response = await self._call_provider(formatted_messages)
            
            # 7. Validate and post-process response
            final_response = self._validate_and_post_process(raw_response, phase, context_info)
            
            return Message(
                role="assistant",
                content=final_response
            )
            
        except Exception as e:
            self.logger.error(f"Error in generate method: {str(e)}")
            return self._get_fallback_response()
    
    def _check_safety(self, context: List[Message]) -> Optional[Message]:
        """Verifica si hay síntomas de emergencia en el último mensaje del usuario."""
        if context and context[-1].role == "user":
            safety_alert = MedicalPrompts.get_safety_check(context[-1].content)
            if safety_alert:
                return Message(
                    role="assistant",
                    content=f"🚨 {safety_alert}\n\nPor favor, busca atención médica inmediata. Esta información no reemplaza la consulta médica profesional."
                )
        return None
    
    def _analyze_context(self, context: List[Message]) -> Dict[str, Any]:
        """Analiza el contexto de la conversación para extraer información clave."""
        context_info = {
            'has_age': False,
            'has_symptom': False,
            'symptom': None,
            'age': None,
            'message_count': len(context),
            'user_messages': [msg for msg in context if msg.role == "user"]
        }
        
        # Análisis básico del contexto
        for msg in context_info['user_messages']:
            content = msg.content.lower()
            
            # Detectar edad (patrones básicos)
            import re
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
            
            # Detectar síntomas básicos
            symptoms = {
                'fiebre': ['fiebre', 'temperatura', 'caliente', 'febril'],
                'tos': ['tos', 'tose', 'tosiendo'],
                'dolor': ['dolor', 'duele', 'molestia'],
                'vómitos': ['vómito', 'vomita', 'vomitar'],
                'diarrea': ['diarrea', 'caca', 'heces']
            }
            
            for symptom, keywords in symptoms.items():
                if any(keyword in content for keyword in keywords):
                    context_info['has_symptom'] = True
                    context_info['symptom'] = symptom
                    break
        
        return context_info
    
    def _determine_phase(self, context: List[Message]) -> ConversationPhase:
        """Determina la fase actual de la conversación."""
        conversation_history = [
            {"role": msg.role, "content": msg.content} 
            for msg in context
        ]
        return MedicalPrompts._determine_phase(conversation_history)
    
    def _generate_system_prompt(self, context: List[Message], phase: ConversationPhase, context_info: Dict[str, Any]) -> str:
        """Genera el prompt del sistema basado en la fase y contexto."""
        conversation_history = [
            {"role": msg.role, "content": msg.content} 
            for msg in context
        ]
        
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
        
        return system_prompt
    
    @abstractmethod
    def _format_messages_for_provider(self, context: List[Message], system_prompt: str) -> Any:
        """Formatea los mensajes para el proveedor específico. Debe ser implementado por cada adapter."""
        pass
    
    @abstractmethod
    async def _call_provider(self, formatted_messages: Any) -> str:
        """Llama al proveedor específico. Debe ser implementado por cada adapter."""
        pass
    
    def _validate_and_post_process(self, raw_response: str, phase: ConversationPhase, context_info: Dict[str, Any]) -> str:
        """Valida y post-procesa la respuesta del LLM."""
        response_text = raw_response.strip()
        
        # Validar y corregir la respuesta para asegurar que tenga la pregunta correcta
        if phase in [ConversationPhase.INITIAL, ConversationPhase.DISCOVERY]:
            response_text = self._force_specific_question(response_text, phase, context_info)
        
        # Asegurar que la respuesta sea apropiada para el contexto médico
        if not response_text:
            if phase == ConversationPhase.INITIAL:
                response_text = "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?"
            else:
                specific_question = MedicalPrompts.get_specific_question_for_phase(phase, context_info)
                response_text = f"Entiendo tu preocupación. {specific_question}"
        
        return response_text
    
    def _force_specific_question(self, response_text: str, phase: ConversationPhase, context_info: Dict[str, Any]) -> str:
        """Fuerza que la respuesta contenga la pregunta específica correcta."""
        specific_question = MedicalPrompts.get_specific_question_for_phase(phase, context_info)
        
        # Si es la fase inicial, forzar la pregunta de edad
        if phase == ConversationPhase.INITIAL:
            if "edad" not in response_text.lower() or "?" not in response_text:
                return f"Hola, soy el pediatra de DocoKids. {specific_question}"
        
        # Verificar si la respuesta ya contiene la pregunta correcta
        if specific_question.lower() in response_text.lower():
            return self._validate_single_question(response_text, phase)
        
        # Si no contiene la pregunta correcta, reemplazar o agregar
        if phase == ConversationPhase.INITIAL:
            return f"Hola, soy el pediatra de DocoKids. {specific_question}"
        else:
            lines = response_text.split('\n')
            cleaned_lines = []
            for line in lines:
                if '?' not in line or specific_question.lower() in line.lower():
                    cleaned_lines.append(line)
            
            if not any('?' in line for line in cleaned_lines):
                cleaned_lines.append(specific_question)
            
            return '\n'.join(cleaned_lines)
    
    def _validate_single_question(self, response_text: str, phase: ConversationPhase) -> str:
        """Valida y corrige la respuesta para asegurar que tenga solo una pregunta."""
        question_marks = response_text.count('?')
        
        if question_marks == 0:
            if phase == ConversationPhase.INITIAL:
                return response_text + "\n\n¿Cuál es la edad del niño?"
            else:
                return response_text + "\n\n¿Podrías contarme más sobre los síntomas?"
        
        elif question_marks == 1:
            return response_text
        
        else:
            self.logger.warning(f"Multiple questions detected in response: {response_text}")
            
            lines = response_text.split('\n')
            cleaned_lines = []
            question_found = False
            
            for line in lines:
                if '?' in line and not question_found:
                    cleaned_lines.append(line)
                    question_found = True
                elif '?' not in line:
                    cleaned_lines.append(line)
            
            if not question_found:
                if phase == ConversationPhase.INITIAL:
                    cleaned_lines.append("¿Cuál es la edad del niño?")
                else:
                    cleaned_lines.append("¿Podrías contarme más sobre los síntomas?")
            
            return '\n'.join(cleaned_lines)
    
    def _get_fallback_response(self) -> Message:
        """Proporciona una respuesta de fallback en caso de error."""
        return Message(
            role="assistant",
            content="Disculpa, estoy teniendo dificultades técnicas. Por favor, consulta directamente con un pediatra para obtener la mejor atención para tu hijo."
        ) 