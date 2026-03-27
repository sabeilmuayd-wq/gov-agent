
```python
import requests
from datetime import datetime, timedelta

class AgentActions:
    """الإجراءات التي يمكن للوكيل تنفيذها"""
    
    def __init__(self, memory):
        self.memory = memory
    
    def get_tax_info(self, user_id, user_input):
        """الحصول على معلومات الضرائب"""
        user = self.memory.get_user(user_id)
        name = user.get("name", "المواطن")
        
        # بيانات محاكاة – يمكن ربطها بـ URA API لاحقاً
        tax_deadline = datetime(2026, 3, 31)
        days_left = (tax_deadline - datetime.now()).days
        
        response = f"📅 آخر موعد لتقديم الإقرار الضريبي: {tax_deadline.strftime('%d %B %Y')}\n"
        if days_left > 0:
            response += f"⏳ متبقي {days_left} يوماً\n"
        else:
            response += f"⚠️ انتهى الموعد! يرجى التواصل مع URA\n"
        
        response += f"💰 المبلغ المقدر: 1,250,000 UGX\n"
        response += f"📞 للاستفسار: 0800-100-100 (URA)\n\n"
        response += f"هل تريد مني أن أذكرك قبل الموعد بـ 7 أيام؟"
        
        return response
    
    def get_license_info(self, user_id, user_input):
        """الحصول على معلومات الرخصة"""
        user = self.memory.get_user(user_id)
        name = user.get("name", "المواطن")
        
        # بيانات محاكاة
        expiry_date = datetime(2026, 5, 15)
        days_left = (expiry_date - datetime.now()).days
        
        response = f"🚗 رخصتك سارية حتى: {expiry_date.strftime('%d %B %Y')}\n"
        if days_left > 0:
            response += f"⏳ متبقي {days_left} يوماً\n"
            if days_left < 30:
                response += f"⚠️ يفضل التجديد قريباً\n"
        else:
            response += f"❌ رخصتك منتهية! يرجى التجديد فوراً\n"
        
        response += f"📞 للاستفسار: 0800-100-200 (وزارة النقل)\n\n"
        response += f"هل تريد مني أن أذكرك قبل انتهاء الرخصة بـ 14 يوماً؟"
        
        return response
    
    def get_health_info(self, user_id, user_input):
        """الحصول على معلومات صحية"""
        user = self.memory.get_user(user_id)
        location = user.get("location", "Kiryandongo")
        
        # بيانات محاكاة – يمكن ربطها بخرائط Google لاحقاً
        response = f"🏥 أقرب مركز صحي في {location}:\n"
        response += f"📍 Kiryandongo Health Centre IV\n"
        response += f"📞 0774-123-456\n"
        response += f"🕒 8:00 صباحاً - 5:00 مساءً (ما عدا الجمعة)\n\n"
        
        if "مرض" in user_input or "sick" in user_input or "دواء" in user_input:
            response += f"💊 هل تحتاج مساعدة في العثور على صيدلية قريبة؟"
        
        return response
    
    def get_education_info(self, user_id, user_input):
        """الحصول على معلومات تعليمية"""
        user = self.memory.get_user(user_id)
        
        response = f"📚 معلومات تعليمية:\n"
        response += f"🏫 مدارس قريبة: Kiryandongo Primary School, Kiryandongo Secondary School\n"
        response += f"📖 برامج المنح: متاح منح للطلاب المتفوقين\n"
        response += f"📞 وزارة التعليم: 0800-100-300\n\n"
        response += f"هل تبحث عن مدرسة معينة أو منحة دراسية؟"
        
        return response
    
    def get_passport_info(self, user_id, user_input):
        """الحصول على معلومات جواز السفر"""
        response = f"🛂 معلومات جواز السفر:\n"
        response += f"📍 أقرب مكتب: Immigration Office, Kampala\n"
        response += f"📞 للاستفسار: 0800-100-400\n"
        response += f"📋 المستندات المطلوبة: بطاقة هوية، شهادة ميلاد، صورتان\n"
        response += f"💰 الرسوم: 250,000 UGX (عادي)، 500,000 UGX (مستعجل)\n\n"
        response += f"هل تريد مني أن أجهز قائمة المستندات؟"
        
        return response
    
    def get_water_info(self, user_id, user_input):
        """الحصول على معلومات المياه"""
        response = f"💧 معلومات المياه:\n"
        response += f"📞 شركة المياه: 0800-100-500\n"
        response += f"📍 أقرب مكتب: NWSC Kiryandongo\n"
        response += f"💰 فاتورة مقدرة: 25,000 - 50,000 UGX شهرياً\n\n"
        response += f"هل تواجه مشكلة في انقطاع المياه؟"
        
        return response
    
    def get_electricity_info(self, user_id, user_input):
        """الحصول على معلومات الكهرباء"""
        response = f"⚡ معلومات الكهرباء:\n"
        response += f"📞 شركة الكهرباء: 0800-100-600\n"
        response += f"📍 أقرب مكتب: UMEME Kiryandongo\n"
        response += f"💰 فاتورة مقدرة: 30,000 - 80,000 UGX شهرياً\n\n"
        response += f"هل تريد الاستعلام عن فاتورتك؟"
        
        return response
    
    def show_help(self, user_id, user_input):
        """عرض المساعدة"""
        response = f"🤖 أنا وكيلك الشخصي. أستطيع مساعدتك في:\n\n"
        response += f"📊 **الضرائب** – مواعيد الإقرار، المبالغ المقدرة\n"
        response += f"🚗 **الرخص** – صلاحية رخصتك، مواعيد التجديد\n"
        response += f"🏥 **الصحة** – أقرب مراكز صحية، معلومات صيدليات\n"
        response += f"📚 **التعليم** – مدارس، منح دراسية\n"
        response += f"🛂 **جواز السفر** – المستندات المطلوبة، الرسوم\n"
        response += f"💧 **المياه** – فواتير، أعطال\n"
        response += f"⚡ **الكهرباء** – فواتير، انقطاعات\n\n"
        response += f"فقط أخبرني ماذا تريد. مثلاً: 'أريد الاستعلام عن الضرائب' أو 'أين أقرب مستشفى؟'"
        
        return response
    
    def execute(self, intent, user_id, user_input):
        """تنفيذ الإجراء المناسب للنية"""
        actions = {
            "tax": self.get_tax_info,
            "license": self.get_license_info,
            "health": self.get_health_info,
            "education": self.get_education_info,
            "passport": self.get_passport_info,
            "water": self.get_water_info,
            "electricity": self.get_electricity_info,
            "help": self.show_help
        }
        
        action = actions.get(intent, self.show_help)
        return action(user_id, user_input)
```
