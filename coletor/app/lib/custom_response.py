from fastapi.responses import ORJSONResponse


def generate_json_response(
    response_data: dict = {}, response_status_code: int = 200
):

    headers = {'Content-Type': 'application/json'}

    if 'pagination_count' in response_data:
        headers['Pagination-Count'] = str(response_data['pagination_count'])

    if 'pagination_offset' in response_data:
        headers['Pagination-Offset'] = str(response_data['pagination_offset'])

    if 'pagination_limit' in response_data:
        headers['Pagination-Limit'] = str(response_data['pagination_limit'])

    if 'data' in response_data:

        if not isinstance(response_data['data'], list):
            content: dict = response_data['data']

        if isinstance(response_data['data'], list):
            content: list = response_data['data']

    return ORJSONResponse(
        content=content, headers=headers, status_code=response_status_code
    )
