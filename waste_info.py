# Define waste categories and their information
waste_categories = {
    "plastic": {
        "characteristics": [
            "Lightweight and durable",
            "Often has recycling symbol (1-7)",
            "Common examples: bottles, containers, packaging"
        ],
        "description": """
        Plastic is a synthetic material made from polymers. It's widely used for packaging, household items, and many consumer products. There are different types of plastics (identified by numbers 1-7), each with different properties and recycling possibilities.
        
        Most common types include:
        • PET (1): Water bottles, soft drink bottles
        • HDPE (2): Milk jugs, detergent bottles
        • PVC (3): Pipes, shower curtains
        • LDPE (4): Plastic bags, food wrap
        • PP (5): Yogurt containers, bottle caps
        • PS (6): Disposable cups, packaging
        • Other (7): Various mixed plastics
        """,
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
        "description": """
        Glass is made primarily from sand (silica), soda ash, and limestone. It's 100% recyclable and can be recycled endlessly without loss in quality or purity. Glass containers come in various colors including clear, green, and amber (brown).
        
        Glass is non-porous and impermeable, making it ideal for food and beverage storage. Unlike plastic, glass doesn't leach chemicals into its contents and provides a superior shelf life for many products.
        
        Glass recycling saves energy, reduces raw material use, and lessens the burden on landfills. Recycled glass (cullet) is crushed and mixed with raw materials to make new glass products.
        """,
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
        "description": """
        Metal waste consists primarily of aluminum, steel, and other metallic materials. Metals are highly valuable recyclable materials that can be recycled repeatedly without degrading their quality. Common household metal waste includes food and beverage cans, aluminum foil, metal bottle caps, and aerosol cans.
        
        Aluminum recycling is particularly valuable, as it saves up to 95% of the energy required to produce new aluminum from raw materials. Steel is the most recycled material in the world by weight, with products like cans, appliances, and construction materials routinely converted into new steel products.
        
        Metals can be separated from other recyclables using magnets (for ferrous metals like steel) or eddy current separators (for non-ferrous metals like aluminum).
        """,
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
        "description": """
        Paper is made from processed wood pulp and plant fibers. It's one of the most commonly recycled materials worldwide. Paper products include newspapers, magazines, office paper, cardboard, paperboard (cereal boxes, etc.), and mixed paper.
        
        Recycling paper conserves natural resources, saves energy, reduces greenhouse gas emissions, and keeps material out of landfills. Paper can typically be recycled 5-7 times before the fibers become too short to make new paper.
        
        Different types of paper products may require different recycling processes. Cardboard and paperboard are often recycled separately from other paper products due to their different compositions and processing requirements.
        """,
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
        "description": """
        Organic waste includes any material that comes from plants or animals and can be broken down by microorganisms. Common examples include food scraps, yard trimmings, agricultural waste, and some paper products. Organic materials make up a significant portion of household waste.
        
        When organic waste goes to landfills, it decomposes without oxygen (anaerobically), producing methane, a potent greenhouse gas. Proper disposal through composting or organic waste collection allows these materials to decompose aerobically, producing nutrient-rich compost instead of harmful gases.
        
        Composting organic waste creates a valuable soil amendment that improves soil structure, provides nutrients to plants, and reduces the need for chemical fertilizers. Many communities now offer curbside organic waste collection programs in addition to traditional recycling.
        """,
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
        "description": """
        Electronic waste or e-waste refers to discarded electrical or electronic devices. This is the fastest-growing waste stream globally, with millions of tons generated annually. E-waste includes computers, televisions, smartphones, tablets, printers, and other electronic equipment.
        
        E-waste contains valuable materials like gold, silver, copper, and rare earth elements that can be recovered through recycling. However, it also contains hazardous materials like lead, mercury, cadmium, and flame retardants that can harm human health and the environment if improperly handled.
        
        Proper e-waste recycling involves specialized processes to safely recover valuable materials while properly containing hazardous substances. Many manufacturers and retailers offer take-back programs, and communities typically have designated e-waste collection events or drop-off locations.
        """,
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
