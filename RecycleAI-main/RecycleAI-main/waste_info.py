# Waste categories and their information
waste_categories = {
    'cardboard': {
        'description': 'Cardboard is a thick paper material that can be recycled into new cardboard products.',
        'characteristics': [
            'Brown or gray in color',
            'Thick, rigid material',
            'Often has corrugated layers',
            'Commonly used for boxes and packaging'
        ],
        'recycling_instructions': """
        1. Flatten cardboard boxes to save space
        2. Remove any non-cardboard materials (tape, labels, etc.)
        3. Keep cardboard dry and clean
        4. Place in recycling bin or take to recycling center
        """
    },
    'glass': {
        'description': 'Glass containers can be recycled indefinitely without losing quality.',
        'characteristics': [
            'Transparent or colored',
            'Hard and brittle',
            'Smooth surface',
            'Commonly used for bottles and jars'
        ],
        'recycling_instructions': """
        1. Rinse containers to remove residue
        2. Remove lids and caps
        3. Handle with care to avoid breakage
        4. Place in glass recycling bin
        """
    },
    'metal': {
        'description': 'Metal items like aluminum cans and steel containers are highly recyclable.',
        'characteristics': [
            'Metallic appearance',
            'Conducts heat and electricity',
            'Often magnetic',
            'Commonly used for cans and containers'
        ],
        'recycling_instructions': """
        1. Rinse containers to remove residue
        2. Remove labels if possible
        3. Crush cans to save space
        4. Place in metal recycling bin
        """
    },
    'paper': {
        'description': 'Paper products can be recycled into new paper items.',
        'characteristics': [
            'Thin, flexible material',
            'Various colors and textures',
            'Can be written or printed on',
            'Commonly used for documents and packaging'
        ],
        'recycling_instructions': """
        1. Remove any non-paper materials
        2. Keep paper dry and clean
        3. Sort by type if required
        4. Place in paper recycling bin
        """
    },
    'plastic': {
        'description': 'Plastic items can be recycled into new plastic products.',
        'characteristics': [
            'Lightweight and flexible',
            'Various colors and transparency',
            'Often has recycling symbol',
            'Commonly used for containers and packaging'
        ],
        'recycling_instructions': """
        1. Check recycling symbol and local guidelines
        2. Rinse containers to remove residue
        3. Remove caps and labels if required
        4. Place in plastic recycling bin
        """
    },
    'trash': {
        'description': 'Non-recyclable waste that should be disposed of properly.',
        'characteristics': [
            'Contaminated materials',
            'Mixed waste items',
            'Non-recyclable materials',
            'Often contains food waste or hazardous materials'
        ],
        'recycling_instructions': """
        1. Separate any recyclable materials
        2. Ensure proper disposal of hazardous materials
        3. Use appropriate waste bin
        4. Follow local waste disposal guidelines
        """
    }
}

def get_recycling_instructions(category):
    """Get recycling instructions for a specific waste category"""
    if category in waste_categories:
        return waste_categories[category]['recycling_instructions']
    return "Category not found. Please check local recycling guidelines."
