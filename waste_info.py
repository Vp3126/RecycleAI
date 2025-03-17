# Define waste categories and their information
waste_categories = {
    "plastic": {
        "characteristics": [
            "Lightweight and durable",
            "Often has recycling symbol (1-7)",
            "Common examples: bottles, containers, packaging"
        ],
        "recycling_instructions": """
        **How to recycle plastic:**
        1. Check the recycling number (1-7) on the bottom
        2. Rinse the container to remove food residue
        3. Remove caps and lids (these can often be recycled separately)
        4. Place in appropriate recycling bin
        
        **Note:** Not all types of plastic are recyclable in all areas. Check your local recycling guidelines.
        """
    },
    "glass": {
        "characteristics": [
            "Hard, brittle, transparent material",
            "Common examples: bottles, jars, containers",
            "Heavy compared to plastic of same size"
        ],
        "recycling_instructions": """
        **How to recycle glass:**
        1. Rinse thoroughly to remove food or drink residue
        2. Remove lids and caps (recycle separately)
        3. Sort by color if required by your local recycling program
        4. Place in appropriate recycling bin
        
        **Note:** Window glass, mirrors, and drinking glasses often have different compositions and may not be recyclable with container glass.
        """
    },
    "metal": {
        "characteristics": [
            "Shiny, malleable materials",
            "Common examples: aluminum cans, tin cans, foil",
            "Magnetic (except aluminum)"
        ],
        "recycling_instructions": """
        **How to recycle metal:**
        1. Rinse containers to remove food residue
        2. Crush cans to save space (optional)
        3. For aluminum foil, clean and ball up pieces
        4. Place in appropriate recycling bin
        
        **Note:** Metal is one of the most valuable recyclable materials and can be recycled indefinitely without loss of quality.
        """
    },
    "paper": {
        "characteristics": [
            "Thin, flexible material made from wood pulp",
            "Common examples: newspapers, cardboard, office paper",
            "Often tears rather than stretches"
        ],
        "recycling_instructions": """
        **How to recycle paper:**
        1. Keep paper clean and dry
        2. Remove any plastic wrapping, tape, or metal fasteners
        3. Flatten cardboard boxes
        4. Place in appropriate recycling bin
        
        **Note:** Shredded paper can be recycled but should be kept separate from other paper products. Paper contaminated with food (like pizza boxes) generally cannot be recycled.
        """
    },
    "organic": {
        "characteristics": [
            "Biodegradable natural materials",
            "Common examples: food scraps, yard waste, wood",
            "Will decompose naturally over time"
        ],
        "recycling_instructions": """
        **How to handle organic waste:**
        1. Separate food scraps from other waste
        2. Compost in a home compost bin or garden
        3. Use municipal organic waste collection if available
        4. Consider vermicomposting for apartment living
        
        **Note:** Composting organic waste reduces methane emissions from landfills and creates nutrient-rich soil for gardening.
        """
    },
    "e-waste": {
        "characteristics": [
            "Electronic devices and components",
            "Common examples: phones, computers, batteries, cables",
            "Often contains valuable materials as well as hazardous components"
        ],
        "recycling_instructions": """
        **How to recycle e-waste:**
        1. Never put electronics in regular trash or recycling bins
        2. Back up and wipe personal data from devices
        3. Take to designated e-waste recycling centers
        4. Some retailers and manufacturers offer take-back programs
        
        **Note:** E-waste contains valuable metals as well as hazardous materials. Proper recycling prevents toxic substances from entering the environment and recovers valuable resources.
        """
    }
}

def get_recycling_instructions(waste_type):
    """
    Get recycling instructions for a specific waste type
    
    Args:
        waste_type: String representing waste category
    
    Returns:
        String with recycling instructions
    """
    if waste_type in waste_categories:
        return waste_categories[waste_type]["recycling_instructions"]
    else:
        return "No specific recycling instructions available for this type of waste."
