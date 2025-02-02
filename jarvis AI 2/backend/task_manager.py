import asyncio
import json
from typing import Dict, Any, Callable
from datetime import datetime, timedelta
import logging

class SmartTaskManager:
    def __init__(self):
        self.tasks = {}
        self.recurring_tasks = {}
        self.task_history = []
        self.logger = logging.getLogger('TaskManager')
    
    async def create_task(
        self, 
        name: str, 
        function: Callable, 
        schedule: Dict[str, Any] = None
    ):
        """
        Create a sophisticated task with advanced scheduling
        """
        task_id = f"{name}_{datetime.now().timestamp()}"
        
        task_config = {
            'id': task_id,
            'name': name,
            'function': function,
            'created_at': datetime.now(),
            'schedule': schedule or {},
            'status': 'pending',
            'attempts': 0,
            'max_attempts': 3
        }
        
        self.tasks[task_id] = task_config
        
        if schedule:
            await self._schedule_task(task_id, schedule)
        
        return task_id
    
    async def _schedule_task(self, task_id: str, schedule: Dict[str, Any]):
        """
        Advanced task scheduling with multiple strategies
        """
        if 'interval' in schedule:
            await self._schedule_interval_task(task_id, schedule)
        elif 'cron' in schedule:
            await self._schedule_cron_task(task_id, schedule)
        elif 'datetime' in schedule:
            await self._schedule_datetime_task(task_id, schedule)
    
    async def _schedule_interval_task(self, task_id: str, schedule: Dict[str, Any]):
        """
        Schedule tasks with interval-based repetition
        """
        interval = schedule.get('interval', timedelta(hours=1))
        
        while True:
            task = self.tasks[task_id]
            try:
                await task['function']()
                task['status'] = 'completed'
                task['attempts'] += 1
                self.task_history.append(task)
            except Exception as e:
                task['status'] = 'failed'
                self.logger.error(f"Task {task_id} failed: {e}")
                
                if task['attempts'] >= task['max_attempts']:
                    break
            
            await asyncio.sleep(interval.total_seconds())
    
    async def _schedule_cron_task(self, task_id: str, schedule: Dict[str, Any]):
        """
        Implement cron-like scheduling
        """
        # Placeholder for advanced cron scheduling
        pass
    
    async def _schedule_datetime_task(self, task_id: str, schedule: Dict[str, Any]):
        """
        Schedule task at a specific datetime
        """
        target_time = schedule.get('datetime')
        
        # Wait until target time
        delay = (target_time - datetime.now()).total_seconds()
        await asyncio.sleep(max(delay, 0))
        
        task = self.tasks[task_id]
        await task['function']()
    
    def list_tasks(self, status: str = None) -> list:
        """
        List tasks with optional status filtering
        """
        if status:
            return [
                task for task in self.tasks.values() 
                if task['status'] == status
            ]
        return list(self.tasks.values())
    
    def get_task_history(self, limit: int = 50) -> list:
        """
        Retrieve recent task execution history
        """
        return self.task_history[-limit:]
    
    async def cancel_task(self, task_id: str):
        """
        Cancel a specific task
        """
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'cancelled'
            del self.tasks[task_id]
    
    def export_task_config(self, task_id: str) -> str:
        """
        Export task configuration as JSON
        """
        task = self.tasks.get(task_id)
        if task:
            return json.dumps({
                'name': task['name'],
                'created_at': str(task['created_at']),
                'schedule': task['schedule']
            })
        return None

# Singleton task manager
task_manager = SmartTaskManager()
