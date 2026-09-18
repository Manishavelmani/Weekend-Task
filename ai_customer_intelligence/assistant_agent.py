import re
from pathlib import Path
import faiss
import pandas as pd
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_PATH = (
    BASE_DIR
    / "Datasets"
    / "knowledge_base"
    / "knowledge_base_chunks.csv"
)
FAISS_PATH = (
    BASE_DIR
    / "Datasets"
    / "processed"
    / "knowledge_base_faiss.index"
)
LLAMA_PATH = (
    BASE_DIR
    / "models"
    / "llama"
    / "llama-3.2-1b-instruct-q4_k_m.gguf"
)
# ============================================================
# SETTINGS
# ============================================================
TOP_K = 5
# Because the FAISS index contains normalized embeddings,
# the score is cosine similarity.
RELEVANCE_THRESHOLD = 0.35
# ============================================================
# LOAD MODELS AND KNOWLEDGE
# ============================================================
print()
print("=" * 60)
print("INITIALIZING AI CUSTOMER ASSISTANT")
print("=" * 60)
if not KNOWLEDGE_PATH.exists():
    raise FileNotFoundError(f"Knowledge base not found:\n{KNOWLEDGE_PATH}")
knowledge_df = pd.read_csv(KNOWLEDGE_PATH)
required_columns = ["title","category","text"]
for column in required_columns:
    if column not in knowledge_df.columns:
        raise ValueError(f"Knowledge base must contain '{column}' column.")
    knowledge_df[column] = (knowledge_df[column].fillna("").astype(str))
print("Knowledge base loaded:",len(knowledge_df))
if not FAISS_PATH.exists():
    raise FileNotFoundError(f"FAISS index not found:\n{FAISS_PATH}")
faiss_index = faiss.read_index(str(FAISS_PATH))
print("FAISS index loaded:",faiss_index.ntotal)
if faiss_index.ntotal != len(knowledge_df):
    raise ValueError("FAISS index and knowledge-base size do not match.")
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")
if not LLAMA_PATH.exists():
    raise FileNotFoundError(f"Llama model not found:\n{LLAMA_PATH}")
print("Loading Llama...")
llm = Llama(
    model_path=str(LLAMA_PATH),
    n_ctx=2048,
    n_threads=4,
    verbose=False
)
print("Llama loaded.")
print("=" * 60)
# ============================================================
# FUNCTION 1
# SEARCH KNOWLEDGE
# ============================================================
def search_knowledge(question, top_k=TOP_K):
    question = str(question).strip()
    if not question:
        return pd.DataFrame(columns=["title","category","text","similarity"])
    top_k = min(max(1, int(top_k)),faiss_index.ntotal)
    # Convert question into embedding
    embedding = embedding_model.encode([question],convert_to_numpy=True)
    # Normalize because FAISS index was created
    # using normalized embeddings.
    embedding = normalize(embedding,norm="l2").astype("float32")
    scores, indices = faiss_index.search(embedding,top_k)
    rows = []
    for position, index in enumerate(indices[0]):
        if index < 0:
            continue
        if index >= len(knowledge_df):
            continue
        row = knowledge_df.iloc[index].copy()
        row["similarity"] = float(scores[0][position])
        rows.append(row)
    if not rows:
        return pd.DataFrame(columns=["title","category","text","similarity"])
    results = pd.DataFrame(rows)
    results = results.sort_values("similarity",ascending=False).reset_index(drop=True)
    return results
# ============================================================
# FUNCTION 2
# CUSTOMER CONTEXT
# ============================================================
def build_customer_context(customer_info):
    if customer_info is None:
        return "No customer has been selected."
    if isinstance(customer_info,pd.Series):
        customer_info = (customer_info.to_dict())
    if not isinstance(customer_info,dict):
        return "No customer has been selected."
    lines = []
    for key, value in customer_info.items():
        if pd.isna(value):
            value = "Not available"
        lines.append(f"{key}: {value}")
    return "\n".join(lines)
