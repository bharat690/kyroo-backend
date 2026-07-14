import json
from app.database.supabase_client import get_supabase
from app.services.memory.service import MemoryService
from app.llm.factory import LLMFactory
from app.llm.base import Prompt
from app.brain.response_validator import ResponseValidator


def _detect_module(message: str) -> str:
    """Detect which life module the message belongs to."""
    msg = message.lower()

    if any(w in msg for w in [
        "gym", "workout", "exercise", "protein", "cardio",
        "pushup", "weight", "muscle", "steps", "calories",
        "diet", "eat", "food", "meal",
    ]):
        return "fitness"

    if any(w in msg for w in [
        "spend", "expense", "money", "rupee", "rs ", "₹",
        "upi", "salary", "saving", "budget", "emi", "bill",
        "pay", "cost", "price", "cheap", "expensive",
    ]):
        return "finance"

    if any(w in msg for w in [
        "sleep", "nap", "tired", "insomnia", "wake",
        "bedtime", "alarm", "dream", "rest",
    ]):
        return "sleep"

    if any(w in msg for w in [
        "mood", "feel", "sad", "happy", "anxious",
        "stressed", "depressed", "angry", "lonely",
        "overwhelm", "burnout", "cry", "mental",
    ]):
        return "mind"

    return "general"


def _detect_emotion(message: str) -> str:
    """Detect user emotion."""
    msg = message.lower()

    if any(w in msg for w in [
        "😭", "😢", "cry", "alone", "lonely", "sad",
        "depressed", "heartbroken", "miss",
    ]):
        return "sad"

    if any(w in msg for w in [
        "😡", "angry", "mad", "frustrated", "pissed",
        "hate", "annoyed",
    ]):
        return "angry"

    if any(w in msg for w in [
        "😫", "burnout", "exhausted", "drained",
        "tired", "done", "can't do this",
    ]):
        return "burnout"

    if any(w in msg for w in [
        "🔥", "💪", "😈", "yay", "letsgo", "lessgo",
        "excited", "amazing", "killed it", "nailed",
        "crushed", "best day",
    ]):
        return "excited"

    if any(w in msg for w in [
        "😰", "anxiety", "panic", "worried", "stress",
        "nervous", "scared", "fear",
    ]):
        return "anxious"

    return "neutral"


def _build_tracking_summary(tracking_logs: list[dict]) -> str:
    """Build a readable summary from tracking logs."""
    if not tracking_logs:
        return "No tracking data yet."

    lines = []
    for log in tracking_logs:
        date = log.get("date", "?")
        parts = [f"📅 {date}:"]
        if log.get("workout_done"):
            name = log.get("workout_name", "")
            dur = log.get("workout_duration", "")
            cal = log.get("calories_burned", "")
            w = f"Workout: {name}" if name else "Workout done ✓"
            if dur:
                w += f" ({dur}min)"
            if cal:
                w += f" {cal}cal"
            parts.append(w)
        if log.get("steps"):
            parts.append(f"Steps: {log['steps']}")
        if log.get("water_glasses"):
            parts.append(f"Water: {log['water_glasses']} glasses")
        if log.get("weight_kg"):
            parts.append(f"Weight: {log['weight_kg']}kg")
        if log.get("spent_today") is not None:
            cat = log.get("spent_category", "")
            s = f"Spent: ₹{log['spent_today']}"
            if cat:
                s += f" ({cat})"
            parts.append(s)
        if log.get("saved_today"):
            parts.append(f"Saved: ₹{log['saved_today']}")
        if log.get("mood_score") is not None:
            parts.append(f"Mood: {log['mood_score']}/10")
        if log.get("stress_score") is not None:
            parts.append(f"Stress: {log['stress_score']}/10")
        if log.get("sleep_hours") is not None:
            q = log.get("sleep_quality", "")
            s = f"Sleep: {log['sleep_hours']}hrs"
            if q:
                s += f" (quality: {q}/10)"
            parts.append(s)
        lines.append(" | ".join(parts))

    return "\n".join(lines)


