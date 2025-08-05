import httpx
import asyncio

async def test_reqres_fixed():
    # Set a browser-like User-Agent to avoid being blocked by APIs
    default_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient(headers=default_headers) as client:
        response = await client.get('https://reqres.in/api/users?page=1')
        print(f'Status: {response.status_code}')
        print(f'Headers sent: {dict(response.request.headers)}')
        print(f'Body: {response.text[:200]}')

if __name__ == "__main__":
    asyncio.run(test_reqres_fixed()) 