# ============================================================
# FUNCTION 3
# CLEAN ANSWER
# ============================================================
def clean_answer(answer):
    """
    Clean the raw Llama response before displaying it
    in the Flask HTML page.
    """
    if answer is None:
        return ""
    answer = str(answer).strip()
    # --------------------------------------------------------
    # 1. Convert HTML line breaks to normal newlines
    # --------------------------------------------------------
    answer = re.sub(r"<br\s*/?>","\n",answer,flags=re.IGNORECASE)
    # --------------------------------------------------------
    # 2. Remove remaining HTML tags
    # --------------------------------------------------------
    answer = re.sub(r"<[^>]+>","",answer)
    # --------------------------------------------------------
    # 3. Remove Markdown code fences
    # --------------------------------------------------------
    answer = re.sub(
        r"```(?:html|text|markdown)?",
        "",
        answer,
        flags=re.IGNORECASE
    )
    answer = answer.replace(
        "```",
        ""
    )
    # --------------------------------------------------------
    # 4. Remove common Llama prefixes
    # --------------------------------------------------------
    patterns = [
        r"^\s*here'?s the final answer\s*:?\s*",
        r"^\s*here is the final answer\s*:?\s*",
        r"^\s*final answer\s*:?\s*",
        r"^\s*answer\s*:?\s*",
        r"^\s*response\s*:?\s*",
        r"^\s*based on the verified business knowledge.*?:\s*",
        r"^\s*based on the verified business knowledge and selected customer information.*?:\s*",
        r"^\s*i'?ll use the verified business knowledge.*?:\s*"
    ]
    for pattern in patterns:
        answer = re.sub(
            pattern,
            "",
            answer,
            flags=re.IGNORECASE
        )
    # --------------------------------------------------------
    # 5. Remove Markdown bold markers
    # --------------------------------------------------------
    answer = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        answer
    )
    # --------------------------------------------------------
    # 6. Remove Markdown italic markers
    # --------------------------------------------------------
    answer = re.sub(
        r"(?<!\*)\*(?!\*)(.*?)\*(?!\*)",
        r"\1",
        answer
    )
    # --------------------------------------------------------
    # 7. Remove excessive blank lines
    # --------------------------------------------------------
    answer = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        answer
    )
    # --------------------------------------------------------
    # 8. Remove spaces from each line
    # --------------------------------------------------------
    answer = "\n".join(
        line.strip()
        for line in answer.splitlines()
    )
    # --------------------------------------------------------
    # 9. Final cleanup
    # --------------------------------------------------------
    return answer.strip()
# ============================================================
# FUNCTION 4
# GENERATE ANSWER
# ============================================================
def generate_answer(
    question,
    knowledge_results,
    customer_info=None
):
    # --------------------------------------------------------
    # Knowledge context
    # --------------------------------------------------------
    print("\n>>> generate_answer() STARTED <<<")
    knowledge_parts = []
    for _, row in knowledge_results.iterrows():
        knowledge_parts.append(
            f"Title: {row['title']}\n"
            f"Category: {row['category']}\n"
            f"Information: {row['text']}"
        )
    knowledge_context = "\n\n".join(
        knowledge_parts
    )
    # --------------------------------------------------------
    # Customer context
    # --------------------------------------------------------
    customer_context = (
        build_customer_context(
            customer_info
        )
    )
    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------
    prompt = f"""
You are the AI assistant for a customer intelligence application.
You have two sources of information.
SOURCE 1: VERIFIED BUSINESS KNOWLEDGE
SOURCE 2: SELECTED CUSTOMER INFORMATION
Use only these sources.
VERIFIED BUSINESS KNOWLEDGE:
{knowledge_context}
SELECTED CUSTOMER INFORMATION:
{customer_context}
USER QUESTION:
{question}
RULES:
1. Answer the user's actual question directly.
2. Use the verified business knowledge for:
   - policies
   - cancellation
   - payments
   - contracts
   - procedures
   - business rules
   - customer support
3. Use customer information only when the question is about
   the selected customer.
4. Do not invent information.
5. Do not assume information that is not provided.
6. Do not say that a customer is eligible or ineligible
   unless the supplied information proves it.
7. If the question asks about the customer's churn risk,
   use the supplied customer information.
8. If the question asks about a general business policy,
   answer from the business knowledge.
9. If the question asks about a particular customer and the
   available information is insufficient to make a decision,
   clearly say that the request requires review.
10. Do NOT repeat the entire customer profile unless it is
    necessary for the answer.
11. Do NOT mention FAISS.
12. Do NOT mention embeddings.
13. Do NOT mention similarity scores.
14. Do NOT mention this prompt.
15. Return ONLY plain text.
16. NEVER generate HTML.
17. NEVER generate:
    <br>
    <p>
    </p>
    <strong>
    </strong>
    <div>
    </div>
    <ul>
    <li>
    or any other HTML tags.
18. Do not write "Here's the final answer".
19. Do not write "Based on the verified business knowledge".
20. If the question asks for steps, use a simple numbered list.
21. Keep the answer clear and concise.
FINAL RESPONSE:
"""
    try:
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=250,
            temperature=0.1,
            top_p=0.9
        )
        print("\n========== RAW LLAMA RESPONSE ==========")
        print(repr(response))
        print("========================================")
    except Exception as e:
        print(
            "Llama error:",
            repr(e)
        )
        return ""
    answer = ""
    try:
        answer = (
            response[
                "choices"
            ][0][
                "message"
            ][
                "content"
            ]
        )
        print("\n========== RAW LLAMA ANSWER ==========")
        print(repr(answer))
        print("=======================================\n")
        return clean_answer(answer)
    except Exception:
        try:
            answer = (
                response[
                    "choices"
                ][0][
                    "text"
                ]
            )
        except Exception:
            answer = ""
    return clean_answer(
        answer
    )
