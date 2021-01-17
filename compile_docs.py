import os
import sys
import re
import argparse


def _fmain(output_file: str):
    chunks: list[tuple[str]] = []
    out_buffer: list[str] = []

    for file in os.listdir(os.path.join(os.path.dirname(__file__), "docs_chunks")):
        if not re.compile(r"\[[0-9]\].[0-9a-zA-Z_ .]*\.chunk\.md$").match(file):
            print("Ignoring {} file because it is not a template".format(file))
            continue
        chunk = tuple(
            list(
                [
                    file.split(".")[0].replace("[", "").replace("]", ""),
                    os.path.abspath(os.path.join(os.path.dirname(__file__), "docs_chunks", file)),
                ]
            )
        )
        chunks.append(chunk)

    for index, chunk_path in chunks:
        print(
            "Reading chunk {} (document position {})".format(
                ".".join(chunk_path.split("\\")[-1].split(".")[1:]), index
            )
        )
        doc_chunk = open(chunk_path, "r")
        chunk_data = doc_chunk.read()
        doc_chunk.close()

        out_buffer.append(chunk_data + "\n")

    if os.path.exists(
        os.path.abspath(os.path.join(os.path.dirname(__file__), output_file))
    ) and os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), output_file))):
        print("Removing provious version")
        os.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), output_file)))

    doc_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), output_file)), "x")
    doc_file.write("\n".join(out_buffer))
    doc_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-of",
        "--output-filename",
        help="Output file's name. If not set it defaults to README.md",
        type=str,
        dest="output_file",
        default="README.md",
    )
    args = parser.parse_args()

    def __is_md(filename: str) -> bool:
        if filename.endswith(".md"):
            return True
        else:
            return False

    if not __is_md(args.output_file):
        raise Exception(
            "Only .md files are supported; got .{} instead".format(
                os.path.splitext(args.output_file)[0]
            )
        )

    _fmain(args.output_file)