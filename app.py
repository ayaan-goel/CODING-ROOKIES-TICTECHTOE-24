import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI

# Set page configuration
st.set_page_config(page_title="AI Gift Suggestion Bot", page_icon="🎁", layout="wide")

# Initialize Google Gemini LLM with API key
google_api_key = "AIzaSyDX7iqE8XTN8npHp9jKZST8HMfZS4ncNpg"
llm = GoogleGenerativeAI(temperature=0.1, google_api_key=google_api_key, model="gemini-pro")

# Define LangChain prompts
gift_prompt = PromptTemplate(
    input_variables=['occasion', 'relationship', 'age', 'gender', 'interests', 'budget'],
    template=(
        "Suggest gifts for the following criteria: "
        "Occasion: {occasion}, Relationship: {relationship}, Age: {age}, "
        "Gender: {gender}, Interests: {interests}, Budget: {budget}. "
        "Please provide a list of suitable gifts."
    )
)

# Create LangChain chain
gift_suggestion_chain = LLMChain(llm=llm, prompt=gift_prompt, verbose=True, output_key='gift_suggestions')

# Simulated function to fetch links from Amazon/eBay based on gift suggestions
def fetch_links(gift_suggestions):
    links_data = {
        "Wireless Earbuds": {
            "amazon": "https://www.amazon.com/dp/B07T81554H",
            "ebay": "https://www.ebay.com/itm/303665593415"
        },
        "Smart Watch": {
            "amazon": "https://www.amazon.com/dp/B07YFKC8MD",
            "ebay": "https://www.ebay.com/itm/283937153017"
        },
        "Bluetooth Speaker": {
            "amazon": "https://www.amazon.com/dp/B082T3F3NT",
            "ebay": "https://www.ebay.com/itm/254821716151"
        }
        # Add more simulated data here
    }

    # Create a list of links for Amazon and eBay
    amazon_links = []
    ebay_links = []

    for gift in gift_suggestions:
        if gift in links_data:
            amazon_links.append((gift, links_data[gift]["amazon"]))
            ebay_links.append((gift, links_data[gift]["ebay"]))

    # Sort by alphabetical order
    amazon_links = sorted(amazon_links, key=lambda x: x[0])
    ebay_links = sorted(ebay_links, key=lambda x: x[0])

    return amazon_links, ebay_links

# Streamlit UI
st.title('AI Gift Suggestion Bot 🎁')

# Input fields for user to provide preferences
occasion = st.selectbox('Select Occasion:', ['Birthday', 'Anniversary', 'Wedding', 'Graduation', 'Holiday', 'Other'])
relationship = st.selectbox('Select Relationship:', ['Friend', 'Family', 'Partner', 'Colleague', 'Other'])
age = st.number_input('Enter Age:', min_value=1, max_value=120)
gender = st.selectbox('Select Gender:', ['Male', 'Female', 'Other'])
interests = st.text_input('Enter Interests (e.g., Sports, Music, Tech, etc.):')
budget = st.number_input('Enter Budget (in $):', min_value=1)

# Button to get suggestions
if st.button('Get Gift Suggestions'):
    try:
        # Call the LangChain model for AI-based suggestions
        inputs = {
            'occasion': occasion,
            'relationship': relationship,
            'age': age,
            'gender': gender,
            'interests': interests,
            'budget': budget
        }
        output = gift_suggestion_chain(inputs)

        # Display final AI-generated suggestions
        gift_suggestions = output['gift_suggestions'].split(', ')
        st.subheader('AI Gift Suggestions:')
        
        # Create columns for card display
        cols = st.columns(3)  # Adjust the number of columns based on your layout preference
        
        for idx, gift in enumerate(gift_suggestions):
            with cols[idx % 3]:  # Distribute gifts across columns
                st.markdown(f"### {gift}")
                st.markdown("#### Buy Links:")
                
                # Fetch links for the current gift
                amazon_link, ebay_link = fetch_links([gift])
                
                if amazon_link:
                    st.markdown(f"[Amazon]({amazon_link[0][1]})")
                if ebay_link:
                    st.markdown(f"[eBay]({ebay_link[0][1]})")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Fill in the details to get gift suggestions.")
