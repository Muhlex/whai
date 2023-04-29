from typing import Annotated

from fastapi import FastAPI, Path

import schemas

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
	item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	return results


@app.post("/translate/", response_model=schemas.Text)
async def translate(text: schemas.Text):
	print(text)
	result = "".join(reversed(text.text))
	print(result)
	text.text = result
	return text
