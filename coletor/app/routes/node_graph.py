from fastapi import APIRouter

from app.lib.logger import Logger
from app.lib.custom_response import generate_json_response

log = Logger()
router = APIRouter()


# node graph
@router.get('/node-graph')
async def node_graph():
    
    graph : list = [
        {
            'id': 'edge1',
            'source': 'node1',
            'target': 'node2',
            'mainstat': 'TheMain',
            'secondarysta': 'TheSub',
            'thickness': 3,
            'highlighted':True,
            'color': 'cyan'
        },
        {
            'id': 'edge2',
            'source': 'node3',
            'target': 'node2',
            'mainstat': 'Main2',
            'secondarysta': 'Sub2',
            'thickness': 1,
            'highlighted':False,
            'color': 'orange'
        }
        
    ]
    
    return generate_json_response(response_data={'data': graph})
