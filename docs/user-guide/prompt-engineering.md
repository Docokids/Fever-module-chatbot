# 🧠 Prompt Engineering System

## Overview

The DocoKids Pediatric Chatbot implements an advanced **prompt engineering system** designed to simulate real pediatric consultations. This system ensures that the AI behaves like an experienced pediatrician, conducting structured conversations that gather information progressively while maintaining medical safety standards.

## 🎯 Objectives

- **Simulate Real Medical Consultations**: Mimic the natural flow of pediatric appointments
- **Ensure Patient Safety**: Detect emergency situations and provide appropriate guidance
- **Maintain Conversation Quality**: One question per response for focused interactions
- **Provide Educational Value**: Offer guidance while avoiding definitive diagnoses
- **Adapt to Context**: Tailor questions based on information already provided

## 🏗️ Architecture

### Core Components

```
src/core/prompts.py
├── MedicalPrompts Class
├── ConversationPhase Enum
├── System Prompts
├── Discovery Questions
├── Safety Checks
└── Context Analysis
```

### Conversation Flow Control

```
src/providers/gemini_client.py
├── Phase Detection
├── Context Analysis
├── Question Validation
├── Response Correction
└── Safety Monitoring
```

## 📋 Conversation Phases

### 1. INITIAL Phase
**Purpose**: Establish basic patient information
**Trigger**: First interaction in a conversation
**Behavior**: 
- Introduces as "pediatra de DocoKids"
- Asks for child's age specifically
- No other questions allowed

**Example**:
```
Bot: "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?"
```

### 2. DISCOVERY Phase
**Purpose**: Explore symptoms and gather basic information
**Trigger**: After age is provided, before detailed assessment
**Behavior**:
- One question per response
- Focuses on main symptom identification
- Avoids multiple questions

**Example**:
```
Bot: "¿Cuál es el síntoma principal que te preocupa?"
User: "Fiebre"
Bot: "¿Cuál es la temperatura del niño?"
```

### 3. ASSESSMENT Phase
**Purpose**: Detailed evaluation of symptoms
**Trigger**: After basic symptom information is gathered
**Behavior**:
- Asks about intensity, duration, and behavior
- Explores related symptoms
- Maintains one-question format

**Example**:
```
Bot: "¿Cuánto tiempo lleva con fiebre?"
User: "Un día"
Bot: "¿Ha tenido algún otro síntoma además de la fiebre?"
```

### 4. GUIDANCE Phase
**Purpose**: Provide educational guidance and recommendations
**Trigger**: Sufficient information has been gathered
**Behavior**:
- Offers educational content
- Provides safety recommendations
- Suggests when to consult a doctor

**Example**:
```
Bot: "Basado en la información que me has proporcionado, 
la fiebre de 39°C en un niño de 1 año requiere observación. 
Te recomiendo consultar con un pediatra si..."
```

## 🔧 Implementation Details

### Phase Detection Logic

```python
def _determine_phase(conversation_history):
    user_messages = [msg for msg in history if msg.get('role') == 'user']
    
    if len(user_messages) == 0:
        return ConversationPhase.INITIAL
    elif len(user_messages) <= 2:
        return ConversationPhase.DISCOVERY
    elif len(user_messages) <= 5:
        return ConversationPhase.ASSESSMENT
    else:
        return ConversationPhase.GUIDANCE
```

### Context Analysis

The system analyzes conversation history to extract key information:

```python
context_info = {
    'has_age': False,
    'has_symptom': False,
    'symptom': None,
    'age': None
}
```

**Detection Patterns**:
- **Age**: `(\d+)\s*(años?|meses?|mes|año)`
- **Symptoms**: Predefined keywords for fever, cough, pain, vomiting, etc.

### Question Validation

The system ensures responses contain exactly one question:

```python
def _validate_single_question(response_text, phase):
    question_marks = response_text.count('?')
    
    if question_marks == 0:
        # Add appropriate question
    elif question_marks == 1:
        # Perfect
    else:
        # Remove extra questions
```

## 🚨 Safety System

### Emergency Detection

The system automatically detects emergency keywords:

```python
emergency_keywords = {
    'dificultad para respirar': 'URGENTE: Busca atención médica inmediata',
    'no responde': 'URGENTE: Busca atención médica inmediata',
    'muy somnoliento': 'URGENTE: Busca atención médica inmediata',
    'convulsión': 'URGENTE: Busca atención médica inmediata',
    'fiebre 40': 'URGENTE: Si es un bebé menor de 3 meses, consulta inmediatamente'
}
```

### Safety Response

When emergency keywords are detected:

```
🚨 URGENTE: Busca atención médica inmediata

Por favor, busca atención médica inmediata. 
Esta información no reemplaza la consulta médica profesional.
```

## 📝 Prompt Templates

### System Prompt Structure

