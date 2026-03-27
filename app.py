import streamlit as st
import uuid
from datetime import datetime
import os
import json
import re

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="وكيلك الشخصي - الخدمات الحكومية",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ملف الذاكرة ====================
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

# ==================== فهم النية (Intent Recognition) ====================
def recognize_intent(text):
    """فهم نية المستخدم"""
    text_lower = text.lower()
    
    intents = {
        "tax": ["ضريبة", "ضرائب", "tax", "taxes", "إقرار", "declaration"],
        "license": ["رخصة", "license", "قيادة", "driving", "سيارة", "car"],
        "health": ["صحي", "health", "مستشفى", "hospital", "مركز صحي", "clinic", "دواء", "medicine"],
        "education": ["مدرسة", "school", "تعليم", "education", "جامعة", "university", "منحة", "scholarship"],
        "passport": ["جواز", "passport", "سفر", "travel", "تأشيرة", "visa"],
        "water": ["ماء", "water", "مياه", "صنبور", "tap"],
        "electricity": ["كهرباء", "electricity", "ضوء", "light", "فاتورة", "bill"],
        "help": ["مساعدة", "help", "ماذا تفعل", "what can you do", "قدراتك", "capabilities"]
    }
    
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent
    
    return "unknown"

# ==================== تنفيذ الإجراءات ====================
def execute_action(intent, user_data, user_input):
    """تنفيذ الإجراء المناسب للنية"""
    
    if intent == "tax":
        return f"""
📊 **معلومات الضرائب**

📅 آخر موعد لتقديم الإقرار الضريبي: 31 مارس 2026
💰 المبلغ المقدر: 1,250,000 UGX
📞 للاستفسار: 0800-100-100 (URA)

هل تريد مني أن أذكرك قبل الموعد بـ 7 أيام؟
"""
    
    elif intent == "license":
        return f"""
🚗 **معلومات الرخصة**

📅 رخصتك سارية حتى: 15 مايو 2026
⏳ متبقي 49 يوماً
📞 للاستفسار: 0800-100-200 (وزارة النقل)

هل تريد مني أن أذكرك قبل انتهاء الرخصة بـ 14 يوماً؟
"""
    
    elif intent == "health":
        location = user_data.get("location", "كيرياندونغو")
        return f"""
🏥 **معلومات صحية**

📍 أقرب مركز صحي في {location}: Kiryandongo Health Centre IV
📞 0774-123-456
🕒 8:00 صباحاً - 5:00 مساءً

💊 هل تحتاج مساعدة في العثور على صيدلية قريبة؟
"""
    
    elif intent == "education":
        return f"""
📚 **معلومات تعليمية**

🏫 مدارس قريبة: Kiryandongo Primary School, Kiryandongo Secondary School
📖 برامج المنح: متاح منح للطلاب المتفوقين
📞 وزارة التعليم: 0800-100-300

هل تبحث عن مدرسة معينة أو منحة دراسية؟
"""
    
    elif intent == "passport":
        return f"""
🛂 **معلومات جواز السفر**

📍 أقرب مكتب: Immigration Office, Kampala
📞 للاستفسار: 0800-100-400
📋 المستندات المطلوبة: بطاقة هوية، شهادة ميلاد، صورتان
💰 الرسوم: 250,000 UGX (عادي)، 500,000 UGX (مستعجل)

هل تريد مني أن أجهز قائمة المستندات؟
"""
    
    elif intent == "water":
        return f"""
💧 **معلومات المياه**

📞 شركة المياه: 0800-100-500
📍 أقرب مكتب: NWSC Kiryandongo
💰 فاتورة مقدرة: 25,000 - 50,000 UGX شهرياً

هل تواجه مشكلة في انقطاع المياه؟
"""
    
    elif intent == "electricity":
        return f"""
⚡ **معلومات الكهرباء**

📞 شركة الكهرباء: 0800-100-600
📍 أقرب مكتب: UMEME Kiryandongo
💰 فاتورة مقدرة: 30,000 - 80,000 UGX شهرياً

هل تريد الاستعلام عن فاتورتك؟
"""
    
    elif intent == "help":
        return """
🤖 **أنا وكيلك الشخصي. أستطيع مساعدتك في:**

📊 **الضرائب** – مواعيد الإقرار، المبالغ المقدرة
🚗 **الرخص** – صلاحية رخصتك، مواعيد التجديد
🏥 **الصحة** – أقرب مراكز صحية، معلومات صيدليات
📚 **التعليم** – مدارس، منح دراسية
🛂 **جواز السفر** – المستندات المطلوبة، الرسوم
💧 **المياه** – فواتير، أعطال
⚡ **الكهرباء** – فواتير، انقطاعات

فقط أخبرني ماذا تريد. مثلاً: "أريد الاستعلام عن الضرائب" أو "أين أقرب مستشفى؟"
"""
    
    else:
        return """
🤔 لم أفهم طلبك. هل يمكنك التوضيح؟

أستطيع مساعدتك في:
- الضرائب
- الرخص
- الصحة
- التعليم
- جواز السفر
- المياه
- الكهرباء

جرب أن تقول: "أريد الاستعلام عن الضرائب" أو "أين أقرب مستشفى؟"
"""

