import faiss
import numpy as np
import os
import json

class FaissIndexManager:
    def __init__(self, dimension: int = 384, index_path: str = "indexes/main.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = index_path + ".metadata.json"
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = []
            os.makedirs(os.path.dirname(index_path), exist_ok=True)

    def add_documents(self, embeddings: list, docs_metadata: list):
        embeddings_np = np.array(embeddings).astype('float32')
        self.index.add(embeddings_np)
        self.metadata.extend(docs_metadata)
        self.save()

    def search(self, query_embedding: list, top_k: int = 5):
        query_np = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "score": float(distances[0][i]),
                    "metadata": self.metadata[idx]
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f)