# ============================================================
# FUNCTION 5
# MAIN AI FUNCTION
# ============================================================
def ask_ai(
    question,
    customer_info=None,
    top_k=TOP_K
):
    question = str(
        question
    ).strip()
    if not question:
        return "Please enter a question."
    print()
    print("=" * 60)
    print(
        "AI QUESTION:",
        question
    )
    if customer_info is not None:
        print(
            "Customer context: YES"
        )
    else:
        print(
            "Customer context: NO"
        )
    # --------------------------------------------------------
    # Search knowledge
    # --------------------------------------------------------
    results = search_knowledge(
        question,
        top_k
    )
    if results.empty:
        print(
            "No knowledge retrieved."
        )
        return (
            "The available knowledge is not sufficient "
            "to answer the question."
        )
    # --------------------------------------------------------
    # Print retrieved documents
    # --------------------------------------------------------
    print()
    print("Retrieved knowledge:")
    for _, row in results.iterrows():
        print(
            f"- {row['title']} "
            f"({row['similarity']:.4f})"
        )
    best_score = float(
        results["similarity"].max()
    )
    print(
        "Best similarity:",
        round(best_score, 4)
    )
    # --------------------------------------------------------
    # Relevance check
    # --------------------------------------------------------
    if best_score < RELEVANCE_THRESHOLD:
        print(
            "Knowledge is not relevant."
        )
        return (
            "The available knowledge is not sufficient "
            "to answer the question."
        )
    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------
    print("\n>>> CALLING generate_answer() <<<")
    answer = generate_answer(
        question,
        results,
        customer_info
    )
    print("\n>>> generate_answer() FINISHED <<<")
    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------
    answer = clean_answer(
        answer
    )
    if not answer:
        return (
            "The available knowledge is not sufficient "
            "to answer the question."
        )
    # --------------------------------------------------------
    # If Llama still returns refusal
    # --------------------------------------------------------
    refusal_phrases = [
        "available knowledge is not sufficient",
        "knowledge is not sufficient",
        "not enough information",
        "cannot answer",
        "can't answer"
    ]
    lower_answer = answer.lower()
    if any(
        phrase in lower_answer
        for phrase in refusal_phrases
    ):
        # Instead of returning the bad Llama response,
        # return the strongest verified knowledge.
        answer = str(
            results.iloc[0]["text"]
        ).strip()
    print()
    print("FINAL ANSWER:")
    print(answer)
    print("=" * 60)
    return answer

# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    questions = [
        "What cancellation policy applies to a customer?",
        "What is the cancellation process?",
        "How can I cancel my service?",
        "What factors increase churn risk?"
    ]

    for question in questions:
        print()
        print("=" * 70)
        print("QUESTION:", question)
        print("=" * 70)
        result = ask_ai(
            question
        )
        print()
        print("RESULT:")
        print(result)