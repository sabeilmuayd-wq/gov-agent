```python
import streamlit as st
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# استيراد مكونات الوكيل
from intent import IntentRecognizer
from memory import AgentMemory
from actions import AgentActions

# تحميل المتغيرات البيئية
load_dotenv()

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="وكيلك الشخصي - الخدمات الحكومية",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تهيئة الوكيل ====================
if "agent" not in st.session_state:
    st.session_state.agent = {
        "intent_recognizer": IntentRecognizer(),
        "memory": AgentMemory(),
        "actions": None
    }
    st.session_state.agent["actions"] = AgentActions(st.session_state.agent["memory"])

if "user_id" not in st.session_state:
    # إنشاء معرف فريد للمستخدم (يمكن ربطه بالهاتف لاحقاً)
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# ==================== واجهة المستخدم ====================
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
user_data = st.session_state.agent["memory"].get_user(st.session_state.user_id)

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
                st.session_state.agent["memory"].update_user(st.session_state.user_id, {
                    "name": name,
                    "phone": phone,
                    "location": location,
                    "registered_at": datetime.now().isoformat()
                })
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
        st.caption(f"أتذكر {len(user_data.get('history', []))} تفاعل")
        
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
        
        # معالجة الطلب بالوكيل
        with st.spinner("🤖 أفكر..."):
            # 1. فهم النية
            intent, response_text, action_name = st.session_state.agent["intent_recognizer"].recognize(user_input)
            
            # 2. تنفيذ الإجراء
            action_response = st.session_state.agent["actions"].execute(intent, st.session_state.user_id, user_input)
            
            # 3. دمج الردود
            final_response = action_response
            
            # 4. تسجيل التفاعل في الذاكرة
            st.session_state.agent["memory"].add_interaction(
                st.session_state.user_id,
                user_input,
                final_response,
                intent
            )
            
            # 5. عرض رد الوكيل
            st.markdown(f"""
            <div class='chat-message assistant-message'>
                {final_response}
            </div>
            """, unsafe_allow_html=True)
            
            # 6. حفظ الرد في المحادثة
            st.session_state.messages.append({"role": "assistant", "content": final_response})
        
        # إعادة تشغيل الصفحة لتحديث الشريط الجانبي
        st.rerun()
```
