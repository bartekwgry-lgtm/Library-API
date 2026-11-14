# Library API

API for library staff to catalog books and track borrowing status.

```bash
docker compose up --build
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

```bash
uv run pytest
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/books` | Add a book |
| `GET` | `/books` | List all books |
| `DELETE` | `/books/{serial_number}` | Delete a book |
| `PATCH` | `/books/{serial_number}/status` | Borrow / return |

Book serial numbers and library card numbers are 6-digit values (`123456`).

```bash
# add a book
curl -X POST http://localhost:8000/books \
  -H 'Content-Type: application/json' \
  -d '{"serial_number":"123456","title":"Solaris","author":"Stanisław Lem"}'

# borrow
curl -X PATCH http://localhost:8000/books/123456/status \
  -H 'Content-Type: application/json' \
  -d '{"is_borrowed":true,"borrower_card":"654321"}'

# return
curl -X PATCH http://localhost:8000/books/123456/status \
  -H 'Content-Type: application/json' \
  -d '{"is_borrowed":false}'
```
