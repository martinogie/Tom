from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import io
import base64
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


app = FastAPI()

# Static files serving
app.mount("/static", StaticFiles(directory="static"), name="static")

model = tf.keras.models.load_model('best_model/model.weights.h5')

# Preprocessing function to transform the image for your model
def preprocess_image(image: Image.Image):
    # Convert the image to grayscale
    image = image.convert('L')  # 'L' mode is for grayscale
    
    # Resize the image to the input size
    image = image.resize((128, 128))
    
    # Convert the image to a NumPy array and normalize the pixel values
    img_array = np.array(image) / 255.0
    
    # Add a channel dimension to match the expected input shape (128, 128, 1)
    img_array = np.expand_dims(img_array, axis=-1)
    
    # Add a batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


# Prediction function
async def predict(image: Image.Image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])  # Get the index of the highest probability

    # Mapping index to tumor type
    tumor_types = ["Meningioma", "Glioma", "Pituitary"]
    return tumor_types[predicted_class]

@app.get("/", response_class=HTMLResponse)
async def get():
    html_content = open('static/index.html').read()
    return HTMLResponse(content=html_content, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            image_data = base64.b64decode(data)
            image_bytes = io.BytesIO(image_data)
            try:
                image = Image.open(image_bytes).convert('RGB')
            except Exception as e:
                print(f"Image processing error: {e}")
                await websocket.send_text("Error processing image")
                continue
            result = await predict(image)
            await websocket.send_text(result)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
