# Define waste categories and their information
waste_categories = {
    "plastic": {
        "description": "Plastic waste includes various types of plastic materials like bottles, containers, packaging, and other plastic items.",
        "characteristics": [
            "Often colorful and shiny",
            "Lightweight",
            "Water-resistant",
            "Can be transparent or opaque"
        ],
        "recycling_instructions": """
1. Clean the plastic item thoroughly
2. Remove any labels or caps
3. Check the recycling number (1-7) on the item
4. Place in the recycling bin
5. Do not include plastic bags or film
        """
    },
    "glass": {
        "description": "Glass waste includes bottles, jars, and other glass containers.",
        "characteristics": [
            "Transparent or colored",
            "Heavy and breakable",
            "Smooth surface",
            "Can be clear or tinted"
        ],
        "recycling_instructions": """
1. Remove any caps or lids
2. Clean the glass container
3. Place in the glass recycling bin
4. Do not include broken glass
5. Separate by color if required
        """
    },
    "metal": {
        "description": "Metal waste includes aluminum cans, steel containers, and other metal items.",
        "characteristics": [
            "Shiny or metallic appearance",
            "Heavy",
            "Magnetic (steel) or non-magnetic (aluminum)",
            "Often cylindrical or rectangular"
        ],
        "recycling_instructions": """
1. Clean the metal container
2. Remove any labels
3. Crush cans if possible
4. Place in metal recycling bin
5. Separate aluminum from steel if required
        """
    },
    "paper": {
        "description": "Paper waste includes newspapers, magazines, cardboard, and other paper products.",
        "characteristics": [
            "Lightweight",
            "Can be white or colored",
            "Often printed",
            "Can be flat or folded"
        ],
        "recycling_instructions": """
1. Remove any plastic or metal parts
2. Flatten cardboard boxes
3. Keep paper dry and clean
4. Place in paper recycling bin
5. Do not include soiled or wet paper
        """
    },
    "organic": {
        "description": "Organic waste includes food scraps, yard waste, and other biodegradable materials.",
        "characteristics": [
            "Natural materials",
            "Biodegradable",
            "Often moist or wet",
            "Can have strong odors"
        ],
        "recycling_instructions": """
1. Separate from other waste
2. Keep in a compost bin
3. Mix with dry materials
4. Turn regularly
5. Use for gardening or disposal
        """
    },
    "e-waste": {
        "description": "Electronic waste includes old electronics, batteries, and other electronic devices.",
        "characteristics": [
            "Contains electronic components",
            "Often contains hazardous materials",
            "Complex structure",
            "May contain batteries"
        ],
        "recycling_instructions": """
1. Remove batteries if possible
2. Wipe personal data
3. Take to e-waste collection center
4. Do not dispose in regular trash
5. Follow local e-waste guidelines
        """
    }
}

def get_recycling_instructions(category):
    """
    Get recycling instructions for a specific waste category
    """
    if category in waste_categories:
        return waste_categories[category]["recycling_instructions"]
    return "Please check local recycling guidelines for proper disposal."
