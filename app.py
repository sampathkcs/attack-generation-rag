import streamlit as st
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
import pandas as pd

def generate_cyber_attack_descriptions(example_attack, num_attacks):
    """
    Generate similar cyber attack descriptions based on a given example.
    
    Args:
    example_attack (str): A base example of a cyber attack description.
    num_attacks (int): Number of similar attack descriptions to generate.
    
    Returns:
    list: A list of generated cyber attack descriptions.
    """
    # Ensure your OpenAI API key is set in your environment or within your application configuration
    openai_api_key = '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'
    
    # Construct the prompt
    prompt = f'''Generate {num_attacks} realistic cyber attack descriptions for vehicles similar to the below example with at least 20 words :
    

Example:
{example_attack}

1.
'''
    
    # Request the generation of attack descriptions
    client = OpenAI(api_key = openai_api_key)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Adjust the model version as needed
        prompt=prompt,
        temperature=0.7,  # Adjust for creativity. Lower is more deterministic.
        max_tokens=150 * num_attacks,  # Adjust based on desired length of responses
        n=num_attacks,  # Number of responses (each with multiple attack descriptions)
        stop="2."  # Stops generating more text at each new line, to separate the attacks
    )
    
    # Extract and return the generated descriptions as a list
    # Splitting responses into individual attacks
    # print(response.choices[0].text)
    # print(type(response.choices))
    # generated_attacks = response["choices"]
    generated_attacks = [choice.text for choice in response.choices]
    print(len(generated_attacks))
    attacks = []
    for i, text in enumerate(generated_attacks):
        attacks.append({
                        "id":i,
                        "text":text
                      })
    return attacks  # Filtering out empty strings





# load from disk
st.session_state.vector_store = Chroma(persist_directory="data/vector_store/attacks_vector_store_db", embedding_function=FastEmbedEmbeddings())

st.session_state.retriever = st.session_state.vector_store.as_retriever(
                        search_type="similarity_score_threshold",
                        search_kwargs={
                            "k": 3,
                            "score_threshold": 0.5,
                        },
                    )

df = pd.read_csv("data/tabular/Mitigation.csv",header=2)





# Set the page layout to wide mode for a full-screen effect
st.set_page_config(layout="wide")

# Load and display an image
logo_path = "logo\logo.png"  # Path to your logo image
logo = st.image(logo_path, width=300)  # You can adjust the width to fit your layout

# Streamlit interface
st.title('🔒 Threat Scenario Generator')
st.write('🔍 Enter an example cyber attack and specify how many similar descriptions you want to generate.')

# Default example for the text area
default_example = "Attacker uses the OBD port and Local Diagnostics Write Function to Modify Existing ECU Firmware or configuration to alter availability of PII or vehicle configuration to compromise availability"

# User inputs
example_attack = st.text_area("📝 Enter example cyber attack description", value=default_example, height=150)
num_attacks = st.number_input("🔢 Number of attacks to generate", min_value=1, max_value=10, value=3)

# Button to trigger generation
st.session_state.drop_down_list=[]
if st.button('🚀 Generate Attacks'):
    if example_attack and num_attacks:
        attack_descriptions = generate_cyber_attack_descriptions(example_attack, num_attacks)
        if attack_descriptions:
            st.write("📄 Generated Attack Descriptions:")
            print(attack_descriptions)
            for i, desc in enumerate(attack_descriptions, start=1):
                st.text_area(f"🔹 Attack {i}", value=desc["text"], height=100)
                st.session_state.drop_down_list.append(desc["text"])

            
        else:
            st.error("🚫 Failed to generate descriptions. Please try again.")
    else:
        st.error("❗ Please enter a valid example and number of attacks to generate.")





# mitigation
st.title('🔒 Threat Mitigation')
# selected_dec = st.text_input("Enter generated attack description")

if len(st.session_state.drop_down_list)>0:
    selected_dec = attack_descriptions[0]["text"].strip()
    st.write(selected_dec)

    st.write()
    # st.write("Retreved Docs")
    docs = st.session_state.retriever.invoke(selected_dec)
    # st.write(docs)
    # st.write(docs[0].page_content.strip())

    most_similar = docs[0].page_content.strip().lower().replace(" ","").replace('\n','')
    print(most_similar)
    # Applying strip and lower to 'Column'
    df['Threat_Description'] = df['Threat_Description'].str.strip().str.lower().str.replace(" ","").str.replace('\n','')
    # st.write(most_similar)
    # st.write(df)
    st.subheader("Most Similar Result and Mitigation Action")
    # st.write(df[df["Threat_Description"]==most_similar])
    threat_col = "Threat_Description"
    mitigation_col = "Mitigation"

    matched_row = df[df[threat_col] == most_similar]  # Use 'page_content' as defined in 'docs_new'
    if not matched_row.empty:
        mitigation_measure = matched_row['Mitigation'].iloc[0]  # Assuming 'Mitigation' is the correct column name for the mitigation measures
        st.subheader(f"Mitigation: {mitigation_measure}")
    else:
        st.write("No matching threat description found in the CSV.")




