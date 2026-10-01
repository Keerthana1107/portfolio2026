from ..catalog import catalog_for,search_url
def fallback(planner,data):
    b=float(data["budget"]); c=catalog_for(planner)
    if planner=="home":
        alloc={"furniture":b*.45,"lighting":b*.15,"decor":b*.20,"storage":b*.20}
        summary="A balanced starter home setup based on your rooms, quantities and style."
        tips=["Measure rooms before buying large furniture.","Keep a small reserve for delivery and installation.","Compare the same search across platforms."]
    elif planner=="party":
        alloc={"catering":b*.50,"decoration":b*.20,"entertainment":b*.15,"venue":b*.15}
        summary="A practical party budget split with the largest share reserved for food."
        tips=["Confirm per-person food pricing.","Keep a 5–10% contingency when possible.","Check venue capacity and cancellation terms."]
    else:
        alloc={"jewelry":b*.85,"reserve":b*.15}
        summary="An occasion-focused jewelry shortlist based on your stated style."
        tips=["Match metal tone with the outfit.","Pair one statement piece with simpler jewelry.","Verify material, size and return policy."]
    items=[{"title":x["name"],"category":x["category"],"platform":x["platform"],"estimated_price":x["price"],
            "reason":"Illustrative catalog suggestion; verify current price and availability.",
            "search_url":search_url(x["platform"],x["q"])} for x in c[:6]]
    return {"planner":planner,"budget":b,"budget_allocation":alloc,"summary":summary,
            "recommendations":items,"tips":tips,
            "disclaimer":"Prices and availability are illustrative search estimates, not live inventory."}
