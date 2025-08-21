import os
from services import HomeMatchApp


def main():
    """Run HomeMatch in CLI mode."""
    from dotenv import load_dotenv
    import os, json

    # Load keys
    load_dotenv(".env")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")

    if not api_key:
        print("⚠️ OpenAI API key not found in key.env!")
        return

    try:
        print("🚀 Initializing HomeMatch...")
        app = HomeMatchApp(api_key, api_base)
        print("✅ Ready to generate single listing...\n")

        if app.generate_listings(3): 
            print(json.dumps(app.listings, indent=2))
        else:
            print("❌ No listing generated.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

    