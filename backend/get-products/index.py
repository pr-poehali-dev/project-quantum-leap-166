import os
import json
import urllib.request

def handler(event: dict, context) -> dict:
    """Получает список товаров с фото и остатками из Яндекс.Маркет Partner API"""

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    token = os.environ['YANDEX_MARKET_TOKEN']
    campaign_id = os.environ['YANDEX_MARKET_CAMPAIGN_ID']

    headers = {
        'Api-Key': token,
        'Content-Type': 'application/json'
    }

    # Получаем businessId по campaignId
    campaign_url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}'
    campaign_req = urllib.request.Request(campaign_url, headers=headers)
    with urllib.request.urlopen(campaign_req) as resp:
        campaign_data = json.loads(resp.read().decode())
    business_id = campaign_data['campaign']['business']['id']

    # Получаем список товаров (новый API)
    offers_url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings?limit=50'
    offers_body = json.dumps({}).encode()
    req = urllib.request.Request(offers_url, data=offers_body, headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        offers_data = json.loads(resp.read().decode())

    entries = offers_data.get('result', {}).get('offerMappings', [])

    # Получаем остатки
    stocks_url = f'https://api.partner.market.yandex.ru/campaigns/{campaign_id}/stocks'
    stocks_body = json.dumps({}).encode()
    stocks_req = urllib.request.Request(stocks_url, data=stocks_body, headers=headers, method='POST')
    with urllib.request.urlopen(stocks_req) as resp:
        stocks_data = json.loads(resp.read().decode())

    # Индексируем остатки по shopSku
    stocks_map = {}
    for item in stocks_data.get('result', {}).get('warehouses', []):
        for offer in item.get('offers', []):
            sku = offer.get('shopSku')
            count = sum(s.get('count', 0) for s in offer.get('stocks', []) if s.get('type') == 'AVAILABLE')
            if sku not in stocks_map:
                stocks_map[sku] = 0
            stocks_map[sku] += count

    products = []
    for entry in entries:
        offer = entry.get('offer', {})
        sku = offer.get('offerId', '')
        name = offer.get('name', '')
        pictures = offer.get('pictures', [])
        image = pictures[0] if pictures else None
        stock = stocks_map.get(sku, 0)

        products.append({
            'sku': sku,
            'name': name,
            'image': image,
            'stock': stock
        })

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'products': products}, ensure_ascii=False)
    }