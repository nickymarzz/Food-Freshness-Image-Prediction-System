STORAGE_ADVICE = {
    "Apple": {
        "tips": "Store in a cool, dark place or the crisper drawer of your fridge. Keep away from other produce as apples release ethylene gas which speed up ripening.",
        "nutrition": "High in fiber and Vitamin C. Great for heart health.",
        "shelf_life": "7-10 days (pantry), 4-6 weeks (fridge)"
    },
    "Banana": {
        "tips": "Store at room temperature away from direct sunlight. To slow ripening, wrap the stems in plastic wrap. Keep separate from other fruits.",
        "nutrition": "Rich in potassium and Vitamin B6. Excellent energy booster.",
        "shelf_life": "2-5 days (room temp)"
    },
    "Mango": {
        "tips": "Keep at room temperature until fully ripe, then move to the fridge. Ripe mangos have a slightly soft feel and sweet aroma.",
        "nutrition": "Packed with Vitamin A and C. Supports immune function.",
        "shelf_life": "1-2 days (ripe, fridge)"
    },
    "Orange": {
        "tips": "Best kept in the fridge to maximize shelf life. They can stay at room temperature for a few days but will dry out faster.",
        "nutrition": "Famous for high Vitamin C content and antioxidants.",
        "shelf_life": "2-3 weeks (fridge)"
    },
    "Strawberry": {
        "tips": "Do not wash until ready to eat! Store in the fridge in a ventilated container. Moisture is the enemy of strawberries.",
        "nutrition": "High in antioxidants, manganese, and potassium.",
        "shelf_life": "3-7 days (fridge)"
    },
    "Bellpepper": {
        "tips": "Store in the crisper drawer of the fridge. Ensure they are dry before storing to prevent mold.",
        "nutrition": "Excellent source of Vitamin A, C, and B6. Low in calories.",
        "shelf_life": "1-2 weeks (fridge)"
    },
    "Carrot": {
        "tips": "Remove green tops before storing as they draw moisture from the root. Store in a plastic bag in the fridge.",
        "nutrition": "High in Beta-Carotene and Vitamin K1. Good for eye health.",
        "shelf_life": "3-4 weeks (fridge)"
    },
    "Cucumber": {
        "tips": "Cucumbers are sensitive to cold; store in the warmest part of the fridge (usually the door or top shelf). Keep dry.",
        "nutrition": "Hydrating and low in calories. Contains Vitamin K.",
        "shelf_life": "1 week (fridge)"
    },
    "Potato": {
        "tips": "Store in a cool, dark, well-ventilated place. Never store in the fridge as the starch turns to sugar. Keep away from onions.",
        "nutrition": "Good source of Vitamin C, B6, and Potassium (especially the skin).",
        "shelf_life": "2-4 months (cool dark place)"
    },
    "Tomato": {
        "tips": "Store at room temperature away from sunlight until fully ripe. Refrigeration can make them mealy and lose flavor.",
        "nutrition": "Major dietary source of the antioxidant lycopene.",
        "shelf_life": "5-7 days (room temp)"
    }
}

def get_storage_html(category):
    data = STORAGE_ADVICE.get(category)
    if not data:
        return "<div style='padding: 10px; opacity: 0.6;'>No specific tips available for this category.</div>"
    
    return f"""
    <div class="storage-card">
        <h3 style="margin-top: 0; color: #3b82f6;">💡 Storage Specialist: {category}</h3>
        <p><strong>Tips:</strong> {data['tips']}</p>
        <p><strong>Nutrition:</strong> {data['nutrition']}</p>
        <p><strong>Est. Shelf Life:</strong> <span style="color: #10b981;">{data['shelf_life']}</span></p>
    </div>
    """
