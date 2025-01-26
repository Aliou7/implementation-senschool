from fastapi import FastAPI, HTTPException # type: ignore
from SPARQLWrapper import SPARQLWrapper, JSON # type: ignore

app = FastAPI()

# Configuration de l'endpoint GraphDB
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/snch_ontology"

@app.get("/")
def read_root():
    return {"message": "Welcome to the GraphDB REST API"}

@app.get("/caliphs")
def get_caliphs():
    query = """
    SELECT ?caliph ?father ?mother ?birthPlace
    WHERE {
        ?caliph a <https://senegalculturalheritage/ontology/Caliph> ;
                <https://senegalculturalheritage/ontology/has_father> ?father ;
                <https://senegalculturalheritage/ontology/has_mother> ?mother ;
                <https://senegalculturalheritage/ontology/birth_place> ?birthPlace .
    }
    """
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        caliphs = [
            {
                "caliph": result["caliph"]["value"],
                "father": result["father"]["value"],
                "mother": result["mother"]["value"],
                "birthPlace": result["birthPlace"]["value"]
            }
            for result in results["results"]["bindings"]
        ]
        return {"caliphs": caliphs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8000)
