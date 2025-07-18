from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import google.generativeai as genai

# Create your views here.

@csrf_exempt
def analyze_mood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')
            if not user_input:
                return JsonResponse({'error': 'No input provided.'}, status=400)

            # Set up Gemini API
            genai.configure(api_key="AIzaSyCKUnoBceGG7HLXpePDGoPbNW0TpQwuPvY")
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
You are a helpful and empathetic mental wellness assistant.
Analyze the user's mood based on the following input:
"{user_input}"

Respond with:
1. Detected mood (1 word only)
2. A short motivational quote (1-2 lines)
3. One simple tip or suggestion for mental wellness
"""
            response = model.generate_content(prompt)
            text = response.text.strip()

            # Try to parse the response into 3 parts
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            mood, quote, tip = '', '', ''
            for line in lines:
                if line.lower().startswith('1.'):
                    mood = line[2:].strip(' :')
                elif line.lower().startswith('2.'):
                    quote = line[2:].strip(' :')
                elif line.lower().startswith('3.'):
                    tip = line[2:].strip(' :')
            if not (mood and quote and tip):
                # fallback: just return the text
                return JsonResponse({'raw': text})
            return JsonResponse({'mood': mood, 'quote': quote, 'tip': tip})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def wellmind_home(request):
    return render(request, 'wellmind_home.html')
