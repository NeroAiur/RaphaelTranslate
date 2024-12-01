import google.generativeai as gemini

def generate_text_response(request, API_Key):
    gemini.configure(api_key=API_Key)
    model = gemini.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(request)
    
    return(response.text)