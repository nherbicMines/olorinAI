# olorinAI
A Python CLI tool which utilized RAG-Powered AI to generate and track a network of NPCs for the user's D&D or other TTRPG campaign.

User should first input any information about their world lore for the AI to be aware of in worldLore.json (e.g. Aasimar are extinct). Upon running main.py, Olorin will prompt the user asking if they wish to generate an NPC or add a pre-existing NPC to the local data. 
If the user wishes to add a pre-existing NPC from their world, they will enter a brief description of the NPC. Olorin will save this NPC to npcs.json to potentially be used when generating a new NPC.
>Example prompt: A Dryad Witherbloom professor of decay named Yedora. She is secretly involved in the Oriq plot, but is helping out the players' investigation in an attempt to steer them in the wrong direction."
If the user wishes to generate a new NPC, they will enter what they need and Olorin will generate and output an NPC with the details in the following example, and may choose to involve an existing NPC in gossip either known by or involving this NPC. The qualitative details of the NPC will be saved in npcs.json (if the user confirms they want that) to potentially reference for future NPCs later. To be more efficient with token usage, the statblock for this NPC will be saved separately in npc_stats.json. This will not be pulled when calling to the OpenAI API, and will only be printed to the end-user.
>Example prompt: A magic store owner in the large city nearby Strixhaven
>Example output:
```
Generated NPC:


==================================================
Name: Maribel Tangrin
==================================================
Species: halfling
Gender: female
Occupation: Owner of Tangrin's Trinkets and Arcana
Location: City of Althoria, near Strixhaven University

Personality:
Cheerful and shrewd, Maribel has a knack for reading people and uncovering hidden desires. She enjoys bartering and telling small tales, always with a twinkle in her eye.

Bonds:
Has a long-standing friendly rivalry with several other merchants in Althoria; secretly seeks rare magical artifacts for her personal collection.

Secrets:
Maribel occasionally deals in forbidden magical items and smuggles minor contraband to discreet clients, including some connected to the Oryx cult.

Involved Plots:
None

Statblock:
 Level: 3
 Role: Merchant/Informant
 Strength: 8
 Dexterity: 14
 Constitution: 10
 Intelligence: 13
 Wisdom: 12
 Charisma: 16

Gossip:
 - Maribel's new shipment of strange, shimmering trinkets has the alchemists at Lorehold whispering.
 - Some say Maribel has a secret backroom where rare magical artifacts disappear and reappear at unusual prices.
 - Rumor has it Maribel once helped a Silverquill student acquire a banned spell scroll under the table.
==================================================
```
