# import azure.functions as func
# from openai import OpenAI
# import pandas as pd
# import logging
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import FastEmbedEmbeddings

# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# @app.route(route="retrieve_mitigation", methods=["POST"])
# def retrieve_mitigation(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Processing request to retrieve mitigation actions.')

#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid request body.", status_code=400)

#     selected_attack = req_body.get("selected_attack")
#     if not selected_attack:
#         return func.HttpResponse("Missing 'selected_attack' in request.", status_code=400)

#     # Load vector store and mitigation CSV
#     vector_store = Chroma(persist_directory="data/vector_store/attacks_vector_store_db", embedding_function=FastEmbedEmbeddings())
#     retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3, "score_threshold": 0.5})
    
#     docs = retriever.invoke(selected_attack)
#     df = pd.read_csv("data/tabular/Mitigation.csv", header=2)

#     # Process the attack descriptions and mitigation data
#     most_similar = docs[0].page_content.strip().lower().replace(" ", "").replace('\n', '')
#     df['Threat_Description'] = df['Threat_Description'].str.strip().str.lower().str.replace(" ", "").str.replace('\n', '')

#     matched_row = df[df['Threat_Description'] == most_similar]
#     if not matched_row.empty:
#         mitigation_measure = matched_row['Mitigation'].iloc[0]
#         return func.HttpResponse(f"Mitigation: {mitigation_measure}", status_code=200)
#     else:
#         return func.HttpResponse("No matching threat description found.", status_code=404)
