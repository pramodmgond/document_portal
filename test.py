from pathlib import Path 
from io import BytesIO
import os
from document_ingestion.data_ingestion_old import DocumentHandler , DocumentComparator      # Your PDFHandler class
from src.document_analyzer.data_analysis import DocumentAnalyzer  # Your DocumentAnalyzer class
from src.document_comparision.document_comparator import DocumentComparatorLLM  # Your DocumentAnalyzer class


# PDF_PATH = r"C:\\Users\\pramod\\Desktop\\KRISH_ACADEMY\\LLMOPS_Projects\\document_portal\\data\\document_analysis\\sample.pdf"

# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()

# def main():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(session_id="test_ingestion_analysis")
        
#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting metadata analysis...")
#         analyzer = DocumentAnalyzer()  # Loads LLM + parser
        
#         analysis_result = analyzer.analyze_document(text_content[0:1000])

#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")

# if __name__ == "__main__":
#     main()



# ---- Step 1: Save and combine PDFs ---- #
def test_compare_documents():
    ref_path = Path("C:\\Users\\pramod\\Desktop\\KRISH_ACADEMY\\LLMOPS_Projects\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
    act_path = Path("C:\\Users\\pramod\\Desktop\\KRISH_ACADEMY\\LLMOPS_Projects\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")

    # Wrap them like Streamlit UploadedFile-style
    class FakeUpload:
        def __init__(self, file_path: Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()

        def getbuffer(self):
            return self._buffer

    # Instantiate
    comparator = DocumentComparator()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    # Save files and combine
    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_documents()
    comparator.clean_old_sessions(keep_latest=3)

    print("\n Combined Text Preview (First 1000 chars):\n")
    print(combined_text[:1000])

    # ---- Step 2: Run LLM comparison ---- #
    llm_comparator = DocumentComparatorLLM()
    df = llm_comparator.compare_documents(combined_text[:5000])
    
    print("\n Comparison DataFrame:\n")
    print(df)
    df.to_csv("data_comparator_output.csv")

if __name__ == "__main__":
    test_compare_documents()
    
