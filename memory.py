
```python
import json
import os
from datetime import datetime

class AgentMemory:
    """ذاكرة الوكيل – يتذكر المستخدم وتفاعلاته"""
    
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self):
        """تحميل الذاكرة من الملف"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_memory(self):
        """حفظ الذاكرة في الملف"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def get_user(self, user_id):
        """الحصول على بيانات مستخدم معين"""
        return self.memory.get(user_id, {})
    
    def update_user(self, user_id, data):
        """تحديث بيانات مستخدم"""
        if user_id not in self.memory:
            self.memory[user_id] = {}
        
        self.memory[user_id].update(data)
        self.memory[user_id]["last_interaction"] = datetime.now().isoformat()
        self._save_memory()
    
    def add_interaction(self, user_id, user_input, agent_response, intent):
        """تسجيل تفاعل جديد"""
        if user_id not in self.memory:
            self.memory[user_id] = {}
        
        if "history" not in self.memory[user_id]:
            self.memory[user_id]["history"] = []
        
        self.memory[user_id]["history"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": agent_response,
            "intent": intent
        })
        
        # الاحتفاظ فقط بآخر 50 تفاعل
        if len(self.memory[user_id]["history"]) > 50:
            self.memory[user_id]["history"] = self.memory[user_id]["history"][-50:]
        
        self._save_memory()
    
    def get_history(self, user_id, limit=10):
        """الحصول على آخر التفاعلات"""
        user = self.get_user(user_id)
        history = user.get("history", [])
        return history[-limit:]
    
    def remember_preference(self, user_id, key, value):
        """تذكر تفضيل المستخدم"""
        user = self.get_user(user_id)
        if "preferences" not in user:
            user["preferences"] = {}
        user["preferences"][key] = value
        self.update_user(user_id, user)
```
