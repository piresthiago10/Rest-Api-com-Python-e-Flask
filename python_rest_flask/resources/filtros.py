def normalize_path_params(cidade = None, estrelas_min = 0, estrelas_max = 5, diaria_min = 0, diaria_max = 10000, limit = 50, offset = 0, **dados):

    # se cidade estiver preenchida
    if cidade is not None:
        return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    # se a cidade não estiver preenchida
    return{
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}

# cada ? é referente a uma variavel
consulta_sem_cidade = "SELECT * FROM hoteis \
WHERE (estrelas >= ? and estrelas <= ?) \
and (diaria >= ? and diaria <= ?) \
LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM hoteis \
WHERE (estrelas >= ? and estrelas <= ?) \
and (diaria >= ? and diaria <= ?) \
and cidade = ? LIMIT ? OFFSET ?"