def _build_style_section(style: dict | None) -> str:
    """Build user style description for prompt."""
    if not style:
        return "User style: unknown (first few messages, mirror them)."

    parts = []
    if style.get("avg_message_length"):
        parts.append(f"Avg message length: {style['avg_message_length']}")
    if style.get("uses_dragged_words"):
        parts.append("Uses dragged words: yes (e.g. heyyyy, achaaaa)")
    if style.get("uses_hinglish"):
        parts.append("Uses Hinglish: YES — reply in Hinglish")
    if style.get("common_emojis"):
        parts.append(f"Common emojis: {style['common_emojis']}")
    if style.get("energy_level"):
        parts.append(f"Energy level: {style['energy_level']}")
    if style.get("engagement_score"):
        parts.append(f"Engagement: {style['engagement_score']}/10")
    if style.get("message_count"):
        parts.append(f"Total messages: {style['message_count']}")

    return "User style: " + ", ".join(parts) if parts else "User style: still learning."


def _build_user_profile(user: dict) -> str:
    """Build user profile section for prompt."""
    parts = [f"Name: {user.get('name', 'unknown')}"]

    if user.get("age"):
        parts.append(f"Age: {user['age']}")
    if user.get("city"):
        parts.append(f"City: {user['city']}")
    if user.get("language"):
        parts.append(f"Language preference: {user['language']}")
    if user.get("plan"):
        parts.append(f"Plan: {user['plan']}")

    goals = []
    if user.get("fitness_goal"):
        goals.append(f"Fitness: {user['fitness_goal']}")
    if user.get("fitness_level"):
        goals.append(f"Fitness level: {user['fitness_level']}")
    if user.get("diet_type"):
        goals.append(f"Diet: {user['diet_type']}")
    if user.get("sleep_hours"):
        goals.append(f"Sleep target: {user['sleep_hours']}hrs")
    if user.get("money_habit"):
        goals.append(f"Money habit: {user['money_habit']}")
    if user.get("energy_peak"):
        goals.append(f"Peak energy: {user['energy_peak']}")
    if user.get("stress_level"):
        goals.append(f"Stress level: {user['stress_level']}/10")

    if goals:
        parts.append("Goals & prefs: " + ", ".join(goals))

    return "\n".join(parts)


