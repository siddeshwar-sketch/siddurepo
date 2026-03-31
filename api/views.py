from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import re
from campaigns.models import Category

class ChatBotView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        message = user_message.lower()
        
        # Fetch categories dynamically
        try:
            categories_list = list(Category.objects.values_list('name', flat=True))
            category_names = ", ".join([f"<b>{c}</b>" for c in categories_list]) if categories_list else "<b>Medical</b>, <b>Education</b>, <b>Disaster Relief</b>"
        except Exception:
            category_names = "<b>Medical</b>, <b>Education</b>, <b>Disaster Relief</b>"

        # Action Buttons
        create_btn = '<a href="/register" class="btn btn-sm btn-primary-custom rounded-pill px-3 mt-2 me-2 shadow-sm text-white text-decoration-none">Create Campaign</a>'
        donate_btn = '<a href="/categories" class="btn btn-sm btn-outline-primary rounded-pill px-3 mt-2 shadow-sm text-decoration-none">Browse Causes</a>'
        support_btn = '<a href="/dashboard/tickets" class="btn btn-sm btn-info text-white rounded-pill px-3 mt-2 shadow-sm text-decoration-none">Contact Support</a>'
        about_btn = '<a href="/about" class="btn btn-sm btn-secondary rounded-pill px-3 mt-2 shadow-sm text-decoration-none">Our Mission</a>'

        # PERFECT SOLUTION ENGINE (v3.0)
        
        # 1. WITHDRAWALS / MONEY COLLECTION
        if re.search(r'\b(withdraw|get my money|receive funds|payout|transfer money)\b', message):
            response_text = "💰 <b>How to get your funds:</b><br>1. Log in to your <b>Dashboard</b>.<br>2. Ensure your campaign is verified by our team.<br>3. Go to your campaign details and request a payout.<br>4. Funds are typically transferred to your bank account within 3-5 business days.<br>" + support_btn

        # 2. DONATION / HELPING OTHERS
        elif re.search(r'\b(donate|help|support|contribute|give)\b', message) and not re.search(r'\b(need|receive|get)\b', message):
            response_text = f"🌟 <b>You're making a difference!</b><br>Supporting a cause is the greatest gift. We have verified campaigns in: {category_names}.<br><br><b>Ready to change a life?</b><br>{donate_btn}"

        # 3. RAISING FUNDS / NEED HELP
        elif re.search(r'\b(raise|need|surgery|funds|money|start|fundraiser|help me|collect)\b', message):
            response_text = "🤝 <b>We're here for you.</b><br>I understand this is a difficult time. Creating a campaign is the fastest way to get support from thousands of donors.<br><br><b>Steps to start:</b><br>• Click 'Create Campaign'<br>• Upload your medical/proof documents<br>• Share your story<br>" + create_btn

        # 4. TRUST / SECURITY / VERIFICATION
        elif re.search(r'\b(safe|trust|secure|verified|legit|real|verify|proof)\b', message):
            response_text = "🛡️ <b>Your Trust is Our Priority.</b><br>• <b>Verification:</b> Every campaign must submit identity and medical/legal proof before going live.<br>• <b>Security:</b> We use 256-bit encryption and industry-leading payment partners.<br>• <b>Transparency:</b> You can track exactly how much has been raised and issued.<br>" + about_btn

        # 5. PAYMENTS / METHODS
        elif re.search(r'\b(payment|razorpay|upi|card|net banking|bank transfer)\b', message):
            response_text = "💳 <b>Secure Payment Methods:</b><br>We support all major payment types including:<br>• <b>UPI</b> (Google Pay, PhonePe, Paytm)<br>• **Debit/Credit Cards** (Visa, Mastercard)<br>• **Net Banking**<br>All transactions are handled through our secure gateway."

        # 6. REFUNDS
        elif re.search(r'\b(refund|cancel donation|back my money)\b', message):
            response_text = "🔄 <b>Refund Policy:</b><br>Donations are typically non-refundable once issued to a fundraiser. However, if you've made a mistake, please contact our support team within 24 hours for assistance.<br>" + support_btn

        # 7. GREETING / INFO
        elif re.search(r'\b(hi|hello|hey|greetings|info|what do you do|who are you)\b', message):
            response_text = "Hello! 👋 I'm your <b>Verified Platform Assistant</b>.<br><br>I can provide perfect solutions for:<br>• **Donations:** How to help others<br>• **Fundraising:** How to raise money<br>• **Security:** Why we are trusted<br>• **Status:** Tracking your impact<br><br>How can I help you today?"

        # DEFAULT
        else:
            response_text = "I'm here to provide the **perfect solution** for your needs! 💎<br><br>Could you please specify if you're looking to **donate**, **start a fundraiser**, or if you have questions about **withdrawals** or **security**?"

        return Response({"response": response_text}, status=status.HTTP_200_OK)
