from fastapi import APIRouter
from elasticsearch import Elasticsearch


router = APIRouter()
es = Elasticsearch("http://localhost:9200")

@router.get("/heatmap")
async def get_heatmap_data():
    query = {
        "size": 1000,  # 根据需要调整大小
        "_source": ["coordinates"],
    }

    result = es.search(index="chicago_yelp_reviews", body=query)

    heatmap_data = [
        {
            "lat": doc["_source"]["coordinates"]["latitude"],
            "lng": doc["_source"]["coordinates"]["longitude"]
        }
        for doc in result["hits"]["hits"]
    ]

    return heatmap_data

@router.get("/rating-distribution")
async def get_rating_distribution():
    query = {
        "size": 0,
        "aggs": {
            "ratings": {
                "terms": {
                    "field": "rating",
                    "size": 10
                }
            }
        }
    }

    result = es.search(index="chicago_yelp_reviews", body=query)

    rating_counts = {f"{round(bucket['key'], 1)}start": bucket['doc_count'] for bucket in result['aggregations']['ratings']['buckets']}

    return rating_counts

@router.get("/business-type-count")
async def get_business_type_count():
    query = {
        "size": 0,
        "aggs": {
            "business_types": {
                "terms": {
                    "field": "categories.title.keyword",
                    "size": 10
                }
            }
        }
    }
    
    result = es.search(index="chicago_yelp_reviews", body=query)
    
    type_counts = {bucket['key']: bucket['doc_count'] for bucket in result['aggregations']['business_types']['buckets']}
    
    return type_counts 