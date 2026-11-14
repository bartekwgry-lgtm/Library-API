from httpx import AsyncClient

BOOK = {"serial_number": "123456", "title": "Solaris", "author": "Stanisław Lem"}


async def create_book(client: AsyncClient, **overrides: str) -> dict:
    response = await client.post("/books", json=BOOK | overrides)
    assert response.status_code == 201
    return response.json()


async def test_create_and_list_books(client: AsyncClient) -> None:
    created = await create_book(client)
    assert created["is_borrowed"] is False
    assert created["borrowed_at"] is None
    assert created["borrower_card"] is None

    await create_book(client, serial_number="111111", title="Fairy Tales")
    response = await client.get("/books")
    assert response.status_code == 200
    serials = [book["serial_number"] for book in response.json()]
    assert serials == ["111111", "123456"]


async def test_create_duplicate_serial(client: AsyncClient) -> None:
    await create_book(client)
    response = await client.post("/books", json=BOOK)
    assert response.status_code == 409
    assert response.json()["detail"] == "Book with this serial number already exists"


async def test_borrow_and_return_book(client: AsyncClient) -> None:
    await create_book(client)

    borrowed = await client.patch(
        "/books/123456/status",
        json={"is_borrowed": True, "borrower_card": "654321"},
    )
    assert borrowed.status_code == 200
    body = borrowed.json()
    assert body["is_borrowed"] is True
    assert body["borrower_card"] == "654321"
    assert body["borrowed_at"] is not None

    returned = await client.patch("/books/123456/status", json={"is_borrowed": False})
    assert returned.status_code == 200
    body = returned.json()
    assert body["is_borrowed"] is False
    assert body["borrower_card"] is None
    assert body["borrowed_at"] is None


async def test_borrow_without_card(client: AsyncClient) -> None:
    await create_book(client)
    response = await client.patch("/books/123456/status", json={"is_borrowed": True})
    assert response.status_code == 422


async def test_borrow_already_borrowed(client: AsyncClient) -> None:
    await create_book(client)
    await client.patch(
        "/books/123456/status",
        json={"is_borrowed": True, "borrower_card": "654321"},
    )
    response = await client.patch(
        "/books/123456/status",
        json={"is_borrowed": True, "borrower_card": "111111"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Book is already borrowed"


async def test_return_already_available(client: AsyncClient) -> None:
    await create_book(client)
    response = await client.patch("/books/123456/status", json={"is_borrowed": False})
    assert response.status_code == 409
    assert response.json()["detail"] == "Book is already available"


async def test_delete_book(client: AsyncClient) -> None:
    await create_book(client)
    response = await client.delete("/books/123456")
    assert response.status_code == 204
    assert (await client.get("/books")).json() == []


async def test_delete_missing_book(client: AsyncClient) -> None:
    response = await client.delete("/books/000000")
    assert response.status_code == 404


async def test_invalid_serial_in_path(client: AsyncClient) -> None:
    response = await client.delete("/books/12345")
    assert response.status_code == 422
