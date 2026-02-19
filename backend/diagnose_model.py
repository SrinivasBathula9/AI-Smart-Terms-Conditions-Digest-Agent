import asyncio
import os
from dotenv import load_dotenv
from app.agents.graph import build_graph

load_dotenv()

async def run_diagnostics():
    print(f"--- Backend Diagnostics (Model: {os.getenv('MODEL', 'gemini-3-flash-preview')}) ---")
    
    graph = build_graph()
    sample_text = "Standard Terms of Service. Users must not share passwords. We collect data for analytics."
    
    print("\nInvoking LangGraph pipeline with gemini-3-flash-preview...")
    try:
        state = {"text": sample_text}
        result = graph.invoke(state)
        print("\nAnalysis successful!")
        print(f"Fairness Score: {result.get('summary', {}).get('fairness_score')}")
        print(f"Summary: {result.get('summary', {}).get('final_summary')[:100]}...")
    except Exception as e:
        print("\n--- ERROR DETECTED ---")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
