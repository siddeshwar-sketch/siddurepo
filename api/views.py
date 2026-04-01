from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from campaigns.models import Category, Campaign
from google import genai
from google.genai import types

class ChatBotView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        if not user_message:
            return Response({"response": "Please enter a message."}, status=status.HTTP_200_OK)
        
        # Action Buttons
        create_btn = '<a href="/campaign/new/" class="btn btn-sm btn-primary-custom rounded-pill px-3 mt-3 me-2 shadow-sm text-white text-decoration-none">Create Campaign</a>'
        donate_btn = '<a href="/categories/" class="btn btn-sm btn-outline-primary rounded-pill px-3 mt-3 shadow-sm text-decoration-none">Browse All Causes</a>'
        support_btn = '<a href="/dashboard/tickets/" class="btn btn-sm btn-info text-white rounded-pill px-3 mt-3 shadow-sm text-decoration-none">Contact Support</a>'

        active_campaigns = Campaign.objects.filter(status='ACTIVE', approved=True).order_by('-raised_amount')
        categories_list = list(Category.objects.values_list('name', flat=True))

        sys_prompt = f"""You are the friendly, intelligent AI Assistant for the 'All-in-One Donation Platform'. 
        You help users find meaningful campaigns to donate to, explain how to start their own fundraisers, and provide details on platform security/withdrawals.
        
        Platform Available Categories: {', '.join(categories_list)}
        
        Currently Trending Campaigns on Platform:
        """
        for camp in active_campaigns[:15]:
            sys_prompt += f"- Title: '{camp.title}' (ID: {camp.pk}, Goal: ₹{camp.goal_amount}, Raised: ₹{camp.raised_amount}). Category: {camp.category.name if camp.category else 'General'}. \n"

        sys_prompt += f"""
        CRITICAL FORMATTING RULES:
        1. When recommending a specific campaign, you MUST provide a clickable HTML link using this format: <a href='/campaign/ID/' class='fw-bold text-decoration-none text-primary-custom'>Title</a>
        2. ALWAYS format your entire response as standard HTML for web viewing (use <br> for new lines, <b> for bold, <i>, <ul class='ps-3'>, <li>). 
        3. DO NOT use Markdown syntax (no ** for bold, no ## for headers). Just HTML.
        4. Be empathetic, polite, and encouraging. Keep answers relatively concise and highly related to the donation platform.
        5. If the user asks how to start a campaign or needs help, instruct them and include this EXACT button code at the very end of your response: {create_btn}
        6. If the user wants to browse or view categories, include this EXACT button: {donate_btn}
        """

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            return Response({"response": f"<b>AI Setup Required:</b> I am ready to be your intelligent assistant, but the platform administrator has not configured the GEMINI_API_KEY yet.<br><br>Please add your valid Google Gemini API Key to the `.env` file so I can wake up! <br>{support_btn}"}, status=status.HTTP_200_OK)
        
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.3, # Keep it factual and helpful
                )
            )
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"<b>System Overload:</b> Sorry, the AI experienced a temporary issue while processing your request.<br><span class='text-muted small'>Exception details: {str(e)}</span><br>{support_btn}"

        return Response({"response": bot_reply}, status=status.HTTP_200_OK)
