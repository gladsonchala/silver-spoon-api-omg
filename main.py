from fastapi import FastAPI, HTTPException
import g4f
import logging
from strings import themessage

app = FastAPI()

model = g4f.models.default

# Configure logging
logging.basicConfig(level=logging.ERROR)


@app.post("/generate-response/")
def generate_response(user_message: str, provider_name: str):
  try:
    pname = provider_name
    pjoin = "g4f.Provider." + pname

    try:
      provider = getattr(g4f.Provider, pname)
    except AttributeError:
      # If not found, raise a custom error
      raise ValueError(
          f"You entered the wrong provider. Please try using a valid provider!"
      )

    # Generate a response using the specified GPT model and provider
    response = g4f.ChatCompletion.create(
        model=model,
        provider=provider,
        messages=[{
            "role":
            "user",
            "content":
            """{} IMPORTANT: Don't write another shits except your thoughts(1 sentence) and answer of the user's question(after thought 1sentence. not related to thought): >> {} <<"""
            .format(themessage, user_message)
        }],
    )

    formatted_response = ""

    for message in response:
      formatted_response += message

    json_response = {
        "response_code": 200,
        "message": formatted_response,
    }

    return json_response

  except ValueError as e:
    error_message = str(e)
    logging.error(error_message)

    error_response = {
        "response_code": 400,
        "message": error_message,
    }

    return error_response

  except Exception as e:
    errors = f"Error generating response: {e}"
    logging.error(errors)

    # Return a generic error response as pure JSON
    error_response = {
        "response_code": 500,
        "message": errors,
    }

    return error_response


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="0.0.0.0", port=3000)
