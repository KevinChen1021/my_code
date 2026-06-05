import contextlib
import io
import json
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "Notebooks"


def execute_notebook(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    execution_count = 0
    failures = []

    for index, cell in enumerate(data["cells"]):
        if cell["cell_type"] != "code":
            continue

        execution_count += 1
        stdout = io.StringIO()
        namespace = {"__name__": "__main__"}
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stdout):
                exec(compile(source, f"{path.name}:cell_{index}", "exec"), namespace)
        except Exception:
            failures.append((index, traceback.format_exc()))

        cell["execution_count"] = execution_count
        text = stdout.getvalue()
        cell["outputs"] = []
        if text:
            cell["outputs"].append(
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": text,
                }
            )

        if failures and failures[-1][0] == index:
            cell["outputs"].append(
                {
                    "ename": "ExecutionError",
                    "evalue": failures[-1][1].splitlines()[-1],
                    "output_type": "error",
                    "traceback": failures[-1][1].splitlines(),
                }
            )

    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return execution_count, failures


def main():
    all_failures = []
    paths = sorted(NOTEBOOK_DIR.glob("chapter_*.ipynb"))
    paths += sorted(NOTEBOOK_DIR.glob("assignment_*.ipynb"))
    for path in paths:
        count, failures = execute_notebook(path)
        print(f"{path.name}: executed {count} code cells")
        for cell_index, failure in failures:
            print(f"  FAILED cell {cell_index}: {failure.splitlines()[-1]}")
            all_failures.append((path.name, cell_index, failure))

    if all_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
