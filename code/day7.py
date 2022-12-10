import typing as t
from dataclasses import dataclass
from pathlib import Path

from anytree import Node, RenderTree  # type: ignore[import]


@dataclass
class File:
    name: str
    size: int


class Directory(Node):  # type: ignore[misc]
    files: list[File]

    def __init__(  # type: ignore[no-untyped-def]
        self, name, parent=None, children=None, **kwargs
    ) -> None:
        self.files = []
        super().__init__(name, parent, children, **kwargs)

    def get_size(self) -> int:
        size = 0
        for file in self.files:
            size += file.size
        for child in self.children:
            size += child.get_size()
        return size


def main() -> None:
    filesystem = read_input()

    sizes: dict[Directory, int] = {}
    total_size = 0
    for dir_ in filesystem.values():
        size = dir_.get_size()
        if size <= 100000:
            total_size += size
        sizes[dir_] = size
    print(f"Part 1 = {total_size}")

    root_size = filesystem[Path("/")].get_size()
    free_space = 70000000 - root_size
    needed_space = 30000000 - free_space
    diff_space = [x - needed_space for x in sizes.values()]
    diff_space_no_neg = [x for x in diff_space if x >= 0]
    remove_dir = list(sizes.keys())[diff_space.index(min(diff_space_no_neg))]
    print(f"Part 2 = {remove_dir.get_size()}")


def read_input() -> dict[Path, Directory]:
    filesystem: dict[Path, Directory] = {Path("/"): Directory("/")}
    directory = cd(filesystem, "/")
    with open("inputs/day7", "r", encoding="utf-8") as file:
        for line in file:
            if "$" in line:
                if "cd" in line:
                    target_dir = line.strip().split()[-1]
                    if target_dir[0] == "/":
                        directory = cd(filesystem, target_dir)
                    else:
                        cur_dir = Path(directory.name)
                        tmp = directory
                        while tmp.parent is not None:
                            tmp = tmp.parent
                            cur_dir = Path(tmp.name) / cur_dir
                        directory = cd(filesystem, target_dir, str(cur_dir))
            else:
                size_, name = line.split()
                if size_ != "dir":
                    size = int(size_)
                    directory.files.append(File(name, size))

    for pre, _, node in RenderTree(cd(filesystem, "/")):
        print(f"{pre}{node.name}")

    return filesystem


def cd(
    filesystem: dict[Path, Directory],
    target_dir: str,
    current_dir: t.Optional[str] = None,
) -> Directory:
    path = Path(current_dir) / Path(target_dir) if current_dir else Path(target_dir)
    path = path.resolve()
    if path in filesystem:
        directory = filesystem[path]
    else:
        parent = filesystem[path.parent]
        directory = Directory(path.name, parent=parent)
        filesystem[path] = directory
    return directory


if __name__ == "__main__":
    main()
