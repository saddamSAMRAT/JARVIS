import spacy
import numpy as np
import torch
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from typing import Dict, Any, List

class AdvancedNLPEngine:
    def __init__(self):
        # Load advanced NLP models
        self.nlp = spacy.load('en_core_web_lg')
        
        # Question Answering Model
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained('deepset/roberta-base-squad2')
        self.qa_tokenizer = AutoTokenizer.from_pretrained('deepset/roberta-base-squad2')
        
        # Sentiment Analysis
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        
        # Named Entity Recognition
        self.ner_model = pipeline('ner')
        
        # Context Management
        self.context_memory = {}
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text
        """
        doc = self.nlp(text)
        return [
            {
                'text': ent.text,
                'label': ent.label_
            } for ent in doc.ents
        ]
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Perform sentiment analysis on text
        """
        result = self.sentiment_analyzer(text)[0]
        return {
            'sentiment': result['label'],
            'confidence': result['score']
        }
    
    def answer_question(self, context: str, question: str) -> str:
        """
        Answer questions based on given context
        """
        inputs = self.qa_tokenizer(question, context, return_tensors='pt')
        outputs = self.qa_model(**inputs)
        
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        
        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits)
        
        answer_tokens = inputs['input_ids'][0][start_index:end_index+1]
        answer = self.qa_tokenizer.decode(answer_tokens)
        
        return answer
    
    def update_context_memory(self, key: str, value: Any):
        """
        Store and manage contextual information
        """
        self.context_memory[key] = {
            'value': value,
            'timestamp': np.datetime64('now')
        }
    
    def retrieve_context(self, key: str, max_age_minutes: int = 60) -> Any:
        """
        Retrieve context with age validation
        """
        if key not in self.context_memory:
            return None
        
        current_time = np.datetime64('now')
        memory_time = self.context_memory[key]['timestamp']
        
        # Check if memory is within max age
        if (current_time - memory_time) / np.timedelta64(1, 'm') > max_age_minutes:
            del self.context_memory[key]
            return None
        
        return self.context_memory[key]['value']
    
    def intent_classification(self, text: str) -> Dict[str, float]:
        """
        Classify user intent with confidence scores
        """
        intents = {
            'task_automation': 0.0,
            'information_retrieval': 0.0,
            'system_control': 0.0,
            'general_conversation': 0.0
        }
        
        # Basic intent classification using spaCy
        doc = self.nlp(text.lower())
        
        # Rule-based intent detection
        if any(token.text in ['automate', 'schedule', 'run'] for token in doc):
            intents['task_automation'] = 0.8
        
        if any(token.text in ['what', 'who', 'when', 'where', 'why', 'how'] for token in doc):
            intents['information_retrieval'] = 0.7
        
        if any(token.text in ['open', 'close', 'start', 'stop', 'restart'] for token in doc):
            intents['system_control'] = 0.6
        
        # Default to general conversation if no strong intent detected
        if all(score == 0.0 for score in intents.values()):
            intents['general_conversation'] = 1.0
        
        return intents

# Singleton instance for global use
nlp_engine = AdvancedNLPEngine()
