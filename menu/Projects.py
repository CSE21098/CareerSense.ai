import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Custom CSS to remove violet outline and change color
custom_css = """
<style>
div.stTextInput > div > input {
    border: 2px solid #d9d9d9 !important;
    border-radius: 4px !important;
    padding: 8px !important;
    width: 100% !important;
    box-shadow: none !important;
}

div.stTextInput > div > input:focus {
    border: 2px solid #FF0000 !important;  /* Red border when focused */
    outline: none !important;  /* Remove default outline */
    box-shadow: 0px 0px 5px rgba(255, 0, 0, 0.5) !important;  /* Optional red shadow effect */
}

</style>

<script>
const observer = new MutationObserver(() => {
    const inputField = document.querySelector('div.stTextInput > div > input');
    if (inputField) {
        inputField.style.borderColor = '#FF0000';  // Force border to red
        inputField.addEventListener('focus', () => {
            inputField.style.borderColor = '#FF0000';
        });
        inputField.addEventListener('blur', () => {
            inputField.style.borderColor = '#d9d9d9';
        });
    }
});

observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def main():
    st.markdown(custom_css, unsafe_allow_html=True)  # Inject the custom CSS

    st.markdown("<h1 style='text-align: center; color: black;'>Projects</h1>", unsafe_allow_html=True)
    
    st.write("Get your project idea here:")
    
    # Create a dropdown box for project type selection
    project_types = ["Project", "Research Paper"]
    selected_project_type = st.selectbox("Select your project type:", project_types)
    
    if selected_project_type == "Project":
        # Create a dropdown box for domain selection
        domains = ["Electrical Engineering", "Software Engineering", "Mechanical Engineering", "Civil Engineering", "Computer Science", "Other"]
        selected_domain = st.selectbox("Select your domain:", domains)
        
        # Generate a prompt based on the user's selection
        prompt = f"Generate project ideas for {selected_domain}."
        
        # Get response from Gemini API
        if st.button("Get Project Ideas"):
            with st.spinner("Fetching project ideas..."):
                try:
                    project_ideas = get_gemini_response(prompt)
                    st.markdown("### Project ideas for **" + selected_domain + "**:")
                    st.markdown(project_ideas)
                except Exception as e:
                    st.error(f"Failed to retrieve project ideas: {e}")
    else:
        st.write("Research paper ideas will be displayed here.")
        
        # Create a text box for user input
        user_input = st.text_input("Enter your research paper prompt:", placeholder="Type your research paper prompt here")
        
        if user_input and st.button("Get Research Paper Ideas"):
            prompt = f"Generate research paper ideas for the following prompt: {user_input}."
            with st.spinner("Fetching research paper ideas..."):
                try:
                    research_ideas = get_gemini_response(prompt)
                    st.write("### Research Papers:")
                    st.markdown(research_ideas)
                except Exception as e:
                    st.error(f"Failed to retrieve research paper ideas: {e}")

if __name__ == "__main__":
    main()
