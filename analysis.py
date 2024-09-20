
import re
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


def extract_entities(text):
    # Apply BERT-based NER
    tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    entities = ner_pipeline(text)
    
    # Filter entities
    companies = [ent['word'] for ent in entities if ent['entity_group'] == 'ORG']
    persons = [ent['word'] for ent in entities if ent['entity_group'] == 'PER']
    locations = [ent['word'] for ent in entities if ent['entity_group'] == 'LOC']
    
    return {"companies": companies, "persons": persons, "locations": locations}

def extract_amounts_and_dates(text):
    # Regex for dollar amounts
    dollar_amounts = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
    
    # Regex for dates
    dates = re.findall(r'\b(?:\d{1,2}[-/thstndrd\s]*)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)?\s?\d{1,2}[-/,\s]*\d{2,4}\b', text)
    
    return {"dollar_amounts": dollar_amounts, "dates": dates}

def process_documents(documents):
    data = []

    for doc_text in documents:
        # Extract named entities using BERT NER
        entities = extract_entities(doc_text)
        
        # Extract dollar amounts and dates using regex
        amounts_and_dates = extract_amounts_and_dates(doc_text)
        
        # Extracted information for this document
        doc_data = {
            "company_names": entities["companies"],
            "stakeholders": entities["persons"],
            "locations": entities["locations"],
            "dollar_amounts": amounts_and_dates["dollar_amounts"],
            "dates": amounts_and_dates["dates"]
        }
        data.append(doc_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def classify_document(text):
    # Define keywords for each category
    rfp_keywords = ["request for proposal", "rfp", "statement of work", "scope of work", "proposal submission"]
    rfq_keywords = ["request for quotation", "rfq", "quotation", "quote submission"]
    bid_keywords = ["invitation to bid", "bid submission", "sealed bid", "bid process"]
    tender_keywords = ["invitation to tender", "tender process", "tender submission", "sealed tender"]
    quote_keywords = ["invitation to quote", "quote submission", "quotation"]
    

    # Lowercase the document for case-insensitive matching
    text_lower = text.lower()

    # Check for keywords and classify accordingly
    if any(keyword in text_lower for keyword in rfp_keywords):
        return "RFP (Request for Proposal)"
    elif any(keyword in text_lower for keyword in rfq_keywords):
        return "RFQ (Request for Quotation)"
    elif any(keyword in text_lower for keyword in bid_keywords):
        return "Invitation to Bid"
    elif any(keyword in text_lower for keyword in tender_keywords):
        return "Invitation to Tender"
    elif any(keyword in text_lower for keyword in quote_keywords):
        return "Invitation to Quote"
    else:
        return "other documents"
    
def classify_documents(documents):
    classifications = []
    for doc_text in documents:
        classification = classify_document(doc_text)
        classifications.append(classification)
    return classifications  

   