def _build_system_prompt(
    user: dict,
    tracking_summary: str,
    emotional_memories: list[dict],
    semantic_memories: list[dict],
    style_section: str,
    user_profile: str,
    module: str,
    emotion: str,
    history_text: str,
) -> str:
    """Build the full system prompt — THIS IS THE GAME CHANGER."""

    # Emotional memory section
    emote_lines = []
    for m in emotional_memories[:5]:
        emote_lines.append(
            f"- [{m.get('event_type', '?')}] {m.get('detail', '')} "
            f"({'followed up' if m.get('follow_up_sent') else 'NEEDS FOLLOW-UP'})"
        )
    emotional_text = "\n".join(emote_lines) if emote_lines else "None yet."

    # Semantic memory section
    memory_lines = []
    for m in semantic_memories[:5]:
        sim = m.get("similarity", 0)
        memory_lines.append(f"- [{sim:.0%}] {m.get('content', '')}")
    memory_text = "\n".join(memory_lines) if memory_lines else "None yet."

    return f"""You are KIRO — an AI Life Operating System.
You run on WhatsApp. You are the user's best friend who actually helps them improve their life.

You are NOT a chatbot. You are NOT an AI assistant. You are KIRO.
Never say "as an AI", never mention Claude, Anthropic, OpenAI, or LLM.
Never give generic advice. Everything you say should be personalized.

═══ USER PROFILE ═══
{user_profile}

═══ USER COMMUNICATION STYLE ═══
{style_section}

CRITICAL: Mirror the user's style exactly.
- If they use Hinglish, you reply in Hinglish.
- If they use dragged words (heyyyy, achaaaa), you do too.
- Match their emoji intensity. Never use more emojis than them.
- Match their message length. Short messages = short replies.
- Match their energy. Low energy = calm reply. High energy = match it.
- Never become more expressive than the user.

═══ RECENT TRACKING DATA (LAST 7 DAYS) ═══
{tracking_summary}

Use this data naturally in conversation. Don't dump it.
Example: if they haven't worked out in 3 days, casually mention it.
Example: if their sleep has been bad, check in on it.

═══ EMOTIONAL MEMORY ═══
{emotional_text}

IMPORTANT: If any emotional memory says "NEEDS FOLLOW-UP", gently follow up on it.
Don't force it. Weave it naturally into conversation.
After following up, the system will mark it as done.

═══ SEMANTIC MEMORY (RELEVANT TO THIS MESSAGE) ═══
{memory_text}

Use these memories naturally. Reference past conversations only when relevant.
Never say "I remember you told me..." — just naturally use the info.

═══ RECENT CHAT HISTORY ═══
{history_text}

═══ CURRENT CONTEXT ═══
Module: {module}
Detected emotion: {emotion}

═══ HOW TO RESPOND ═══

1. REACT FIRST, ADVISE SECOND
   - User says "crushed my workout" → "LESSSSGOOO 🔥" NOT "Great job, keep it up!"
   - User says "I'm so tired" → "aareee 😭" NOT "It sounds like you're tired"

2. BE SHORT. ALWAYS.
   - Greeting: 2-8 words max
   - Normal reply: 8-20 words
   - Emotional support: 15-35 words
   - NEVER exceed 45 words per bubble
   - Split into multiple bubbles with double newlines

3. NEVER INTERVIEW
   - Don't ask "how was your day?" "what are you up to?" "how have you been?"
   - Only ask questions when user shares something meaningful
   - 70% reactions, 20% observations, 10% questions

4. USE TRACKING DATA NATURALLY
   - "bhai 3 din se gym nahi gaya 😤" (if they haven't logged a workout)
   - "sleep last night was rough huh" (if sleep_hours was low)
   - "₹2000 spend kar diye aaj 🤡" (if spent_today was high)
   - DON'T dump all data. Pick the MOST RELEVANT one thing.

5. MODULE-SPECIFIC BEHAVIOR
   Fitness: Tease them if skipping, hype them if consistent, suggest workouts based on their level.
   Finance: Call out overspending casually, celebrate savings, suggest budget tweaks.
   Sleep: Track patterns, suggest bedtime adjustments, check in on sleep quality.
   Mind: Validate feelings first, then gently suggest actions. Never toxic positivity.
   General: Be a friend. React, joke, exist.

6. EMOTION HANDLING
   Sad → Comfort first. "yaar 😭" then "wanna talk about it?"
   Angry → Stay calm. "oh shit" then listen.
   Burnout → Validate. "bhai I can tell" then suggest rest.
   Excited → Match energy. "BROOO 🔥🔥🔥" go all out.
   Anxious → Slow down. "hey hey" then ground them.
   Neutral → Normal chat energy.

7. LANGUAGE RULES
   English user → Pure English
   Hinglish user → Natural Hinglish (not forced)
   Drag words naturally: heyyyy, achaaaa, kyaaaa, whaaaa, lesssgooooo
   Use lowercase. Never write paragraphs. Max 2 emojis per bubble.

8. WHATSAPP FORMATTING
   Separate bubbles with double newlines (\\n\\n)
   Each bubble = one message the user receives
   Max 3 bubbles per response

═══ EXAMPLES ═══

User: "hi"
You: heyyyy 😭

User: "bhai gym jaake aaya, chest day tha"
You: chest dayyyyy 🔥\n\nkaisa laga?

User: "aaj nahi gaya, bahut thak gaya tha"
You: thik hai bhai\n\nrest is also gains 💪

User: "₹1500 kharcha kar diya swiggy pe"
You: swiggy pe ₹1500 😭\n\nkal se khana bana le yaar

User: "mujhe nahi rehna ab"
You: yaar\n\ntu thik hai?

User: "letsgooooo cleared my exam"
You: BROOOOOOO 🔥🔥🔥\n\nLESSSSGOOOOO

User: "best protein powder?"
You: optimum gold standard\n\nya muscleblaze if budget tight"""


