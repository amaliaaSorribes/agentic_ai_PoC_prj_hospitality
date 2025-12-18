from agents.hotel_details_agent import hotel_details_agent

import sys
from pathlib import Path
from util.configuration import PROJECT_ROOT

def test_exercise_1():
    """Test the Exercise 1 agent with sample queries."""
    
    # Check configuration
    try:
        from config.agent_config import get_agent_config
        config = get_agent_config()
        print(f"✅ Configuration loaded: provider={config.provider}, model={config.model}")
    except ValueError as e:
        print(f"❌ ERROR: Configuration error: {e}")
        print("Please set AI_AGENTIC_API_KEY environment variable or configure in config/agent_config.yaml")
        return False
    except Exception as e:
        print(f"❌ ERROR: Failed to load configuration: {e}")
        return False
    
    print("🧪 Testing Exercise 1: Simple Agentic Assistant\n")
    print("=" * 60)
    
    # Test queries
    test_queries2 = [
        "What is the full address of Obsidian Tower?",
        "What are the meal charges for Half Board in hotels in Paris?",
        "List all hotels in France with their cities",
        "What is the discount for extra bed in Grand Victoria?",
        "Compare room prices between peak and off season for hotels in Nice"
    ]

    test_queries = ["What is the full address of Onyx Cliffs?"]
    
    success_count = 0
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}/{len(test_queries)}: {query}")
        print("-" * 60)
        
        try:
            response = hotel_details_agent(query)
            print(f"✅ Response received ({len(response)} characters)")
            print(f"\n{response}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"\n📊 Results: {success_count}/{len(test_queries)} tests passed")
    
    if success_count == len(test_queries):
        print("✅ All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = test_exercise_1()
    sys.exit(0 if success else 1)
