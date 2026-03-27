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

# ==================== فهم النية (Intent Recognition) – موسع ====================
def recognize_intent(text):
    """فهم نية المستخدم – يدخل كل ما قد يقوله المستخدم"""
    text_lower = text.lower()
    
    # نوايا موسعة مع كل الكلمات الممكنة
    intents = {
        "tax": [
            "ضريبة", "ضرائب", "tax", "taxes", "إقرار", "declaration", 
            "الضرائب", "ضريبة الدخل", "income tax", "ضريبة القيمة", "VAT"
        ],
        "license": [
            "رخصة", "license", "قيادة", "driving", "سيارة", "car", 
            "الرخصة", "رخصة قيادة", "رخصة السيارة", "تجديد رخصة"
        ],
        "health": [
            "صحي", "health", "مستشفى", "hospital", "مركز صحي", "clinic", 
            "دواء", "medicine", "الصحة", "مستوصف", "علاج", "طبيب", 
            "doctor", "عيادة", "اسعاف", "emergency", "مستشفى قريب",
            "أقرب مستشفى", "مستشفى", "مركز صحي قريب"
        ],
        "education": [
            "مدرسة", "school", "تعليم", "education", "جامعة", "university", 
            "منحة", "scholarship", "المدارس", "الدراسة", "طلاب", "معلم"
        ],
        "passport": [
            "جواز", "passport", "سفر", "travel", "تأشيرة", "visa", 
            "جواز سفر", "السفر", "السفارة", "embassy"
        ],
        "water": [
            "ماء", "water", "مياه", "صنبور", "tap", "الماء", "المياه", 
            "NWSC", "فواتير الماء"
        ],
        "electricity": [
            "كهرباء", "electricity", "ضوء", "light", "فاتورة", "bill", 
            "التيار", "النهار", "UMEME", "فواتير الكهرباء"
        ],
        "help": [
            "مساعدة", "help", "ماذا تفعل", "what can you do", "قدراتك", 
            "capabilities", "ممكن", "تساعدني", "كيف", "what can"
        ]
    }
    
    # البحث في كل النوايا
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent
    
    return "unknown"

