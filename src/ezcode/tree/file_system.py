from functools import cmp_to_key


class iNode:
    def __init__(self, name: str, parent=None, is_file=False, content=None):
        self.name = name
        self.is_file = is_file
        self.content = content
        self.parent = parent
        self.inodes = dict()  # <name, iNode>

    def __str__(self):
        df = "f" if self.is_file else "d"
        return f"[{df}] {self.name}"

    def get_inode(self, path: str = ""):
        node = self
        for d in path.split("/"):
            if d:
                if d == "..":
                    node = node.parent
                elif d not in node.inodes:
                    raise FileNotFoundError(path)
                else:
                    node = node.inodes[d]
        return node

    @staticmethod
    def cmp(inode1, inode2):
        if not isinstance(inode1, iNode) or not isinstance(inode2, iNode):
            raise NotImplementedError
        if not inode1.is_file and inode2.is_file:
            return 1
        if inode1.is_file and not inode2.is_file:
            return -1
        if inode1.name > inode2.name:
            return 1
        if inode1.name < inode2.name:
            return -1
        return 0


class FileSystem:
    def __init__(self):
        self.root = iNode("/")
        self.current = self.root

    def get_inode(self, path: str = ""):
        return self.root.get_inode(path) if path.startswith("/") else self.current.get_inode(path)

    def basename(self, path: str):
        return path.split("/")[-1]

    def dirname(self, path: str):
        directories = "/".join(path.split("/")[:-1:])
        return "/" + directories if path.startswith("/") else directories

    def pwd(self):
        # print(self.current.path)
        node = self.current
        directories = list()
        while node != self.root:
            directories.append(node.name)
            node = node.parent
        print(self.root.name + "/".join(directories[::-1]))

    def cd(self, path: str = ""):
        self.current = self.get_inode(path)

    def ls(self, path: str = ""):
        inode = self.get_inode(path)
        result = [inode] if inode.is_file else list(inode.inodes.values())
        result.sort(key=cmp_to_key(iNode.cmp))
        for r in result:
            print(r)

    def rm(self, path: str):
        parent_path = self.dirname(path)
        parent_node = self.get_inode(parent_path)
        if parent_node.is_file:
            raise NotADirectoryError(parent_path)
        del parent_node.inodes[self.basename(path)]

    def mkdir(self, path: str, create_intermediate_directories=False):
        if create_intermediate_directories:
            node = self.root if path.startswith("/") else self.current
            for d in path.split("/"):
                if d:
                    if d not in node.inodes:
                        node.inodes[d] = iNode(name=d, parent=node)
                    node = node.inodes[d]
        else:
            parent_path = self.dirname(path)
            parent_node = self.get_inode(parent_path)
            if parent_node.is_file:
                raise NotADirectoryError(parent_path)
            basename = self.basename(path)
            parent_node.inodes[basename] = iNode(name=basename, parent=parent_node, is_file=False)

    def touch(self, path: str):
        parent_path = self.dirname(path)
        parent_node = self.get_inode(parent_path)
        if parent_node.is_file:
            raise NotADirectoryError(parent_path)
        basename = self.basename(path)
        parent_node.inodes[basename] = iNode(name=basename, parent=parent_node, is_file=True)

    def cat(self, path: str):
        inode = self.get_inode(path)
        if not inode.is_file:
            raise IsADirectoryError(path)
        print(inode.content)

    def echo_to(self, path: str, content: str):
        parent_path = self.dirname(path)
        parent_node = self.get_inode(parent_path)
        if parent_node.is_file:
            raise NotADirectoryError(parent_path)
        basename = self.basename(path)
        if basename not in parent_node.inodes:
            parent_node.inodes[basename] = iNode(name=basename, parent=parent_node, is_file=True, content=content)
        else:
            node = parent_node.inodes[basename]
            if not node.is_file:
                raise IsADirectoryError(path)
            node.content = node.content + content if node.content else content

    def tree(self, path: str = "", depth: int = None):
        def _dfs(inode, depth, last_one):
            if depth is not None and len(last_one) > depth:
                return
            if len(last_one) > 0:
                indentation = ""
                for bar in last_one[:-1]:
                    indentation += "    " if bar else "│   "
                connector = "└" if last_one[-1] else "├"
                print(indentation + f"{connector}── " + inode.name)
            children = list(inode.inodes.values())
            children.sort(key=cmp_to_key(iNode.cmp))
            for i, node in enumerate(children):
                last_one.append(i == len(children) - 1)
                _dfs(node, depth, last_one)
                last_one.pop()

        if path:
            print(path)
        else:
            self.pwd()
        _dfs(inode=self.get_inode(path), depth=depth, last_one=list())

