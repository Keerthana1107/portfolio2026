from urllib.parse import quote_plus
PLATFORMS={
"Amazon":"https://www.amazon.in/s?k={q}","Flipkart":"https://www.flipkart.com/search?q={q}",
"IKEA":"https://www.ikea.com/in/en/search/?q={q}","Swiggy":"https://www.swiggy.com/search?query={q}",
"Zomato":"https://www.zomato.com/chennai/restaurants?query={q}","OYO":"https://www.oyorooms.com/search?location={q}"}
CATALOG=[
{"name":"LED ceiling light","category":"lighting","platform":"Amazon","price":899,"q":"led ceiling light"},
{"name":"Decorative table lamp","category":"lighting","platform":"IKEA","price":1499,"q":"table lamp"},
{"name":"Ceiling fan","category":"fan","platform":"Amazon","price":2499,"q":"ceiling fan"},
{"name":"4-seater dining table","category":"dining","platform":"IKEA","price":12990,"q":"dining table"},
{"name":"Storage cabinet","category":"storage","platform":"IKEA","price":7990,"q":"storage cabinet"},
{"name":"Wall art set","category":"decor","platform":"Amazon","price":999,"q":"wall art decor"},
{"name":"Indoor artificial plant","category":"decor","platform":"Flipkart","price":699,"q":"indoor plant"},
{"name":"Party food search","category":"catering","platform":"Swiggy","price":350,"q":"party food"},
{"name":"Party food search","category":"catering","platform":"Zomato","price":350,"q":"party food"},
{"name":"Event decoration search","category":"decoration","platform":"Amazon","price":2500,"q":"party decoration"},
{"name":"Venue search","category":"venue","platform":"OYO","price":5000,"q":"event venue"},
{"name":"Stud earrings","category":"earrings","platform":"Amazon","price":799,"q":"stud earrings"},
{"name":"Minimal necklace","category":"necklace","platform":"Flipkart","price":1299,"q":"minimal necklace"},
{"name":"Statement earrings","category":"earrings","platform":"Amazon","price":1599,"q":"statement earrings"},
{"name":"Bangle set","category":"bangles","platform":"Flipkart","price":999,"q":"bangle set"}]
def catalog_for(p):
    groups={"home":{"lighting","fan","dining","storage","decor"},"party":{"catering","decoration","venue"},"jewelry":{"earrings","necklace","bangles"}}
    return [x for x in CATALOG if x["category"] in groups[p]]
def search_url(platform,q): return PLATFORMS[platform].format(q=quote_plus(q))
