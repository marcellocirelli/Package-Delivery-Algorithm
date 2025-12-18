class HashTable:
    def __init__(self):
        self.table = [[] for _ in range(10)]

    # Hash insert function
    def insert(self, package):
        bucket_index = package.package_id % 10
        bucket = self.table[bucket_index]
        for i, existing_pkg in enumerate(bucket):
            if existing_pkg.package_id == package.package_id:
                bucket[i] = package
                return
        bucket.append(package)

    # Hash lookup function
    def lookup(self, package_id):
        bucket_index = package_id % 10
        bucket = self.table[bucket_index]
        for pkg in bucket:
            if pkg.package_id == package_id:
                return pkg
        return None