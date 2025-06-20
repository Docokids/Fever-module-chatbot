# src/core/prompts.py
from typing import List, Dict, Any
from enum import Enum

class ConversationPhase(Enum):
    INITIAL = "initial"
    DISCOVERY = "discovery"
    ASSESSMENT = "assessment"
    GUIDANCE = "guidance"

class MedicalPrompts:
    """Clase que contiene todos los prompts y directrices para el chatbot médico pediátrico"""
    
    SYSTEM_PROMPT = """Eres un pediatra experto y empático que trabaja en DocoKids. Tu objetivo es ayudar a los padres a entender mejor la situación de salud de sus hijos a través de una conversación natural y educativa.

DIRECTRICES PRINCIPALES:
1. ACTÚA COMO UN PEDIATRA REAL: Haz preguntas de descubrimiento una por una, como lo harías en una consulta real
2. NO DAR DIAGNÓSTICOS DEFINITIVOS: Solo proporciona información educativa y orientación general
3. SIEMPRE RECOMIENDA CONSULTAR CON UN MÉDICO: Para cualquier síntoma preocupante
4. USA LENGUAJE CLARO Y EMPÁTICO: Adaptado a padres preocupados
5. HAZ UNA PREGUNTA A LA VEZ: No bombardees con múltiples preguntas
6. CONSTRUYE SOBRE LA INFORMACIÓN PREVIA: Usa lo que ya sabes del niño

LÍMITES IMPORTANTES:
- NO prescribir medicamentos específicos
- NO hacer diagnósticos definitivos
- NO reemplazar la consulta médica profesional
- SIEMPRE priorizar la seguridad del niño"""

    # Preguntas estructuradas por fase de descubrimiento
    DISCOVERY_QUESTIONS = {
        "basic_info": [
            "¿Cuál es la edad del niño?",
            "¿Cuál es el síntoma principal que te preocupa?",
            "¿Cuándo comenzó este problema?"
        ],
        "symptom_details": [
            "¿Qué tan intenso es el síntoma? (leve, moderado, severo)",
            "¿El síntoma es constante o va y viene?",
            "¿Hay algo que mejore o empeore el síntoma?",
            "¿El niño tiene otros síntomas además del principal?"
        ],
        "behavior_changes": [
            "¿Cómo se comporta el niño normalmente?",
            "¿Qué cambios has notado en su comportamiento?",
            "¿Está comiendo y durmiendo normalmente?",
            "¿El niño está más irritable o somnoliento de lo usual?"
        ],
        "medical_history": [
            "¿El niño tiene alguna condición médica conocida?",
            "¿Está tomando algún medicamento actualmente?",
            "¿Ha tenido síntomas similares antes?",
            "¿Hay antecedentes familiares relevantes?"
        ]
    }

    # Mapeo de síntomas a preguntas específicas
    SYMPTOM_SPECIFIC_QUESTIONS = {
        "fiebre": [
            "¿Cuál es la temperatura del niño?",
            "¿Cómo se comporta el niño con la fiebre?",
            "¿Ha tomado algún medicamento para la fiebre?",
            "¿La fiebre ha subido o bajado desde que comenzó?"
        ],
        "tos": [
            "¿Qué tipo de tos tiene? (seca, con flema, ronca)",
            "¿Cuándo tose más? (noche, día, al comer)",
            "¿La tos le impide dormir o comer?",
            "¿Hay algún sonido al respirar?"
        ],
        "dolor": [
            "¿Dónde exactamente siente el dolor?",
            "¿Qué tipo de dolor es? (punzante, sordo, cólico)",
            "¿El dolor es constante o intermitente?",
            "¿Hay algo que alivie el dolor?"
        ],
        "vómitos": [
            "¿Cuántas veces ha vomitado?",
            "¿Qué aspecto tiene el vómito?",
            "¿El niño puede retener líquidos?",
            "¿Hay dolor abdominal asociado?"
        ]
    }

    SAFETY_REDIRECTS = [
        "Si el niño tiene dificultad para respirar, busca atención médica inmediata.",
        "Si el niño está muy somnoliento o no responde normalmente, consulta urgentemente.",
        "Si hay signos de deshidratación severa, busca atención médica.",
        "Si la fiebre es muy alta (más de 40°C) en un bebé menor de 3 meses, consulta inmediatamente."
    ]

    @classmethod
    def get_contextual_prompt(cls, conversation_history: List[Dict[str, Any]], phase: ConversationPhase = None) -> str:
        """Genera un prompt contextual basado en el historial de la conversación y la fase actual"""
        
        contextual_prompt = f"{cls.SYSTEM_PROMPT}\n\n"
        
        # Determinar la fase si no se proporciona
        if phase is None:
            phase = cls._determine_phase(conversation_history)
        
        contextual_prompt += f"FASE ACTUAL: {phase.value.upper()}\n\n"
        
        if phase == ConversationPhase.INITIAL:
            contextual_prompt += "INSTRUCCIONES ESPECÍFICAS:\n"
            contextual_prompt += "- Esta es la primera interacción. DEBES hacer UNA pregunta específica.\n"
            contextual_prompt += "- Pregunta EXACTAMENTE: '¿Cuál es la edad del niño?'\n"
            contextual_prompt += "- NO hagas preguntas generales como '¿cuál es el motivo?'\n"
            contextual_prompt += "- NO preguntes sobre síntomas hasta saber la edad.\n"
            contextual_prompt += "- Tu respuesta debe ser: 'Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?'\n"
            
        elif phase == ConversationPhase.DISCOVERY:
            contextual_prompt += "INSTRUCCIONES ESPECÍFICAS:\n"
            contextual_prompt += "- Estás en fase de descubrimiento. Haz UNA pregunta específica.\n"
            contextual_prompt += "- Basa tu pregunta en la información que ya tienes.\n"
            contextual_prompt += "- Si ya sabes la edad pero no el síntoma: '¿Cuál es el síntoma principal que te preocupa?'\n"
            contextual_prompt += "- Si ya sabes edad y síntoma: pregunta sobre detalles específicos del síntoma.\n"
            contextual_prompt += "- NO hagas preguntas generales o vagas.\n"
            
        elif phase == ConversationPhase.ASSESSMENT:
            contextual_prompt += "INSTRUCCIONES ESPECÍFICAS:\n"
            contextual_prompt += "- Ya tienes información básica. Haz una pregunta de evaluación específica.\n"
            contextual_prompt += "- Pregunta sobre intensidad, duración, o comportamiento específico.\n"
            contextual_prompt += "- Mantén el enfoque en UNA pregunta a la vez.\n"
            
        elif phase == ConversationPhase.GUIDANCE:
            contextual_prompt += "INSTRUCCIONES ESPECÍFICAS:\n"
            contextual_prompt += "- Ya tienes suficiente información. Proporciona orientación educativa.\n"
            contextual_prompt += "- Explica qué puede estar pasando y cuándo consultar.\n"
            contextual_prompt += "- Siempre recomienda consultar con un médico si hay preocupación.\n"
        
        contextual_prompt += "\nREGLAS ESTRICTAS:\n"
        contextual_prompt += "- SOLO UNA PREGUNTA por respuesta en fase de descubrimiento\n"
        contextual_prompt += "- Preguntas ESPECÍFICAS, NO generales\n"
        contextual_prompt += "- Lenguaje empático y profesional\n"
        contextual_prompt += "- Siempre priorizar la seguridad del niño\n"
        contextual_prompt += "- Si detectas síntomas de emergencia, responde inmediatamente con alerta de seguridad"
        
        return contextual_prompt

    @classmethod
    def _determine_phase(cls, conversation_history: List[Dict[str, Any]]) -> ConversationPhase:
        """Determina la fase actual de la conversación basada en el historial"""
        if not conversation_history:
            return ConversationPhase.INITIAL
        
        user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
        
        if len(user_messages) == 0:
            return ConversationPhase.INITIAL
        elif len(user_messages) <= 2:
            return ConversationPhase.DISCOVERY
        elif len(user_messages) <= 5:
            return ConversationPhase.ASSESSMENT
        else:
            return ConversationPhase.GUIDANCE

    @classmethod
    def get_specific_question_for_phase(cls, phase: ConversationPhase, context: Dict[str, Any] = None) -> str:
        """Genera una pregunta específica para la fase actual"""
        
        if phase == ConversationPhase.INITIAL:
            return "¿Cuál es la edad del niño?"
        
        elif phase == ConversationPhase.DISCOVERY:
            if context and context.get('has_age') and not context.get('has_symptom'):
                return "¿Cuál es el síntoma principal que te preocupa?"
            elif context and context.get('has_age') and context.get('has_symptom'):
                symptom = context.get('symptom', 'general')
                if symptom in cls.SYMPTOM_SPECIFIC_QUESTIONS:
                    return cls.SYMPTOM_SPECIFIC_QUESTIONS[symptom][0]
                else:
                    return "¿Cuándo comenzó este problema?"
            else:
                return "¿Cuál es la edad del niño?"
        
        elif phase == ConversationPhase.ASSESSMENT:
            return "¿Qué tan intenso es el síntoma? (leve, moderado, severo)"
        
        else:
            return "¿Hay algo más que deba saber sobre la situación?"

    @classmethod
    def get_safety_check(cls, user_message: str) -> str:
        """Verifica si hay síntomas de emergencia en el mensaje del usuario"""
        emergency_keywords = {
            'dificultad para respirar': 'URGENTE: Busca atención médica inmediata',
            'no responde': 'URGENTE: Busca atención médica inmediata',
            'muy somnoliento': 'URGENTE: Busca atención médica inmediata',
            'convulsión': 'URGENTE: Busca atención médica inmediata',
            'deshidratación severa': 'URGENTE: Busca atención médica inmediata',
            'fiebre 40': 'URGENTE: Si es un bebé menor de 3 meses, consulta inmediatamente',
            'sangrado': 'URGENTE: Busca atención médica inmediata',
            'inconsciente': 'URGENTE: Busca atención médica inmediata',
            'paro respiratorio': 'URGENTE: Busca atención médica inmediata'
        }
        
        message_lower = user_message.lower()
        for keyword, response in emergency_keywords.items():
            if keyword in message_lower:
                return response
        
        return None 