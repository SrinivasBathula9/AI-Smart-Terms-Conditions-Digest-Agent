import asyncio
import os
from dotenv import load_dotenv
from app.agents.graph import build_graph

load_dotenv()

async def run_diagnostics():
    print("--- Backend Diagnostics ---")
    print(f"Current Directory: {os.getcwd()}")
    print(f"GEMINI_API_KEY present: {'Yes' if os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE API KEY') else 'No'}")
    
    graph = build_graph()
    sample_text = "This is a sample legal clause for testing purposes. The provider reserves the right to terminate the service at any time without notice."
    
    print("\nInvoking LangGraph pipeline...")
    try:
        state = {"text": sample_text}
        # LangGraph invoke is synchronous in the current implementation
        result = graph.invoke(state)
        print("\nAnalysis successful!")
        print(f"Fairness Score: {result.get('summary', {}).get('fairness_score')}")
    except Exception as e:
        print("\n--- ERROR DETECTED ---")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
