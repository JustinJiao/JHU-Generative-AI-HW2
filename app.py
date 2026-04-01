import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# 加载 .env 文件
load_dotenv()

# 配置 Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Prompt 模板 - 可以直接在这里修改
PROMPT_TEMPLATE = """You are an AI assistant that extracts action items from meeting transcripts.

Given a meeting transcript, extract all actionable to-do items.

For each action item, provide:
- Task description
- Responsible person (if mentioned)
- Deadline (if mentioned)

Rules:
- Only extract clear, actionable tasks
- Do NOT hallucinate information that is not in the transcript
- Ignore completed tasks and general discussion
- If no action items exist, return an empty list

Format your response as a JSON array:
[
  {
    "task": "task description",
    "owner": "person name or null",
    "deadline": "deadline or null"
  }
]

Meeting transcript:
{transcript}
"""

# 测试集 - 从 eval_set.md 中提取的测试用例
test_cases = [
    {
        "name": "Case 1 - Normal Case",
        "transcript": """Alright, quick updates. John finished the frontend login page. Sarah, can you finalize the API integration by Friday? Also, we need someone to prepare slides for Monday's client meeting. Mike, can you take that? Oh and we should fix the payment bug reported yesterday."""
    },
    {
        "name": "Case 2 - Noisy Input",
        "transcript": """Hey everyone, how was your weekend? Mine was great. Anyway, let's get started. So yeah, the marketing campaign is doing okay. We might want to improve the landing page. Not urgent though. Also, I think we should probably review the analytics dashboard sometime this week."""
    },
    {
        "name": "Case 3 - Hallucination Risk",
        "transcript": """We discussed several ideas about improving user retention. Maybe onboarding could be better. Some people mentioned emails, but nothing is decided yet."""
    },
    {
        "name": "Case 4 - Multi-Task",
        "transcript": """Okay, let's align on next steps. Alice will redesign the dashboard UI by next Wednesday. Bob and Charlie will work together on database optimization, no strict deadline yet. Also, we need to hire a new backend engineer—HR team should start drafting the job description."""
    },
    {
        "name": "Case 5 - Long Context",
        "transcript": """Let's go through updates. Sales numbers are up 10%, which is great. The customer feedback indicates issues with checkout speed. We should investigate that. Also, the mobile app crash reported last week still hasn't been fixed—can someone take ownership? David, can you look into that by Thursday? Lastly, we might explore AI features in Q3."""
    }
]


def extract_action_items(transcript, model_name="gemini-2.5-flash"):
    """使用 Gemini 提取行动项"""
    # 填充模板
    prompt = PROMPT_TEMPLATE.replace("{transcript}", transcript)

    # 调用 Gemini API
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text


def parse_json_response(response_text):
    """解析 JSON 响应"""
    try:
        # 尝试提取 JSON（可能包含在 markdown 代码块中）
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text.strip()

        return json.loads(json_str)
    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response_text
        }


def run_evaluation(output_file="results.json"):
    """运行评估并保存结果到 JSON 文件"""
    print("=" * 60)
    print("开始评估 - Meeting Action Items Extraction")
    print("=" * 60)
    print()

    results = {
        "timestamp": datetime.now().isoformat(),
        "model": "gemini-2.5-flash",
        "test_cases": []
    }

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"测试用例 {i}: {test_case['name']}")
        print(f"{'=' * 60}")

        result = {
            "case_number": i,
            "case_name": test_case['name'],
            "input": test_case['transcript'],
            "raw_response": None,
            "extracted_items": None,
            "error": None
        }

        try:
            # 调用 Gemini
            response = extract_action_items(test_case['transcript'])
            result["raw_response"] = response

            print(f"✓ Gemini 响应已获取")

            # 解析 JSON
            action_items = parse_json_response(response)

            if isinstance(action_items, list):
                result["extracted_items"] = action_items
                print(f"✓ 提取了 {len(action_items)} 个行动项")
            elif isinstance(action_items, dict) and "error" in action_items:
                result["error"] = action_items["error"]
                result["extracted_items"] = []
                print(f"✗ JSON 解析失败: {action_items['error']}")
            else:
                result["extracted_items"] = action_items
                print(f"✓ 响应已解析")

        except Exception as e:
            result["error"] = str(e)
            print(f"✗ 错误: {e}")

        results["test_cases"].append(result)

    # 保存结果到 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"✓ 评估完成！结果已保存到: {output_file}")
    print(f"{'=' * 60}")

    return results


if __name__ == "__main__":
    # 检查 API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("错误: 请设置 GEMINI_API_KEY 环境变量")
        print("提示: 在 .env 文件中添加: GEMINI_API_KEY=your-api-key")
        exit(1)

    # 运行评估
    run_evaluation()
