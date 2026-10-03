import streamlit as st
from agent import build_agent

from pypdf import PdfReader
from docx import Document
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 18px;
        margin-bottom: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Research Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Ask anything. Upload a file when you want the AI to work with it.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "agent" not in st.session_state:
    st.session_state.agent = build_agent()


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_file_content(uploaded_file):

    filename = uploaded_file.name.lower()

    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    if filename.endswith(".txt"):

        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore",
        )


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    elif filename.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            text = page.extract_text() or ""

            pages.append(
                f"\n--- PAGE {page_number} ---\n"
                f"{text}"
            )

        return "\n".join(pages)


    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    elif filename.endswith(".docx"):

        document = Document(uploaded_file)

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                paragraphs.append(
                    paragraph.text
                )

        return "\n".join(paragraphs)


    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    elif filename.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        return df.to_string(
            index=False
        )


    # --------------------------------------------------------
    # XLSX
    # --------------------------------------------------------

    elif filename.endswith(".xlsx"):

        excel_file = pd.ExcelFile(
            uploaded_file
        )

        output = []

        for sheet in excel_file.sheet_names:

            df = pd.read_excel(
                uploaded_file,
                sheet_name=sheet,
            )

            output.append(
                f"\n--- SHEET: {sheet} ---"
            )

            output.append(
                df.to_string(
                    index=False
                )
            )

            # Reset pointer for next sheet
            uploaded_file.seek(0)

        return "\n".join(output)


    # --------------------------------------------------------
    # Unsupported
    # --------------------------------------------------------

    else:

        return (
            "This file type is not currently "
            "supported for text extraction."
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        # File information
        if message.get("file_name"):

            st.caption(
                f"📎 {message['file_name']}"
            )

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT + FILE UPLOAD
# ============================================================

submission = st.chat_input(
    "Ask anything about your file...",
    accept_file=True,
    file_type=[
        "pdf",
        "txt",
        "docx",
        "csv",
        "xlsx",
    ],
)


# ============================================================
# PROCESS SUBMISSION
# ============================================================

if submission:

    # --------------------------------------------------------
    # Get text
    # --------------------------------------------------------

    prompt = submission.text.strip()


    # --------------------------------------------------------
    # Get uploaded files
    # --------------------------------------------------------

    files = submission.files


    # --------------------------------------------------------
    # No question + no file
    # --------------------------------------------------------

    if not prompt and not files:

        st.stop()


    # --------------------------------------------------------
    # Process file
    # --------------------------------------------------------

    file_context = ""

    file_names = []


    if files:

        for uploaded_file in files:

            file_names.append(
                uploaded_file.name
            )

            try:

                content = extract_file_content(
                    uploaded_file
                )

                file_context += (
                    "\n\n"
                    "================================================\n"
                    f"FILE: {uploaded_file.name}\n"
                    "================================================\n\n"
                    f"{content}\n"
                )

            except Exception as e:

                file_context += (
                    f"\nCould not read "
                    f"{uploaded_file.name}: {str(e)}"
                )


    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    display_prompt = prompt

    if not display_prompt:

        display_prompt = (
            "Please analyze the uploaded file."
        )


    st.session_state.messages.append(
        {
            "role": "user",
            "content": display_prompt,
            "file_name": (
                ", ".join(file_names)
                if file_names
                else None
            ),
        }
    )


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        if file_names:

            st.caption(
                "📎 "
                + ", ".join(file_names)
            )

        st.markdown(
            display_prompt
        )


    # ========================================================
    # AI RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Working..."
        ):

            try:

                # ------------------------------------------------
                # Build prompt
                # ------------------------------------------------

                if file_context:

                    agent_prompt = f"""
You are an intelligent AI assistant that can work
with user-uploaded files.

The user has uploaded the following file(s):

{", ".join(file_names)}

Here is the extracted content:

================ FILE CONTENT ================

{file_context}

============== END FILE CONTENT ==============

USER REQUEST:

{display_prompt}

YOUR JOB:

Understand what the user wants and perform the
requested task using the uploaded file.

The user can ask ANYTHING about the file.

Examples include:

- summarize it
- explain it
- extract information
- find specific information
- analyze it
- compare information
- identify errors
- answer questions
- rewrite content
- transform information
- extract tables
- find names
- find dates
- find emails
- calculate values
- explain specific sections
- provide insights
- answer questions about particular pages
- organize information
- convert information into another format

Do NOT restrict yourself to a predefined list of operations.

Use the uploaded file as the primary source when
the question is about the file.

Do not invent information that is not supported
by the uploaded file.

If the requested information is not present,
clearly say that it could not be found.

If the user asks for analysis or calculations,
perform them when possible.

Answer naturally and directly.
"""

                else:

                    agent_prompt = display_prompt


                # ------------------------------------------------
                # Run agent
                # ------------------------------------------------

                response = (
                    st.session_state.agent.run(
                        agent_prompt
                    )
                )


                answer = response.content


                # ------------------------------------------------
                # Display
                # ------------------------------------------------

                st.markdown(answer)


                # ------------------------------------------------
                # Save
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )


            except Exception as e:

                error_message = (
                    f"❌ Error: {str(e)}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("### 📎 Supported files")

    st.write(
        """
        - PDF
        - TXT
        - DOCX
        - CSV
        - XLSX
        """
    )

    st.divider()

    st.write("### 🤖 Agent")

    st.write(
        """
        Upload a file directly in the
        chat box and ask the AI anything
        about it.
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()
