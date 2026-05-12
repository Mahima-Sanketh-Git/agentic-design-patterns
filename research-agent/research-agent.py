from datetime import datetime
from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
from tavily import TavilyClient
import re
import json
from urllib.parse import urlparse

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key  = os.getenv("TAVILY_API_KEY")
client = genai.Client(api_key=gemini_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

TOP_DOMAINS = {
    # =========================
    # General Reference / Institutions
    # =========================
    "wikipedia.org",
    "britannica.com",

    # =========================
    # Academic / Research (AI + CS)
    # =========================
    "arxiv.org",
    "acm.org",
    "ieee.org",
    "neurips.cc",
    "icml.cc",
    "openreview.net",
    "jmlr.org",
    "springer.com",
    "sciencedirect.com",
    "pnas.org",

    # =========================
    # Tech News / Industry (IMPORTANT for our use case)
    # =========================
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "arstechnica.com",
    "zdnet.com",
    "venturebeat.com",
    "thenextweb.com",
    "digitaltrends.com",

    # =========================
    # Big Tech / Official Engineering Blogs
    # =========================
    "blog.google",
    "ai.google",
    "openai.com",
    "anthropic.com",
    "developer.nvidia.com",
    "aws.amazon.com",
    "cloud.google.com",
    "azure.microsoft.com",

    # =========================
    # Science & High-quality media
    # =========================
    "nature.com",
    "science.org",
    "sciencemag.org",
    "cell.com",
    "elifesciences.org",

    # =========================
    # Space / Climate / Govt science
    # =========================
    "nasa.gov",
    "noaa.gov",
    "europa.eu",

    # =========================
    # Education / Learning
    # =========================
    "mit.edu",
    "stanford.edu",
    "harvard.edu",
    "codecademy.com",
    "datacamp.com",

    # =========================
    # Misc credible public knowledge
    # =========================
    "pbs.org",
    "britannica.com"
}

def web_search(search_query:str):
    """
    Web search using tavily general web search api

    Args:
        search_query (str): pass search query that need to search on web
    """
    print("Tool selection : using web searching.............")

    try:
        response = tavily_client.search(search_query)
        print("Web search is done ✅")
        return response
    except Exception as exc:
        error_message = f"Web search failed: {exc}"
        print(error_message)
        return error_message

def web_page_extract(web_url_path:str):
    """
    Web pages extract using tavily web extract api

    Args:
        web_url_path (str): pass web url path to extract web page
    """
    print("Tool selection : using web page extracting.............")

    try:
        response = tavily_client.extract(web_url_path)
        print("Web page extraction is done ✅")
        return response
    except Exception as exc:
        error_message = f"Web page extraction failed: {exc}"
        print(error_message)
        return error_message


def web_crawl(web_url_path:str,instruction:str):
    """
    Web crawl using tavily web crawl api

    Args:
        web_url_path (str): pass web url path to crawl web page
        instruction (str): pass instruction for crawler
    """
    print("Tool selection : using web page crawling.............")

    try:
        response = tavily_client.search(web_url_path, instruction=instruction)
        print("Web crawling is done ✅")
        return response
    except Exception as exc:
        error_message = f"Web crawling failed: {exc}"
        print(error_message)
        return error_message

def web_page_map(web_url_path:str):
    """
    Web map using tavily web page map api

    Args:
        web_url_path (str): pass web url path to crawl web page
        instruction (str): pass instruction for crawler
    """
    print("Tool selection : using web page mapping.............")
    try:
        response = tavily_client.map(web_url_path)
        print("Web page mapping is done ✅")
        return response
    except Exception as exc:
        error_message = f"Web page mapping failed: {exc}"
        print(error_message)
        return error_message

def reserach(topic:str):
    """
    research on specific topic with tavily reserach api

    Args:
        topic (str): pass topic that need to reserach
    """
    print("Tool selection : using research.............")
    try:
        response = tavily_client.research(topic)
        print("Research is done ✅")
        return response
    except Exception as exc:
        error_message = f"Research failed: {exc}"
        print(error_message)
        return error_message

def get_current_time():
    """
    Get the current time in HH:MM:SS format and return it as a string.
    """
    return datetime.now().strftime("%H:%M:%S")

def reflection_agent(output_draft:str):
    """
      reflect generated reserach draft and generate final output
      Args:
        output_draft (str): pass generated reserach draft to reflect and generate final output
    """
    prompt = f"""
         You are a research assistant. Your task is to research on the topic of {output_draft}. 
         Use the available tools to gather information, extract relevant data from web pages, and map out the key findings. 
         Provide a comprehensive summary of your research findings.
         
         Prefer credible sources such as:
            -TechCrunch, The Verge, Wired, Arxiv, IEEE, official tech blogs.
            -Always prioritize recent and authoritative sources.
         
         *Strict*
            - Use get_current_time tool to check current time and date to validate the research draft and provide feedback based on the accuracy and comprehensiveness of the information presented in the research draft.
            - Ouput must be only in json format with two keys: "score", "feedback" and final draft should be in markdown format with properly strcutured final research findings and also web sources links.
            - "score" should be a number between 1 and 5, where 1 indicates a poor research draft and 5 indicates an excellent research draft.
            - "feedback" should provide specific suggestions for improving the research draft, such as identifying gaps in the research, suggesting additional sources to consult, or recommending ways to better organize the information.
            - Do not provide any feedback that is not constructive or actionable.
            - Focus on providing feedback that will help improve the quality of the research draft, rather than simply criticizing it.
            - Check global web sources to validate the research draft and provide feedback based on the accuracy and comprehensiveness of the information presented.

         example output:
         {{
            "score": 3,
            "feedback": "The research draft provides a good overview of the topic, but it could be improved by including more recent sources and providing a clearer organization of the information. Consider adding more specific examples and case studies to support your points, and make sure to cite all sources properly.",
            "final_draft": "## Final Research Findings\n\n### Key Insights\n- Insight 1: ...\n- Insight 2: ...\n\n### Takeaways\n- Takeaway 1: ...\n- Takeaway 2: ...\n\n### Web Sources\n- [Source 1](https://www.example.com)\n- [Source 2](https://www.example.com)"
         }}
        """
    print("Reflection agent is working.............")
    try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            print("Reflection agent is done ✅")
            return response.text
    except Exception as exc:
            error_message = f"Reflection agent failed: {exc}"
            print(error_message)
            return error_message

def evaluate_tavily_results(TOP_DOMAINS, raw: str, min_ratio=0.4):
    
    """
    Evaluate whether plain-text research results mostly come from preferred domains.

    Args:
        TOP_DOMAINS (set[str]): Set of preferred domains (e.g., 'arxiv.org', 'nature.com').
        raw (str): Plain text or Markdown containing URLs.
        min_ratio (float): Minimum preferred ratio required to pass (e.g., 0.4 = 40%).

    Returns:
        tuple[bool, str]: (flag, markdown_report)
            flag -> True if PASS, False if FAIL
            markdown_report -> Markdown-formatted summary of the evaluation
    """
    
    # Extract URLs from the text
    url_pattern = re.compile(r'https?://[^\s\]\)>\}]+', flags=re.IGNORECASE)
    urls = url_pattern.findall(raw)
    
    
    if not urls:
        return False, """### Evaluation — Tavily Preferred Domains
        No URLs detected in the provided text. 
        Please include links in your research results.
        """
        
    total = len(urls)
    preferred_count = 0
    details = []
    
    for url in urls:
        domain  = urlparse(url).netloc.lower()  # Extract domain from URL
        domain = domain.replace("www.", "")  # Remove 'www.' prefix if present
        is_preferred = domain in TOP_DOMAINS

        if is_preferred:
            preferred_count += 1

        details.append((url, domain, is_preferred))

    preferred_ratio = preferred_count / total if total > 0 else 0
    pass_evaluation = preferred_ratio >= min_ratio

    # Generate markdown report
    markdown_report = """### Evaluation — Tavily Preferred Domains

"""
    for url, domain, is_preferred in details:
        status = "✅" if is_preferred else "❌"
        markdown_report += f"- {status} [{url}]({url}) - {domain}\n"

    markdown_report += f"\n**Preferred URLs:** {preferred_count}/{total} ({preferred_ratio:.2%})\n"

    if pass_evaluation:
        markdown_report += "\n✅ Evaluation PASSED: Most URLs come from preferred domains."
    else:
        markdown_report += "\n❌ Evaluation FAILED: Too many URLs come from non-preferred domains."

    return pass_evaluation, markdown_report


def run_workflow():
    max_iterations = 3
     # Main Agent
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        tools=[web_search, web_page_extract, web_crawl, web_page_map]
        )
    )
    while max_iterations > 0:
        try:
            user_message = "What are the current tech news?"
            pormpt = f"""
        You are a research assistant. Your task is to research on the topic of {user_message}. 
        Use the available tools to gather information, extract relevant data from web pages, and map out the key findings. 
        Provide a comprehensive summary of your research findings.
        
        Today is {get_current_time()}
        
        Prefer credible sources such as:
            -TechCrunch, The Verge, Wired, Arxiv, IEEE, official tech blogs.
            -Always prioritize recent and authoritative sources.
        
        *Consider*
            - Use reflection_agent to reflect on the research draft and provide feedback for improvement (example output:  {{
                "score": 3,
                "feedback": "The research draft provides a good overview of the topic, but it could be improved by including more recent sources and providing a clearer organization of the information. Consider adding more specific examples and case studies to support your points, and make sure to cite all sources properly."
            }}).
            
        Final output:
            - Provide a comprehensive summary of your research findings, including key insights and takeaways from the research process. Make sure to cite all sources properly and provide a clear and organized presentation of the information you have gathered.
            - Final Response must be in markdown format with properly strcutured final research findings and also web sources links.  

        
        """
            response = chat.send_message(pormpt)
            
            # Evaluate tavily web search result
            flag, markdown = evaluate_tavily_results(TOP_DOMAINS=TOP_DOMAINS,raw=response.text,min_ratio=0.4)
            
            if flag == False:
                max_iterations -= 1
                print("================== Threshhold ===================")
                print(markdown)
                if(max_iterations > 0):                    
                   print("Main agent is re run again...")
                   continue
                else:
                    print("Session is stop due to Agent couldn't met minimum threshhold")
                    break
            
            # Reflection Agent
            final_response = reflection_agent(response.text)
            try:
              obj = json.loads(final_response)
            except json.JSONDecodeErroras as exe:
                print("Invalid JSON from reflection agent")
                print(final_response)
                continue
            
            reflection_agent_feedback = str(obj.get("feedback", "")).strip()
            feedback_score = obj.get("score", 0)
            final_output = str(obj.get("final_draft", "")).strip()
            
            if feedback_score < 3:
                max_iterations -= 1
                print("================== Threshhold ===================")
                print(f"Reflection Agent Feedback: {reflection_agent_feedback}")
                if(max_iterations > 0):
                    print("Main agent is re run again...")
                    continue
                else:
                    print("Session is stop due to Reflection Agent feedback score is less than 3")
                    break
            
            # Final output
            print("================== Final Research Output ===================")
            print(final_output)
            
            print("=================== Final Reflection Agent Feedback ===================")
            print(f"Feedback Score: {feedback_score}")
            print(f"Feedback: {reflection_agent_feedback}")
            
            print("Workflow is done ✅")
            break
            
        except Exception as exc:
            print(f"Workflow failed: {exc}")
            max_iterations -= 1



if __name__ == "__main__":
    try:
        run_workflow()
    except Exception as exc:
        print(f"Unexpected error: {exc}")
