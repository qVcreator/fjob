import uvicorn

uvicorn.run(
    'fjob.app:app',
    reload='True'
)