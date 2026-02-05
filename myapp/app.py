from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Hello World API", version="1.0.0")

class HelloResponse(BaseModel):
    message: str
    status: str

@app.get('/', response_class=HTMLResponse)
async def hello_world():
    """Main route that returns Hello World"""
    return '<h1>Hello, World!</h1>'

@app.get('/api/hello', response_model=HelloResponse)
async def hello_api():
    """API endpoint that returns JSON"""
    return HelloResponse(
        message='Hello, World!',
        status='success'
    )

@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {'status': 'healthy'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)