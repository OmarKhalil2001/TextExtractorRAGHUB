from pymongo import MongoClient
import PyPDF2

class MongoExtractor():
    def __init__(self, client: MongoClient, databasName : str, collection : str) -> None:
        self.client = client
        self.database = self.client[databasName]
        self.collection = self.database[collection]

    def extractTextPDF(self, file) -> str:
        text = ""
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    
    def storePDF(self, file) -> str:
        text = self.extractTextPDF(file)
        result = self.collection.insert_one(
            {
                "text":text
            }
        )
        return str(result.inserted_id)

        