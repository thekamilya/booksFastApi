import httpx
import asyncio

API_KEY = 'your api key'
BASE_URL = 'https://www.googleapis.com/books/v1'


async def fetch_books(query: str, start_index: int = 0, max_results: int = 10):
    url = f"{BASE_URL}/volumes"
    params = {
        'q': query,
        'startIndex': start_index,
        'maxResults': max_results,
        'key': API_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def get_books(query: str, num_books: int = 10, start_index:int = 0):
    result = await fetch_books(query, start_index= start_index, max_results=num_books)
    books = result.get('items', [])

    selected_books = []
    for book in books:
        volume_info = book.get('volumeInfo', {})
        title = volume_info.get('title', 'No title')
        description = volume_info.get('description', 'No description')
        image_links = volume_info.get('imageLinks', {})
        thumbnail = image_links.get('thumbnail', 'No image')

        selected_books.append({
            'id': book.get('id', 'No id'),
            'title': title,
            'description': description,
            'image_resourse': thumbnail
        })

    return selected_books


async def get_book_by_id(book_id: str):
    url = f"{BASE_URL}/volumes/{book_id}"
    params = {
        'key': API_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        book_data = response.json()

        # Extract relevant information from the book_data
        volume_info = book_data.get('volumeInfo', {})
        title = volume_info.get('title', 'No title')
        description = volume_info.get('description', 'No description')
        image_link = volume_info.get('imageLinks', {}).get('thumbnail', 'No image')

        # Example of extracting more fields if needed
        authors = volume_info.get('authors', [])
        published_date = volume_info.get('publishedDate', 'Unknown')

        return {
            'title': title,
            'description': description,
            'image_resource': image_link,
        }