def kyroo_brain(
    user: dict,
    message: str,
    history: list[dict] | None = None,
    image_base64: str | None = None,
    image_media_type: str | None = None,
) -> dict:
    """Main brain — takes user data, builds rich prompt, generates response."""

    user_id = user["id"]
    db = get_supabase()

    # 1. Detect module and emotion
    module = _detect_module(message)
    emotion = _detect_emotion(message)

    # 2. Get tracking data (last 7 days)
    try:
        tracking_res = (
            db.table("user_tracking")
            .select("*")
            .eq("user_id", user_id)
            .order("date", desc=True)
            .limit(7)
            .execute()
        )
        tracking_logs = tracking_res.data or []
    except Exception:
        tracking_logs = []

    # 3. Get emotional memories
    memory_service = MemoryService()
    emotional_memories = memory_service.get_emotional_memory(user_id, limit=5)

    # 4. Get semantic memories (relevant to this message)
    semantic_memories = memory_service.search_memories(user_id, message, limit=3)

    # 5. Get user style
    try:
        style_res = (
            db.table("user_style")
            .select("*")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        style = style_res.data
    except Exception:
        style = None

    # 6. Build history text
    history_lines = []
    if history:
        for h in reversed(history):
            if h.get("user_message"):
                history_lines.append(f"User: {h['user_message']}")
            if h.get("kiro_response"):
                history_lines.append(f"KIRO: {h['kiro_response']}")
    history_text = "\n".join(history_lines[-20:]) if history_lines else "No previous messages."

    # 7. Build all sections
    user_profile = _build_user_profile(user)
    tracking_summary = _build_tracking_summary(tracking_logs)
    style_section = _build_style_section(style)

    # 8. Build THE prompt
    system_prompt = _build_system_prompt(
        user=user,
        tracking_summary=tracking_summary,
        emotional_memories=emotional_memories,
        semantic_memories=semantic_memories,
        style_section=style_section,
        user_profile=user_profile,
        module=module,
        emotion=emotion,
        history_text=history_text,
    )

    # 9. Call LLM
    prompt = Prompt(
        system_prompt=system_prompt,
        user_message=message,
    )

    provider = LLMFactory.create()
    response = provider.generate(prompt)
    reply = response.content

    # 10. Validate into bubbles
    validator = ResponseValidator()
    bubbles = validator.validate(reply)

    # 11. Save semantic memory if user shared something important
    _maybe_save_memory(memory_service, user_id, message, module)

    # 12. Save emotional event
    if emotion != "neutral":
        memory_service.save_emotional_memory(user_id, emotion, message[:300])

    # 13. Update user style (async-like, fire and forget)
    _update_user_style(db, user_id, message, style)

    return {
        "response": reply,
        "bubbles": bubbles,
        "module": module,
        "emotion": emotion,
    }


def _maybe_save_memory(
    memory_service: MemoryService,
    user_id: str,
    message: str,
    module: str,
) -> None:
    """Save important facts to semantic memory."""
    memory_keywords = [
        "my name is", "i work at", "i live in", "my goal is",
        "i want to", "i'm studying", "i'm learning", "i have a",
        "mera naam", "main kaam karta", "mera goal", "meri girlfriend",
        "my girlfriend", "my boyfriend", "my mom", "my dad",
        "i'm from", "i belong to", "my company",
    ]

    msg_lower = message.lower()
    if any(kw in msg_lower for kw in memory_keywords):
        memory_service.save_memory(user_id, message, source="chat")


def _update_user_style(
    db,
    user_id: str,
    message: str,
    existing_style: dict | None,
) -> None:
    """Update user style based on latest message."""
    import re

    EMOJIS = re.compile(
        "[" "\U0001F300-\U0001FAFF" "\U00002700-\U000027BF" "]",
        flags=re.UNICODE,
    )

    DRAGGED = re.compile(r"(.)\1{2,}")

    HINGLISH = {
        "hai", "ho", "kya", "yaar", "bhai", "nahi", "acha",
        "accha", "kar", "kr", "mera", "teri", "tum", "abhi",
        "bhot", "bahut", "fir", "phir", "kal", "haan", "nhi",
    }

    words = message.split()
    word_count = len(words)

    if existing_style:
        count = existing_style.get("message_count", 0) + 1
        avg_len = existing_style.get("avg_message_length", "short")

        # Recalculate average (rough)
        if count > 1:
            if word_count < 5:
                avg_len = "tiny"
            elif word_count < 12:
                avg_len = "short"
            elif word_count < 25:
                avg_len = "medium"
            else:
                avg_len = "long"
    else:
        count = 1
        if word_count < 5:
            avg_len = "tiny"
        elif word_count < 12:
            avg_len = "short"
        else:
            avg_len = "medium"

    uses_dragged = bool(DRAGGED.search(message))
    uses_hinglish = any(w.lower() in HINGLISH for w in words)
    emoji_matches = EMOJIS.findall(message)

    style_data = {
        "avg_message_length": avg_len,
        "uses_dragged_words": uses_dragged,
        "uses_hinglish": uses_hinglish,
        "common_emojis": ", ".join(emoji_matches[:5]) if emoji_matches else "",
        "message_count": count,
    }

    try:
        if existing_style:
            db.table("user_style").update(style_data).eq("user_id", user_id).execute()
        else:
            db.table("user_style").insert({
                "user_id": user_id,
                **style_data,
            }).execute()
    except Exception:
        pass


def generate_morning_nudge(user: dict) -> str:
    """Generate personalized morning nudge using user data."""
    db = get_supabase()
    user_id = user["id"]

    # Get yesterday's tracking
    from datetime import datetime, timedelta
    import pytz

    IST = pytz.timezone("Asia/Kolkata")
    yesterday = (datetime.now(IST) - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        tracking_res = (
            db.table("user_tracking")
            .select("*")
            .eq("user_id", user_id)
            .eq("date", yesterday)
            .single()
            .execute()
        )
        yesterday_data = tracking_res.data
    except Exception:
        yesterday_data = None

    # Build nudge context
    name = user.get("name", "friend")
    goal = user.get("fitness_goal", "")
    level = user.get("fitness_level", "")
    language = user.get("language", "Hinglish")

    yesterday_note = ""
    if yesterday_data:
        if yesterday_data.get("workout_done"):
            yesterday_note = "They worked out yesterday — acknowledge consistency."
        elif yesterday_data.get("sleep_hours") and yesterday_data["sleep_hours"] < 6:
            yesterday_note = "They slept less than 6 hours — be gentle."
        elif yesterday_data.get("mood_score") and yesterday_data["mood_score"] < 4:
            yesterday_note = "Mood was low yesterday — check in softly."

    system = f"""You are KIRO, sending a morning nudge on WhatsApp.
User: {name}. Goal: {goal or 'not set'}. Level: {level or 'not set'}.
Language: {language}.
{yesterday_note}

Rules:
- 2-3 bubbles max
- Each bubble under 12 words
- Sound like a friend texting, NOT an alarm
- Never say "good morning" boringly
- Reference their goals or yesterday if relevant
- Hinglish users: use Hinglish
- NO questions in morning nudges
- End with energy"""

    prompt = Prompt(
        system_prompt=system,
        user_message="Send morning nudge",
    )

    provider = LLMFactory.create()
    response = provider.generate(prompt)
    return response.content


def validate_response(text: str) -> list[str]:
    """Validate and split response into WhatsApp bubbles."""
    validator = ResponseValidator()
    return validator.validate(text)


def generate_weekly_report(user_id: str) -> str:
    """Generate weekly report using real tracking data."""
    db = get_supabase()

    # Get user
    try:
        user_res = db.table("users").select("*").eq("id", user_id).single().execute()
        user = user_res.data
    except Exception:
        return "Couldn't generate report."

    # Get 7 days tracking
    try:
        tracking_res = (
            db.table("user_tracking")
            .select("*")
            .eq("user_id", user_id)
            .order("date", desc=True)
            .limit(7)
            .execute()
        )
        tracking = tracking_res.data or []
    except Exception:
        tracking = []

    tracking_summary = _build_tracking_summary(tracking)

    # Count workouts
    workouts = [t for t in tracking if t.get("workout_done")]
    workout_days = len(workouts)

    # Avg sleep
    sleeps = [t["sleep_hours"] for t in tracking if t.get("sleep_hours")]
    avg_sleep = sum(sleeps) / len(sleeps) if sleeps else 0

    # Total spend
    spends = [t["spent_today"] for t in tracking if t.get("spent_today") is not None]
    total_spent = sum(spends)

    # Avg mood
    moods = [t["mood_score"] for t in tracking if t.get("mood_score") is not None]
    avg_mood = sum(moods) / len(moods) if moods else 0

    name = user.get("name", "friend")
    language = user.get("language", "Hinglish")

    system = f"""You are KIRO, generating a weekly report for {name}.
Language: {language}. Use WhatsApp bubble format (double newlines).

DATA:
Workouts this week: {workout_days}/7
Average sleep: {avg_sleep:.1f} hours
Total spending: ₹{total_spent:.0f}
Average mood: {avg_mood:.1f}/10

Detailed tracking:
{tracking_summary}

Rules:
- 4-6 bubbles max
- Start with a vibe check (excited/proud/concerned based on data)
- Cover: fitness, sleep, money, mood — each as its own bubble
- End with ONE specific suggestion for next week
- Be honest but encouraging
- Never generic. Reference actual numbers.
- Hinglish if that's their language"""

    prompt = Prompt(
        system_prompt=system,
        user_message="Generate weekly report",
    )

    provider = LLMFactory.create()
    response = provider.generate(prompt)
    return response.content