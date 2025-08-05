import httpx
import asyncio

async def test_reqres():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://reqres.in/api/users?page=1')
        print(f'Status: {response.status_code}')
        print(f'Headers sent: {dict(response.request.headers)}')
        print(f'Body: {response.text[:200]}')

if __name__ == "__main__":
    asyncio.run(test_reqres()) 