# ==================== تنفيذ الإجراءات – مع إجابات مفصلة ====================
def execute_action(intent, user_data, user_input):
    """تنفيذ الإجراء المناسب للنية"""
    location = user_data.get("location", "كيرياندونغو")
    name = user_data.get("name", "صديقي")
    
    if intent == "tax":
        return f"""
📊 **معلومات الضرائب**

مرحباً {name}، إليك معلومات الضرائب:

📅 آخر موعد لتقديم الإقرار الضريبي: **31 مارس 2026**
💰 المبلغ المقدر (للفرد): 1,250,000 UGX
📞 للاستفسار: 0800-100-100 (URA)

هل تريد مني أن أذكرك قبل الموعد بـ 7 أيام؟
"""
    
    elif intent == "license":
        return f"""
🚗 **معلومات الرخصة**

مرحباً {name}، إليك معلومات رخصتك:

📅 رخصتك سارية حتى: **15 مايو 2026**
⏳ متبقي 49 يوماً
📞 للاستفسار: 0800-100-200 (وزارة النقل)

هل تريد مني أن أذكرك قبل انتهاء الرخصة بـ 14 يوماً؟
"""
    
    elif intent == "health":
        return f"""
🏥 **معلومات صحية – {location}**

مرحباً {name}، إليك أقرب المراكز الصحية في منطقتك:

📍 **كيرياندونغو (Kiryandongo)**
- Kiryandongo Health Centre IV
- العنوان: بالقرب من السوق المركزي
- 📞 0774-123-456
- 🕒 8:00 صباحاً - 5:00 مساءً (ما عدا الجمعة)

📍 **بويالي (Bweyale)**
- Bweyale Health Centre III
- 🕒 24 ساعة للطوارئ

💊 **صيدليات قريبة:**
- Kiryandongo Pharmacy (بجانب المستشفى) – 0774-789-012
- Bweyale Drug Store – 0774-345-678

🚑 **للطوارئ:** اتصل 911

هل تريد معلومات عن مستشفى آخر أو صيدلية؟
"""
    
    elif intent == "education":
        return f"""
📚 **معلومات تعليمية – {location}**

مرحباً {name}، إليك معلومات المدارس في منطقتك:

🏫 **مدارس قريبة:**
- Kiryandongo Primary School (صفوف 1-7)
- Kiryandongo Secondary School (ثانوي)
- Bweyale Primary School
- Bweyale Secondary School

📖 **برامج المنح:**
- منحة الحكومة للطلاب المتفوقين
- منحة منظمة اليونيسف للأطفال المحتاجين

📞 **وزارة التعليم:**
- 0800-100-300

هل تبحث عن مدرسة معينة أو منحة دراسية محددة؟
"""
    
    elif intent == "passport":
        return f"""
🛂 **معلومات جواز السفر**

مرحباً {name}، إليك خطوات استخراج جواز السفر:

📍 **أقرب مكتب:** Immigration Office, Kampala
📞 للاستفسار: 0800-100-400

📋 **المستندات المطلوبة:**
- بطاقة هوية سارية (NIN)
- شهادة ميلاد أصلية
- صورتان شخصيتان حديثتان (خلفية بيضاء)
- إيصال الدفع

💰 **الرسوم:**
- عادي (3 أسابيع): 250,000 UGX
- مستعجل (أسبوع): 500,000 UGX

هل تريد مني أن أجهز قائمة المستندات كاملة؟
"""
    
    elif intent == "water":
        return f"""
💧 **معلومات المياه – {location}**

مرحباً {name}، إليك معلومات المياه في منطقتك:

📞 **شركة المياه:** NWSC (National Water and Sewerage Corporation)
- الخط الساخن: 0800-100-500

📍 **أقرب مكتب خدمة:**
- NWSC Kiryandongo
- العنوان: بجانب البريد المركزي

💰 **فاتورة مقدرة:**
- منزل عادي: 25,000 - 50,000 UGX شهرياً
- تجاري: حسب الاستهلاك

🚰 **لإبلاغ عطل:**
- اتصل 0800-100-500 أو أرسل رسالة "WATER" إلى 6789

هل تواجه مشكلة في انقطاع المياه حالياً؟
"""
    
    elif intent == "electricity":
        return f"""
⚡ **معلومات الكهرباء – {location}**

مرحباً {name}، إليك معلومات الكهرباء في منطقتك:

📞 **شركة الكهرباء:** UMEME
- الخط الساخن: 0800-100-600
- خدمة العملاء: 0312-200-200

📍 **أقرب مكتب خدمة:**
- UMEME Kiryandongo
- العنوان: بجانب السوق

💰 **فاتورة مقدرة:**
- منزل عادي: 30,000 - 80,000 UGX شهرياً
- حسب الاستهلاك

⚡ **للاستعلام عن فاتورتك:**
- أرسل رسالة "BILL" إلى 6789

🔌 **لإبلاغ عطل:**
- اتصل 0800-100-600 أو أرسل "POWER" إلى 6789

هل تريد الاستعلام عن فاتورتك الحالية؟
"""
    
    elif intent == "help":
        return f"""
🤖 **مرحباً {name}! أنا وكيلك الشخصي.**

أستطيع مساعدتك في هذه الخدمات:

📊 **الضرائب**
- مواعيد تقديم الإقرار الضريبي
- المبالغ المقدرة
- جهات الاتصال

🚗 **الرخص**
- صلاحية رخصتك
- مواعيد التجديد
- الرسوم المطلوبة

🏥 **الصحة**
- أقرب مراكز صحية في {location}
- أرقام الطوارئ
- صيدليات قريبة

📚 **التعليم**
- مدارس في منطقتك
- برامج المنح الدراسية
- جهات الاتصال

🛂 **جواز السفر**
- المستندات المطلوبة
- الرسوم والإجراءات
- أقرب مكتب

💧 **المياه**
- فواتير المياه
- الإبلاغ عن أعطال
- أرقام الاتصال

⚡ **الكهرباء**
- فواتير الكهرباء
- الإبلاغ عن انقطاع
- أرقام الطوارئ

**فقط قل لي ماذا تريد، مثلاً:**
- "أين أقرب مستشفى؟"
- "متى آخر موعد للضرائب؟"
- "كيف أستخرج جواز سفر؟"
- "فاتورة الكهرباء متى تنتهي؟"

كيف يمكنني مساعدتك اليوم؟
"""
    
    else:
        return f"""
🤔 **عذراً {name}، لم أفهم طلبك.**

أستطيع مساعدتك في:
- 📊 **الضرائب** – قل "الضرائب" أو "ضريبة الدخل"
- 🚗 **الرخص** – قل "رخصة" أو "رخصة قيادة"
- 🏥 **الصحة** – قل "مستشفى" أو "أين أقرب مستشفى"
- 📚 **التعليم** – قل "مدرسة" أو "منحة"
- 🛂 **جواز السفر** – قل "جواز" أو "سفر"
- 💧 **المياه** – قل "ماء" أو "فاتورة المياه"
- ⚡ **الكهرباء** – قل "كهرباء" أو "فاتورة"

**جرب أن تقول:**
- "أين أقرب مستشفى؟"
- "متى آخر موعد للضرائب؟"
- "كيف أستخرج جواز سفر؟"

أعد صياغة طلبك وسأحاول مساعدتك.
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
        max-width: 85%;
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
                    st.caption(f"📝 {h.get('user', '')[:40]}...")
        
        st.markdown("---")
        st.markdown("### 💡 ماذا أستطيع أن أفعل؟")
        st.markdown("""
        - 📊 **الضرائب** – قل "الضرائب"
        - 🚗 **الرخص** – قل "رخصة"
        - 🏥 **الصحة** – قل "مستشفى" أو "أين أقرب مستشفى"
        - 📚 **التعليم** – قل "مدرسة"
        - 🛂 **جواز السفر** – قل "جواز"
        - 💧 **المياه** – قل "ماء"
        - ⚡ **الكهرباء** – قل "كهرباء"
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
        <p style='font-size: 0.8rem;'>💡 جرب: "أين أقرب مستشفى؟" أو "متى آخر موعد للضرائب؟"</p>
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
