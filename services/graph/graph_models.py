from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class GraphNode:

    id: str

    label: str

    node_type: str

    properties: Dict = field(default_factory=dict)


@dataclass
class GraphEdge:

    source: str

    target: str

    relation: str

    properties: Dict = field(default_factory=dict)


NODE_TYPES = {

    "equipment",

    "document",

    "work_order",

    "incident",

    "inspection",

    "maintenance",

    "component",

    "regulation",

    "failure",

    "location"

}


EDGE_TYPES = {

    "HAS_DOCUMENT",

    "HAS_COMPONENT",

    "HAS_FAILURE",

    "HAS_INCIDENT",

    "HAS_INSPECTION",

    "HAS_WORK_ORDER",

    "REGULATED_BY",

    "CONNECTED_TO",

    "LOCATED_AT",

    "MENTIONS"

}