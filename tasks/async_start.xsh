uv sync --extra test
cd atest/async/event
uv run robot -L TRACE .
cd ../evenOdd
uv run robot -L TRACE .

