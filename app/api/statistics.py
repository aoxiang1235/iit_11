from fastapi import APIRouter,FastAPI, HTTPException
from elasticsearch import Elasticsearch
from typing import List, Dict
import openai
from pydantic import BaseModel
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

es = Elasticsearch("http://localhost:9200")

es1 = Elasticsearch("http://localhost:9201")

class QueryRequest(BaseModel):
    query_text: str


def text_to_vector(texts: str) -> List[float]:
    # 新版写法：Embeddings（复数）.create
    response = openai.Embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return response["data"][0]["embedding"]

@router.get("/recommend", response_model=List[Dict])
async def get_recommend(request: QueryRequest):
    try:
        # 记录请求开始
        logger.info(f"收到推荐请求，查询文本: {request.query_text}")

        # 将文本转换为向量
        logger.debug("开始将查询文本转换为向量")
        query_vector = text_to_vector(request.query_text)
        logger.info("文本向量转换完成")

        # 执行向量查询
        logger.debug("开始执行Elasticsearch向量查询")
        response = es1.search(
            index="chicago_yelp_bussinesses_reviewed",
            body={
                "size": 5,
                "query": {
                    "knn": {
                        "field": "chicago_yelp_businesses_vector",
                        "query_vector": query_vector,  # 修复注释掉的代码
                        "k": 5,
                        "num_candidates": 50
                    }
                }
            }
        )
        logger.info("向量查询完成，返回结果数: %d", len(response["hits"]["hits"]))
        logger.debug(f"查询响应: {response}")

        # 解析查询结果
        logger.debug("开始解析查询结果")
        places = [
            {
                "id": hit["_id"],
                "name": hit["_source"]["name"],
                "type": hit["_source"]["categories"][0]["title"],
                "venue": hit["_source"]["location"]["display_address"],
                "address": hit["_source"]["location"]["display_address"],
                "rating": hit["_source"]["rating"],
                "reviewCount": hit["_source"]["review_count"],
                "coordinates": hit["_source"]["coordinates"]
            }
            for hit in response["hits"]["hits"]
        ]
        logger.info(f"成功解析 {len(places)} 个推荐地点")

        return places

    except Exception as e:
        # 记录错误日志
        logger.error(f"处理推荐请求时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# 定义API端点
@router.get("/places", response_model=List[Dict])
async def get_places():
    try:
        response = es.search(index="chicago_yelp_reviews", body={
            "query": {
                "match": {
                    "location.city": "Chicago"
                }
            }
        })
        places = [
            {
                "id": hit["_id"],
                "name": hit["_source"]["name"],
                "type": hit["_source"]["categories"][0]["title"],
                "venue": hit["_source"]["location"]["display_address"],
                "address": hit["_source"]["location"]["display_address"],
                "rating": hit["_source"]["rating"],
                "reviewCount": hit["_source"]["review_count"],
                "coordinates": hit["_source"]["coordinates"]
            }
            for hit in response["hits"]["hits"]
        ]
        return places
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events", response_model=List[Dict])
async def get_events():
    try:
        response = es.search(index="chicago_yelp_reviews", body={
            "query": {
                "match": {
                    "location.city": "Chicago"
                }
            }
        })
        events = [
            {
                "id": hit["_id"],
                "name": hit["_source"]["name"],
                "type": hit["_source"]["categories"][0]["title"],
                "venue": hit["_source"]["location"]["display_address"],
                "zipCode": hit["_source"]["location"]["zip_code"],
                "reviewCount": hit["_source"]["review_count"],
                "coordinates": hit["_source"]["coordinates"]
            }
            for hit in response["hits"]["hits"]
        ]
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/divvy-stations", response_model=List[Dict])
async def get_divvy_stations():
    try:
        response = es.search(index="chicago_yelp_reviews", body={
            "query": {
                "match": {
                    "location.city": "Chicago"
                }
            }
        })
        stations = [
            {
                "id": hit["_id"],
                "name": hit["_source"]["name"],
                 "status": "Active" if not hit["_source"].get("is_closed", True) else "Inactive",
                "availableBikes": hit["_source"].get("availableBikes", 0),
                "totalDocks": hit["_source"].get("totalDocks", 0),
                "coordinates": hit["_source"]["coordinates"]
            }
            for hit in response["hits"]["hits"]
        ]
        return stations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/zip-codes", response_model=List[str])
async def get_zip_codes():
    try:
        response = es.search(index="chicago_yelp_reviews", body={
            "query": {
                "match": {
                    "location.city": "Chicago"
                }
            }
        })
        # 使用 set 去重，并使用正确的字段名称
        zip_codes = list(set(
            hit["_source"]["location"].get("zip_code", "") for hit in response["hits"]["hits"]
        ))
        return zip_codes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[str])
async def get_categories():
    try:
        # 从 Elasticsearch 中搜索类别数据
        response = es.search(index="chicago_yelp_reviews", body={
            "size": 1000,  # 假设最多有 1000 个类别
            "query": {
                "match": {
                    "location.city": "Chicago"  # 正确的 match 查询格式
                }
            }
        })

        # 提取类别数据
        categories = list(set(
            category["title"] for hit in response["hits"]["hits"]
            for category in hit["_source"].get("categories", [])
        ))

        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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