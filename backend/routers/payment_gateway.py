import os
import stripe
from fastapi import Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from utils import verify_token
import models
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

# Apni Secret Key yahan dalein
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") 

# Mapping: Frontend name -> Stripe Price ID
basicPriceKey = os.getenv("BASIC_PRICE_KEY")
premiumPriceKey = os.getenv("PREMIUM_PRICE_KEY")
STRIPE_PLANS = {
    "basic": basicPriceKey,    # Dashboard se copy karein
    "premium": premiumPriceKey  # Dashboard se copy karein
}

@router.post("/create-checkout-session")
async def create_checkout(data: dict = Body(...), 
                          db: Session = Depends(get_db),
                          current_user: models.User = Depends(verify_token) # <--- Security happens here
                          ):
    plan_name = data.get("plan") # Frontend se 'basic' ya 'premium' aayega
    
    # Check karein ke kya ye plan hamari list mein hai
    price_id = STRIPE_PLANS.get(plan_name)
    
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid Plan Selected")

    try:
        print(f"Selected Plan: {plan_name}, Price ID: {price_id}")  # Debugging ke liye print statement
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:3000/dashboard',
            cancel_url='http://localhost:3000/subscription',
        )
        if(session and session.url):
            # update the user's subscription status in the database here
            db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
            if db_user:
                db_user.plan = plan_name
                db.commit()

        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}