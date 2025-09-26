#!/usr/bin/env python3
"""
Example usage of the vidIQ Python API
"""

import os
from vidiq_api import VidiqAPI

# Initialize the API with your auth token
# Get this from your vidIQ browser extension or environment variable
auth_token = os.getenv('VIDIQ_TOKEN')
api = VidiqAPI(auth_token)

# Example 1: Analyze a single keyword
def analyze_single_keyword():
    try:
        result = api.analyze_keyword("youtube SEO")
        print(f"Keyword: {result['keyword']}")
        print(f"Volume: {result['data']['volume']}")
        print(f"Competition: {result['data']['competition']}")
        print(f"Difficulty: {result['levels']['overall_level']}")
    except Exception as e:
        print(f"Error: {e}")

# Example 2: Analyze multiple keywords
def analyze_multiple_keywords():
    keywords = ["youtube SEO", "video marketing", "content creation"]
    
    results = api.analyze_multiple_keywords(keywords)
    
    for keyword, data in results.items():
        if 'error' in data:
            print(f"❌ {keyword}: {data['error']}")
        else:
            print(f"✅ {keyword}: Volume={data['data']['volume']}, Competition={data['data']['competition']}")

# Example 3: Use in your own functions
def get_keyword_difficulty(keyword: str) -> str:
    """Get just the difficulty level for a keyword"""
    try:
        result = api.analyze_keyword(keyword)
        return result['levels']['overall_level']
    except Exception as e:
        return f"Error: {e}"

def get_keyword_volume(keyword: str) -> int:
    """Get just the search volume for a keyword"""
    try:
        result = api.analyze_keyword(keyword)
        return result['data']['volume']
    except Exception as e:
        return 0

# Example 4: Batch processing with custom logic
def process_keyword_batch(keywords: list):
    """Process keywords and filter by difficulty"""
    results = api.analyze_multiple_keywords(keywords, delay=1.0)
    
    easy_keywords = []
    medium_keywords = []
    hard_keywords = []
    
    for keyword, data in results.items():
        if 'error' in data:
            continue
            
        level = data['levels']['overall_level']
        if level in ['Very Low', 'Low']:
            easy_keywords.append(keyword)
        elif level == 'Medium':
            medium_keywords.append(keyword)
        else:
            hard_keywords.append(keyword)
    
    print(f"Easy keywords: {easy_keywords}")
    print(f"Medium keywords: {medium_keywords}")
    print(f"Hard keywords: {hard_keywords}")

# Example 5: Get matching keywords (permutations)
def get_matching_keywords_example():
    """Get matching keywords for a given term"""
    try:
        result = api.get_matching_keywords("cats", limit=10)
        print(f"\n🔍 Matching keywords for '{result['keyword']}':")
        print(f"Found {result['count']} matches")
        
        # Display first few matches
        keywords = result['data'].get('permutations', [])
        for i, keyword in enumerate(keywords[:5]):
            if isinstance(keyword, dict):
                print(f"  {i+1}. {keyword.get('keyword', keyword)}")
            else:
                print(f"  {i+1}. {keyword}")
                
    except Exception as e:
        print(f"Error getting matching keywords: {e}")

# Example 6: Get related keywords
def get_related_keywords_example():
    """Get related keywords for a given term"""
    try:
        result = api.get_related_keywords("cats")
        print(f"\n🔗 Related keywords for '{result['keyword']}':")
        print(f"Found {result['count']} related terms")
        
        # Display related keywords
        related = result['data']
        for i, keyword in enumerate(related[:5]):
            if isinstance(keyword, dict):
                print(f"  {i+1}. {keyword.get('keyword', keyword)}")
            else:
                print(f"  {i+1}. {keyword}")
                
    except Exception as e:
        print(f"Error getting related keywords: {e}")

# Example 7: Get questions
def get_questions_example():
    """Get question-based keywords for a given term"""
    try:
        result = api.get_questions("cats", limit=10)
        print(f"\n❓ Questions for '{result['keyword']}':")
        print(f"Found {result['count']} questions")
        
        # Display first few questions
        questions = result['data'].get('questions', [])
        for i, question in enumerate(questions[:5]):
            if isinstance(question, dict):
                print(f"  {i+1}. {question.get('keyword', question)}")
            else:
                print(f"  {i+1}. {question}")
                
    except Exception as e:
        print(f"Error getting questions: {e}")

# Example 8: Complete keyword research workflow
def complete_keyword_research(keyword: str):
    """Perform complete keyword research for a given term"""
    print(f"\n🎯 Complete Keyword Research for: '{keyword}'")
    print("=" * 50)
    
    try:
        # 1. Basic analysis
        analysis = api.analyze_keyword(keyword)
        print(f"📊 Basic Analysis:")
        print(f"  Volume: {analysis['data']['volume']}")
        print(f"  Competition: {analysis['data']['competition']}")
        print(f"  Overall Level: {analysis['levels']['overall_level']}")
        
        # 2. Get matching keywords
        matching = api.get_matching_keywords(keyword, limit=5)
        print(f"\n🔍 Top 5 Matching Keywords:")
        keywords = matching['data'].get('permutations', [])
        for i, kw in enumerate(keywords[:5]):
            if isinstance(kw, dict):
                print(f"  {i+1}. {kw.get('keyword', kw)}")
            else:
                print(f"  {i+1}. {kw}")
        
        # 3. Get related keywords
        related = api.get_related_keywords(keyword)
        print(f"\n🔗 Top 5 Related Keywords:")
        related_kws = related['data']
        for i, kw in enumerate(related_kws[:5]):
            if isinstance(kw, dict):
                print(f"  {i+1}. {kw.get('keyword', kw)}")
            else:
                print(f"  {i+1}. {kw}")
        
        # 4. Get questions
        questions = api.get_questions(keyword, limit=5)
        print(f"\n❓ Top 5 Questions:")
        question_kws = questions['data'].get('questions', [])
        for i, q in enumerate(question_kws[:5]):
            if isinstance(q, dict):
                print(f"  {i+1}. {q.get('keyword', q)}")
            else:
                print(f"  {i+1}. {q}")
                
    except Exception as e:
        print(f"Error in complete research: {e}")

if __name__ == "__main__":
    print("vidIQ Python API Examples")
    print("=" * 30)
    
    # Uncomment the examples you want to run:
    
    # Basic functionality
    # analyze_single_keyword()
    # analyze_multiple_keywords()
    # print(get_keyword_difficulty("youtube SEO"))
    # process_keyword_batch(["youtube SEO", "video marketing", "content creation"])
    
    # New functionality
    get_matching_keywords_example()
    get_related_keywords_example()
    get_questions_example()
    
    # Complete workflow
    complete_keyword_research("cats")
