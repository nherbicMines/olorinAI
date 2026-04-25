import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an AI assistant that generates structured D&D NPC data.

You MUST return valid JSON only. Do not include any extra text.

The JSON must follow this schema:

{
  "npc": {
    "name": "",
    "gender": "",
    "species": "",
    "occupation": "",
    "location": "",
    "personality": "",
    "bonds": "",
    "secrets": "",
    "involvedPlots": []
  },
  "statblock": {
    "level": "",
    "role": "",
    "strength": "",
    "dexterity": "",
    "constitution": "",
    "intelligence": "",
    "wisdom": "",
    "charisma": ""
  },
  "gossip": [
    ""
  ]
}

Rules:
- NPC must fit within provided world lore if available, otherwise default to a Forgotten Realms fantasy setting
- Scale statblock appropriately to the NPC's role
- Gossip may reference other NPCs if provided
- Secrets should not be obvious from personality
- Keep responses concise but flavorful
"""

def extract_json(text):
    try:
        # Remove markdown code fences like ```json ... ```
        cleaned = re.sub(r"```json|```", "", text).strip()

        # Extract JSON object
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        raise ValueError("No JSON object found")

    except Exception as e:
        print("Failed to parse JSON:", e)
        return None

def load_json(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def summarize_world(world_lore):
    return json.dumps(world_lore, indent=2)[:1000]  # truncate for safety

def summarize_npcs(npcs):
    return json.dumps(npcs, indent=2)[:1000] # truncate for safety

def retrieve_relevant_npcs(query, npcs):
    results = []

    for npc in npcs:
        if any(word in npc["occupation"].lower() for word in query.lower().split()):
            results.append(npc)

    return results[:5]  # limit to avoid token bloat

def append_npc(npc_data):
    npcs = load_json("npcs.json")
    npcs.append(npc_data)
    save_json("npcs.json", npcs)

def generate_npc(user_input, world_lore, npcs, mode):
    relevant_npcs = retrieve_relevant_npcs(user_input, npcs)

    world_lore_snippet = summarize_world(world_lore)
    npc_snippet = summarize_npcs(relevant_npcs)

    if mode == "add":
        instruction = "Convert the user description into a structured NPC. Do not invent major new traits."
    else:
        instruction = "Creatively generate a new NPC based on the request."

    prompt = f"""
World Lore:
{world_lore_snippet}

Existing NPCs:
{npc_snippet}

User Instruction:
{instruction}

User Request:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("1) Add pre-existing NPC")
    print("2) Generate new NPC")

    choice = input("Select an option: ")
    user_input = input("Describe the NPC: ")

    world_lore = load_json("worldLore.json")
    npcs = load_json("npcs.json")

    if choice == "1":
        # treat as structured generation from description
        result = generate_npc(user_input, world_lore, npcs, mode="add")

    elif choice == "2":
        result = generate_npc(user_input, world_lore, npcs, mode="generate")

    else:
        print("Invalid option")
        exit()
    parsed = json.loads(result)

    print("\nGenerated NPC:\n")
    print(json.dumps(parsed, indent=2))

    save = input("\nSave this NPC? (y/n): ")

    if save.lower() == "y":
        append_npc(parsed["npc"])

        stats = load_json("npc_stats.json")
        stats.append({
            "name": parsed["npc"]["name"],
            "statblock": parsed["statblock"]
        })
        save_json("npc_stats.json", stats)

        print("NPC saved.")