```python
SYSTEM_PROMPT = """
Eres un pediatra experto y empático que trabaja en DocoKids.

DIRECTRICES PRINCIPALES:
1. ACTÚA COMO UN PEDIATRA REAL
2. NO DAR DIAGNÓSTICOS DEFINITIVOS
3. SIEMPRE RECOMIENDA CONSULTAR CON UN MÉDICO
4. USA LENGUAJE CLARO Y EMPÁTICO
5. HAZ UNA PREGUNTA A LA VEZ
6. CONSTRUYE SOBRE LA INFORMACIÓN PREVIA

LÍMITES IMPORTANTES:
- NO prescribir medicamentos específicos
- NO hacer diagnósticos definitivos
- NO reemplazar la consulta médica profesional
- SIEMPRE priorizar la seguridad del niño
"""
```

### Phase-Specific Instructions

Each phase has specific instructions added to the system prompt:

**INITIAL Phase**:
```
- Esta es la primera interacción. DEBES hacer UNA pregunta específica.
- Pregunta EXACTAMENTE: '¿Cuál es la edad del niño?'
- NO hagas preguntas generales como '¿cuál es el motivo?'
```

**DISCOVERY Phase**:
```
- Estás en fase de descubrimiento. Haz UNA pregunta específica.
- Si ya sabes la edad pero no el síntoma: '¿Cuál es el síntoma principal que te preocupa?'
- NO hagas preguntas generales o vagas.
```

## 🔄 Conversation Flow Examples

### Complete Example

```
Phase: INITIAL
Bot: "Hola, soy el pediatra de DocoKids. ¿Cuál es la edad del niño?"
User: "1 año"

Phase: DISCOVERY
Bot: "¿Cuál es el síntoma principal que te preocupa?"
User: "Fiebre"
Bot: "¿Cuál es la temperatura del niño?"
User: "39°C"

Phase: ASSESSMENT
Bot: "¿Cuánto tiempo lleva con fiebre?"
User: "Un día"
Bot: "¿Ha tenido algún otro síntoma además de la fiebre?"
User: "No, solo fiebre"

Phase: GUIDANCE
Bot: "Basado en la información proporcionada, la fiebre de 39°C 
en un niño de 1 año requiere observación. Te recomiendo..."
```

### Emergency Detection Example

```
User: "Mi hijo tiene dificultad para respirar"
Bot: "🚨 URGENTE: Busca atención médica inmediata

Por favor, busca atención médica inmediata. 
Esta información no reemplaza la consulta médica profesional."
```

## 🛠️ Configuration

### Environment Variables

```bash
LLM_PROVIDER=gemini  # or openai
GEMINI_API_KEY=your_api_key
OPENAI_API_KEY=your_api_key
```

### Customization

To modify the prompt engineering system:

1. **Add New Phases**: Extend `ConversationPhase` enum
2. **Modify Questions**: Update `DISCOVERY_QUESTIONS` or `SYMPTOM_SPECIFIC_QUESTIONS`
3. **Add Safety Keywords**: Extend `emergency_keywords` dictionary
4. **Change Phase Logic**: Modify `_determine_phase` function

## 🧪 Testing

### Unit Tests

```bash
# Test prompt generation
pytest tests/test_prompts.py

# Test conversation flow
pytest tests/test_conversation_flow.py

# Test safety detection
pytest tests/test_safety_checks.py
```

### Integration Tests

```bash
# Test complete conversation flow
pytest tests/integration/test_full_conversation.py
```

## 📊 Monitoring

### Logging

The system provides detailed logging for debugging:

```python
logger.info(f"Conversation phase: {phase.value}")
logger.info(f"Generated response for phase {phase.value}: {response_text[:100]}...")
logger.warning(f"Multiple questions detected in response: {response_text}")
```

### Metrics

Track conversation quality metrics:
- Phase transition frequency
- Question validation success rate
- Emergency detection accuracy
- Response time per phase

## 🔮 Future Enhancements

### Planned Features

1. **Multi-language Support**: Extend prompts for different languages
2. **Symptom-Specific Flows**: Specialized conversation paths for different conditions
3. **Age-Appropriate Questions**: Tailor questions based on child's age
4. **Cultural Sensitivity**: Adapt prompts for different cultural contexts
5. **Learning System**: Improve prompts based on conversation outcomes

### Research Areas

- **Conversation Quality Metrics**: Develop better ways to measure conversation effectiveness
- **Prompt Optimization**: A/B testing for different prompt variations
- **Safety Enhancement**: Improve emergency detection algorithms
- **Personalization**: Adapt prompts based on user history and preferences

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Medical AI Ethics Guidelines](https://www.who.int/health-topics/artificial-intelligence)
- [Pediatric Assessment Guidelines](https://www.aap.org/)

## 🤝 Contributing

To contribute to the prompt engineering system:

1. Review the current implementation in `src/core/prompts.py`
2. Test your changes thoroughly
3. Update this documentation
4. Submit a pull request with detailed description

For questions or suggestions, please open an issue in the repository. 