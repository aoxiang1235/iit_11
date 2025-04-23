from fastapi import APIRouter, FastAPI, HTTPException, Query, Depends
from elasticsearch import Elasticsearch
from typing import List, Dict, Optional
import openai
from pydantic import BaseModel
import logging

from core.auth import get_current_user
from models import User

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
#Two different images chicago_yelp_reviews
#Search page with
es = Elasticsearch("http://localhost:9200")
#Recommended query
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
async def get_recommend(
        request: QueryRequest,
        current_user: User = Depends(get_current_user)
):
    try:
        # 记录请求开始
        logger.info(f"收到推荐请求，查询文本Received recommendation request, query text: {request.query_text}")
        # 将文本转换为向量
        logger.debug("开始将查询文本转换为向量 Start converting query text into vectors")
        logger.debug("If no information is entered, then get the user's information for recommendation")
        search_text = request.query_text if request.query_text else current_user.social_preferen
        query_vector = text_to_vector(search_text)
        logger.info("文本向量转换完成Text vector conversion completed")
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
async def get_places(
        search: Optional[str] = Query(None, description="搜索关键词"),
        zip_code: Optional[str] = Query(None, description="邮政编码"),
        categories: Optional[str] = Query(None, description="类别，多个类别用逗号分隔"),
        limit: int = Query(10, description="返回结果数量限制"),
        offset: int = Query(0, description="分页偏移量"),
        user_id: Optional[str] = Query(None, description="用户ID")
):
    try:
        # 构建查询
        query = {
            "size": limit,
            "from": offset,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"location.city": "Chicago"}}
                    ]
                }
            }
        }

        # 如果有搜索关键词，添加全文搜索条件
        if search:
            query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": search,
                    "fields": ["name^3", "categories.title^2", "location.display_address"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })

        # 如果有邮政编码，添加邮政编码过滤
        if zip_code:
            query["query"]["bool"]["must"].append({
                "match": {
                    "location.zip_code": zip_code
                }
            })
        # 如果有类别，添加类别过滤
        if categories:
            # 将逗号分隔的类别转换为列表
            category_list = [cat.strip() for cat in categories.split(",")]
            query["query"]["bool"]["must"].append({
                "terms": {
                    "categories.title": category_list
                }
            })

        # 添加排序
        query["sort"] = [
            {"rating": {"order": "desc"}},
            {"review_count": {"order": "desc"}}
        ]
        response = es.search(index="chicago_yelp_reviews", body=query)
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
        # 记录搜索历史 search_history
        if user_id:
            search_params = {
                "search": search,
                "zip_code": zip_code,
                "categories": categories,
                "limit": limit,
                "offset": offset
            }
        return places
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events", response_model=List[Dict])
async def get_events(
search: Optional[str] = Query(None, description="搜索关键词"),
    zip_code: Optional[str] = Query(None, description="邮政编码"),
    categories: Optional[str] = Query(None, description="类别，多个类别用逗号分隔"),
    limit: int = Query(10, description="返回结果数量限制"),
    offset: int = Query(0, description="分页偏移量")
):
    try:
        # 构建查询
        query = {
            "size": limit,
            "from": offset,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"location.city": "Chicago"}}
                    ]
                }
            }
        }

        # 如果有搜索关键词，添加全文搜索条件
        if search:
            query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": search,
                    "fields": ["name^3", "categories.title^2", "location.display_address"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })

        # 如果有邮政编码，添加邮政编码过滤
        if zip_code:
            query["query"]["bool"]["must"].append({
                "match": {
                    "location.zip_code": zip_code
                }
            })

        # 如果有类别，添加类别过滤
        if categories:
            # 将逗号分隔的类别转换为列表
            category_list = [cat.strip() for cat in categories.split(",")]
            query["query"]["bool"]["must"].append({
                "terms": {
                    "categories.title": category_list
                }
            })

        # 添加排序
        query["sort"] = [
            {"rating": {"order": "desc"}},
            {"review_count": {"order": "desc"}}
        ]

        response = es.search(index="chicago_yelp_reviews", body=query)
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