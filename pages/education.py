import streamlit as st
from waste_info import waste_categories

st.set_page_config(
    page_title="Education - Waste Classification System",
    page_icon="♻️",
    layout="wide"
)

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Styled page title
st.markdown('<h1 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">📚 Waste Education Center</h1>', unsafe_allow_html=True)

# Main container with styled intro
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('''
<h2 style="color: #2E7D32; margin-bottom: 15px;">Learn About Waste Types and Recycling</h2>

<p style="font-size: 1.1rem; line-height: 1.6; color: #333; background-color: #f1f8e9; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50;">
    Proper waste sorting and recycling are essential for environmental sustainability. This guide explains different waste types, 
    how to identify them, and best practices for recycling each type.
</p>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create tabs for different waste categories
tabs = st.tabs(list(waste_categories.keys()))

# Fill each tab with educational content
for i, (category, info) in enumerate(waste_categories.items()):
    with tabs[i]:
        st.header(f"{category.capitalize()} Waste")
        
        # Two columns - one for characteristics, one for recycling
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("How to Identify")
            for char in info["characteristics"]:
                st.markdown(f"- {char}")
                
            st.subheader("Common Examples")
            if category == "plastic":
                st.markdown("""
                - Water and soda bottles (PET - Type 1)
                - Milk jugs and detergent bottles (HDPE - Type 2)
                - Food containers and packaging
                - Plastic bags and wraps
                - Toys and consumer goods
                """)
            elif category == "glass":
                st.markdown("""
                - Glass bottles (clear, green, brown)
                - Jars and containers
                - Glass food packaging
                - Beverage glasses
                - Decorative glass items
                """)
            elif category == "metal":
                st.markdown("""
                - Aluminum cans (soda, beer)
                - Tin cans (food packaging)
                - Aluminum foil and trays
                - Metal bottle caps
                - Hardware and tools
                """)
            elif category == "paper":
                st.markdown("""
                - Newspapers and magazines
                - Cardboard boxes
                - Office paper and envelopes
                - Paper bags
                - Books and notebooks
                """)
            elif category == "organic":
                st.markdown("""
                - Food scraps and leftovers
                - Fruit and vegetable peels
                - Coffee grounds and tea bags
                - Yard waste (leaves, grass)
                - Plant trimmings
                """)
            elif category == "e-waste":
                st.markdown("""
                - Mobile phones and computers
                - Televisions and monitors
                - Batteries and chargers
                - Cables and peripherals
                - Home electronics
                """)
        
        with col2:
            st.subheader("Recycling Instructions")
            st.markdown(info["recycling_instructions"])
            
            st.subheader("Environmental Impact")
            if category == "plastic":
                st.markdown("""
                **Improper disposal impacts:**
                - Takes 450+ years to decompose
                - Harms marine life when enters oceans
                - Releases microplastics into environment
                
                **Benefits of recycling:**
                - Reduces oil consumption (plastic production uses oil)
                - Decreases landfill waste
                - Lowers carbon emissions by 30-80% compared to new plastic
                """)
            elif category == "glass":
                st.markdown("""
                **Improper disposal impacts:**
                - Takes 1+ million years to decompose
                - Creates safety hazards in landfills
                - Wastes reusable material
                
                **Benefits of recycling:**
                - 100% recyclable indefinitely without quality loss
                - Saves energy (recycling uses 40% less energy than new glass)
                - Reduces mining for raw materials
                """)
            elif category == "metal":
                st.markdown("""
                **Improper disposal impacts:**
                - Takes 50-500 years to decompose
                - Mining for new metal causes environmental degradation
                - Wastes valuable resources
                
                **Benefits of recycling:**
                - Infinitely recyclable without quality loss
                - Saves up to 95% of energy compared to mining new metal
                - Reduces greenhouse gas emissions significantly
                """)
            elif category == "paper":
                st.markdown("""
                **Improper disposal impacts:**
                - Takes 2-6 weeks to decompose
                - Contributes to deforestation when new paper is produced
                - Creates methane in landfills when decomposing
                
                **Benefits of recycling:**
                - Saves trees (1 ton of recycled paper saves 17 trees)
                - Uses 40% less energy than making new paper
                - Reduces water pollution by 35%
                """)
            elif category == "organic":
                st.markdown("""
                **Improper disposal impacts:**
                - Creates methane (powerful greenhouse gas) in landfills
                - Takes up ~30% of landfill space
                - Wastes nutrients that could enrich soil
                
                **Benefits of composting:**
                - Creates nutrient-rich soil for gardening
                - Reduces methane emissions
                - Decreases need for chemical fertilizers
                """)
            elif category == "e-waste":
                st.markdown("""
                **Improper disposal impacts:**
                - Leaches toxic chemicals (lead, mercury) into soil and water
                - Causes health problems for communities near informal recycling sites
                - Wastes valuable rare earth elements and metals
                
                **Benefits of recycling:**
                - Recovers valuable materials (gold, silver, copper)
                - Prevents toxic elements from entering environment
                - Reduces need for destructive mining practices
                """)

# Add section on general recycling best practices
st.markdown("---")
st.header("General Recycling Best Practices")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("What Makes Something Recyclable?")
    st.markdown("""
    Whether an item is recyclable depends on several factors:
    
    1. **Material composition** - What the item is made of
    2. **Contamination level** - How clean the item is
    3. **Local facilities** - What your area can process
    4. **Market demand** - Whether there's demand for the recycled material
    
    Always check local recycling guidelines as they vary by location.
    """)
    
    st.subheader("The Recycling Process")
    st.markdown("""
    1. **Collection** - Items are collected from homes and businesses
    2. **Sorting** - Materials are separated by type (often using AI systems!)
    3. **Processing** - Materials are cleaned and prepared for manufacturing
    4. **Manufacturing** - Recycled materials become new products
    5. **Purchasing** - Consumers buy products made from recycled materials
    
    This completes the recycling loop, making it a truly circular process.
    """)

with col2:
    st.subheader("Common Recycling Mistakes")
    st.markdown("""
    Avoid these common mistakes that can contaminate recycling:
    
    - **Wishcycling:** Putting items in recycling hoping they're recyclable
    - **Not cleaning containers:** Food residue can contaminate entire batches
    - **Recycling plastic bags:** These jam sorting machines (return to stores instead)
    - **Including small items:** Items smaller than a credit card fall through sorting machines
    - **Leaving caps on bottles:** Different materials need separate processing
    """)
    
    st.subheader("Reduce, Reuse, Recycle Hierarchy")
    st.markdown("""
    Remember that recycling is just one part of sustainable waste management:
    
    1. **Reduce:** Best option - avoid creating waste in the first place
    2. **Reuse:** Second best - use items multiple times before discarding
    3. **Recycle:** Third best - process items into new materials
    
    Following this hierarchy maximizes environmental benefits.
    """)

st.markdown("---")
st.markdown("♻️ Waste Classification System - Powered by AI")
