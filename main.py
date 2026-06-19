from io import BytesIO
import requests
import streamlit as st
from huggingface_hub import InferenceClient
import config

from groq import generate_response

MATH_SYSTEM = """You are a Math Mastermind.
Solve with clear step-by-step reasoning, correct notation, and a final answer.
Verify when possible; mention an alternative method briefly if relevant."""

CHAT_CSS = """
<style>
.history-wrap {max-height: 420px; overflow-y: auto; padding-right: 6px;}
.qa-card{border: 1px solid #e6e6e6;background: #ffffff;border-radius: 10px;padding: 14px 16px;margin: 10px 0;box-shadow: 0 1px 2px rgba(0,0,0,0.04);}.q{font-weight: 700; color: #0a6ebd; margin-bottom: 8px;}
.a{white-space: pre-wrap; color: #333; line-height: 1.5;}</style>
"""

def export_txt(history):
    txt = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history,1)])
    bio  = io.ByetesIO(txt.encode("utf-8")); bio.seek(0); return bio 

def teaching_answer(q: str) -> str:
    return generate_response(q, temperature=0.3, max_tokens=1024)

def math_answer(q: str, level: str) -> str:
    prompt = f"{MATH_SYSTEM}\n\nDifficulty: {level}\nMath problem: {q}"
    return generate_response{prompt, temperature = 0.1, max_tokens = 1024}

def run_ai_teaching_assitant():
    st.title("Ai teaching assistant")
    st.session_state.setdefault("history_ata", [])
    c1, c2 = st.columns([1,2])
    if c1.button("Clear", key="c_ata"): st.session_state.history_ata = []; st.rerun()
    if st.session_state.history_ata:
        c2.download_button("Export", export_txt(st.session_state.history_ata), "Ai_teaching assitant_conversation.txt", "text/plain")
    
    q = st.text_input("Enter your question:", key= "q_ata")
    if st.button("Ask", key = "a_ata"):
        if not q.strip(): st.warning("enter a question")
        else:
            with st.spinner("Thinking"):
                st.session_state.history_ata.append({"question": q.strip(),"answer": teaching_answer(q.strip())})
            st.rerun()
    
    if not st.session_state.history_ata: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_ata, 1):
        html += f'<div class="card"><div class= "q">Q{i}: {qa["question"]}</div><div class= "a">{qa["answer"]}</div></div'
        st.markdown(html+ "<\div>", unsafe_allow_html=True)

def run_math_mastermind():
    st.title("Math Mastermind")
    st.session_state.setdefault("history_mm", [])
    st.session_state.setdefault("k_mm", 0)
    c1, c2 = st.columns([1, 2])
    if c1.button("🧹 Clear", key="c_mm"): st.session_state.history_mm = []; st.rerun()
    if st.session_state.history_mm:
        c2.download_button("Export", export_txt(st.session_state.history_mm),
                           "Math_Mastermind_Solutions.txt", "text/plain")
    with st.form("mm_form", clear_on_submit=True):
        q = st.text_area("Math problem:", height=100, key=f"mm_{st.session_state.k_mm}")
        a, b = st.columns([3, 1])
        go = a.form_submit_button("Solve", use_container_width=True)
        lvl = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
        if go:
            if not q.strip(): st.warning("⚠️ Enter a problem.")
            else:
                with st.spinner("Solving..."):
                    ans = math_answer(q.strip(), lvl)
                st.session_state.history_mm.insert(0, {"question": q.strip(), "answer": ans, "difficulty": lvl})
                st.session_state.k_mm += 1; st.rerun()

    if not st.session_state.history_mm: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_mm, 1):
        html += (f'<div class="card"><div class="q">Q{i}: {qa["question"]}'
                 f'<span class="meta">{qa["difficulty"]}</span></div>'
                 f'<div class="a">{qa["answer"]}</div></div>')
    st.markdown(html + "</div>", unsafe_allow_html=True)