from typing import List, Any, Optional

class PoolQueryEngine:
    def __init__(self, pool: List[Any]):
        self.pool = pool

    def search_by_keyword(self, keyword: str) -> List[Any]:
        results = []
        keyword_lower = keyword.lower()
        for record in self.pool:
            data_str = str(record.canonical_data).lower()
            prov_str = str(record.provenance).lower()
            if keyword_lower in data_str or keyword_lower in prov_str:
                results.append(record)
        return results

    def filter_records(self, source_filter: Optional[str] = None, date_prefix: Optional[str] = None) -> List[Any]:
        filtered = []
        for record in self.pool:
            match = True
            if source_filter and source_filter.lower() not in record.provenance.lower():
                match = False
            if date_prefix and not record.timestamp.startswith(date_prefix):
                match = False
            if match:
                filtered.append(record)
        return filtered