# ==================== تهيئة الجلسة ====================
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

# الحصول على بيانات المستخدم
user_data = st.session_state.memory.get(st.session_state.user_id, {})

# ==================== تصميم الصفحة ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-message {
        background: #667eea;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background: #f0f2f6;
        color: #1e3c72;
        margin-right: auto;
    }
    .sidebar-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== تسجيل المستخدم ====================
if not user_data.get("name"):
    st.markdown(f"""
    <div class='main-header'>
        <h1>🤖 وكيلك الشخصي</h1>
        <p>أنا هنا لمساعدتك في الخدمات الحكومية. فقط تحدث معي.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("registration"):
        st.markdown("### 📝 لنبدأ بالتعارف")
        name = st.text_input("ما اسمك؟")
        phone = st.text_input("رقم هاتفك (للإشعارات)")
        location = st.selectbox("أين تسكن؟", ["Kiryandongo", "Masindi", "Gulu", "Kampala", "أخرى"])
        
        if st.form_submit_button("ابدأ"):
            if name:
                st.session_state.memory[st.session_state.user_id] = {
                    "name": name,
                    "phone": phone,
                    "location": location,
                    "registered_at": datetime.now().isoformat(),
                    "history": []
                }
                save_memory(st.session_state.memory)
                st.rerun()
            else:
                st.warning("الرجاء إدخال اسمك")

else:
    # ==================== الشريط الجانبي ====================
    with st.sidebar:
        st.markdown(f"""
        <div class='sidebar-card'>
            <h3>👤 {user_data.get('name', 'زائر')}</h3>
            <p>📞 {user_data.get('phone', 'غير مسجل')}</p>
            <p>📍 {user_data.get('location', 'غير محدد')}</p>
            <p>🆔 {st.session_state.user_id}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🧠 ذاكرتي")
        history_count = len(user_data.get("history", []))
        st.caption(f"أتذكر {history_count} تفاعل")
        
        if history_count > 0:
            with st.expander("آخر التفاعلات"):
                for h in user_data.get("history", [])[-3:]:
                    st.caption(f"📝 {h.get('user', '')[:30]}...")
        
        st.markdown("---")
        st.markdown("### 💡 ماذا أستطيع أن أفعل؟")
        st.markdown("""
        - 📊 **الضرائب**: مواعيد الإقرار
        - 🚗 **الرخص**: صلاحية رخصتك
        - 🏥 **الصحة**: أقرب مراكز صحية
        - 📚 **التعليم**: مدارس ومنح
        - 🛂 **جواز السفر**: المستندات المطلوبة
        - 💧 **المياه**: فواتير وأعطال
        - ⚡ **الكهرباء**: فواتير وانقطاعات
        """)
        
        st.markdown("---")
        st.markdown("### 📞 للطوارئ")
        st.markdown("""
        🚑 الإسعاف: 911  
        👮 الشرطة: 999  
        🔥 الإطفاء: 112
        """)
    
    # ==================== المحادثة الرئيسية ====================
    st.markdown(f"""
    <div class='main-header'>
        <h1>🤖 وكيلك الشخصي</h1>
        <p>مرحباً {user_data.get('name', 'صديقي')}! كيف يمكنني مساعدتك اليوم؟</p>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض المحادثة السابقة
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class='chat-message user-message'>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message assistant-message'>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # إدخال المستخدم
    user_input = st.chat_input("اكتب طلبك هنا...")
    
    if user_input:
        # إضافة رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f"""
        <div class='chat-message user-message'>
            {user_input}
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("🤖 أفكر..."):
            # 1. فهم النية
            intent = recognize_intent(user_input)
            
            # 2. تنفيذ الإجراء
            response = execute_action(intent, user_data, user_input)
            
            # 3. تسجيل التفاعل في الذاكرة
            if "history" not in user_data:
                user_data["history"] = []
            
            user_data["history"].append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input[:100],
                "intent": intent
            })
            
            # الاحتفاظ بآخر 50 تفاعل فقط
            if len(user_data["history"]) > 50:
                user_data["history"] = user_data["history"][-50:]
            
            st.session_state.memory[st.session_state.user_id] = user_data
            save_memory(st.session_state.memory)
            
            # 4. عرض رد الوكيل
            st.markdown(f"""
            <div class='chat-message assistant-message'>
                {response}
            </div>
            """, unsafe_allow_html=True)
            
            # 5. حفظ الرد في المحادثة
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # إعادة تشغيل الصفحة لتحديث الشريط الجانبي
        st.rerun()
