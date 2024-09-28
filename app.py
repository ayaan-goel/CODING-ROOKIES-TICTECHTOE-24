import streamlit as st
from langchain_community.llms import OpenAI
import requests

# Define your Gemini API key
GEMINI_API_KEY = "AIzaSyBgzo4fpUEQKN5ZltUq3kG_51T_ZdmA-Vs"

# Helper function to call the Gemini API
def get_gift_recommendations(occasion, relationship, age, gender, interests, budget):
    payload = {
        "occasion": occasion,
        "relationship": relationship,
        "age": age,
        "gender": gender,
        "interests": interests,
        "budget": budget
    }
    
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post('https://actual-gemini-api-endpoint.com/suggest-gifts', json=payload, headers=headers)


    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch gift recommendations"}

# Streamlit UI
st.title("Gift Finder Chatbot")
st.write("I'll help you find the perfect, personalized gift for that special person in your life.")
st.write("Just a quick round of questions and voila - the dream gift will be at your fingertips!")

# First question: Occasion
occasion = st.selectbox(
    "What's the special occasion?",
    [
        "Boss's Day (Oct 14, 2024)", "Diwali (Oct 29, 2024)", "Halloween (Oct 31, 2024)", "Birthday", 
        "Anniversary", "Housewarming", "Graduation", "Wedding", "Engagement", "Retirement", 
        "Bridal Shower", "Wedding Shower", "Baby Shower", "Quinceañera", "Bat Mitzvah", 
        "Bar Mitzvah", "Bachelor Party", "Bachelorette Party", "Baptism", "New Job", 
        "Promotion", "Work Anniversary", "Get Well", "Sympathy", "Thank You", "Host", 
        "Hostess", "Holiday", "Christmas (Dec 25, 2024)", "Valentine's Day (Feb 14, 2025)", 
        "Mother's Day (May 11, 2025)", "Father's Day (Jun 15, 2025)", "New Year's (Jan 1, 2025)", 
        "Easter (Apr 6, 2025)", "Thanksgiving (Nov 28, 2024)", "Memorial Day (May 26, 2025)", 
        "Purim (Mar 21, 2025)", "Hanukkah (Dec 2, 2024)", "Rosh Hashanah (Sep 28, 2025)", 
        "Passover (Apr 12, 2025)", "Eid (Apr 22, 2025)", "Ramadan (Mar 31, 2025)", 
        "Secret Santa (Dec 24, 2024)", "White Elephant"
    ]
)

# Second question: Relationship
relationship = st.selectbox(
    "Who's the lucky individual deserving of this fabulous gift?",
    [
        "Friend", "Friends", "Best Friend", "Myself", "Wife", "Girlfriend", "Husband", 
        "Boyfriend", "Fiance", "Parents", "Mom", "Dad", "Grandparents", "Grandma", "Grandpa", 
        "Son", "Sons", "Daughter", "Daughters", "Brother", "Brothers", "Sister", "Sisters", 
        "Siblings", "Aunt", "Uncle", "Cousin", "Niece", "Nephew", "Teacher", "Employee", 
        "Employees", "Coworker", "Coworkers", "Boss", "Client", "Clients", "Neighbor", 
        "Neighbors", "Groomsmen", "Bridesmaid", "Coach", "Nurse"
    ]
)

# Third question: Age
age = st.selectbox(
    "Time to spill the beans, how old are they?",
    [
        "60+: Senior", "40-60: Middle Age", "26-40: Adult", "18-25: Young Adult", 
        "12-18: Teen", "4-12: Child", "2-4: Preschool", "0-2: Toddler"
    ]
)

# Fourth question: Gender
gender = st.selectbox(
    "Do you mind sharing their gender?",
    [
        "Male", "Female", "Other", "Prefer not to say"
    ]
)

# Fifth question: Interests
interests = st.multiselect(
    "What are some interests and hobbies that make them smile?",
    [
        "Tech and Gadgets", "Food", "Drinks", "Snacks & Sweets", "Movies and TV", "Music", 
        "Clothing and Accessories", "Beauty", "Sports and Activities", "Pets", "Health and Wellness", 
        "Reading", "Cooking", "Home Decor and Improvement", "Games and Puzzles", "Outdoors", 
        "Art and Design"
    ]
)

# Sixth question: Budget
budget = st.selectbox(
    "Last but not least, how much are you willing to spend on this spectacular gift?",
    [
        "Rs10-25", "Rs25-50", "Rs50-100", "Rs100-200", "Rs200-300", "Rs300-500", "Rs500-1,000"
    ]
)

# When user is done selecting, call Gemini API
if st.button("Suggest Gifts"):
    with st.spinner("Finding the perfect gift..."):
        result = get_gift_recommendations(occasion, relationship, age, gender, interests, budget)

        if "error" not in result:
            st.success("Here are some personalized gift suggestions!")
            st.write("### Personalized Gifts:")
            st.write(result)

            for gift in result['personalized']:
                st.write(f"- {gift['name']} (Amazon link: {gift['url']})")
            
            st.write("### Trending Gifts:")
            for gift in result['trending']:
                st.write(f"- {gift['name']} (Amazon link: {gift['url']})")

            st.write("### Best-Sellers:")
            for gift in result['best_sellers']:
                st.write(f"- {gift['name']} (Amazon link: {gift['url']})")
        else:
            st.error("Failed to get gift suggestions. Please try again.")

