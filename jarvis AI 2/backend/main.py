import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import speech_recognition as sr
import pyttsx3
import openai
import uvicorn
import asyncio
from datetime import timedelta

# Import new advanced modules
from .nlp_engine import nlp_engine
from .task_manager import task_manager
from .task_automation import TaskAutomator
from .config import Config

# Configuration and Environment Setup
openai.api_key = Config.OPENAI_API_KEY

class AIAssistant:
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        
        # Text-to-Speech
        self.engine = pyttsx3.init()
        
        # Task Automation
        self.task_automator = TaskAutomator()
    
    async def process_query(self, query: str) -> str:
        """
        Advanced query processing with intent classification
        """
        # Analyze intent
        intents = nlp_engine.intent_classification(query)
        
        # Determine primary intent
        primary_intent = max(intents, key=intents.get)
        
        # Process based on intent
        if primary_intent == 'task_automation':
            return await self.handle_task_automation(query)
        
        elif primary_intent == 'information_retrieval':
            return await self.handle_information_query(query)
        
        elif primary_intent == 'system_control':
            return await self.handle_system_control(query)
        
        else:
            return await self.handle_general_conversation(query)
    
    async def handle_task_automation(self, query: str) -> str:
        """
        Handle task automation requests
        """
        # Extract task details using NLP
        entities = nlp_engine.extract_entities(query)
        
        # Create and schedule task
        async def example_task():
            print(f"Executing automated task for: {query}")
        
        task_id = await task_manager.create_task(
            name="user_requested_task",
            function=example_task,
            schedule={'interval': timedelta(hours=1)}
        )
        
        return f"Task created with ID: {task_id}"
    
    async def handle_information_query(self, query: str) -> str:
        """
        Handle information retrieval queries
        """
        # Use OpenAI for complex queries
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    
    async def handle_system_control(self, query: str) -> str:
        """
        Handle system control commands
        """
        # Implement system control logic
        return "System control command processed"
    
    async def handle_general_conversation(self, query: str) -> str:
        """
        Handle general conversation
        """
        # Sentiment analysis
        sentiment = nlp_engine.analyze_sentiment(query)
        
        # Generate conversational response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Respond with {sentiment['sentiment']} tone"},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content

# FastAPI Application
app = FastAPI()
assistant = AIAssistant()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await assistant.process_query(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("WebSocket disconnected")

# Background task for periodic system checks
@app.on_event("startup")
async def startup_event():
    async def system_health_check():
        # Implement system health monitoring
        print("Performing periodic system health check")
    
    await task_manager.create_task(
        name="system_health_check",
        function=system_health_check,
        schedule={'interval': timedelta(hours=1)}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
