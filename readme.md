
# RFX Document Analysis Report

## Introduction
In this analysis, we started by finding all opportunities from the [BC Bid website](https://bcbid.gov.bc.ca/page.aspx/en/rfp/request_browse_public). We focused on categorizing and analyzing RFX (Request for X) documents such as **Request for Proposals (RFPs)**, **Request for Quotations (RFQs)**, **Invitation to Bid (ITB)**, **Invitation to Tender (Rft)**, and **Invitation to Offer (IO)**.

### Categories of Documents
The following categories were used to filter and classify the documents:
```python
categories = {
    "itb": "Invitation to Bid",
    "itq": "Invitation to Quote",
    "rfp": "Request for Proposal",
    "Rft": "Request for Tenders",
    "io": "Invitation to Offer"
}
```

## Approach

### 1. Web Scraping for Opportunities
We began by scraping the BC Bid website to identify opportunities under the above categories. Using Selenium, we navigated to the page, selected the categories from the dropdown, and extracted the links for each opportunity. Each URL was then processed to identify downloadable files for further analysis.

### 2. File Downloading
For each URL, we looked for downloadable links. We successfully downloaded **33 files** that were classified as relevant opportunities. These files were saved for further analysis, including entity extraction and question-answering tasks.

### 3. File Classification and Entity Extraction
For analysis, we classified the documents into categories such as **RFP**, **RFQ**, **ITB**, etc., using keyword-based approaches. Additionally, we extracted key information from each document using **BERT NER classifiers** and **SpaCy** for named entity recognition (NER). We focused on extracting the following entities:
- **Dates**
- **Organizations**
- **Offered Money**
- **Locations**
![this](/photo_2024-09-20_13-42-08.jpg) is the results of categorizing the documents.
![this](/photo_2024-09-20_13-42-25.jpg) is the results of finding entities.

### 4. Deep Insights with GPT-4
To gain more detailed insights, we used **GPT-4** to generate deeper analyses and explanations of the content. For example, GPT-4 was used to answer questions about the objectives, deliverables, and specific requirements mentioned in the RFX documents.
![this](/photo_2024-09-20_13-43-01.jpg) and [this](/photo_2024-09-20_13-43-16.jpg) and  [this](/photo_2024-09-20_13-43-25.jpg)  are the results of some insights from a document.

#### Example
Here’s an example where GPT-4 was used to answer a question:
- **Question**: "What is the key objective of this RFP?"
- **Answer**: "The key objective of this RFP is to solicit proposals for ... [specific details]."


### 5. Question-Answering with RAG (Retrieval-Augmented Generation)
For more complex question-answering tasks, we employed **RAG** (Retrieval-Augmented Generation) using **Chroma** for vector storage and **GPT-4** as the text generator. This allowed us to retrieve relevant parts of the documents and generate more precise answers.

#### Example
- **Question**: "What is the deadline for this proposal?"
- **RAG Answer**: "The deadline for this proposal is [insert deadline]."

 you can find another example ![here](/image_2024-09-20_13-40-03.png)

## How to Run
## 1. Install Dependencies

Before running the script, ensure that all required Python packages are installed. You can install the necessary dependencies using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 2. Running the Script

After installing the dependencies, you can run the main analysis script using the following command:

```bash
python -m main
```

This command will execute the RFX document analysis pipeline, entity extraction, and question-answering.

## 3. Requirements

Make sure you have the following prerequisites:
- A valid path to the WebDriver (e.g., ChromeDriver) for Selenium
- OPEN AI key 

Ensure that you have set up the WebDriver correctly before running the script.Through this process, we were able to classify, extract, and analyze key information from 33 RFX documents. The combination of BERT NER for entity extraction, GPT-4 for deeper insights, and RAG.
